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

    $FileInfo: prewand.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import os
import re
import upcean.fonts

# Compatibility for Python 2 and 3
try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase
    file = IOBase

try:
    file
except NameError:
    from io import IOBase as file
try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

try:
    import pkg_resources
    pkgres = True
except ImportError:
    pkgres = False

# Font paths for different font types
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

# Common file extensions supported by ImageMagick and Wand
WAND_SUPPORTED_EXTENSIONS = {
    'PNG': 'png', 'JPG': 'jpeg', 'JPEG': 'jpeg', 'GIF': 'gif', 'WEBP': 'webp',
    'BMP': 'bmp', 'ICO': 'ico', 'TIFF': 'tiff', 'HEIC': 'heic', 'XPM': 'xpm',
    'XBM': 'xbm', 'PBM': 'pbm', 'PGM': 'pgm'
}

def snapCoords(ctx, x, y):
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(image, x1, y1, x2, y2, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with Drawing() as draw:
        draw.fill_color = Color(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(image)  # Apply drawing to the `image` (which should be an Image instance)
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with Drawing() as draw:
        draw.stroke_color = Color(color)
        draw.stroke_width = width
        draw.line((x1, y1), (x2, y2))
        draw(image)  # Apply drawing to the `image`
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra
    with Drawing() as draw:
        draw.font = font_path
        draw.font_size = size
        draw.fill_color = Color(color)
        draw.text(x, y, text)
        draw(image)  # Apply drawing to the `image`
    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with Drawing() as draw:
        draw.stroke_color = Color(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(image)  # Apply drawing to the `image`
    return True

def new_image_surface(sizex, sizey, bgcolor):
    if isinstance(bgcolor, tuple) and len(bgcolor) == 3:
        bgcolor = '#{:02x}{:02x}{:02x}'.format(*bgcolor)
    upc_preimg = Image(width=sizex, height=sizey, background=Color(bgcolor))
    upc_img = upc_preimg
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, upc_preimg]

# Define supported extensions if not defined elsewhere
WAND_SUPPORTED_EXTENSIONS = {
    "PNG": "png",
    "JPEG": "jpeg",
    "JPG": "jpeg",
    "WEBP": "webp",
}

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Uses WAND_SUPPORTED_EXTENSIONS as a reference for supported formats.

    Parameters:
        outfile (str, tuple, list, None, bool): The output file specification.

    Returns:
        tuple: (filename, EXTENSION) or False if invalid.
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if(isinstance(outfile, file) or outfile=="-"):
        return (outfile, "png")

    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)

        base, ext = os.path.splitext(outfile)
        ext = ext[1:].upper() if ext else None

        if ext and ext in WAND_SUPPORTED_EXTENSIONS:
            return (outfile, WAND_SUPPORTED_EXTENSIONS[ext])
        elif ext:
            return (outfile, "png")  # Default to PNG if unsupported
        return (outfile, "png")  # Default to PNG if no extension

    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile
        filename = filename.strip() if isinstance(filename, str) else filename
        ext = ext.strip().upper()

        if ext in WAND_SUPPORTED_EXTENSIONS:
            ext = WAND_SUPPORTED_EXTENSIONS[ext]
        else:
            ext = "png"  # Default to PNG if unsupported

        return (filename, ext)

    return False

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the given image to a file with specified format and comment.

    Parameters:
        inimage (Image): The Wand image object to save.
        outfile (str): The output filename.
        outfileext (str): The format to save as, such as 'png' or 'jpeg'.
        imgcomment (str): Optional comment to include in the image metadata.
    """
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    upc_img.comment = imgcomment
    upc_img.format = outfileext.lower()  # Ensure format is lowercase for compatibility
    uploadfile = None
    outfiletovar = False
    if re.findall("^(ftp|ftps|sftp):\\/\\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile=="-":
        outfiletovar = True
        outfile = BytesIO()
    # Set specific options for certain formats
    if outfileext.lower() == "webp":
        upc_img.compression_quality = 100
    elif outfileext.lower() == "jpeg":
        upc_img.compression_quality = 100
    if(isinstance(outfile, file)):
        upc_img.save(file=outfile)
    else:
        upc_img.save(filename=outfile)
    if re.findall("^(ftp|ftps|sftp):\\/\\/", str(uploadfile)):
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
    elif outfiletovar:
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte
    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, tuple):
        outfile, outfileext = oldoutfile
    else:
        return [imgout, "wand"]

    return save_to_file(imgout, outfile, outfileext, imgcomment)
