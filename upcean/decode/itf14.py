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

    $FileInfo: itf14.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
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


# ITF digit patterns: 5 bits where 1 = wide, 0 = narrow
_ITF_DIGITS = {
    "00110": "0",
    "10001": "1",
    "01001": "2",
    "11000": "3",
    "00101": "4",
    "10100": "5",
    "01100": "6",
    "00011": "7",
    "10010": "8",
    "01010": "9",
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


def _itf14_check_digit_valid(code):
    """
    ITF-14 check digit is the same mod-10 algorithm used by GTIN:
      - Working from the rightmost digit (excluding check), weights 3,1,3,1...
      - check digit makes total multiple of 10.
    """
    try:
        if not isinstance(code, (str,)):
            code = str(code)
    except Exception:
        return False

    if len(code) != 14:
        return False
    for c in code:
        if c < "0" or c > "9":
            return False

    digits = [ord(c) - 48 for c in code]
    data = digits[:-1]
    check = digits[-1]

    # weights from right of data: 3,1,3,1...
    total = 0
    w = 3
    i = len(data) - 1
    while i >= 0:
        total += data[i] * w
        w = 1 if w == 3 else 3
        i -= 1

    calc = (10 - (total % 10)) % 10
    return calc == check


def decode_itf14_barcode(
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
    # ITF-14 expectations
    expected_digits=14,          # set to None to accept any even digit length
    validate_check_digit=False,  # True => validate ITF-14 check digit when expected_digits==14
):
    """
    Returns:
      - locatebarcode=False: decoded digits string or False
      - locatebarcode=True : ("itf14", prestartx, startx, 0, 0, endx, top, mid_up, mid_down, bottom, top, digit_count)

    Strategy (still lightweight):
      1) Find start guard (narrow 1010) optionally via shiftcheck.
      2) Run-length encode the scanline into alternating black/white runs.
      3) After the start guard, decode in chunks of 10 runs => 2 digits per chunk.
      4) Stop when a stop guard pattern is detected near the end.
      5) Majority vote across scanlines.
    """

    r = _clamp_resize(resize)
    narrow = float(barwidth[0]) * r
    if narrow < 1.0:
        narrow = 1.0

    img = _open_rgb_image(infile, cairosupport=cairosupport)
    if img is None:
        return False

    w, h = img.size
    px = img.load()

    base_y = (h // 2) - ((barwidth[1] - 1) * 9) + int(shiftxy[1])

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

    def is_black(p):
        return _is_color(p, black, tol)

    def is_white(p):
        return _is_color(p, white, tol)

    step = max(1, int(round(narrow)))

    # Your originals default to startx = 17*narrow (+ shiftxy[0])
    default_startx = int(round(17 * narrow + shiftxy[0]))

    def find_startx_1010(y):
        """
        Find start guard '1010' at module spacing and return x after it (4 modules).
        """
        x = max(0, int(shiftxy[0]))
        limit = w - int(round(4 * narrow)) - 1
        while x < limit:
            p0 = px[x, y]
            if not is_black(p0):
                x += 1
                continue
            x1 = x + step
            x2 = x + 2 * step
            x3 = x + 3 * step
            if x3 >= w:
                break
            if is_white(px[x1, y]) and is_black(px[x2, y]) and is_white(px[x3, y]):
                return x + int(round(4 * narrow))
            x += 1
        return None

    def rle_scanline(y, x0):
        """
        RLE list of (color_is_black, width_px) starting at x0.
        Stops if pixels are neither close to black nor white (per tolerance).
        """
        runs = []
        if x0 < 0:
            x0 = 0
        if x0 >= w:
            return runs

        p = px[x0, y]
        if is_black(p):
            cur_black = True
        elif is_white(p):
            cur_black = False
        else:
            return runs

        run = 0
        x = x0
        while x < w:
            p = px[x, y]
            if cur_black:
                ok = is_black(p)
            else:
                ok = is_white(p)
            if ok:
                run += 1
                x += 1
                continue

            # switch only if pixel is the other color
            if cur_black and is_white(p):
                runs.append((cur_black, run))
                cur_black = False
                run = 0
                continue
            if (not cur_black) and is_black(p):
                runs.append((cur_black, run))
                cur_black = True
                run = 0
                continue
            break

        if run > 0:
            runs.append((cur_black, run))
        return runs

    def classify_width(run_px):
        # wide if clearly larger than narrow; ITF usually wide=2*narrow.
        return "1" if run_px >= (1.5 * narrow) else "0"

    def decode_runs_to_digits(runs):
        """
        Decode alternating runs into digits.
        After the start guard, ITF encodes 2 digits per 10 runs:
          bars:  5 runs (black) => digit A (5 bits)
          spaces:5 runs (white) => digit B (5 bits)
        Stop when a stop guard is detected:
          typically B(W), W(n), B(n) and then a quiet zone (big white run).
        """
        # Ensure we start on a black run
        idx = 0
        if runs and runs[0][0] is False:
            idx = 1

        digits = []

        while idx + 9 < len(runs):
            # stop-guard heuristic
            if idx + 2 < len(runs):
                b0, w1, b2 = runs[idx], runs[idx + 1], runs[idx + 2]
                if b0[0] is True and w1[0] is False and b2[0] is True:
                    if classify_width(b0[1]) == "1" and classify_width(w1[1]) == "0" and classify_width(b2[1]) == "0":
                        # look for quiet zone soon after
                        j = idx + 3
                        while j < min(len(runs), idx + 10):
                            if runs[j][0] is False and runs[j][1] >= (4 * narrow):
                                return "".join(digits)
                            j += 1

            chunk = runs[idx:idx + 10]

            bars = []
            spaces = []
            k = 0
            while k < 10:
                color_is_black, width_px = chunk[k]
                if (k % 2) == 0:
                    if color_is_black is not True:
                        return None
                    bars.append(classify_width(width_px))
                else:
                    if color_is_black is not False:
                        return None
                    spaces.append(classify_width(width_px))
                k += 1

            left_pat = "".join(bars)
            right_pat = "".join(spaces)

            ld = _ITF_DIGITS.get(left_pat)
            rd = _ITF_DIGITS.get(right_pat)
            if ld is None or rd is None:
                return None

            digits.append(ld)
            digits.append(rd)

            idx += 10

        return "".join(digits) if digits else None

    def decode_at_y(y):
        sx = default_startx
        if shiftcheck:
            found = find_startx_1010(y)
            if found is None:
                return None, None, None
            sx = found

        runs = rle_scanline(y, sx)
        if not runs:
            return None, None, None

        code = decode_runs_to_digits(runs)
        if not code:
            return None, None, None

        # If caller expects a specific digit length, enforce it.
        if expected_digits is not None:
            try:
                exp = int(expected_digits)
            except Exception:
                exp = None
            if exp is not None and len(code) != exp:
                return None, None, None
        else:
            # ITF must be even-length
            if (len(code) % 2) != 0:
                return None, None, None

        if validate_check_digit and expected_digits == 14:
            if not _itf14_check_digit_valid(code):
                return None, None, None

        # estimate endx as sx + sum run widths (clamped)
        endx = sx + sum([rw for _, rw in runs])
        if endx > w:
            endx = w
        return code, sx, endx

    # --- Decode with voting across scanlines ---
    results = []
    meta = None
    for y in ys:
        code, sx, ex = decode_at_y(y)
        if code:
            results.append(code)
            if meta is None:
                meta = (sx, ex, y)

    try:
        img.close()
    except Exception:
        pass

    if not results:
        return False

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

    # --- Location mode ---
    if meta is None:
        return False
    sx, ex, y0 = meta

    prestartx = int(round(sx - 4 * narrow))
    if prestartx < 0:
        prestartx = 0

    # vertical bounds similar to other decoders
    top = y0
    x_probe0 = max(0, min(w - 1, prestartx))
    x_probe1 = max(0, min(w - 1, prestartx + step))

    while top > 0:
        p0 = px[x_probe0, top]
        p1 = px[x_probe1, top]
        if _is_color(p0, white, tol) or _is_color(p1, black, tol):
            break
        top -= 1

    bottom = y0
    while bottom < h - 1:
        p0 = px[x_probe0, bottom]
        p1 = px[x_probe1, bottom]
        if _is_color(p0, white, tol) or _is_color(p1, black, tol):
            break
        bottom += 1

    return ("itf14", prestartx, sx, 0, 0, ex,
            top, round(top / 2.0), round(bottom * 2.0), bottom, top, len(chosen))


def get_itf14_barcode_location(
    infile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_itf14_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )


def decode_itf6_barcode(
    infile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False, cairosupport=False, **kwargs
):
    # ITF-6 is still ITF; set expected_digits=6 by default unless caller overrides
    if "expected_digits" not in kwargs:
        kwargs["expected_digits"] = 6
    return decode_itf14_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=locatebarcode, cairosupport=cairosupport, **kwargs
    )


def get_itf6_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_itf6_barcode(*args, **kwargs)
