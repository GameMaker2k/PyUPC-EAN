# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: precv2.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
import cv2
import numpy as np
import re
import os
from io import BytesIO
from upcean.xml.downloader import upload_file_to_internet_file  # Assuming this function is available

try:
    import pkg_resources
    pkgres = True
except ImportError:
    pkgres = False

try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

def drawColorRectangle(img, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color using OpenCV.
    """
    # OpenCV uses BGR color order
    color_bgr = (color[2], color[1], color[0])
    cv2.rectangle(img, (x1, y1), (x2, y2), color_bgr, thickness=cv2.FILLED)
    return True

def drawColorLine(img, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color using OpenCV.
    """
    # Ensure width is at least 1
    width = max(1, int(width))
    # OpenCV uses BGR color order
    color_bgr = (color[2], color[1], color[0])
    cv2.line(img, (x1, y1), (x2, y2), color_bgr, thickness=width)
    return True

def load_freetype():
    """
    Loads the FreeType module from OpenCV if available.
    """
    if cv2.__version__ >= '4.0' and hasattr(cv2, 'freetype'):
        try:
            ft2 = cv2.freetype.createFreeType2()
            return ft2
        except Exception as e:
            print("Could not load cv2.freetype module:", e)
            return None
    else:
        print("cv2.freetype module is not available")
        return None

def drawColorText(img, size, x, y, text, color, ftype="ocrb", ft2=None):
    """
    Draws text on the image using OpenCV's freetype module for custom fonts.
    """
    if ft2 is None:
        print("FreeType module is not loaded")
        return False
    # Map ftype to font file path
    if ftype == "ocra":
        fontpath = fontpathocra if os.path.isfile(fontpathocra) else fontpathocraalt
    elif ftype == "ocrb":
        fontpath = fontpathocrb if os.path.isfile(fontpathocrb) else fontpathocrbalt
    else:
        fontpath = fontpathocra
    # Check if font file exists
    if not os.path.isfile(fontpath):
        print("Font file not found:", fontpath)
        return False
    # Load the font
    ft2.loadFontData(fontFileName=fontpath, id=0)
    color_bgr = (color[2], color[1], color[0])
    ft2.putText(img, text, (x, y), fontHeight=size, color=color_bgr, thickness=-1, line_type=cv2.LINE_AA, bottomLeftOrigin=False)
    return True

def drawColorRectangleAlt(img, x1, y1, x2, y2, color):
    """
    Draws a rectangle outline from (x1, y1) to (x2, y2) with the specified color using OpenCV.
    """
    color_bgr = (color[2], color[1], color[0])
    cv2.rectangle(img, (x1, y1), (x2, y2), color_bgr, thickness=1)
    return True

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Returns a tuple (filename, EXTENSION),
    the original `outfile` if it's of type None, bool, or a file object, or
    False for unsupported input types.
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            # Match extension pattern and extract if valid
            ext_match = re.match(r"^\.(?P<ext>[A-Za-z]+)$", ext)
            if ext_match:
                outfileext = ext_match.group('ext').upper()
            else:
                outfileext = None
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                outfileext = custom_match.group('ext').upper()
            else:
                outfileext = None

        # Default to "PNG" if no valid extension was found
        if not outfileext:
            outfileext = "PNG"
        if ext.strip().upper() == ".RAW":
            return (outfile, outfileext)
        # Supported formats
        supported_exts = ["PNG", "JPG", "JPEG", "BMP", "WEBP", "RAW"]
        if outfileext in supported_exts:
            return (outfile, outfileext)
        else:
            outfileext = "PNG"  # Default to PNG if unsupported
            return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False  # Invalid tuple/list length

        filename, ext = outfile

        # Ensure the extension is a valid string
        if not isinstance(ext, str):
            return False

        ext = ext.strip().upper()
        if ext == "RAW":
            return (filename, "RAW")
        # Supported formats
        supported_exts = ["PNG", "JPG", "JPEG", "BMP", "WEBP", "RAW"]
        if ext in supported_exts:
            return (filename, ext)
        else:
            ext = "PNG"  # Default to PNG if unsupported

        return (filename, ext)

    # Unsupported type
    return False

def new_image_surface(sizex, sizey, bgcolor):
    """
    Creates a new image surface with the specified background color using OpenCV.
    """
    img = np.zeros((sizey, sizex, 3), dtype=np.uint8)
    img[:, :] = bgcolor[::-1]  # OpenCV uses BGR, so reverse the color
    return [img, None]

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the image to a file or stream using OpenCV, with support for FTP uploads
    and returning image data when outfile is '-'.
    """
    img = inimage[1]
    uploadfile = None
    outfiletovar = False

    if re.match(r"^(ftp|ftps|sftp)://", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Prepare image encoding parameters
    encode_params = []
    if outfileext.lower() == "webp":
        encode_params = [cv2.IMWRITE_WEBP_QUALITY, 100]
    elif outfileext.lower() in ["jpg", "jpeg"]:
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    elif outfileext.lower() == "png":
        encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 9]
    # OpenCV does not support image comments directly

    # Encode image into memory buffer
    result, buf = cv2.imencode('.' + outfileext.lower(), img, encode_params)
    if not result:
        return False

    if uploadfile is not None:
        # Upload via FTP/SFTP
        buffer = BytesIO(buf.tobytes())
        upload_file_to_internet_file(buffer, uploadfile)
        buffer.close()
        return True
    elif outfiletovar:
        # Return image data
        return buf.tobytes()
    elif isinstance(outfile, str):
        # Save to file
        with open(outfile, 'wb') as f:
            f.write(buf.tobytes())
        return True
    elif hasattr(outfile, 'write'):
        # outfile is a file-like object
        outfile.write(buf.tobytes())
        return True
    else:
        # Unsupported outfile type
        return False

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """
    Processes the output filename and saves the image using save_to_file().
    """
    if outfile is None:
        oldoutfile = None
        outfile = None
        outfileext = None
    else:
        oldoutfile = get_save_filename(outfile)
        if isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list):
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
        else:
            return False
    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [imgout[0], imgout[1], "opencv"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
