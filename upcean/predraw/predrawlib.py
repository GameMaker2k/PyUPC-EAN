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

    $FileInfo: predrawlib.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

import os
import re
import math

from drawlib.apis import (
    clear, config, rectangle, line, text, save,
    ShapeStyle, LineStyle, TextStyle, Colors, FontFile
)
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
    from io import BytesIO, IOBase
except ImportError:  # Py2
    from StringIO import StringIO as BytesIO  # bytes-ish in many Py2 setups
    try:
        from StringIO import StringIO as IOBase
    except Exception:
        IOBase = object

try:
    import gzip
except ImportError:
    gzip = None

# -------------------------
# Fonts
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt

# -------------------------
# Regex / constants
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z0-9]+)$")

_DEFAULT_EXT = "png"

# Cache FontFile instances (FontFile(ttf) can be non-trivial)
_FONTFILE_CACHE = {}


def _get_fontfile(ftype):
    f = (ftype or "ocrb").lower()
    if f == "ocra":
        ttf = fontpathocra if os.path.exists(fontpathocra) else fontpathocraalt
    else:
        ttf = fontpathocrb if os.path.exists(fontpathocrb) else fontpathocrbalt

    key = ttf
    ff = _FONTFILE_CACHE.get(key)
    if ff is None:
        ff = FontFile(ttf)
        _FONTFILE_CACHE[key] = ff
    return ff


def _is_file_like(x):
    return hasattr(x, "write") or isinstance(x, IOBase)


def _to_bytes(data):
    # Py2/3 safe: ensure bytes
    if isinstance(data, bytes):
        return data
    try:
        return data.encode("utf-8")
    except Exception:
        return bytes(data)


def _gzip_bytes(data_bytes, compresslevel=9):
    if gzip is None:
        raise ImportError("gzip module not available")
    out = BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=out, compresslevel=compresslevel)
    try:
        gz.write(data_bytes)
    finally:
        gz.close()
    return out.getvalue()


def snapCoords(ctx, x, y):
    # keeps signature compatibility with other backends
    return (round(x) + 0.5, round(y) + 0.5)


# -------------------------
# Coordinate conversion
# -------------------------
def _img_to_draw_y(H, y_img):
    """
    Convert image coords (origin top-left, y down)
    to drawlib coords (origin bottom-left, y up).
    """
    return float(H) - float(y_img)


def _rect_img_to_draw(H, x1, y1, x2, y2):
    """
    Input is image-style half-open rectangle:
      [x1,x2) and [y1,y2)
    Return drawlib-style rectangle (x, y, w, h)
    where (x,y) is *top-left* in image coords, but drawlib uses bottom-left.
    So we flip by using y = H - y2.
    """
    x1 = float(x1); y1 = float(y1); x2 = float(x2); y2 = float(y2)
    w = x2 - x1
    h = y2 - y1
    # y2 is "lower" in image coords; in draw coords it becomes the bottom distance
    y_draw = float(H) - y2
    return x1, y_draw, w, h


# -------------------------
# Drawlib context shim
# -------------------------
class DrawlibContext(object):
    """
    Shim context so existing code can call ctx.rectangle/line/text like Pillow/Cairo backends.

    IMPORTANT: drawlib's coordinate system is (0,0) bottom-left. Upcean renderers are top-left.
    We convert incoming coords from image-space to drawlib-space here.
    """
    def __init__(self, width, height, dpi=100):
        self.width = float(width)
        self.height = float(height)
        self.dpi = int(dpi)

    def user_to_device(self, x, y):
        # keep signature compatibility; return drawlib coords
        return float(x), _img_to_draw_y(self.height, y)

    def rectangle(self, coords, fill=None, outline=None):
        (x1, y1), (x2, y2) = coords
        x, y, w, h = _rect_img_to_draw(self.height, x1, y1, x2, y2)

        if fill is not None:
            style = ShapeStyle(halign="left", valign="bottom", fcolor=fill, lwidth=0)
        else:
            style = ShapeStyle(
                halign="left", valign="bottom",
                fcolor=Colors.Transparent, lcolor=outline, lwidth=1
            )

        rectangle(xy=(x, y), width=w, height=h, style=style)

    def line(self, pts, fill, width):
        (x1, y1), (x2, y2) = pts
        x1 = float(x1); x2 = float(x2)
        y1d = _img_to_draw_y(self.height, y1)
        y2d = _img_to_draw_y(self.height, y2)

        style = LineStyle(width=max(1, int(width)), color=fill)
        line((x1, y1d), (x2, y2d), style=style)

    def text(self, pos, txt, font=None, fill=None, size=None):
        x, y = pos
        s = int(size) if size is not None else None

        # Upcean y is "top aligned" for text in several backends.
        # Convert to drawlib coords and subtract size to keep it top-aligned.
        y_draw = _img_to_draw_y(self.height, y)
        if s:
            y_draw -= float(s)

        style = TextStyle(color=fill, font=font)
        # enforce sensible anchor (if supported by drawlib)
        try:
            style.halign = "left"
            style.valign = "bottom"
        except Exception:
            pass
        if s is not None:
            style.size = s

        text(xy=(float(x), float(y_draw)), text=str(txt), style=style)


