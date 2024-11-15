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

    $FileInfo: premagick.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
import PythonMagick
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

# Common file extensions supported by PythonMagick (ImageMagick)
PYTHONMAGICK_SUPPORTED_EXTENSIONS = {
    'PNG': 'PNG', 'JPG': 'JPEG', 'JPEG': 'JPEG', 'GIF': 'GIF', 'WEBP': 'WEBP',
    'BMP': 'BMP', 'ICO': 'ICO', 'TIFF': 'TIFF', 'HEIC': 'HEIC', 'XPM': 'XPM',
    'XBM': 'XBM', 'PBM': 'PBM', 'PGM': 'PGM'
}

def snapCoords(ctx, x, y):
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(image, x1, y1, x2, y2, color):
    draw = PythonMagick.Draw()
    draw.fillColor(PythonMagick.Color(color))
    draw.rectangle(x1, y1, x2, y2)
    image.draw(draw)
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    draw = PythonMagick.Draw()
    draw.strokeColor(PythonMagick.Color(color))
    draw.strokeWidth(width)
    draw.line(x1, y1, x2, y2)
    image.draw(draw)
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra
    draw = PythonMagick.Draw()
    draw.font(font_path)  # Directly use the font path
    draw.fontPointsize(size)
    draw.fillColor(PythonMagick.Color(color))
    draw.text(x, y, text)
    image.draw(draw)
    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    draw = PythonMagick.Draw()
    draw.strokeColor(PythonMagick.Color(color))
    draw.rectangle(x1, y1, x2, y2)
    image.draw(draw)
    return True

def new_image_surface(sizex, sizey, bgcolor):
    upc_preimg = PythonMagick.Image(str(sizex)+"x"+str(sizey), bgcolor)
    upc_img = upc_preimg
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, upc_preimg]

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Uses PYTHONMAGICK_SUPPORTED_EXTENSIONS as a reference for supported formats.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple: (filename, EXTENSION) or False if invalid.
    """
    if outfile is None or isinstance(outfile, bool) or outfile=="-":
        return outfile
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)
        base, ext = os.path.splitext(outfile)
        ext = ext[1:].upper() if ext else None
        if ext and ext in PYTHONMAGICK_SUPPORTED_EXTENSIONS:
            return (outfile, PYTHONMAGICK_SUPPORTED_EXTENSIONS[ext])
        elif ext:
            return (outfile, "PNG")
        return (outfile, "PNG")
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False
        filename, ext = outfile
        if isinstance(filename, str):
            filename = filename.strip()
        else:
            return False
        ext = ext.strip().upper()
        if ext in PYTHONMAGICK_SUPPORTED_EXTENSIONS:
            ext = PYTHONMAGICK_SUPPORTED_EXTENSIONS[ext]
        else:
            ext = "PNG"
        return (filename, ext)
    return False

def get_save_file(outfile):
    return get_save_filename(outfile)

def save_to_file(image, outfile, outfileext, imgcomment="barcode"):
    # Set file format and compression options based on `outfileext`
    image.quality(100)  # Set high quality for formats like JPEG/WEBP
    image.comment(imgcomment)
    image.magick(outfileext.upper())
    image.write(outfile)
    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    if outfile is None:
        oldoutfile = None
        outfile = None
        outfileext = None
    else:
        oldoutfile = get_save_filename(outfile)
        if isinstance(oldoutfile, tuple):
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [imgout, "pythonmagick"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
