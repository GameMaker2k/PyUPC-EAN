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
    oldoutfile = None
    if(isinstance(outfile, basestring)):
        oldoutfile = outfile[:]
    elif(isinstance(outfile, tuple)):
        oldoutfile = tuple(outfile[:])
    elif(isinstance(outfile, list)):
        oldoutfile = list(outfile[:])
    elif(outfile is None or isinstance(outfile, bool)):
        oldoutfile = None
    else:
        return False
    if(isinstance(oldoutfile, basestring)):
        if(outfile != "-" and outfile != "" and outfile != " "):
            if(len(re.findall("^\\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1])) > 0):
                outfileext = re.findall(
                    "^\\.([A-Za-z]+)", os.path.splitext(outfile)[1])[0].upper()
            if(len(re.findall("^\\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1])) == 0 and len(re.findall("(.*)\\:([a-zA-Z]+)", oldoutfile)) > 0):
                tmpoutfile = re.findall("(.*)\\:([a-zA-Z]+)", oldoutfile)
                del(outfile)
                outfile = tmpoutfile[0][0]
                outfileext = tmpoutfile[0][1].upper()
            if(len(re.findall("^\\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1])) == 0 and len(re.findall("(.*)\\:([a-zA-Z]+)", oldoutfile)) == 0):
                outfileext = "PNG"
        if(outfileext == "BYTES"):
            outfileext = "BYTES"
        else:
            outfileext = Image.registered_extensions().get("."+outfileext.lower(), "PNG")
        return (outfile, outfileext.upper())
    elif(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
        del(outfile)
        outfile = oldoutfile[0]
        outfileext = oldoutfile[1]
        return (outfile, outfileext.upper())
    elif(outfile is None or isinstance(outfile, bool) or isinstance(outfile, file)):
        return outfile
    else:
        return False
