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

    $FileInfo: upce.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from PIL import Image
    try:
        from PIL import UnidentifiedImageError
        _HAS_UIE = True
    except Exception:
        UnidentifiedImageError = Exception
        _HAS_UIE = False
except Exception:
    Image = None

try:
    from io import BytesIO
except Exception:
    try:
        from cStringIO import StringIO as BytesIO
    except Exception:
        from StringIO import StringIO as BytesIO


# UPC-E parity pattern -> Number System (first digit)
# NOTE: Your original mapping is unusual (many entries map to "0"; one maps to "9").
# This reproduces your mapping exactly for round-trip symmetry with your encoder/decoder pair.
_FIRST_DIGIT_FROM_PARITY = {
    "EEEOOO": "0", "EEOEOO": "0", "EEOOEO": "0", "EEOOOE": "0",
    "EOEEOO": "0", "EOOEEO": "0", "EOOOEE": "0", "EOEOEO": "0",
    "EOEOOE": "0", "EOOEOE": "0", "OOOEEE": "1", "OOEOEE": "1",
    "OOEEOE": "1", "OOEEEO": "1", "OEOOEE": "1", "OEEOOE": "1",
    "OEEEOO": "1", "OEOEOE": "1", "OEOEEO": "1", "OEEOEO": "9",
}

# UPC-E parity pattern -> Check digit (last digit)
_LAST_DIGIT_FROM_PARITY = {
    "EEEOOO": "0", "EEOEOO": "1", "EEOOEO": "2", "EEOOOE": "3",
    "EOEEOO": "4", "EOOEEO": "5", "EOOOEE": "6", "EOEOEO": "7",
    "EOEOOE": "8", "EOOEOE": "9", "OOOEEE": "0", "OOEOEE": "1",
    "OOEEOE": "2", "OOEEEO": "3", "OEOOEE": "4", "OEEOOE": "5",
    "OEEEOO": "6", "OEOEOE": "7", "OEOEEO": "8", "OEEOEO": "9",
}

# UPC-A/EAN L-code and G-code patterns (7 modules)
# In your UPC-E code:
# - "O" uses L-code patterns
# - "E" uses G-code patterns
_O_CODE = {
    "0001101": "0", "0011001": "1", "0010011": "2", "0111101": "3",
    "0100011": "4", "0110001": "5", "0101111": "6", "0111011": "7",
    "0110111": "8", "0001011": "9",
}
_E_CODE = {
    "0100111": "0", "0110011": "1", "0011011": "2", "0100001": "3",
    "0011101": "4", "0111001": "5", "0000101": "6", "0010001": "7",
    "0001001": "8", "0010111": "9",
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


def decode_upce_barcode(
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
    # validate_checksum left off by default because UPC-E check validation is tricky without expansion rules;
    # this implementation returns the same 8-digit code as your original mapping.
):
    """
    Returns:
      - locatebarcode=False: 8-digit UPC-E string (NS + 6 digits + check digit), or False
      - locatebarcode=True : ("upce", prestartx, startx, 0, 0, endx, postendx, top, mid_up, mid_down, bottom, 8)
    """

    r = _clamp_resize(resize)
    barsize = float(barwidth[0]) * r
    if barsize < 1.0:
        barsize = 1.0

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

    def sample_bit(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return None
        p = px[x, y]
        if _is_color(p, black, tol):
            return "1"
        if _is_color(p, white, tol):
            return "0"
        return None

    # Geometry aligned to your code:
    # - startx after left guard (assumes quiet zone & guard offset similar to upca/ean8)
    # - the UPC-E body is 6 digits => 42 modules
    startx = int(round(12 * barsize + shiftxy[0]))
    endx = int(round(42 * barsize + shiftxy[0]))  # body width (42 modules)

    step = int(round(barsize))
    if step < 1:
        step = 1

    def find_startx_by_guard(y):
        """
        Find left guard '101' and return x after it.
        UPC-E has left guard too; we keep the same lightweight approach.
        """
        x0 = max(0, int(shiftxy[0]))
        x1 = w - int(round(3 * barsize)) - 1
        x = x0
        while x < x1:
            b0 = sample_bit(x, y)
            if b0 == "1":
                x_a = int(round(x + 1 * barsize))
                x_b = int(round(x + 2 * barsize))
                b1 = sample_bit(x_a, y)
                b2 = sample_bit(x_b, y)
                if b1 == "0" and b2 == "1":
                    return int(round(x + 3 * barsize))
            x += 1
        return None

    if shiftcheck:
        found = find_startx_by_guard(ys[0])
        if found is None:
            try:
                img.close()
            except Exception:
                pass
            return False
        startx = found
        endx = int(round(startx + 42 * barsize))

    if locatebarcode:
        prestartx = int(round(startx - 3 * barsize))
        endx_loc = int(round(startx + 42 * barsize))
        postendx = int(round(endx_loc + 6 * barsize))  # UPC-E has an extended right guard/quiet area

        x_probe0 = max(0, min(w - 1, prestartx))
        x_probe1 = max(0, min(w - 1, prestartx + int(round(barsize))))

        top = ys[0]
        while top > 0:
            p0 = px[x_probe0, top]
            p1 = px[x_probe1, top]
            if _is_color(p0, white, tol) or _is_color(p1, black, tol):
                break
            top -= 1

        bottom = ys[0]
        while bottom < h - 1:
            p0 = px[x_probe0, bottom]
            p1 = px[x_probe1, bottom]
            if _is_color(p0, white, tol) or _is_color(p1, black, tol):
                break
            bottom += 1

        try:
            img.close()
        except Exception:
            pass

        return ("upce", prestartx, startx, 0, 0, endx_loc, postendx,
                top, round(top / 2.0), round(bottom * 2.0), bottom, 8)

    # --- Extract and decode ---
    total_modules = 42  # 6 digits * 7 modules

    def extract_groups_at_y(y, sx):
        cursor = sx
        modules = 0
        groups = []
        # Read 6 groups of 7 modules
        while modules < total_modules:
            bits = []
            i = 0
            while i < 7:
                b = sample_bit(cursor, y)
                if b is None:
                    return None
                bits.append(b)
                cursor += step
                modules += 1
                i += 1
            groups.append("".join(bits))
        if len(groups) != 6:
            return None
        return groups

    def decode_groups(groups):
        digits = []
        parity = []
        for g in groups:
            if g in _O_CODE:
                parity.append("O")
                digits.append(_O_CODE[g])
            elif g in _E_CODE:
                parity.append("E")
                digits.append(_E_CODE[g])
            else:
                return None

        parity_key = "".join(parity)
        first_digit = _FIRST_DIGIT_FROM_PARITY.get(parity_key, "0")
        last_digit = _LAST_DIGIT_FROM_PARITY.get(parity_key, "0")
        return first_digit + "".join(digits) + last_digit

    stable_startx = startx
    results = []
    for y in ys:
        groups = extract_groups_at_y(y, stable_startx)
        if groups is None:
            continue
        code = decode_groups(groups)
        if code is None:
            continue
        results.append(code)

    try:
        img.close()
    except Exception:
        pass

    if not results:
        return False
    if len(results) == 1:
        return results[0]

    # majority vote
    counts = {}
    for c in results:
        counts[c] = counts.get(c, 0) + 1

    best = None
    bestn = -1
    for k, v in counts.items():
        if v > bestn:
            best, bestn = k, v
    return best


def get_upce_barcode_location(
    infile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_upce_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )
