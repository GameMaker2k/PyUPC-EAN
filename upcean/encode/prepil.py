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

    $FileInfo: prepil.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from PIL import Image, ImageDraw, ImageFont
import os
import re
import upcean.fonts

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

fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

''' // Source: http://stevehanov.ca/blog/index.php?id=28 '''


def snapCoords(ctx, x, y):
    (xd, yd) = ctx.user_to_device(x, y)
    return (round(x) + 0.5, round(y) + 0.5)


def drawColorRectangle(draw, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color.
    
    Parameters:
    - draw: ImageDraw.Draw object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B).
    """
    # Calculate width and height
    width_rect = x2 - x1
    height_rect = y2 - y1
    
    # Draw the rectangle
    draw.rectangle([x1, y1, x2, y2], fill=color)
    
    return True  # Optional, based on your use case


def drawColorLine(draw, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color.
    
    Parameters:
    - draw: ImageDraw.Draw object.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple representing (R, G, B).
    """
    # Ensure width is at least 1
    width = max(1, int(width))
    
    # Draw the line with the specified width
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    
    return True  # Optional, based on your use case



def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    font = ImageFont.truetype(fontpathocra, size)
    if(ftype == "ocra"):
        try:
            font = ImageFont.truetype(fontpathocra, size)
        except OSError:
            font = ImageFont.truetype(fontpathocraalt, size)
    if(ftype == "ocrb"):
        try:
            font = ImageFont.truetype(fontpathocrb, size)
        except OSError:
            font = ImageFont.truetype(fontpathocrbalt, size)
    text = str(text)
    ctx.text((x, y), text, font=font, fill=color)
    del(font)
    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color):
    ctx.rectangle([(x1, y1), (x2, y2)], outline=color)
    return True

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files (e.g., images). Returns a tuple (filename, EXTENSION)
    or the original `outfile` if it's of type None, bool, or a file object. Returns False
    for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple or original `outfile` or False
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly
    if isinstance(outfile, file):
        return outfile

    # Handle string types (basestring covers both str and unicode in Python 2)
    if isinstance(outfile, basestring):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)

        # Initialize extension
        outfileext = None

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            # Match extension pattern
            ext_match = re.match(r"^\.(?P<ext>[A-Za-z]+)$", ext)
            if ext_match:
                outfileext = ext_match.group('ext').upper()
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                outfileext = custom_match.group('ext').upper()

        # Assign default extension if none found
        if not outfileext:
            outfileext = "PNG"

        # Handle specific extensions using PIL's Image.registered_extensions()
        # Lookup the extension in PIL's registered extensions
        pil_extension = ".{}".format(outfileext.lower())
        pil_format = Image.registered_extensions().get(pil_extension, "PNG").upper()
        outfileext = pil_format

        return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            # Invalid tuple/list length
            return False
        filename, ext = outfile
        if not isinstance(filename, basestring) or not isinstance(ext, basestring):
            # Invalid types within tuple/list
            return False
        ext = ext.strip().upper()
        # Lookup the extension in PIL's registered extensions
        pil_extension = ".{}".format(ext.lower())
        pil_format = Image.registered_extensions().get(pil_extension, "PNG").upper()
        ext = pil_format
        return (filename, ext)

    # Unsupported type
    return False


