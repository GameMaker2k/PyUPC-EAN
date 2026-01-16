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

    $FileInfo: prepgmagick.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts
import pgmagick

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    basestring  # Py2
except NameError:  # Py3
    basestring = str

try:
    file  # Py2
except NameError:  # Py3
    from io import IOBase as file  # alias

from io import IOBase

try:
    from io import BytesIO
except ImportError:  # old Py2
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

# -------------------------
# Fonts
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath  # kept for compatibility

# -------------------------
# Supported extensions / regex
# -------------------------
PGMAGICK_SUPPORTED_EXTENSIONS = set([
    'PNG', 'JPG', 'JPEG', 'GIF', 'WEBP', 'BMP', 'ICO', 'TIFF', 'HEIC', 'XPM', 'XBM', 'PBM', 'PGM'
])

_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")


# -------------------------
# Helpers
# -------------------------
def _to_pg_color(color):
    """
    Convert color input to pgmagick.Color.
    Preserves original behavior:
    - if (R,G,B) tuple -> convert to #RRGGBB string
    - else -> interpret as pgmagick.Color(color) (name/hex/etc)
    """
    if isinstance(color, tuple) and len(color) == 3:
        return pgmagick.Color('#{:02x}{:02x}{:02x}'.format(*color))
    return pgmagick.Color(color)


def _normalize_ext(ext):
    """Normalize ext to supported set; default PNG. Accepts '.png' or 'png'."""
    if not ext:
        return "PNG"
    e = ext.strip().upper()
    if e.startswith("."):
        e = e[1:]
    if e not in PGMAGICK_SUPPORTED_EXTENSIONS:
        return "PNG"
    return e


def _configure_output_format(img, outfileext_upper):
    """
    Apply the same format-specific options as your original save_to_file.
    """
    # set a default quality (same as original)
    img.quality(100)

    if outfileext_upper == "PNG":
        img.magick('PNG')
        img.interlaceType(pgmagick.InterlaceType.LineInterlace)

    elif outfileext_upper in ("JPG", "JPEG", "JPE"):
        img.magick('JPEG')
        img.interlaceType(pgmagick.InterlaceType.PlaneInterlace)

    elif outfileext_upper == "WEBP":
        img.magick('WEBP')
        img.interlaceType(pgmagick.InterlaceType.PlaneInterlace)
        img.quality(100)
        # keep the same webp lossless define
        img.defineValue('webp', 'lossless', 'true')

    elif outfileext_upper == "TIFF":
        img.magick('TIFF')
        img.compression(pgmagick.CompressionType.LZWCompression)
        img.interlaceType(pgmagick.InterlaceType.LineInterlace)

    elif outfileext_upper == "BMP":
        img.magick('BMP')
        img.depth(24)

    elif outfileext_upper == "GIF":
        img.magick('GIF')
        img.type(pgmagick.ImageType.PaletteType)
        img.interlaceType(pgmagick.InterlaceType.LineInterlace)

    else:
        # fallback: set magick to whatever extension says
        img.magick(outfileext_upper)


# -------------------------
# Public API
# -------------------------
def snapCoords(x, y):
    return (round(x) + 0.5, round(y) + 0.5)


def drawColorRectangle(image, x1, y1, x2, y2, color):
    c = _to_pg_color(color)
    image.fillColor(c)

    dlist = pgmagick.DrawableList()
    dlist.append(pgmagick.DrawableRectangle(x1, y1, x2, y2))
    image.draw(dlist)
    return True


def drawColorLine(image, x1, y1, x2, y2, width, color):
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    c = _to_pg_color(color)
    image.strokeColor(c)
    image.strokeWidth(width)

    dlist = pgmagick.DrawableList()
    dlist.append(pgmagick.DrawableLine(x1, y1, x2, y2))
    image.draw(dlist)
    return True


def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    """
    Keep original behavior:
    - if (R,G,B) tuple: scale to 16-bit (c*257) and construct pgmagick.Color(r,g,b)
      (original did this, unlike rectangle/line)
    - else: pgmagick.Color(color)
    """
    text = str(text)

    if isinstance(color, tuple) and len(color) == 3:
        r, g, b = [int(c) * 257 for c in color]
        c = pgmagick.Color(r, g, b)
    else:
        c = pgmagick.Color(color)

    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra

    image.fillColor(c)
    image.strokeColor('none')
    image.strokeWidth(0)

    image.fontPointsize(size)
    image.font(font_path)

    dlist = pgmagick.DrawableList()
    dlist.append(pgmagick.DrawableText(x, y, text))
    image.draw(dlist)
    return True


def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    # Preserve original (alias)
    return drawColorRectangle(image, x1, y1, x2, y2, color)


def new_image_surface(sizex, sizey, bgcolor):
    bg = _to_pg_color(bgcolor)
    geometry = pgmagick.Geometry(int(sizex), int(sizey))
    img = pgmagick.Image(geometry, bg)
    img.type(pgmagick.ImageType.TrueColorType)
    img.colorSpace(pgmagick.ColorspaceType.sRGBColorspace)
    img.depth(24)
    return [img, None]


def get_save_filename(outfile):
    """
    Same behavior as your original:
    - None/bool passthrough
    - file-like or "-" -> (outfile, "PNG")
    - string -> supports "name.ext" and "name:EXT", defaults to PNG if unsupported
    - tuple/list (filename, ext) -> defaults to PNG if unsupported
    - invalid -> False
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if outfile == "-" or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return (out, "PNG")

        base, ext = os.path.splitext(out)
        if ext:
            return (out, _normalize_ext(ext))

        m = _RE_NAME_COLON_EXT.match(out)
        if m:
            name = m.group("name")
            ext_norm = _normalize_ext(m.group("ext"))
            return (name, ext_norm)

        return (out, "PNG")

    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False
        filename, ext = outfile

        if isinstance(filename, (file, IOBase)) or filename == "-":
            fn = filename
        elif isinstance(filename, basestring):
            fn = filename.strip()
        else:
            return False

        if not isinstance(ext, basestring):
            return False

        return (fn, _normalize_ext(ext))

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the image; keeps:
    - ftp/ftps/sftp upload (via BytesIO)
    - outfile == "-" returns bytes
    - file-like outputs via Blob
    - same format-specific options and comment attribute
    """
    img = inimage[0]

    uploadfile = None
    outfiletovar = False
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    outfmt = _normalize_ext(outfileext)
    _configure_output_format(img, outfmt)

    # Add comment metadata (same as original)
    img.attribute('comment', imgcomment)

    # Write image
    try:
        if isinstance(outfile, (file, IOBase)) or isinstance(outfile, BytesIO):
            blob = pgmagick.Blob()
            img.write(blob)
            outfile.write(blob.data)
        else:
            img.write(outfile)
    except Exception as e:
        raise RuntimeError("Failed to save image: {0}".format(e))

    # Upload / return bytes
    if uploadfile is not None:
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


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, (tuple, list)):
        outdest, outfmt = oldoutfile
        return save_to_file(imgout, outdest, outfmt, imgcomment)
    return [imgout, "pgmagick"]
