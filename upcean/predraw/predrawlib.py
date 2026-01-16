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
    # ctx.user_to_device kept for signature-compat (even if unused by drawlib)
    return (round(x) + 0.5, round(y) + 0.5)


class DrawlibContext(object):
    """Shim context so existing code can call ctx.rectangle/line/text like Pillow/Cairo backends."""

    def user_to_device(self, x, y):
        return x, y

    def rectangle(self, coords, fill=None, outline=None):
        (x1, y1), (x2, y2) = coords
        w = x2 - x1
        h = y2 - y1
        if fill is not None:
            style = ShapeStyle(halign="left", valign="top", fcolor=fill, lwidth=0)
        else:
            style = ShapeStyle(
                halign="left", valign="top",
                fcolor=Colors.Transparent, lcolor=outline, lwidth=1
            )
        rectangle(xy=(x1, y1), width=w, height=h, style=style)

    def line(self, pts, fill, width):
        (x1, y1), (x2, y2) = pts
        style = LineStyle(width=max(1, int(width)), color=fill)
        line((x1, y1), (x2, y2), style=style)

    def text(self, pos, txt, font=None, fill=None, size=None):
        x, y = pos
        style = TextStyle(color=fill, font=font)
        if size is not None:
            style.size = size  # keep your sizing behavior
        text(xy=(x, y), text=str(txt), style=style)


def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], fill=color)
    return True


def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib=None):
    ctx.line([(x1, y1), (x2, y2)], fill=color, width=width)
    return True


def drawColorText(ctx, size, x, y, txt, color, ftype="ocrb", imageoutlib=None):
    font_file = _get_fontfile(ftype)
    ctx.text((x, y), str(txt), font=font_file, fill=color, size=size)
    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], outline=color)
    return True


def get_save_filename(outfile, imageoutlib=None):
    """
    Returns:
      - outfile unchanged if None/bool
      - (outfile, "png") for file-like objects or "-"
      - (name_or_path_or_url, ext) for strings/tuples

    Now also supports: .svgz (or :svgz) returning ext "svgz"
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


def new_image_surface(sizex, sizey, bgcolor, imageoutlib=None):
    clear()
    config(width=sizex, height=sizey, background_color=bgcolor)
    return [DrawlibContext(), None]


def _normalize_local_path(path, outfileext):
    """
    Only for local filesystem string paths (NOT urls, NOT file-like).
    Expands ~ and env vars, makes absolute, appends extension if missing.
    """
    p = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
    ext = str(outfileext).lower()
    if ext and not p.lower().endswith("." + ext):
        p = p + "." + ext
    return p


def _save_svgz_to_destination(outfile, upload_target=None, return_bytes=False):
    """
    drawlib doesn't directly write SVGZ. We:
      1) save SVG into a BytesIO
      2) gzip it
      3) write/upload/return
    """
    # 1) render SVG to bytes
    svg_buf = BytesIO()
    save(file=svg_buf, format="svg")  # SVG XML
    svg_buf.seek(0)
    svg_bytes = svg_buf.read()
    svg_buf.close()

    # 2) gzip
    gz_bytes = _gzip_bytes(_to_bytes(svg_bytes))

    # 3) deliver
    if upload_target:
        tmp = BytesIO()
        tmp.write(gz_bytes)
        tmp.seek(0)
        upload_file_to_internet_file(tmp, upload_target)
        tmp.close()
        return True

    if return_bytes:
        return gz_bytes

    # file-like object
    if _is_file_like(outfile):
        outfile.write(gz_bytes)
        return True

    # path
    f = open(outfile, "wb")
    try:
        f.write(gz_bytes)
    finally:
        f.close()
    return True


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode", imageoutlib=None):
    """
    drawlib save() can write to:
      - path string
      - file-like (e.g., BytesIO)

    Added: SVGZ support
      - if outfileext is "svgz" or parsed from .svgz
      - produces gzip-compressed SVG bytes
      - supports: local path, file-like, ftp upload, "-" return bytes
    """
    upload_target = None
    return_bytes = False

    ext = (outfileext or _DEFAULT_EXT).lower()

    # remote upload via URL
    if isinstance(outfile, basestring) and _RE_URL.match(outfile):
        upload_target = outfile
        # svgz and binary outputs need BytesIO
        outfile = BytesIO()
    elif outfile == "-":
        outfile = BytesIO()
        return_bytes = True

    # local path normalization
    if isinstance(outfile, basestring) and not _RE_URL.match(outfile) and outfile not in ("-", ""):
        outfile = _normalize_local_path(outfile, ext)

    # --- SVGZ handling ---
    if ext == "svgz":
        # If outfile is a path string, ensure it ends with .svgz
        if isinstance(outfile, basestring) and not _RE_URL.match(outfile) and outfile not in ("-", ""):
            if not outfile.lower().endswith(".svgz"):
                outfile = outfile + ".svgz"
        return _save_svgz_to_destination(outfile, upload_target=upload_target, return_bytes=return_bytes)

    # --- Normal formats ---
    save(file=outfile, format=ext)

    # Upload / bytes handling
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
        # Preserve your convention: False means invalid, None/bool passes through
        return False if parsed is False else [None, None, imageoutlib]

    name, ext = parsed
    return save_to_file(imgout, name, ext, imgcomment, imageoutlib)
