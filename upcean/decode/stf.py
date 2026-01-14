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
    color_tolerance=0,
    scanlines=1,
    digits_count=None,   # None => auto-detect
    max_digits=64,       # safety cap for auto-detect
):
    r = _clamp_resize(resize)
    module = float(barwidth[0]) * r
    if module < 1.0:
        module = 1.0

    img = _open_rgb_image(infile, cairosupport=cairosupport)
    if img is None:
        return False

    w, h = img.size
    px = img.load()

    base_y = (h // 2) - ((barwidth[1] - 1) * 9) + int(shiftxy[1])

    # scanlines for mild robustness
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

    default_startx = int(round(21 * module + shiftxy[0]))

    def find_startx(y):
        x = max(0, int(shiftxy[0]))
        limit = w - int(round(8 * module)) - 1
        while x < limit:
            if bit_at(x, y) == "1":
                x7 = x + 7 * step
                if bit_at(x7, y) == "0":
                    return x + int(round(8 * module))
            x += 1
        return None

    def decode_digit_at(x, y):
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
        return _STF_DIGITS.get(pat)

    def decode_line(y):
        sx = default_startx
        if shiftcheck:
            got = find_startx(y)
            if got is None:
                return None
            sx = got

        # If fixed length requested, decode exactly that many digits
        if digits_count is not None:
            try:
                n = int(digits_count)
            except Exception:
                return None
            if n <= 0:
                return None
            x = sx
            endx = x + int(round(n * 14 * module))
            if endx > w:
                return None
            out = []
            i = 0
            while i < n:
                d = decode_digit_at(x, y)
                if d is None:
                    return None
                out.append(d)
                x += 14 * step
                i += 1
            return ("".join(out), sx, endx)

        # Auto-detect: keep decoding 14-module chunks until we fail
        out = []
        x = sx
        nread = 0
        while nread < int(max_digits):
            # ensure there is room to read another 14-module digit
            if x + (14 * step) > w:
                break
            d = decode_digit_at(x, y)
            if d is None:
                break
            out.append(d)
            x += 14 * step
            nread += 1

        if not out:
            return None

        endx = x
        return ("".join(out), sx, endx)

    # vote across scanlines
    codes = []
    meta = None
    for y in ys:
        res = decode_line(y)
        if res is None:
            continue
        code, sx, ex = res
        codes.append(code)
        if meta is None:
            meta = (sx, ex, y)

    try:
        img.close()
    except Exception:
        pass

    if not codes:
        return False

    if len(codes) == 1:
        chosen = codes[0]
    else:
        counts = {}
        for c in codes:
            counts[c] = counts.get(c, 0) + 1
        chosen = None
        bestn = -1
        for k, v in counts.items():
            if v > bestn:
                chosen, bestn = k, v

    if not locatebarcode:
        return chosen

    if meta is None:
        return False
    sx, ex, y0 = meta
    prestartx = int(round(sx - 8 * module))
    if prestartx < 0:
        prestartx = 0

    top = y0
    while top > 0:
        if bit_at(prestartx, top) == "0":
            break
        top -= 1

    bottom = y0
    while bottom < h - 1:
        if bit_at(prestartx, bottom) == "0":
            break
        bottom += 1

    return ("stf", prestartx, sx, 0, 0, ex,
            top, round(top / 2.0), round(bottom * 2.0), bottom, top, len(chosen))


# wrappers (keep your API style)
def get_stf_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_stf_barcode(*args, **kwargs)

def decode_code25_barcode(*args, **kwargs):
    return decode_stf_barcode(*args, **kwargs)

def get_code25_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_code25_barcode(*args, **kwargs)
