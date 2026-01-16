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

    $FileInfo: preskimage.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

import numpy as np
import skimage.draw

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    basestring  # Py2
except NameError:  # Py3
    basestring = str

try:
    unicode  # Py2
except NameError:  # Py3
    unicode = str

try:
    file  # Py2
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import BytesIO
except ImportError:
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

# Text drawing (fast)
from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL import ImageFont as PILImageFont

# Fonts
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

# Regex / constants
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

_SUPPORTED_EXTS = set(["PNG", "JPG", "JPEG", "BMP", "TIFF", "RAW"])


# -------------------------
# Drawing helpers
# -------------------------
def _clip_rrcc(rr, cc, h, w):
    m = (rr >= 0) & (rr < h) & (cc >= 0) & (cc < w)
    return rr[m], cc[m]


def drawColorRectangle(img, x1, y1, x2, y2, color):
    """
    Filled rectangle (x1,y1) -> (x2,y2) in image coords.
    Uses skimage.draw.rectangle; end is inclusive in skimage rectangle API when given end.
    Original code used end=(y2-1,x2-1) to make [x1,x2) and [y1,y2) semantics.
    """
    h, w = img.shape[0], img.shape[1]
    x1 = int(x1); y1 = int(y1); x2 = int(x2); y2 = int(y2)
    if x2 <= x1 or y2 <= y1:
        return True

    # clamp to bounds while preserving half-open semantics
    x1c = max(0, min(w, x1))
    x2c = max(0, min(w, x2))
    y1c = max(0, min(h, y1))
    y2c = max(0, min(h, y2))
    if x2c <= x1c or y2c <= y1c:
        return True

    rr, cc = skimage.draw.rectangle(start=(y1c, x1c), end=(y2c - 1, x2c - 1))
    img[rr, cc] = color
    return True


import math
import skimage.draw

def drawColorLine(img, x1, y1, x2, y2, width, color):
    """
    Draw a line and emulate thickness by drawing parallel lines offset
    perpendicular to the line direction (fixes diagonal "teeth" artifacts).
    """
    width = max(1, int(width))
    h, w = img.shape[0], img.shape[1]

    x1 = int(x1); y1 = int(y1); x2 = int(x2); y2 = int(y2)

    def _plot_line(ax1, ay1, ax2, ay2):
        rr, cc = skimage.draw.line(ay1, ax1, ay2, ax2)
        m = (rr >= 0) & (rr < h) & (cc >= 0) & (cc < w)
        rr = rr[m]; cc = cc[m]
        if rr.size:
            img[rr, cc] = color

    half = width // 2

    # Fast/common cases (barcodes are usually vertical)
    if x1 == x2:
        for dx in range(-half, half + 1):
            _plot_line(x1 + dx, y1, x2 + dx, y2)
        return True

    if y1 == y2:
        for dy in range(-half, half + 1):
            _plot_line(x1, y1 + dy, x2, y2 + dy)
        return True

    # General case: offset along the unit normal
    dx = float(x2 - x1)
    dy = float(y2 - y1)
    length = math.hypot(dx, dy)
    if length <= 0.0:
        _plot_line(x1, y1, x2, y2)
        return True

    # Normal vector (perpendicular)
    nx = -dy / length
    ny =  dx / length

    for off in range(-half, half + 1):
        ox = int(round(nx * off))
        oy = int(round(ny * off))
        _plot_line(x1 + ox, y1 + oy, x2 + ox, y2 + oy)

    return True


# Cache PIL fonts: (path, size) -> ImageFont
_FONT_CACHE = {}


def _pick_font_path(ftype):
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    elif ftype == "ocrb":
        primary, alt = fontpathocrb, fontpathocrbalt
    else:
        primary, alt = fontpath, None

    if primary and os.path.isfile(primary):
        return primary
    if alt and os.path.isfile(alt):
        return alt
    return primary


