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

    $FileInfo: itf.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
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


def decode_itf_barcode(
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
):
    """
    Returns:
      - locatebarcode=False: decoded digits (string) or False
      - locatebarcode=True : ("itf", prestartx, startx, 0, 0, endx, top, mid_up, mid_down, bottom, top, digit_count)

    This decoder expects encoder-aligned images where:
      - narrow module width ~= barwidth[0] * resize pixels
      - wide element width   ~= 2 * narrow (typical ITF), or generally > 1.5 * narrow
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

    # Match your original vertical bias
    base_y = (h // 2) - ((barwidth[1] - 1) * 9) + int(shiftxy[1])

    # choose scanlines for mild robustness
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

    # --- Start finding ---
    # Your original uses startx = 17*barnarrow and shiftcheck searches for "1010" (black/white/black/white).
    default_startx = int(round(17 * narrow + shiftxy[0]))

    def find_startx_1010(y):
        # find first occurrence of black/white/black/white at module spacing and return x after it (4 modules)
        x = max(0, int(shiftxy[0]))
        limit = w - int(round(4 * narrow)) - 1
        step = max(1, int(round(narrow)))
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

    # --- Stop finding (end pattern) ---
    # Your original tries to detect the ITF stop pattern by scanning chunks.
    # A more robust (still lightweight) approach:
    # 1) Run-length encode (RLE) the scanline into alternating black/white widths.
    # 2) Find start guard, then parse pairs until stop guard.
    #
    # ITF guards:
    # Start:  n n n n  (bar, space, bar, space) all narrow (often "1010")
    # Stop : W n n     (bar wide, space narrow, bar narrow) (often "1101" in element terms)
    #
    # We'll locate start by 1010 and then decode until we see a stop-ish guard near the end.
    #

    def rle_scanline(y, x0):
        """
        Return RLE list of (color_is_black, run_width_in_pixels) starting at x0.
        Colors are classified by tolerance (black/white); non-matching pixels end scan.
        """
        runs = []
        if x0 < 0:
            x0 = 0
        if x0 >= w:
            return runs

        # Determine initial color
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
            # switch only if the new pixel is the other color; otherwise stop
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
        # wide if clearly larger than narrow (ITF typically wide=2*narrow)
        # Use a forgiving threshold so fractional scaling still works.
        return "1" if run_px >= (1.5 * narrow) else "0"

    def decode_from_runs(runs):
        """
        runs: alternating black/white runs starting right after the start guard.
        ITF encodes digits in 10 runs per 2 digits:
          - 5 black runs (bars) => one digit pattern
          - 5 white runs (spaces) => other digit pattern
        Between digit-pairs, runs naturally continue (no separators besides run alternation).
        """
        # We expect runs to start with a black bar after the start guard.
        # But depending on where x0 is, it might start on white; handle both.
        idx = 0
        # Ensure first run is black
        if runs and runs[0][0] is False:
            idx = 1

        digits = []

        # Parse in chunks of 10 runs: B W B W ... (10 total)
        while idx + 9 < len(runs):
            # Heuristic stop detection: lookahead for a stop guard pattern near end:
            # stop is typically: black wide, white narrow, black narrow (W n n) plus quiet zone after.
            # In run terms that is: B(W), W(n), B(n) and then often a large white quiet zone.
            # If we're close to the end and see that, break.
            if idx + 2 < len(runs):
                b0, w1, b2 = runs[idx], runs[idx + 1], runs[idx + 2]
                if b0[0] is True and w1[0] is False and b2[0] is True:
                    if classify_width(b0[1]) == "1" and classify_width(w1[1]) == "0" and classify_width(b2[1]) == "0":
                        # likely stop; but only accept if remaining runs look like quiet zone
                        # (a big white run soon after)
                        for j in range(idx + 3, min(len(runs), idx + 8)):
                            if runs[j][0] is False and runs[j][1] >= (4 * narrow):
                                return "".join(digits)

            # Collect 10 runs (should alternate B/W)
            chunk = runs[idx:idx + 10]
            # Extract black run widths at even offsets within chunk (0,2,4,6,8 if chunk starts with black)
            bars = []
            spaces = []
            k = 0
            while k < 10:
                color_is_black, width_px = chunk[k]
                if (k % 2) == 0:
                    # expected black
                    if color_is_black is not True:
                        return None
                    bars.append(classify_width(width_px))
                else:
                    # expected white
                    if color_is_black is not False:
                        return None
                    spaces.append(classify_width(width_px))
                k += 1

            if len(bars) != 5 or len(spaces) != 5:
                return None

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
        # find start
        sx = default_startx
        if shiftcheck:
            found = find_startx_1010(y)
            if found is None:
                return None
            sx = found

        # RLE from sx
        runs = rle_scanline(y, sx)
        if not runs:
            return None

        decoded = decode_from_runs(runs)
        return decoded

    # Majority vote across scanlines
    results = []
    for y in ys:
        code = decode_at_y(y)
        if code:
            results.append(code)

    try:
        img.close()
    except Exception:
        pass

    if not results:
        return False

    # pick most common
    if len(results) > 1:
        counts = {}
        for c in results:
            counts[c] = counts.get(c, 0) + 1
        best = None
        bestn = -1
        for k, v in counts.items():
            if v > bestn:
                best, bestn = k, v
        decoded = best
    else:
        decoded = results[0]

    if locatebarcode:
        # We can approximate endx by walking from the chosen start and summing run widths.
        # This is used for "location" mode like other decoders.
        # We'll compute it using the first scanline.
        y0 = ys[0]
        sx = default_startx
        if shiftcheck:
            found = find_startx_1010(y0)
            if found is None:
                return False
            sx = found

        runs0 = rle_scanline(y0, sx)
        if not runs0:
            return False

        # endx = sx + sum(run widths until a likely stop (or full sum)
        # Simple: sum all runs, but clamp within image.
        endx = sx + sum([rw for _, rw in runs0])
        if endx > w:
            endx = w

        prestartx = int(round(sx - 4 * narrow))
        if prestartx < 0:
            prestartx = 0

        # vertical bounds scan similar to your originals
        top = y0
        x_probe0 = max(0, min(w - 1, prestartx))
        x_probe1 = max(0, min(w - 1, prestartx + int(round(narrow))))
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

        # digit count should be even for ITF; we report length if decoded
        return ("itf", prestartx, sx, 0, 0, endx,
                top, round(top / 2.0), round(bottom * 2.0), bottom, top, len(decoded))

    return decoded


def get_itf_barcode_location(
    infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    cairosupport=False, **kwargs
):
    return decode_itf_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=True, cairosupport=cairosupport, **kwargs
    )


def decode_code25_interleaved_barcode(
    infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1),
    shiftcheck=False, shiftxy=(0, 0),
    barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),
    locatebarcode=False, cairosupport=False, **kwargs
):
    return decode_itf_barcode(
        infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor,
        locatebarcode=locatebarcode, cairosupport=cairosupport, **kwargs
    )


def get_code25_interleaved_barcode_location(*args, **kwargs):
    kwargs["locatebarcode"] = True
    return decode_code25_interleaved_barcode(*args, **kwargs)
