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

    $FileInfo: prepil.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts

from PIL import Image, ImageDraw, ImageFont
from PIL import PngImagePlugin

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
# Small helpers
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_DOT_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")


def _pil_extension_map():
    """
    Returns mapping like:
      {"JPG": "JPEG", "JPEG": "JPEG", "PNG": "PNG", ...}
    """
    # Image.registered_extensions(): {".jpg": "JPEG", ".png": "PNG", ...}
    # Normalize keys to extension-without-dot uppercased.
    return {ext[1:].upper(): fmt.upper() for ext, fmt in Image.registered_extensions().items()}


def _normalize_ext(ext):
    """
    Normalize an extension string like "jpg" / "JPG" / ".jpg" into
    a Pillow format like "JPEG", or default to "PNG".
    RAW is preserved as "RAW".
    """
    if ext is None:
        return "PNG"

    ext = ext.strip()
    if not ext:
        return "PNG"

    # allow ".jpg"
    if ext.startswith("."):
        ext = ext[1:]

    ext_u = ext.upper()

    if ext_u == "RAW":
        return "RAW"

    pil_map = _pil_extension_map()
    return pil_map.get(ext_u, "PNG")


def _build_save_kwargs(outfileext, imgcomment):
    """
    Build Pillow save kwargs. Keep behavior, but avoid redundant dict updates.
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
        # NOTE: 'quality' is not a standard PNG parameter in Pillow; kept for compatibility
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
    Original intent: snap to pixel centers (useful in Cairo).
    Optimized/safe: if ctx has user_to_device, keep that call (even though unused),
    otherwise just do the rounding behavior.
    """
    if hasattr(ctx, "user_to_device"):
        try:
            ctx.user_to_device(x, y)
        except Exception:
            pass
    return (round(x) + 0.5, round(y) + 0.5)


def drawColorRectangle(draw, x1, y1, x2, y2, color):
    """
    Draw filled rectangle.
    Kept signature/return behavior.
    """
    draw.rectangle([x1, y1, x2, y2], fill=color)
    return True


def drawColorLine(draw, x1, y1, x2, y2, width, color):
    """
    Draw a line with width >= 1.
    Kept signature/return behavior.
    """
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    return True


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    """
    Draw text using OCR-A or OCR-B font with fallback.
    Kept signature/return behavior.
    """
    # Choose paths based on ftype
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    else:
        # default to ocrb
        primary, alt = fontpathocrb, fontpathocrbalt

    try:
        font = ImageFont.truetype(primary, size)
    except OSError:
        font = ImageFont.truetype(alt, size)

    ctx.text((x, y), str(text), font=font, fill=color)
    # del(font) not required; kept behavior without explicit deletion
    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color):
    """
    Draw outlined rectangle.
    Kept signature/return behavior.
    """
    ctx.rectangle([(x1, y1), (x2, y2)], outline=color)
    return True


def get_save_filename(outfile):
    """
    Same behavior as your original:
    - None/bool -> return as-is
    - file-like or "-" -> (outfile, "PNG")
    - string -> (path, normalized_format) with support for "name:EXT"
    - tuple/list (filename, ext) -> normalized format
    - invalid -> False
    """
    # None / bool passthrough
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # file-like or "-" passthrough as (dest, "PNG")
    if outfile == "-" or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    # strings (Py2/3)
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

        # Default if none
        if not outfileext:
            outfileext = "PNG"

        # Preserve RAW handling consistent with your original:
        # If the *path extension* is ".RAW" (case-insensitive), return (outfile, outfileext) early.
        # In the original, outfileext might already be "RAW" here; keep semantics.
        if ext and ext.strip().upper() == ".RAW":
            return (out, _normalize_ext(outfileext))

        return (out, _normalize_ext(outfileext))

    # tuple/list (filename, ext)
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False

        filename, ext = outfile

        # filename can be file-like or string
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
    Create an RGB image and a Draw context, fill background.
    Returns [draw_obj, image_obj].
    """
    img = Image.new("RGB", (sizex, sizey))
    draw = ImageDraw.Draw(img)
    drawColorRectangle(draw, 0, 0, sizex, sizey, bgcolor)
    return [draw, img]


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Save the image. Keeps:
    - ftp/ftps/sftp URL upload behavior
    - outfile == "-" returns bytes
    - RAW dumps raw bytes
    - format-specific mode conversions
    """
    upc_preimg = inimage[1]
    outfileext = (outfileext or "PNG").upper()

    save_kwargs = _build_save_kwargs(outfileext, imgcomment)

    uploadfile = None
    outfiletovar = False

    # If saving to a remote URL, save into memory then upload
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Mode conversions per format constraints
    if outfileext in ("XPM", "GIF"):
        upc_preimg.convert("P").save(outfile, outfileext, **save_kwargs)
    elif outfileext in ("XBM", "PBM"):
        upc_preimg.convert("1").save(outfile, outfileext, **save_kwargs)
    elif outfileext == "PGM":
        upc_preimg.convert("L").save(outfile, outfileext, **save_kwargs)
    elif outfileext == "ICO":
        # check alpha: getbands() contains 'A' if an alpha channel exists
        if "A" in upc_preimg.getbands():
            upc_preimg.convert("RGBA").save(outfile, outfileext, **save_kwargs)
        else:
            upc_preimg.convert("P").save(outfile, outfileext, **save_kwargs)
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
            # discard alpha for formats that don't support it (keeps original behavior)
            if upc_preimg.mode == "RGBA":
                upc_preimg.convert("RGB").save(outfile, outfileext, **save_kwargs)
            else:
                upc_preimg.save(outfile, outfileext, **save_kwargs)

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
    - if outfile is None OR get_save_filename(outfile) returns None/bool -> return [draw, img, "pillow"]
    - else save via save_to_file
    """
    upc_img = imgout[0]
    upc_preimg = imgout[1]

    if outfile is None:
        oldoutfile = None
    else:
        oldoutfile = get_save_filename(outfile)

    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [upc_img, upc_preimg, "pillow"]

    if not isinstance(oldoutfile, (tuple, list)) or len(oldoutfile) != 2:
        # Keep the original "False" invalid behavior consistent:
        # original would likely error downstream; here we return False cleanly.
        return False

    outdest, outfmt = oldoutfile
    return save_to_file(imgout, outdest, outfmt, imgcomment)