# -------------------------
# Drawing functions (public API)
# -------------------------
def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], fill=color)
    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], outline=color)
    return True


def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib=None):
    """
    IMPORTANT: For barcode bars, stroked lines can create end-caps/oddness.
    Emulate Cairo backend behavior:
      - if perfectly vertical/horizontal -> draw a filled rectangle of thickness `width`
      - else fallback to drawlib line()
    """
    try:
        w = int(width)
    except Exception:
        w = 1
    if w < 1:
        w = 1

    # Vertical line => rectangle
    if int(x1) == int(x2):
        cx = float(x1) - (w / 2.0)
        y_top = min(float(y1), float(y2))
        y_bot = max(float(y1), float(y2))
        ctx.rectangle([(cx, y_top), (cx + w, y_bot)], fill=color)
        return True

    # Horizontal line => rectangle
    if int(y1) == int(y2):
        cy = float(y1) - (w / 2.0)
        x_left = min(float(x1), float(x2))
        x_right = max(float(x1), float(x2))
        ctx.rectangle([(x_left, cy), (x_right, cy + w)], fill=color)
        return True

    # Diagonal => stroke
    ctx.line([(x1, y1), (x2, y2)], fill=color, width=w)
    return True


def drawColorText(ctx, size, x, y, txt, color, ftype="ocrb", imageoutlib=None):
    font_file = _get_fontfile(ftype)

    # drawlib’s “normal” look is around dpi=100
    base_dpi = 100
    dpi = getattr(ctx, "dpi", base_dpi) or base_dpi

    scaled_size = int(round(float(size) * (float(base_dpi) / float(dpi))))
    if scaled_size < 1:
        scaled_size = 1

    ctx.text((x, y), str(txt), font=font_file, fill=color, size=scaled_size)
    return True


# -------------------------
# Save filename parsing
# -------------------------
def get_save_filename(outfile, imageoutlib=None):
    """
    Returns:
      - outfile unchanged if None/bool
      - (outfile, "png") for file-like objects or "-"
      - (name_or_path_or_url, ext) for strings/tuples
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if outfile == "-" or _is_file_like(outfile):
        return (outfile, _DEFAULT_EXT)

    if isinstance(outfile, basestring):
        s = outfile.strip()
        if s == "" or s == "-":
            return (s, _DEFAULT_EXT)
        if _RE_URL.match(s):
            return (s, _DEFAULT_EXT)

        base, ext = os.path.splitext(s)
        if ext:
            ext = ext.lstrip(".").lower()
            name = base
        else:
            m = _RE_NAME_EXT.match(s)
            if m:
                name = m.group("name")
                ext = m.group("ext").lower()
            else:
                name = s
                ext = _DEFAULT_EXT

        if not ext:
            ext = _DEFAULT_EXT
        return (name, ext)

    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        return (outfile[0], str(outfile[1]).lower())

    return False


get_save_file = get_save_filename


# -------------------------
# Surface creation
# -------------------------
def new_image_surface(sizex, sizey, bgcolor, imageoutlib=None):
    clear()

    dpi = int(math.ceil(float(sizex) / 10.0))
    if dpi < 1:
        dpi = 1

    config(width=sizex, height=sizey, dpi=dpi, background_color=bgcolor)
    print(sizex, sizey, "dpi=", dpi)

    return [DrawlibContext(sizex, sizey, dpi=dpi), None]


# -------------------------
# Saving
# -------------------------
def _normalize_local_path(path, outfileext):
    p = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    ext = str(outfileext).lower()
    if ext and not p.lower().endswith("." + ext):
        p = p + "." + ext
    return p


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode", imageoutlib=None):
    """
    drawlib save() can write to:
      - path string
      - file-like (e.g., BytesIO)
    """
    upload_target = None
    return_bytes = False

    ext = (outfileext or _DEFAULT_EXT).lower()

    if isinstance(outfile, basestring) and _RE_URL.match(outfile):
        upload_target = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfile = BytesIO()
        return_bytes = True

    if isinstance(outfile, basestring) and not _RE_URL.match(outfile) and outfile not in ("-", ""):
        outfile = _normalize_local_path(outfile, ext)

    save(file=outfile, format=ext)

    if upload_target:
        outfile.seek(0)
        upload_file_to_internet_file(outfile, upload_target)
        outfile.close()
        return True

    if return_bytes:
        outfile.seek(0)
        data = outfile.read()
        outfile.close()
        return data

    return True


def save_to_filename(imgout, outfile, imgcomment="barcode", imageoutlib=None):
    parsed = get_save_filename(outfile, imageoutlib)
    if not parsed or isinstance(parsed, bool):
        return False if parsed is False else [None, None, imageoutlib]

    name, ext = parsed
    return save_to_file(imgout, name, ext, imgcomment, imageoutlib)
