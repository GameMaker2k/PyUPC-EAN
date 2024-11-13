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

def drawColorRectangle(draw, x1, y1, x2, y2, color):
    with Drawing() as draw:
        draw.fill_color = Color(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(draw)
    return True

def drawColorLine(draw, x1, y1, x2, y2, width, color):
    with Drawing() as draw:
        draw.stroke_color = Color(color)
        draw.stroke_width = width
        draw.line((x1, y1), (x2, y2))
        draw(draw)
    return True

def drawColorText(draw, size, x, y, text, color, ftype="ocrb"):
    # Set the font path based on the specified type
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra
    with Drawing() as draw:
        draw.font = font_path  # Directly use the font path
        draw.font_size = size
        draw.fill_color = Color(color)
        draw.text(x, y, text)
        draw(draw)
    return True

def drawColorRectangleAlt(draw, x1, y1, x2, y2, color):
    with Drawing() as draw:
        draw.stroke_color = Color(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(draw)
    return True

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Uses WAND_SUPPORTED_EXTENSIONS as a reference for supported formats.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple: (filename, EXTENSION) or False if invalid.
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Check if outfile is a file object
    if isinstance(outfile, file):
        return (outfile, "PNG")

    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)

        base, ext = os.path.splitext(outfile)
        ext = ext[1:].upper() if ext else None

        if ext and ext in WAND_SUPPORTED_EXTENSIONS:
            return (outfile, WAND_SUPPORTED_EXTENSIONS[ext])
        elif ext:
            return (outfile, "PNG")
        return (outfile, "PNG")

    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False

        filename, ext = outfile
        if isinstance(filename, file):
            filename = filename
        elif isinstance(filename, str):
            filename = filename.strip()
        else:
            return False

        ext = ext.strip().upper()
        if ext in WAND_SUPPORTED_EXTENSIONS:
            ext = WAND_SUPPORTED_EXTENSIONS[ext]
        else:
            ext = "PNG"

        return (filename, ext)

    return False

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    img = inimage
    with Image() as img:
        img.comment = imgcomment
        img.format = outfileext.upper()
        if outfileext == "WEBP":
            img.compression_quality = 100
        elif outfileext == "JPEG":
            img.compression_quality = 100
        img.save(filename=outfile)
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
        return [imgout, "wand"]
    save_to_file(imgout, outfile, outfileext, imgcomment)
    return True
