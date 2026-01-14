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

    $FileInfo: upca.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

try:
    # Pillow
    from PIL import Image
    try:
        from PIL import UnidentifiedImageError
        _HAS_UIE = True
    except Exception:
        UnidentifiedImageError = Exception  # Py2 compatibility / older Pillow
        _HAS_UIE = False
except Exception:
    Image = None  # will fail later

try:
    from io import BytesIO
except Exception:
    try:
        from cStringIO import StringIO as BytesIO
    except Exception:
        from StringIO import StringIO as BytesIO


# UPC-A digit patterns (7 modules each)
_LEFT = {
    "0001101": "0", "0011001": "1", "0010011": "2", "0111101": "3",
    "0100011": "4", "0110001": "5", "0101111": "6", "0111011": "7",
    "0110111": "8", "0001011": "9",
}
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
    # Manhattan distance is fast and good enough for thresholding
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def _is_color(px, target, tol):
    # tol=0 means exact match
    return _rgb_dist(px, target) <= tol


def _upc_check_digit_is_valid(upc12):
    # UPC-A check digit: (3*sum of odd positions + sum of even positions + check) % 10 == 0
    if not isinstance(upc12, (str,)):
        try:
            upc12 = str(upc12)
        except Exception:
            return False
    if len(upc12) != 12:
        return False
    for c in upc12:
        if c < "0" or c > "9":
            return False
    digits = [ord(c) - 48 for c in upc12]
    odd_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8] + digits[10]
    even_sum = digits[1] + digits[3] + digits[5] + digits[7] + digits[9]
    total = odd_sum * 3 + even_sum + digits[11]
    return (total % 10) == 0


def decode_upca_barcode(
    infile,
    resize=1,
    barheight=(48, 54),
    barwidth=(1, 1),
    shiftcheck=False,
    shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False,
    cairosupport=False,
    # Lightweight robustness options (still Pillow-only)
    color_tolerance=0,
    scanlines=1,
    validate_checksum=False,
):
    """
    Returns:
      - locatebarcode=False: 12-digit UPC string, or False
      - locatebarcode=True : ("upca", prestartx, startx, jumpcode, jumpcodeend, endx, top, mid_up, mid_down, bottom, top, 12)
    """

    r = _clamp_resize(resize)
    barsize = float(barwidth[0]) * r
    if barsize < 1.0:
        barsize = 1.0

    img = _open_rgb_image(infile, cairosupport=cairosupport)
    if img is None:
        return False

    w, h = img.size
    px = img.load()  # fast pixel access

    # base scanline near center
    base_y = (h // 2) - ((barwidth[1] - 1) * 6) + int(shiftxy[1])

    # determine y sample rows (multi-scanline vote)
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

    def sample_bit(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return None
        p = px[x, y]
        if _is_color(p, black, int(color_tolerance)):
            return "1"
        if _is_color(p, white, int(color_tolerance)):
            return "0"
        return None

    # Default geometry (same spirit as your original)
    startx = int(round(12 * barsize + shiftxy[0]))
    jumpcode = int(round(54 * barsize + shiftxy[0]))
    endx_width = int(round((42 + 42) * barsize))  # 84 modules (digits only)

    def find_startx_by_guard(y):
        """
        Simple guard search: find left guard '101' at module spacing.
        Returns x right after left guard (start of digit patterns), or None.
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
        jumpcode = int(round(startx + 42 * barsize))  # center guard starts after left digits

    if locatebarcode:
        prestartx = int(round(startx - 3 * barsize))
        jumpcodeend = int(round(jumpcode + 4 * barsize))
        endx = int(round(startx + (42 + 4 + 42) * barsize))
        # Estimate top/bottom by scanning at prestartx
        x_probe0 = max(0, min(w - 1, prestartx))
        x_probe1 = max(0, min(w - 1, prestartx + int(round(barsize))))

        top = ys[0]
        while top > 0:
            p0 = px[x_probe0, top]
            p1 = px[x_probe1, top]
            if _is_color(p0, white, int(color_tolerance)) or _is_color(p1, black, int(color_tolerance)):
                break
            top -= 1

        bottom = ys[0]
        while bottom < h - 1:
            p0 = px[x_probe0, bottom]
            p1 = px[x_probe1, bottom]
            if _is_color(p0, white, int(color_tolerance)) or _is_color(p1, black, int(color_tolerance)):
                break
            bottom += 1

        try:
            img.close()
        except Exception:
            pass

        return ("upca", prestartx, startx, jumpcode, jumpcodeend, endx,
                top, round(top / 2.0), round(bottom * 2.0), bottom, top, 12)

    total_modules = 84  # 12 digits * 7 modules
    step = int(round(barsize))
    if step < 1:
        step = 1
    jumpskip = int(round(5 * barsize))
    if jumpskip < 5:
        jumpskip = 5

    def extract_and_decode_at_y(y, sx, jc):
        cursor = sx
        modules = 0
        bits7 = []

        # Read 12 groups of 7 modules (84 modules). Skip center guard once.
        while modules < total_modules:
            if cursor == jc:
                cursor += jumpskip

            d_bits = []
            i = 0
            while i < 7:
                if cursor == jc:
                    cursor += jumpskip
                bit = sample_bit(cursor, y)
                if bit is None:
                    return None
                d_bits.append(bit)
                cursor += step
                modules += 1
                i += 1
            bits7.append("".join(d_bits))

        if len(bits7) != 12:
            return None

        out = []
        i = 0
        while i < 12:
            b = bits7[i]
            if i < 6:
                d = _LEFT.get(b)
            else:
                d = _RIGHT.get(b)
            if d is None:
                return None
            out.append(d)
            i += 1

        code = "".join(out)
        if validate_checksum and not _upc_check_digit_is_valid(code):
            return None
        return code

    # Vote across scanlines
    results = []
    stable_startx = startx
    stable_jump = jumpcode
    for y in ys:
        code = extract_and_decode_at_y(y, stable_startx, stable_jump)
        if code is not None:
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


# --- wrappers with correct argument order ---

def get_upca_barcode_location(
    infile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_upca_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )


def decode_ean12_barcode(
    infile="./ean12.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False, cairosupport=False, **kwargs
):
    return decode_upca_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=locatebarcode, cairosupport=cairosupport, **kwargs
    )


def decode_gtin12_barcode(*args, **kwargs):
    return decode_ean12_barcode(*args, **kwargs)


def decode_ucc12_barcode(*args, **kwargs):
    return decode_ean12_barcode(*args, **kwargs)


def get_ean12_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_ean12_barcode(*args, **kwargs)


def get_gtin12_barcode_location(*args, **kwargs):
    return get_ean12_barcode_location(*args, **kwargs)


def get_ucc12_barcode_location(*args, **kwargs):
    return get_ean12_barcode_location(*args, **kwargs)
