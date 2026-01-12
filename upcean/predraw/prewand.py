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

    $FileInfo: prewand.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor
from wand.version import formats as wformats

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
# Regex / supported formats
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

# Cache supported formats once (uppercase)
_WAND_FORMATS = None


def _wand_supported_formats():
    global _WAND_FORMATS
    if _WAND_FORMATS is None:
        _WAND_FORMATS = set(fmt.upper() for fmt in wformats())
    return _WAND_FORMATS


def _to_hex_color(color):
    """
    Convert (R,G,B) to '#RRGGBB' string. If already a string, return as-is.
    """
    if isinstance(color, tuple) and len(color) == 3:
        return '#{:02x}{:02x}{:02x}'.format(*color)
    return color


def snapCoords(ctx, x, y):
    # ctx unused; kept for signature compatibility with other backends
    return (round(x) + 0.5, round(y) + 0.5)


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(image, x1, y1, x2, y2, color):
    c = _to_hex_color(color)
    with wDrawing() as draw:
        draw.fill_color = wColor(c)
        draw.rectangle(left=x1, top=y1, width=(x2 - x1), height=(y2 - y1))
        draw(image)
    return True


def drawColorLine(image, x1, y1, x2, y2, width, color):
    c = _to_hex_color(color)
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    with wDrawing() as draw:
        draw.stroke_color = wColor(c)
        draw.stroke_width = width
        draw.line((x1, y1), (x2, y2))
        draw(image)
    return True


def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    c = _to_hex_color(color)
    text = str(text)

    # match original: choose OCRB vs OCRA path
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra

    with wDrawing() as draw:
        draw.font = font_path
        draw.font_size = size
        draw.fill_color = wColor(c)
        draw.text(x, y, text)
        draw(image)
    return True


def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    c = _to_hex_color(color)
    with wDrawing() as draw:
        draw.stroke_color = wColor(c)
        # preserve original: no explicit fill_color set (Wand defaults apply)
        draw.rectangle(left=x1, top=y1, width=(x2 - x1), height=(y2 - y1))
        draw(image)
    return True


def new_image_surface(sizex, sizey, bgcolor):
    """
    Create a new truecolor RGB image with background color.
    Returns [image, drawing_obj] to match your original structure.
    """
    bg = _to_hex_color(bgcolor)
    img = wImage(width=int(sizex), height=int(sizey), background=wColor(bg))

    # Keep these settings as in original (best-effort; some are IM-version dependent)
    try:
        img.alpha_channel = False
    except Exception:
        pass
    try:
        img.type = 'truecolor'
    except Exception:
        pass
    try:
        img.colorspace = 'rgb'
    except Exception:
        pass
    try:
        img.depth = 24
    except Exception:
        pass
    try:
        img.options['png:color-type'] = '2'
    except Exception:
        pass

    # Fill background explicitly (same as original)
    drawColorRectangle(img, 0, 0, sizex, sizey, bgcolor)

    return [img, wDrawing()]


# -------------------------
# Filename / extension parsing
# -------------------------
def get_save_filename(outfile):
    """
    Same behavior as original, but cleaned up and cached supported formats.
    Returns:
    - None/bool passthrough
    - (outfile, "PNG") for file-like or "-" or empty
    - string path: ext from filename or "name:EXT", validated against wand formats, default PNG
    - tuple/list (filename, ext): validate ext similarly
    - invalid: False
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if outfile == "-" or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    fmts = _wand_supported_formats()

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
                ext_u = None

        if not ext_u or ext_u not in fmts:
            ext_u = "PNG"
        return (out, ext_u)

    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile

        if isinstance(filename, (file, IOBase)) or filename == "-":
            fn = filename
        elif isinstance(filename, basestring):
            fn = filename.strip()
        else:
            return False

        if not isinstance(ext, basestring):
            return False

        ext_u = ext.strip().upper()
        if ext_u not in fmts:
            ext_u = "PNG"
        return (fn, ext_u)

    return False


def get_save_file(outfile):
    # Fix a bug in original (it returned the function object instead of calling it)
    return get_save_filename(outfile)


# -------------------------
# Saving
# -------------------------
def _apply_format_options(img, ext_upper):
    """
    Apply the same format-specific options your original save_to_file used.
    (Some attributes vary by ImageMagick/Wand version; guarded with try/except.)
    """
    ext = ext_upper.lower()
    img.format = ext

    if ext == "png":
        try:
            img.depth = 24
        except Exception:
            pass
        try:
            img.interlace_scheme = "line"
        except Exception:
            pass
        try:
            img.compression_quality = 100
        except Exception:
            pass

    elif ext in ("jpg", "jpeg", "jpe"):
        try:
            img.interlace_scheme = "plane"
        except Exception:
            pass
        try:
            img.compression_quality = 100
        except Exception:
            pass

    elif ext == "webp":
        try:
            img.compression_quality = 100
        except Exception:
            pass
        # lossless webp is version-dependent; left as-is like your comment

    elif ext == "tiff":
        try:
            img.compression = "lzw"
        except Exception:
            pass
        try:
            img.interlace_scheme = "line"
        except Exception:
            pass

    elif ext == "bmp":
        try:
            img.depth = 24
        except Exception:
            pass

    elif ext == "gif":
        try:
            img.type = "palette"
        except Exception:
            pass


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Save image to path/file/BytesIO with upload and "-" semantics.
    Keeps behavior:
    - ftp/ftps/sftp: write to BytesIO then upload
    - outfile == "-": return bytes
    - file-like: write directly
    - path: write to filename
    """
    img = inimage[0]

    # normalize ext via Wand supported formats (default PNG)
    info = get_save_filename((outfile, outfileext)) if outfileext else None
    if isinstance(info, (tuple, list)) and len(info) == 2:
        # use validated ext from wand formats
        _, ext_upper = info
    else:
        ext_upper = (outfileext or "PNG").upper()

    # metadata/comment
    try:
        img.metadata["comment"] = imgcomment
    except Exception:
        pass

    uploadfile = None
    outfiletovar = False
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    _apply_format_options(img, ext_upper)

    try:
        if isinstance(outfile, (file, IOBase, BytesIO)):
            img.save(file=outfile)
        else:
            img.save(filename=outfile)
    except Exception as e:
        raise RuntimeError("Failed to save image: {0}".format(e))

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
        outdest, outext = oldoutfile
        return save_to_file(imgout, outdest, outext, imgcomment)
    return [imgout, "wand"]
