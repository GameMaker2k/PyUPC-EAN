# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: stf.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from PIL import Image
except Exception:
    Image = None

try:
    from io import BytesIO
except Exception:
    try:
        from cStringIO import StringIO as BytesIO
    except Exception:
        from StringIO import StringIO as BytesIO


# Your digit map (14 modules per digit)
_STF_DIGITS = {
    "10101110111010": "0",
    "11101010101110": "1",
    "10111010101110": "2",
    "11101110101010": "3",
    "10101110101110": "4",
    "11101011101010": "5",
    "10111011101010": "6",
    "10101011101110": "7",
    "11101010111010": "8",
    "10111010111010": "9",
}


def _clamp_resize(resize):
    try:
        r = float(resize)
        if r < 1.0:
            return 1.0
        return r
    except Exception:
        return 1.0


def _open_rgb_image(infile, cairosupport=False):
    if Image is None:
        return None

    # Pillow Image directly
    try:
        if isinstance(infile, Image.Image):
            return infile.convert("RGB")
    except Exception:
        pass

    # legacy list/tuple with Pillow image at index 1
    if isinstance(infile, (list, tuple)) and len(infile) >= 2:
        try:
            if isinstance(infile[1], Image.Image):
                return infile[1].convert("RGB")
        except Exception:
            pass

    # Optional cairo ImageSurface
    if cairosupport:
        try:
            import cairo
            if isinstance(infile, cairo.ImageSurface):
                buf = BytesIO()
                infile.write_to_png(buf)
                buf.seek(0)
                return Image.open(buf).convert("RGB")
            if isinstance(infile, (list, tuple)) and len(infile) >= 2 and isinstance(infile[1], cairo.ImageSurface):
                buf = BytesIO()
                infile[1].write_to_png(buf)
                buf.seek(0)
                return Image.open(buf).convert("RGB")
        except Exception:
            pass

    # file-like
    try:
        infile.seek(0)
        try:
            return Image.open(infile).convert("RGB")
        except Exception:
            return None
    except Exception:
        pass

    # path
    try:
        return Image.open(infile).convert("RGB")
    except Exception:
        return None


def _rgb_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def _is_color(px, target, tol):
    return _rgb_dist(px, target) <= tol


def decode_stf_barcode(
    infile,
    resize=1,
    barheight=(48, 54),
    barwidth=(1, 1),
    shiftcheck=False,
    shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False,
    cairosupport=False,
    # lightweight robustness
    color_tolerance=0,
    scanlines=1,
    # STF in your code is fixed 12 digits; make it configurable but default identical.
    digits_count=12,
):
    """
    Returns:
      - locatebarcode=False: decoded digit string or False
      - locatebarcode=True : ("stf", prestartx, startx, 0, 0, endx, top, mid_up, mid_down, bottom, top, digits_count)

    Contract:
      - each digit is 14 modules sampled at module width (barwidth[0] * resize)
      - black/white must be close to barcolor[0]/barcolor[2] (tolerance optional)
    """

    r = _clamp_resize(resize)
    module = float(barwidth[0]) * r
    if module < 1.0:
        module = 1.0

    img = _open_rgb_image(infile, cairosupport=cairosupport)
    if img is None:
        return False

    w, h = img.size
    px = img.load()

    # Match your vertical placement
    base_y = (h // 2) - ((barwidth[1] - 1) * 9) + int(shiftxy[1])

    # scanlines vote
    if scanlines is None or scanlines <= 1:
        ys = [max(0, min(h - 1, int(base_y)))]
    else:
        half = int(scanlines) // 2
        ys = []
        dy = -half
        while dy <= half and len(ys) < int(scanlines):
            y = int(base_y) + dy
            if y < 0:
                y = 0
            if y >= h:
                y = h - 1
            ys.append(y)
            dy += 1

    black = barcolor[0]
    white = barcolor[2]
    tol = int(color_tolerance)

    def bit_at(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return None
        p = px[x, y]
        if _is_color(p, black, tol):
            return "1"
        if _is_color(p, white, tol):
            return "0"
        return None

    step = int(round(module))
    if step < 1:
        step = 1

    # Start position:
    # Your non-shiftcheck default is 21 * module
    default_startx = int(round(21 * module + shiftxy[0]))

    def find_startx(y):
        """
        Your shiftcheck looks for a black pixel and then checks an 8-module span,
        and sets startx = prestartx + 8*module.
        We'll keep it lightweight and very similar:
          - scan left->right
          - if pixel is black, check that the 8th sampled module looks white
          - return x + 8*module
        """
        x = max(0, int(shiftxy[0]))
        limit = w - int(round(8 * module)) - 1
        while x < limit:
            if bit_at(x, y) == "1":
                x7 = x + 7 * step
                b7 = bit_at(x7, y)
                if b7 == "0":
                    return x + int(round(8 * module))
            x += 1
        return None

    def decode_at_y(y):
        sx = default_startx
        if shiftcheck:
            got = find_startx(y)
            if got is None:
                return None
            sx = got

        # Sample digits_count blocks, each 14 modules
        out = []
        x = sx
        total_modules = int(digits_count) * 14
        endx = x + int(round(total_modules * module))

        # quick bounds
        if x < 0:
            x = 0
        if endx > w:
            # if we can't even fit the expected width, fail deterministically
            return None

        i = 0
        while i < int(digits_count):
            bits = []
            j = 0
            while j < 14:
                b = bit_at(x, y)
                if b is None:
                    return None
                bits.append(b)
                x += step
                j += 1
            pat = "".join(bits)
            d = _STF_DIGITS.get(pat)
            if d is None:
                return None
            out.append(d)
            i += 1
        return "".join(out), sx, endx

    # vote across scanlines
    results = []
    meta = None
    for y in ys:
        res = decode_at_y(y)
        if res is None:
            continue
        code, sx, ex = res
        results.append(code)
        if meta is None:
            meta = (sx, ex, y)

    try:
        img.close()
    except Exception:
        pass

    if not results:
        return False

    # choose most common decoded value
    if len(results) == 1:
        chosen = results[0]
    else:
        counts = {}
        for c in results:
            counts[c] = counts.get(c, 0) + 1
        chosen = None
        bestn = -1
        for k, v in counts.items():
            if v > bestn:
                chosen, bestn = k, v

    if not locatebarcode:
        return chosen

    # location mode: approximate like other decoders
    if meta is None:
        return False
    sx, ex, y0 = meta
    prestartx = int(round(sx - 8 * module))
    if prestartx < 0:
        prestartx = 0

    # vertical bounds similar to your originals
    top = y0
    while top > 0:
        if bit_at(prestartx, top) == "0":  # white background reached
            break
        top -= 1
    bottom = y0
    while bottom < h - 1:
        if bit_at(prestartx, bottom) == "0":
            break
        bottom += 1

    return ("stf", prestartx, sx, 0, 0, ex,
            top, round(top / 2.0), round(bottom * 2.0), bottom, top, int(digits_count))


def get_stf_barcode_location(
    infile="./stf.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_stf_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )


def decode_code25_barcode(
    infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False, cairosupport=False, **kwargs
):
    # Alias, preserving the original library behavior
    return decode_stf_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=locatebarcode, cairosupport=cairosupport, **kwargs
    )


def get_code25_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_code25_barcode(*args, **kwargs)
