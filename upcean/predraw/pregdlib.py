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

    $FileInfo: prepil_gd.py - Last Update: 1/16/2026 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts

from PIL import Image
from PIL import PngImagePlugin

# Your GD-like Pillow wrapper
# (adjust import path/module name as needed)
import upcean.gdlib as gd


# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    basestring  # noqa: F401  (Py2)
except NameError:  # Py3
    basestring = str

try:
    unicode  # noqa: F401  (Py2)
except NameError:  # Py3
    unicode = str

try:
    file  # noqa: F401  (Py2)
except NameError:  # Py3
    from io import IOBase as file  # alias

try:
    from io import BytesIO
except ImportError:  # very old Py2
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

from io import IOBase


# -------------------------
# Font paths (from upcean)
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath  # kept for compatibility; may be used elsewhere


# -------------------------
# Regex helpers
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_DOT_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")


# -------------------------
# Pillow format normalization
# -------------------------
def _pil_extension_map():
    # Image.registered_extensions(): {".jpg": "JPEG", ".png": "PNG", ...}
    return {ext[1:].upper(): fmt.upper() for ext, fmt in Image.registered_extensions().items()}


def _normalize_ext(ext):
    if ext is None:
        return "PNG"
    ext = ext.strip()
    if not ext:
        return "PNG"
    if ext.startswith("."):
        ext = ext[1:]
    ext_u = ext.upper()
    if ext_u == "RAW":
        return "RAW"
    pil_map = _pil_extension_map()
    return pil_map.get(ext_u, "PNG")


def _build_save_kwargs(outfileext, imgcomment):
    """
    Mirror your original behavior/knobs, but used for Pillow save().
    """
    ext = (outfileext or "PNG").upper()
    kwargs = {'comment': imgcomment}

    if ext == "WEBP":
        kwargs.update({'lossless': True, 'quality': 100, 'method': 6})
    elif ext == "HEIC":
        kwargs.update({'lossless': True, 'quality': 100})
    elif ext == "JPEG":
        kwargs.update({'quality': 100, 'optimize': True, 'progressive': True})
    elif ext == "GIF":
        kwargs.update({'optimize': True})
    elif ext == "PNG":
        # NOTE: 'quality' isn't a standard Pillow PNG arg; kept for compatibility
        kwargs.update({'optimize': True, 'compress_level': 9, 'quality': 100})
        info = PngImagePlugin.PngInfo()
        info.add_text("Comment", imgcomment)
        kwargs['pnginfo'] = info

    return kwargs


# -------------------------
# Public API (same names)
# -------------------------

# Source mentioned: http://stevehanov.ca/blog/index.php?id=28
def snapCoords(ctx, x, y):
    """
    Keep behavior: snap to pixel centers.
    In the GD wrapper there's no cairo ctx; ignore ctx and just return snapped coords.
    """
    return (round(x) + 0.5, round(y) + 0.5)


def _as_imageresource(obj):
    """
    Accept either:
      - gd.ImageResource
      - raw PIL Image (wrap it)
    """
    if isinstance(obj, gd.ImageResource):
        return obj
    if hasattr(obj, "mode") and hasattr(obj, "size"):
        return gd.ImageResource(obj)
    return None


def drawColorRectangle(draw, x1, y1, x2, y2, color):
    """
    In GD mode, 'draw' should be an ImageResource (recommended).
    'color' may be:
      - a GD color index (int)
      - an (r,g,b) or (r,g,b,a) tuple -> will be allocated in the resource
    """
    imr = _as_imageresource(draw)
    if imr is None:
        return False

    # Normalize color argument
    if isinstance(color, int):
        cidx = color
    else:
        try:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            cidx = gd.imagecolorresolve(imr, r, g, b)
        except Exception:
            cidx = gd.imagecolorresolve(imr, 0, 0, 0)

    gd.imagefilledrectangle(imr, int(x1), int(y1), int(x2), int(y2), cidx)
    return True


def drawColorLine(draw, x1, y1, x2, y2, width, color):
    imr = _as_imageresource(draw)
    if imr is None:
        return False

    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    if isinstance(color, int):
        cidx = color
    else:
        try:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            cidx = gd.imagecolorresolve(imr, r, g, b)
        except Exception:
            cidx = gd.imagecolorresolve(imr, 0, 0, 0)

    # set thickness for this call
    old_thick = getattr(imr, "thickness", 1)
    gd.imagesetthickness(imr, width)
    gd.imageline(imr, int(x1), int(y1), int(x2), int(y2), cidx)
    gd.imagesetthickness(imr, old_thick)
    return True


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    """
    ctx should be an ImageResource.
    Uses gd.imagefttext with OCR fonts, falling back to alternate font path.
    """
    imr = _as_imageresource(ctx)
    if imr is None:
        return False

    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    else:
        primary, alt = fontpathocrb, fontpathocrbalt

    # allocate/resolve color
    if isinstance(color, int):
        cidx = color
    else:
        try:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            cidx = gd.imagecolorresolve(imr, r, g, b)
        except Exception:
            cidx = gd.imagecolorresolve(imr, 0, 0, 0)

    # Try primary font, then alternate
    try:
        gd.imagefttext(imr, int(size), 0, int(x), int(y), cidx, primary, str(text))
    except Exception:
        gd.imagefttext(imr, int(size), 0, int(x), int(y), cidx, alt, str(text))

    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color):
    """
    Outlined rectangle.
    """
    imr = _as_imageresource(ctx)
    if imr is None:
        return False

    if isinstance(color, int):
        cidx = color
    else:
        try:
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            cidx = gd.imagecolorresolve(imr, r, g, b)
        except Exception:
            cidx = gd.imagecolorresolve(imr, 0, 0, 0)

    gd.imagerectangle(imr, int(x1), int(y1), int(x2), int(y2), cidx)
    return True