def _get_pil_font(ftype, size):
    size = int(size)
    if size <= 0:
        size = 12
    path = _pick_font_path(ftype)
    key = (path, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    try:
        f = PILImageFont.truetype(path, size) if path else PILImageFont.load_default()
    except Exception:
        f = PILImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


def drawColorText(img, size, x, y, text, color, ftype="ocrb"):
    """
    Fast text drawing using PIL instead of matplotlib figure rendering.
    Semantics: draw at (x, y) with top-aligned text (like your matplotlib code used verticalalignment='top').
    """
    # Ensure uint8 RGB
    if img.dtype != np.uint8:
        img[:] = np.clip(img, 0, 255).astype(np.uint8)
    if img.ndim != 3 or img.shape[2] != 3:
        return False

    t = str(text)
    x = int(x); y = int(y)

    # Convert numpy -> PIL (view/copy). Using fromarray copies; acceptable and fast enough.
    pil = PILImage.fromarray(img, mode="RGB")
    draw = PILImageDraw.Draw(pil)
    font = _get_pil_font(ftype, size)

    # PIL expects RGB tuple
    rgb = (int(color[0]), int(color[1]), int(color[2]))
    draw.text((x, y), t, font=font, fill=rgb)

    # Write back
    img[:] = np.asarray(pil, dtype=np.uint8)
    return True


def drawColorRectangleAlt(img, x1, y1, x2, y2, color):
    # Outline rectangle using 1px lines
    drawColorLine(img, x1, y1, x2, y1, 1, color)
    drawColorLine(img, x1, y2 - 1, x2, y2 - 1, 1, color)
    drawColorLine(img, x1, y1, x1, y2, 1, color)
    drawColorLine(img, x2 - 1, y1, x2 - 1, y2, 1, color)
    return True


# -------------------------
# File handling
# -------------------------
def get_save_filename(outfile):
    """
    Returns:
      - outfile (unchanged) if None or bool
      - (outfile, "PNG") for file-like objects or "-"
      - (filename, EXT) for strings / (filename, ext) tuples
      - False for invalid
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # file-like or "-" => default PNG (matches other backends)
    if outfile == "-" or hasattr(outfile, "write") or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return (out, "PNG")

        base, ext = os.path.splitext(out)
        if ext:
            ext_u = ext[1:].upper()
        else:
            m = _RE_NAME_COLON_EXT.match(out)
            if m:
                out = m.group("name")
                ext_u = m.group("ext").upper()
            else:
                ext_u = "PNG"

        if not ext_u:
            ext_u = "PNG"
        if ext_u not in _SUPPORTED_EXTS:
            ext_u = "PNG"
        return (out, ext_u)

    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile
        if not (isinstance(ext, basestring)):
            return False
        ext_u = ext.strip().upper()
        if ext_u not in _SUPPORTED_EXTS:
            ext_u = "PNG"
        return (filename, ext_u)

    return False


def new_image_surface(sizex, sizey, bgcolor):
    img = np.zeros((int(sizey), int(sizex), 3), dtype=np.uint8)
    img[:, :] = (int(bgcolor[0]), int(bgcolor[1]), int(bgcolor[2]))
    return [img, "skimage"]


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves using imageio directly (no skimage.io plugin warnings).
    RAW writes/returns raw RGB bytes (row-major).
    """
    img = inimage[0]
    ext_u = (outfileext or "PNG").upper()
    if ext_u not in _SUPPORTED_EXTS:
        ext_u = "PNG"

    uploadfile = None
    outfiletovar = False

    if isinstance(outfile, basestring):
        if _RE_URL.match(str(outfile)):
            uploadfile = outfile
            outfile = BytesIO()
        elif outfile == "-":
            outfiletovar = True
            outfile = BytesIO()

    # RAW: just dump bytes (no header)
    if ext_u == "RAW":
        data = img.tobytes()
        if uploadfile:
            outfile.write(data)
            outfile.seek(0)
            upload_file_to_internet_file(outfile, uploadfile)
            outfile.close()
            return True
        if outfiletovar:
            return data
        if hasattr(outfile, "write"):
            outfile.write(data)
            return True
        if isinstance(outfile, basestring):
            f = open(outfile, "wb")
            try:
                f.write(data)
            finally:
                f.close()
            return True
        return False

    # Normalize format string for imageio
    fmt = ext_u.lower()
    if fmt == "jpg":
        fmt = "jpeg"

    # Use imageio directly (avoid skimage.io plugin infra)
    try:
        import imageio.v2 as imageio  # preferred: stable "v2" API, no deprecation spam
    except Exception:
        import imageio  # fallback

    if isinstance(outfile, basestring):
        # Let imageio infer from filename; still pass format for consistency
        imageio.imwrite(outfile, img, format=fmt)
        return True

    if hasattr(outfile, "write"):
        # file-like object
        imageio.imwrite(outfile, img, format=fmt)

        if uploadfile:
            outfile.seek(0)
            upload_file_to_internet_file(outfile, uploadfile)
            outfile.close()
            return True

        if outfiletovar:
            outfile.seek(0)
            outbyte = outfile.read()
            outfile.close()
            return outbyte

        return True

    return False


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    if outfile is None:
        old = None
        outdest = None
        ext = None
    else:
        old = get_save_filename(outfile)
        if isinstance(old, (tuple, list)):
            outdest, ext = old[0], old[1]
        else:
            return False

    if old is None or isinstance(old, bool):
        return [imgout[0], imgout[1], "skimage"]

    return save_to_file(imgout, outdest, ext, imgcomment)
