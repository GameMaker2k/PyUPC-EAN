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

    $FileInfo: ean13.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

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


# First digit parity patterns for the left 6 digits (EAN-13)
_FIRST_DIGIT_PARITY = {
    "LLLLLL": "0", "LLGLGG": "1", "LLGGLG": "2", "LLGGGL": "3",
    "LGLLGG": "4", "LGGLLG": "5", "LGGGLL": "6", "LGLGLG": "7",
    "LGLGGL": "8", "LGGLGL": "9",
}

# Left side encodings: L-code and G-code (7 modules each)
_LEFT_L = {
    "0001101": "0", "0011001": "1", "0010011": "2", "0111101": "3",
    "0100011": "4", "0110001": "5", "0101111": "6", "0111011": "7",
    "0110111": "8", "0001011": "9",
}
_LEFT_G = {
    "0100111": "0", "0110011": "1", "0011011": "2", "0100001": "3",
    "0011101": "4", "0111001": "5", "0000101": "6", "0010001": "7",
    "0001001": "8", "0010111": "9",
}

# Right side encoding is the same as UPC-A right
_RIGHT = {
    "1110010": "0", "1100110": "1", "1101100": "2", "1000010": "3",
    "1011100": "4", "1001110": "5", "1010000": "6", "1000100": "7",
    "1001000": "8", "1110100": "9",
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
    """
    Accepts:
      - Pillow Image.Image
      - file path
      - file-like object
      - list/tuple legacy: [ctx, surface] or [something, pillow_image]
      - cairo.ImageSurface (optional)
    Returns: RGB Pillow image or None on failure
    """
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


def _ean13_check_digit_is_valid(code13):
    """
    EAN-13 checksum:
      sum(odd positions 1,3,5,...,11) + 3*sum(even positions 2,4,...,12) + checkdigit ≡ 0 (mod 10)
    Using 0-based indices: even idx = positions 1,3,5... ; odd idx = positions 2,4,6...
    """
    try:
        if not isinstance(code13, (str,)):
            code13 = str(code13)
    except Exception:
        return False

    if len(code13) != 13:
        return False
    for c in code13:
        if c < "0" or c > "9":
            return False

    digits = [ord(c) - 48 for c in code13]
    # indices 0..11 are data, 12 is check
    odd_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8] + digits[10]
    even_sum = digits[1] + digits[3] + digits[5] + digits[7] + digits[9] + digits[11]
    total = odd_sum + (even_sum * 3) + digits[12]
    return (total % 10) == 0


def decode_ean13_barcode(
    infile,
    resize=1,
    barheight=(48, 54),
    barwidth=(1, 1),
    shiftcheck=False,
    shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False,
    cairosupport=False,
    # lightweight robustness (still Pillow-only)
    color_tolerance=0,
    scanlines=1,
    validate_checksum=False,
):
    """
    Returns:
      - locatebarcode=False: 13-digit EAN-13 string, or False
      - locatebarcode=True : ("ean13", prestartx, startx, jumpcode, jumpcodeend, endx, top, mid_up, mid_down, bottom, top, 13)
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

    # EAN-13 tends to have a slightly different text area; keep your original bias:
    base_y = (h // 2) - ((barwidth[1] - 1) * 9) + int(shiftxy[1])

    # choose scanlines
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

    # Layout assumptions matching your original:
    # For EAN-13, left quiet zone + left guard + first digit area results in a different start offset than UPC-A.
    startx = int(round(14 * barsize + shiftxy[0]))  # matches your code
    jumpcode = int(round(56 * barsize + shiftxy[0]))  # center guard location estimate
    endx_width = int(round((42 + 42) * barsize))  # digits-only modules for both halves (84 modules)

    step = int(round(barsize))
    if step < 1:
        step = 1
    jumpskip = int(round(5 * barsize))
    if jumpskip < 5:
        jumpskip = 5

    def find_startx_by_guard(y):
        """
        Lightweight: look for left guard '101' at module spacing, then return x after guard.
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
        # For EAN-13, after left guard comes:
        # - 6 left digits (42 modules)
        # Center guard begins after those. Our extractor handles skipping when cursor==jumpcode.
        startx = found
        jumpcode = int(round(startx + 42 * barsize))

    if locatebarcode:
        prestartx = int(round(startx - 3 * barsize))
        jumpcodeend = int(round(jumpcode + 4 * barsize))
        endx = int(round(startx + (42 + 4 + 42) * barsize))

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

        return ("ean13", prestartx, startx, jumpcode, jumpcodeend, endx,
                top, round(top / 2.0), round(bottom * 2.0), bottom, top, 13)

    # --- Extract & decode ---
    # EAN-13 data structure:
    # - Left half: 6 digits encoded as L or G patterns; parity determines leading digit.
    # - Right half: 6 digits encoded as R patterns.
    # Total encoded digit groups across halves = 12 groups of 7 modules = 84 modules.
    total_modules = 84

    def extract_groups_at_y(y, sx, jc):
        cursor = sx
        modules = 0
        groups = []

        while modules < total_modules:
            if cursor == jc:
                cursor += jumpskip

            bits = []
            i = 0
            while i < 7:
                if cursor == jc:
                    cursor += jumpskip
                b = sample_bit(cursor, y)
                if b is None:
                    return None
                bits.append(b)
                cursor += step
                modules += 1
                i += 1
            groups.append("".join(bits))

        if len(groups) != 12:
            return None
        return groups

    def decode_groups(groups):
        # Decode left 6 groups as L/G, record parity, then determine first digit from parity.
        parity = []
        digits = []

        # Left 6
        i = 0
        while i < 6:
            g = groups[i]
            if g in _LEFT_L:
                parity.append("L")
                digits.append(_LEFT_L[g])
            elif g in _LEFT_G:
                parity.append("G")
                digits.append(_LEFT_G[g])
            else:
                return None

            i += 1

        first = _FIRST_DIGIT_PARITY.get("".join(parity))
        if first is None:
            return None

        # Right 6
        i = 6
        while i < 12:
            g = groups[i]
            d = _RIGHT.get(g)
            if d is None:
                return None
            digits.append(d)
            i += 1

        # Insert first digit at front
        code = first + "".join(digits)

        if validate_checksum and not _ean13_check_digit_is_valid(code):
            return None
        return code

    stable_startx = startx
    stable_jump = jumpcode

    results = []
    for y in ys:
        groups = extract_groups_at_y(y, stable_startx, stable_jump)
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

    # Majority vote
    counts = {}
    for c in results:
        counts[c] = counts.get(c, 0) + 1

    best = None
    bestn = -1
    for k, v in counts.items():
        if v > bestn:
            best, bestn = k, v
    return best


# --- wrappers with correct argument order (and fixed typos) ---

def get_ean13_barcode_location(
    infile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_ean13_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )


def decode_gtin13_barcode(
    infile="./gtin13.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False, cairosupport=False, **kwargs
):
    return decode_ean13_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=locatebarcode, cairosupport=cairosupport, **kwargs
    )


def get_gtin13_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_gtin13_barcode(*args, **kwargs)


def decode_ucc13_barcode(*args, **kwargs):
    return decode_gtin13_barcode(*args, **kwargs)


def get_ucc13_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_ucc13_barcode(*args, **kwargs)
