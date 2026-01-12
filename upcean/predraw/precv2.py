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

    $FileInfo: precv2.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

import cv2
import numpy as np

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
# Regex / constants
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_DOT_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

_SUPPORTED_EXTS = set(["PNG", "JPG", "JPEG", "BMP", "WEBP", "RAW"])


def _rgb_to_bgr(color):
    """Convert (R,G,B) -> (B,G,R) as int tuples."""
    return (int(color[2]), int(color[1]), int(color[0]))


def _pick_font_path(ftype):
    """Pick OCR-A/OCR-B font file with fallback, matching your original logic."""
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    elif ftype == "ocrb":
        primary, alt = fontpathocrb, fontpathocrbalt
    else:
        primary, alt = fontpathocra, fontpathocraalt

    if primary and os.path.isfile(primary):
        return primary
    return alt if alt and os.path.isfile(alt) else primary


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(img, x1, y1, x2, y2, color):
    """
    Filled rectangle, `color` is (R,G,B) 0..255.
    """
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), _rgb_to_bgr(color), thickness=cv2.FILLED)
    return True


def drawColorLine(img, x1, y1, x2, y2, width, color):
    """
    Line, `color` is (R,G,B) 0..255.
    """
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), _rgb_to_bgr(color), thickness=width)
    return True


def load_freetype():
    """
    Loads the FreeType module from OpenCV if available.
    Returns the ft2 object or None.
    """
    # Keep behavior similar, but avoid noisy prints unless truly needed.
    if hasattr(cv2, "freetype"):
        try:
            return cv2.freetype.createFreeType2()
        except Exception:
            return None
    return None


def drawColorText(img, size, x, y, text, color, ftype="ocrb", ft2=None):
    """
    Draws text using OpenCV's freetype module for custom fonts.
    Behavior preserved:
    - returns False if ft2 not provided/available
    - chooses OCR-A/OCR-B path with fallback
    - loads font each call (same behavior as original; safe but slower)
    """
    if ft2 is None:
        return False

    font_path = _pick_font_path(ftype)
    if not font_path or not os.path.isfile(font_path):
        return False

    try:
        ft2.loadFontData(fontFileName=font_path, id=0)
    except Exception:
        return False

    bgr = _rgb_to_bgr(color)
    try:
        ft2.putText(
            img,
            str(text),
            (int(x), int(y)),
            fontHeight=int(size),
            color=bgr,
            thickness=-1,
            line_type=cv2.LINE_AA,
            bottomLeftOrigin=False
        )
    except Exception:
        return False

    return True


def drawColorRectangleAlt(img, x1, y1, x2, y2, color):
    """
    Rectangle outline, thickness=1.
    """
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), _rgb_to_bgr(color), thickness=1)
    return True


# -------------------------
# Output filename parsing
# -------------------------
def get_save_filename(outfile):
    """
    Same behavior as original:
    - None/bool passthrough
    - string "-" or "" -> ("-", "PNG") / ("", "PNG")
    - string "name.ext" or "name:EXT" -> validated to supported list else PNG
    - tuple/list (filename, ext) -> validated to supported list else PNG
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Strings
    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return (out, "PNG")

        base, ext = os.path.splitext(out)
        out_ext = None

        if ext:
            m = _RE_DOT_EXT.match(ext)
            if m:
                out_ext = m.group("ext").upper()
        else:
            m = _RE_NAME_COLON_EXT.match(out)
            if m:
                out = m.group("name")
                out_ext = m.group("ext").upper()

        if not out_ext:
            out_ext = "PNG"

        # Preserve original special-case: .RAW returns RAW
        if ext and ext.strip().upper() == ".RAW":
            return (out, out_ext)

        if out_ext not in _SUPPORTED_EXTS:
            out_ext = "PNG"

        return (out, out_ext)

    # Tuple/list
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False
        filename, ext = outfile
        if not isinstance(ext, basestring):
            return False
        ext_u = ext.strip().upper()
        if ext_u == "RAW":
            return (filename, "RAW")
        if ext_u not in _SUPPORTED_EXTS:
            ext_u = "PNG"
        return (filename, ext_u)

    return False


# -------------------------
# Surface creation / saving
# -------------------------
def new_image_surface(sizex, sizey, bgcolor):
    """
    Creates a new image (numpy uint8 HxWx3) filled with bgcolor (R,G,B).
    Returns [img, "opencv"] matching original structure.
    """
    w = int(sizex)
    h = int(sizey)
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:, :] = _rgb_to_bgr(bgcolor)
    return [img, "opencv"]


def _encode_image(img, outfileext):
    """
    Encode image to bytes for PNG/JPEG/BMP/WEBP.
    Returns bytes or None.
    """
    ext = (outfileext or "PNG").lower()
    params = []

    if ext == "webp":
        params = [cv2.IMWRITE_WEBP_QUALITY, 100]
    elif ext in ("jpg", "jpeg"):
        params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    elif ext == "png":
        params = [cv2.IMWRITE_PNG_COMPRESSION, 9]

    ok, buf = cv2.imencode("." + ext, img, params)
    if not ok:
        return None
    return buf.tobytes()


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the image to a file or stream.
    Behavior preserved:
    - ftp/ftps/sftp: encode in-memory then upload
    - outfile == "-": return bytes
    - RAW: returns raw BGR bytes (no header) and writes raw bytes to file if path/file-like
    - otherwise: encode (png/jpeg/bmp/webp) and write/upload/return
    """
    img = inimage[0]
    ext_u = (outfileext or "PNG").strip().upper()

    uploadfile = None
    outfiletovar = False

    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # RAW: write raw bytes of current OpenCV buffer
    if ext_u == "RAW":
        data = img.tobytes()

        if uploadfile is not None:
            bio = BytesIO(data)
            upload_file_to_internet_file(bio, uploadfile)
            bio.close()
            return True

        if outfiletovar:
            return data

        if isinstance(outfile, basestring):
            with open(outfile, "wb") as f:
                f.write(data)
            return True

        if hasattr(outfile, "write") or isinstance(outfile, (file, IOBase)):
            outfile.write(data)
            return True

        return False

    # Encoded formats
    data = _encode_image(img, ext_u)
    if data is None:
        return False

    if uploadfile is not None:
        bio = BytesIO(data)
        upload_file_to_internet_file(bio, uploadfile)
        bio.close()
        return True

    if outfiletovar:
        return data

    if isinstance(outfile, basestring):
        with open(outfile, "wb") as f:
            f.write(data)
        return True

    if hasattr(outfile, "write") or isinstance(outfile, (file, IOBase)):
        outfile.write(data)
        return True

    return False


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """
    Same wrapper behavior as original.
    """
    if outfile is None:
        oldoutfile = None
        outdest = None
        outext = None
    else:
        oldoutfile = get_save_filename(outfile)
        if isinstance(oldoutfile, (tuple, list)):
            outdest, outext = oldoutfile[0], oldoutfile[1]
        else:
            return False

    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [imgout[0], imgout[1], "opencv"]

    return save_to_file(imgout, outdest, outext, imgcomment)
