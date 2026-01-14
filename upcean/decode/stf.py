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


# 14-module digit patterns (threewidebar=True)
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

# Your encoder's end guard begins with these 8 modules:
_END_PREFIX = "11010110"

_START_GUARD_LEN = 21
_START_FALLBACK_OFFSET = 8   # your prior heuristic returned x + 8 modules
_DIGIT_LEN = 14


def _clamp_resize(resize):
    try:
        r = float(resize)
        return 1.0 if r < 1.0 else r
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
    digits_count=None,     # if set, decode exactly N digits (like your working one)
    max_digits=128,        # cap for safety
    enforce_even=False,    # set True if you want to mirror your encoder rule
    min_digits=0,          # set 6 if you want to mirror your encoder rule
    use_end_guard=True,    # True = decode between start and end; False = old "until fail"
    end_search_pad_digits=2,   # skip first few digits before looking for end prefix
    quiet_zero_modules=0,      # optional: require some zeros after end prefix (0 = don't require)
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

    # Same default as your working version
    default_startx = int(round(_START_GUARD_LEN * module + shiftxy[0]))

    def read_bits(x, y, n):
        bits = []
        i = 0
        while i < n:
            b = bit_at(x + i * step, y)
            if b is None:
                return None
            bits.append(b)
            i += 1
        return "".join(bits)

    def find_startx(y):
        """
        Keep your original cheap heuristic (fast, worked for your generated images):
          find a black pixel then 7 modules later white, return x + 8 modules
        """
        x = max(0, int(shiftxy[0]))
        limit = w - int(round(8 * module)) - 1
        while x < limit:
            if bit_at(x, y) == "1":
                x7 = x + 7 * step
                if bit_at(x7, y) == "0":
                    return x + int(round(_START_FALLBACK_OFFSET * module))
            x += 1
        return None

    def decode_digit_at(x, y):
        pat = read_bits(x, y, _DIGIT_LEN)
        if pat is None:
            return None
        return _STF_DIGITS.get(pat)

    def find_end_by_alignment(y, payload_x):
        """
        Robust end finder:
        - search for end prefix on module grid
        - choose the RIGHTMOST prefix whose distance from payload_x is a multiple of 14 modules
        - optionally require some zeros after the prefix if requested
        This survives partial clipping of the far-right quiet zone / tail.
        """
        best = None
        # don't let an early accidental prefix end the decode
        x = payload_x + int(end_search_pad_digits) * _DIGIT_LEN * step
        if x < payload_x:
            x = payload_x

        max_x = w - (8 * step) - 1
        while x <= max_x:
            if read_bits(x, y, 8) == _END_PREFIX:
                modules = int(round((x - payload_x) / float(step)))
                if modules > 0 and (modules % _DIGIT_LEN) == 0:
                    if quiet_zero_modules and quiet_zero_modules > 0:
                        tail = read_bits(x + 8 * step, y, int(quiet_zero_modules))
                        if tail != ("0" * int(quiet_zero_modules)):
                            x += step
                            continue
                    best = x  # rightmost aligned candidate wins
            x += step
        return best

    def decode_line(y):
        sx = default_startx
        if shiftcheck:
            got = find_startx(y)
            if got is None:
                return None
            sx = got

        # Fixed length mode (exactly like your working version)
        if digits_count is not None:
            try:
                n = int(digits_count)
            except Exception:
                return None
            if n <= 0:
                return None
            x = sx
            endx = x + int(round(n * _DIGIT_LEN * module))
            if endx > w:
                return None
            out = []
            i = 0
            while i < n:
                d = decode_digit_at(x, y)
                if d is None:
                    return None
                out.append(d)
                x += _DIGIT_LEN * step
                i += 1
            return ("".join(out), sx, endx)

        # Start/end-guard mode
        if use_end_guard:
            end_prefix_x = find_end_by_alignment(y, sx)
            if end_prefix_x is None:
                return None

            payload_modules = int(round((end_prefix_x - sx) / float(step)))
            if payload_modules <= 0 or (payload_modules % _DIGIT_LEN) != 0:
                return None

            n_digits = payload_modules // _DIGIT_LEN
            if n_digits > int(max_digits):
                return None
            if enforce_even and (n_digits % 2) != 0:
                return None
            if n_digits < int(min_digits):
                return None

            out = []
            x = sx
            i = 0
            while i < n_digits:
                d = decode_digit_at(x, y)
                if d is None:
                    return None
                out.append(d)
                x += _DIGIT_LEN * step
                i += 1

            # endx at start of end prefix (like other decoders: payload bounds)
            return ("".join(out), sx, end_prefix_x)

        # Fallback: old behavior (decode until fail)
        out = []
        x = sx
        nread = 0
        while nread < int(max_digits):
            if x + (_DIGIT_LEN * step) > w:
                break
            d = decode_digit_at(x, y)
            if d is None:
                break
            out.append(d)
            x += _DIGIT_LEN * step
            nread += 1

        if not out:
            return None
        return ("".join(out), sx, x)

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
    prestartx = int(round(sx - _START_FALLBACK_OFFSET * module))
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


def get_stf_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_stf_barcode(*args, **kwargs)


def decode_code25_barcode(*args, **kwargs):
    return decode_stf_barcode(*args, **kwargs)


def get_code25_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_code25_barcode(*args, **kwargs)