def get_save_filename(outfile):
    """
    Same behavior as your original get_save_filename().
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if outfile == "-" or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return ("-" if out == "-" else out, "PNG")

        base, ext = os.path.splitext(out)

        outfileext = None
        if ext:
            m = _RE_DOT_EXT.match(ext)
            if m:
                outfileext = m.group('ext')
        else:
            m = _RE_NAME_COLON_EXT.match(out)
            if m:
                out = m.group('name')
                outfileext = m.group('ext')

        if not outfileext:
            outfileext = "PNG"

        if ext and ext.strip().upper() == ".RAW":
            return (out, _normalize_ext(outfileext))

        return (out, _normalize_ext(outfileext))

    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False

        filename, ext = outfile

        if isinstance(filename, (file, IOBase)):
            fn = filename
        elif isinstance(filename, basestring):
            fn = filename.strip()
        else:
            return False

        if not isinstance(ext, basestring):
            return False

        ext_norm = _normalize_ext(ext)
        return (fn, ext_norm)

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


def new_image_surface(sizex, sizey, bgcolor):
    """
    GD-backed surface:
      - element[0] is a gd.ImageResource (instead of ImageDraw)
      - element[1] is the underlying PIL image (kept for compatibility)
    """
    imr = gd.imagecreatetruecolor(int(sizex), int(sizey))

    # bgcolor may be GD color index or tuple
    if isinstance(bgcolor, int):
        bg_idx = bgcolor
    else:
        try:
            r, g, b = int(bgcolor[0]), int(bgcolor[1]), int(bgcolor[2])
        except Exception:
            r, g, b = 255, 255, 255
        bg_idx = gd.imagecolorresolve(imr, r, g, b)

    gd.imagefilledrectangle(imr, 0, 0, int(sizex), int(sizey), bg_idx)

    # Keep same return shape as before: [ctx/draw_like, pil_image]
    return [imr, imr.image]


def _save_pillow_image(img, outfile, fmt, save_kwargs):
    """
    Central save path used by save_to_file().
    """
    # RAW is handled elsewhere
    fmt = (fmt or "PNG").upper()

    if isinstance(outfile, (file, IOBase)):
        img.save(outfile, fmt, **save_kwargs)
        return True

    # outfile path string
    img.save(outfile, fmt, **save_kwargs)
    return True


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    GD-backed saver:
    - preserves ftp/ftps/sftp upload behavior
    - outfile == "-" returns bytes
    - RAW dumps raw bytes (RGBA/RGB bytes)
    - keeps your special mode conversions for some formats
    """
    # inimage[0] = gd.ImageResource, inimage[1] = PIL Image (kept)
    imr = _as_imageresource(inimage[0]) or _as_imageresource(inimage[1])
    if imr is None:
        return False

    upc_preimg = imr.image
    outfileext = (outfileext or "PNG").upper()
    save_kwargs = _build_save_kwargs(outfileext, imgcomment)

    uploadfile = None
    outfiletovar = False

    # remote URL -> memory then upload
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Special constraints (mirror your original)
    if outfileext in ("XPM", "GIF"):
        img_to_save = upc_preimg.convert("P")
        _save_pillow_image(img_to_save, outfile, outfileext, save_kwargs)

    elif outfileext in ("XBM", "PBM"):
        img_to_save = upc_preimg.convert("1")
        _save_pillow_image(img_to_save, outfile, outfileext, save_kwargs)

    elif outfileext == "PGM":
        img_to_save = upc_preimg.convert("L")
        _save_pillow_image(img_to_save, outfile, outfileext, save_kwargs)

    elif outfileext == "ICO":
        if "A" in upc_preimg.getbands():
            img_to_save = upc_preimg.convert("RGBA")
        else:
            img_to_save = upc_preimg.convert("P")
        _save_pillow_image(img_to_save, outfile, outfileext, save_kwargs)

    else:
        if outfileext == "RAW":
            data = upc_preimg.tobytes()
            if isinstance(outfile, (file, IOBase)):
                outfile.write(data)
            else:
                f = open(outfile, "wb")
                try:
                    f.write(data)
                finally:
                    f.close()
        else:
            # discard alpha for formats that don't support it
            img_to_save = upc_preimg
            if img_to_save.mode == "RGBA" and outfileext in ("JPEG", "BMP"):
                img_to_save = img_to_save.convert("RGB")
            _save_pillow_image(img_to_save, outfile, outfileext, save_kwargs)

    # Upload or return bytes if requested
    if uploadfile is not None:
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
        return True

    if outfiletovar:
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    return True


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """
    Wrapper:
    - if outfile is None OR get_save_filename(outfile) returns None/bool -> return [ctx, img, "gd"]
    - else save via save_to_file
    """
    imr = _as_imageresource(imgout[0]) or _as_imageresource(imgout[1])
    if imr is None:
        return False

    if outfile is None:
        oldoutfile = None
    else:
        oldoutfile = get_save_filename(outfile)

    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [imr, imr.image, "gd"]

    if not isinstance(oldoutfile, (tuple, list)) or len(oldoutfile) != 2:
        return False

    outdest, outfmt = oldoutfile
    return save_to_file([imr, imr.image], outdest, outfmt, imgcomment)
