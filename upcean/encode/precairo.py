# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2023 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: precairo.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import re
import cairo
import upcean.fonts

try:
    import pkg_resources
    pkgres = True
except ImportError:
    pkgres = False

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

'''
http://stevehanov.ca/blog/index.php?id=28
'''


def snapCoords(x, y):
    """
    Snaps the coordinates to the nearest half-pixel for crisp rendering.
    
    Parameters:
    - x, y: Original coordinates.
    
    Returns:
    - Tuple of snapped coordinates.
    """
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(ctx, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color.
    
    Parameters:
    - ctx: Cairo context.
    - x1, y1: Coordinates of the top-left corner.
    - x2, y2: Coordinates of the bottom-right corner.
    - color: Tuple of (R, G, B) with values in [0, 1].
    """
    # Set the fill color
    ctx.set_source_rgb(*color)
    
    # Calculate width and height
    width_rect = x2 - x1
    height_rect = y2 - y1
    
    # Create the rectangle path
    ctx.rectangle(x1, y1, width_rect, height_rect)
    
    # Fill the rectangle
    ctx.fill()
    
    # Start a new path to avoid unintended connections
    ctx.new_path()

def drawColorLine(ctx, x1, y1, x2, y2, width, color):
    """
    Draws a colored line from (x1, y1) to (x2, y2) with specified width.
    Uses rectangles to simulate thick vertical and horizontal lines.
    
    Parameters:
    - ctx: Cairo context.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple of (R, G, B) with values in [0, 1].
    """
    # Ensure width is at least 1
    width = max(1, int(width))
    
    # Set the fill color
    ctx.set_source_rgb(*color)
    
    # Snap coordinates for crisp lines
    x1, y1 = snapCoords(x1, y1)
    x2, y2 = snapCoords(x2, y2)
    
    if x1 == x2:
        # Vertical line: draw a rectangle with specified width
        rect_x = x1 - width / 2
        rect_y = min(y1, y2)
        rect_width = width
        rect_height = abs(y2 - y1)
        ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
        ctx.fill()
    elif y1 == y2:
        # Horizontal line: draw a rectangle with specified width
        rect_x = min(x1, x2)
        rect_y = y1 - width / 2
        rect_width = abs(x2 - x1)
        rect_height = width
        ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
        ctx.fill()
    else:
        # If not purely vertical or horizontal, use Cairo's line with set_line_width
        ctx.set_line_width(width)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
    
    # Start a new path to avoid unintended connections
    ctx.new_path()


def drawText(ctx, size, x, y, text, ftype="ocrb"):
    text = str(text)
    point1 = snapCoords(x, y)
    ctx.select_font_face("Monospace")
    ctx.set_font_size(size)
    fo = cairo.FontOptions()
    fo.set_antialias(cairo.ANTIALIAS_DEFAULT)
    fo.set_hint_style(cairo.HINT_STYLE_FULL)
    fo.set_hint_metrics(cairo.HINT_METRICS_ON)
    ctx.set_font_options(fo)
    ctx.move_to(point1[0], point1[1])
    ctx.show_text(text)
    ctx.stroke()
    return True


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    text = str(text)
    ctx.set_source_rgb(color[0], color[1], color[2])
    drawText(ctx, size, x, y, text, ftype)
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
        elif(outfileext == "SVG"):
            outfileext = "SVG"
        elif(outfileext == "PDF"):
            outfileext = "PDF"
        elif(outfileext == "PS"):
            outfileext = "PS"
        elif(outfileext == "EPS"):
            outfileext = "EPS"
        else:
            outfileext = "PNG"
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
