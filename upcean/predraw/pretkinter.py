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

    $FileInfo: pretkinter.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

try:
    import tkinter
    from tkinter import font as tkFont
except ImportError:
    import Tkinter as tkinter
    import tkFont

import os
import re

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

''' // Source: http://stevehanov.ca/blog/index.php?id=28 '''

def color_to_hex(color):
    if isinstance(color, tuple):
        return '#%02x%02x%02x' % color
    elif isinstance(color, str):
        return color
    else:
        raise ValueError("Color must be a tuple or string.")

def drawColorRectangle(canvas, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color on a Tkinter Canvas.

    Parameters:
    - canvas: Tkinter Canvas object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: String or tuple representing color, e.g., "#RRGGBB" or (R, G, B).
    """
    color_hex = color_to_hex(color)
    # Draw the rectangle
    canvas.create_rectangle(x1, y1, x2, y2, fill=color_hex, outline=color_hex)
    return True

def drawColorLine(canvas, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color on a Tkinter Canvas.

    Parameters:
    - canvas: Tkinter Canvas object.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: String or tuple representing color, e.g., "#RRGGBB" or (R, G, B).
    """
    # Ensure width is at least 1
    width = max(1, int(width))
    color_hex = color_to_hex(color)
    # Draw the line with the specified width
    canvas.create_line(x1, y1, x2, y2, fill=color_hex, width=width)
    return True

def drawColorText(canvas, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text at (x, y) with the specified size, text, color, and font type on a Tkinter Canvas.

    Parameters:
    - canvas: Tkinter Canvas object.
    - size: Font size.
    - x, y: Position to draw the text.
    - text: Text to display.
    - color: String or tuple representing color, e.g., "#RRGGBB" or (R, G, B).
    - ftype: Font type, default "ocrb".
    """
    text = str(text)
    color_hex = color_to_hex(color)
    # Prepare a list of font families to try
    font_family_list = []
    if ftype == "ocra":
        font_family_list.extend(["OCR A Extended", "OCR A"])
    elif ftype == "ocrb":
        font_family_list.append("OCR B")
    # Add monospace fonts to the list as fallbacks
    font_family_list.extend(["Monospace", "Courier New", "Courier", "Consolas", "Lucida Console"])
    # Try to create the font using the fonts in the list
    font = None
    for font_family in font_family_list:
        try:
            font = tkFont.Font(family=font_family, size=size)
            break
        except Exception:
            continue
    if font is None:
        # If none of the fonts are available, use the default font
        font = tkFont.Font(size=size)
    canvas.create_text(x, y, text=text, fill=color_hex, font=font)
    return True

def drawColorRectangleAlt(canvas, x1, y1, x2, y2, color):
    """
    Draws a rectangle outline from (x1, y1) to (x2, y2) with the specified color on a Tkinter Canvas.

    Parameters:
    - canvas: Tkinter Canvas object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: String or tuple representing color, e.g., "#RRGGBB" or (R, G, B).
    """
    color_hex = color_to_hex(color)
    # Draw the rectangle outline
    canvas.create_rectangle(x1, y1, x2, y2, outline=color_hex)
    return True

def new_image_surface(sizex, sizey, bgcolor):
    """
    Creates a new Tkinter Canvas of specified size and fills it with the background color.

    Parameters:
    - sizex: Width of the canvas.
    - sizey: Height of the canvas.
    - bgcolor: String or tuple representing color, e.g., "#RRGGBB" or (R, G, B).

    Returns:
    - canvas: The Tkinter Canvas object.
    - root: The Tkinter root window.
    """
    bgcolor_hex = color_to_hex(bgcolor)
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=sizex, height=sizey)
    canvas.pack()
    canvas.create_rectangle(0, 0, sizex, sizey, fill=bgcolor_hex, outline=bgcolor_hex)
    return [canvas, root]
