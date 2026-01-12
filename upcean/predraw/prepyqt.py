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

    $FileInfo: prepyqt.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QFontDatabase, QPen
from PyQt5.QtCore import QRect, QBuffer, QIODevice

from upcean.fonts import (
    fontpathocra, fontpathocraalt,
    fontpathocrb, fontpathocrbalt,
    fontpath
)
from upcean.downloader import upload_file_to_internet_file

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
    from io import BytesIO
except ImportError:  # old Py2
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

# -------------------------
# Regex / constants
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

_VALID_EXTS = set(["PNG", "JPEG", "JPG", "BMP", "GIF", "RAW"])


# -------------------------
# Helpers
# -------------------------
def color_to_qcolor(color):
    if isinstance(color, tuple):
        if len(color) in (3, 4):
            return QColor(*color)
        raise ValueError("Color tuple must be of length 3 or 4.")
    if isinstance(color, basestring):
        return QColor(color)
    raise ValueError("Color must be a tuple or string.")


def _rect_from_coords(x1, y1, x2, y2):
    return QRect(int(x1), int(y1), int(x2 - x1), int(y2 - y1))


def _with_painter(image):
    """
    Small helper to ensure painter.end() always happens.
    Usage:
        painter = _with_painter(img)
        ...
        painter.end()
    (Kept explicit end() calls to remain close to original behavior.)
    """
    return QPainter(image)


# Cache loaded application fonts so we don't re-add them every draw call.
# Key: absolute path -> family name (or None if failed)
_FONT_FAMILY_CACHE = {}


def _load_font_family(path):
    """
    Add a font file to the QFontDatabase once and cache its family name.
    Returns family name or None.
    """
    if not path:
        return None

    cached = _FONT_FAMILY_CACHE.get(path, None)
    # Use a sentinel to distinguish "not attempted" vs "failed"
    if path in _FONT_FAMILY_CACHE:
        return cached

    try:
        font_id = QFontDatabase.addApplicationFont(path)
    except Exception:
        font_id = -1

    if font_id == -1:
        _FONT_FAMILY_CACHE[path] = None
        return None

    families = QFontDatabase.applicationFontFamilies(font_id)
    fam = families[0] if families else None
    _FONT_FAMILY_CACHE[path] = fam
    return fam


def _pick_qfont(ftype, size):
    """
    Match your original preference order:
    - ocra: try primary then alt
    - ocrb: try primary then alt
    - else: try fontpath, else default system font
    """
    size = int(size) if int(size) > 0 else 12

    if ftype == "ocra":
        fam = _load_font_family(fontpathocra) or _load_font_family(fontpathocraalt)
    elif ftype == "ocrb":
        fam = _load_font_family(fontpathocrb) or _load_font_family(fontpathocrbalt)
    else:
        fam = _load_font_family(fontpath)

    if fam:
        return QFont(fam, size)

    # fallback default font
    f = QFont()
    f.setPointSize(size)
    return f


def _qimage_to_bytes(image, fmt_upper):
    """
    Encode via QBuffer for normal formats.
    """
    buf = QBuffer()
    buf.open(QIODevice.ReadWrite)
    ok = image.save(buf, fmt_upper)
    if not ok:
        buf.close()
        raise IOError("Failed to encode image.")
    data = bytes(buf.data().data())
    buf.close()
    return data


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(image, x1, y1, x2, y2, color):
    c = color_to_qcolor(color)
    painter = _with_painter(image)
    painter.setPen(c)
    painter.setBrush(c)
    painter.drawRect(_rect_from_coords(x1, y1, x2, y2))
    painter.end()
    return True


def drawColorLine(image, x1, y1, x2, y2, width, color):
    w = int(width)
    if w < 1:
        w = 1
    c = color_to_qcolor(color)

    painter = _with_painter(image)
    pen = QPen(c)
    pen.setWidth(w)
    painter.setPen(pen)
    painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    painter.end()
    return True


def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    """
    Keeps original baseline adjustment: draws at (x, y + size).
    """
    c = color_to_qcolor(color)
    t = str(text)

    painter = _with_painter(image)
    painter.setPen(c)

    font = _pick_qfont(ftype, size)
    painter.setFont(font)

    painter.drawText(int(x), int(y) + int(size), t)
    painter.end()
    return True


def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    c = color_to_qcolor(color)
    painter = _with_painter(image)
    painter.setPen(c)
    painter.drawRect(_rect_from_coords(x1, y1, x2, y2))
    painter.end()
    return True


def new_image_surface(sizex, sizey, bgcolor):
    """
    Keeps original: ARGB32 QImage filled with bgcolor.
    """
    bg = color_to_qcolor(bgcolor)
    img = QImage(int(sizex), int(sizey), QImage.Format_ARGB32)
    img.fill(bg)
    return img


# -------------------------
# Filename parsing
# -------------------------
def get_save_filename(outfile):
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # file-like or "-" => default PNG
    if outfile == "-" or hasattr(outfile, "write"):
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

        if ext_u not in _VALID_EXTS:
            ext_u = "PNG"
        return (out, ext_u)

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


# -------------------------
# Saving
# -------------------------
def save_to_file(image, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the QImage to a file, uploads it, writes to a file-like object,
    or returns bytes when outfile is '-' or None.
    RAW behavior: returns/writes image.bits() (ARGB32 bytes) rather than an encoded file.
    """
    ext_u = (outfileext or "PNG").upper()
    if ext_u not in _VALID_EXTS:
        ext_u = "PNG"

    uploadfile = None
    outfiletovar = False

    if isinstance(outfile, basestring):
        if _RE_URL.match(outfile):
            uploadfile = outfile
            outfile = BytesIO()
        elif outfile == "-":
            outfiletovar = True
            outfile = BytesIO()
        else:
            # Save directly to filename unless RAW
            if ext_u == "RAW":
                # Write raw pixel bytes to path
                data = bytes(image.bits().asstring(image.byteCount()))
                with open(outfile, "wb") as f:
                    f.write(data)
                return True

            ok = image.save(outfile, ext_u)
            if not ok:
                raise IOError("Failed to save image to file.")
            return True

    # outfile is None => return bytes
    if outfile is None:
        if ext_u == "RAW":
            return bytes(image.bits().asstring(image.byteCount()))
        return _qimage_to_bytes(image, ext_u)

    # file-like => write bytes
    if hasattr(outfile, "write"):
        if ext_u == "RAW":
            data = bytes(image.bits().asstring(image.byteCount()))
        else:
            data = _qimage_to_bytes(image, ext_u)
        outfile.write(data)
        return True

    # If we got here, outfile was turned into BytesIO for upload or "-" return
    if uploadfile or outfiletovar:
        if ext_u == "RAW":
            data = bytes(image.bits().asstring(image.byteCount()))
            outfile.write(data)
        else:
            data = _qimage_to_bytes(image, ext_u)
            outfile.write(data)

        if uploadfile:
            outfile.seek(0)
            upload_file_to_internet_file(outfile, uploadfile)
            outfile.close()
            return True

        # "-" semantics: return bytes
        outfile.seek(0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    raise ValueError("Invalid outfile type")


def save_to_filename(image, outfile, imgcomment="barcode"):
    info = get_save_filename(outfile) if outfile is not None else None
    if isinstance(info, (tuple, list)):
        outdest, ext_u = info[0], info[1]
    else:
        outdest, ext_u = outfile, "PNG"

    if ext_u is None:
        ext_u = "PNG"

    return save_to_file(image, outdest, ext_u, imgcomment)
