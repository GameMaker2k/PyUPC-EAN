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

    $FileInfo: premagick.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts
import PythonMagick

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
# Font paths
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocrb = upcean.fonts.fontpathocrb

# -------------------------
# Supported extensions / regex
# -------------------------
PYTHONMAGICK_SUPPORTED_EXTENSIONS = {
    'PNG': 'PNG', 'JPG': 'JPEG', 'JPEG': 'JPEG', 'GIF': 'GIF', 'WEBP': 'WEBP',
    'BMP': 'BMP', 'ICO': 'ICO', 'TIFF': 'TIFF', 'HEIC': 'HEIC', 'XPM': 'XPM',
    'XBM': 'XBM', 'PBM': 'PBM', 'PGM': 'PGM'
}

_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")


# -------------------------
# Helpers
# -------------------------
def _to_magick_color(rgb):
    """
    Convert (R,G,B) where components are 0..255 into PythonMagick.Color using 16-bit scaling.
    ImageMagick uses QuantumRange (often 16-bit); 255 -> 65535 by *257.
    """
    r, g, b = rgb
    return PythonMagick.Color(int(r) * 257, int(g) * 257, int(b) * 257)


def _normalize_ext(ext):
    """Normalize an extension string to a supported magick format, default PNG."""
    if not ext:
        return "PNG"
    ext_u = ext.strip().upper()
    if ext_u.startswith("."):
        ext_u = ext_u[1:]
    # map JPG -> JPEG etc (values are canonical format names)
    return PYTHONMAGICK_SUPPORTED_EXTENSIONS.get(ext_u, "PNG")


# -------------------------
# Public API
# -------------------------
def snapCoords(ctx, x, y):
    # ctx unused; kept for signature compatibility
    return (round(x) + 0.5, round(y) + 0.5)


def drawColorRectangle(image, x1, y1, x2, y2, color):
    """Draw a filled rectangle on the image. `color` is (R,G,B) in 0..255."""
    draw_color = _to_magick_color(color)
    image.fillColor(draw_color)
    image.strokeColor("none")  # no border
    image.draw(PythonMagick.DrawableRectangle(x1, y1, x2, y2))
    return True


def drawColorLine(image, x1, y1, x2, y2, width, color):
    """Draw a line on the image. `color` is (R,G,B) in 0..255."""
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    stroke_color = _to_magick_color(color)
    image.strokeColor(stroke_color)
    image.strokeWidth(width)
    image.draw(PythonMagick.DrawableLine(x1, y1, x2, y2))
    return True


def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    """
    Draw colored text using OCR-A or OCR-B font.
    Behavior preserved:
    - If `color` is a 3-tuple, treat as RGB 0..255.
    - Otherwise pass through as a string to PythonMagick.Color (names/hex).
    - No stroke/outline.
    """
    text = str(text)

    if isinstance(color, tuple) and len(color) == 3:
        fill_color = _to_magick_color(color)
    else:
        fill_color = PythonMagick.Color(color)

    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra

    image.fillColor(fill_color)
    image.strokeColor("none")
    image.strokeWidth(0)

    image.fontPointsize(size)
    image.font(font_path)

    image.draw(PythonMagick.DrawableText(x, y, text))
    return True


def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    """Draw a rectangle outline (no fill). `color` is (R,G,B) in 0..255."""
    stroke_color = _to_magick_color(color)
    image.fillColor("none")
    image.strokeColor(stroke_color)
    image.draw(PythonMagick.DrawableRectangle(x1, y1, x2, y2))
    return True


def new_image_surface(sizex, sizey, bgcolor):
    """Create a new image with background color. Returns [image, None] (same as original)."""
    background_color = _to_magick_color(bgcolor)
    geometry = PythonMagick.Geometry(int(sizex), int(sizey))
    img = PythonMagick.Image(geometry, background_color)
    img.depth(24)
    # keep the explicit fill call as in original
    drawColorRectangle(img, 0, 0, sizex, sizey, bgcolor)
    return [img, None]


def get_save_filename(outfile):
    """
    Normalize outfile spec to (destination, EXT).
    Same behavior as original:
    - None/bool passthrough
    - file-like or "-" -> (outfile, "PNG")
    - string -> supports "name.ext" and "name:EXT" and defaults to PNG if unsupported
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
            ext_norm = _normalize_ext(ext)
            return (out, ext_norm)

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


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Save image with comment and format.
    Keeps:
    - ftp/ftps/sftp upload via BytesIO buffer
    - outfile == "-" returns bytes
    - file-like objects: write via Blob
    """
    img = inimage[0]
    outfmt = _normalize_ext(outfileext)

    # set metadata/format
    img.comment(imgcomment)
    img.magick(outfmt)

    uploadfile = None
    outfiletovar = False

    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Write to destination
    if isinstance(outfile, (file, IOBase)):
        blob = PythonMagick.Blob()
        img.write(blob)
        # PythonMagick.Blob().data is bytes-like
        outfile.write(blob.data)
    else:
        # outfile is path OR BytesIO; PythonMagick can write to a filename,
        # and for in-memory we handle via blob below.
        if isinstance(outfile, BytesIO):
            blob = PythonMagick.Blob()
            img.write(blob)
            outfile.write(blob.data)
        else:
            img.write(outfile)

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
    """
    Wrapper consistent with your original:
    - If outfile parses to (dest, ext): save.
    - Else: return [imgout, "pythonmagick"].
    """
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, (tuple, list)):
        outdest, outfmt = oldoutfile
        return save_to_file(imgout, outdest, outfmt, imgcomment)
    return [imgout, "pythonmagick"]
