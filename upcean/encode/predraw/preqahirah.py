# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Cool Dude 2k
    Copyright 2011-2023 Game Maker 2k
    Copyright 2011-2023 Kazuki Przyborowski

    $FileInfo: preqahirah.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import re
import qahirah as qah
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
    from io import IOBase as file

fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

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
    - ctx: Qahirah context.
    - x1, y1: Coordinates of the top-left corner.
    - x2, y2: Coordinates of the bottom-right corner.
    - color: Tuple of (R, G, B) with values in [0, 255].
    """
    # Set the color for filling (scaled to [0, 1] for Qahirah)
    ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    
    # Calculate width and height
    width_rect = x2 - x1
    height_rect = y2 - y1
    
    # Define the rectangle path and fill it
    ctx.rectangle(qah.Rect(qah.Vector(x1, y1), qah.Vector(width_rect, height_rect)))
    ctx.fill()
    
    # Start a new path to avoid unintended connections
    ctx.new_path()

def drawColorLine(ctx, x1, y1, x2, y2, width, color):
    """
    Draws a colored line from (x1, y1) to (x2, y2) with specified width.
    Uses rectangles to simulate thick vertical and horizontal lines.
    
    Parameters:
    - ctx: Qahirah context.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple of (R, G, B) with values in [0, 255].
    """
    # Ensure width is at least 1
    width = max(1, int(width))
    
    # Set the fill color (scaled to [0, 1])
    ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    
    # Snap coordinates for crisp lines
    x1, y1 = snapCoords(x1, y1)
    x2, y2 = snapCoords(x2, y2)
    
    if x1 == x2:
        # Vertical line: draw a rectangle with specified width
        rect_x = x1 - width / 2
        rect_y = min(y1, y2)
        rect_width = width
        rect_height = abs(y2 - y1)
        ctx.rectangle(qah.Rect(qah.Vector(rect_x, rect_y), qah.Vector(rect_width, rect_height)))
        ctx.fill()
    elif y1 == y2:
        # Horizontal line: draw a rectangle with specified width
        rect_x = min(x1, x2)
        rect_y = y1 - width / 2
        rect_width = abs(x2 - x1)
        rect_height = width
        ctx.rectangle(qah.Rect(qah.Vector(rect_x, rect_y), qah.Vector(rect_width, rect_height)))
        ctx.fill()
    else:
        # If not purely vertical or horizontal, use Qahirah's line with set_line_width
        ctx.set_line_width(width)
        ctx.move_to(qah.Vector(x1, y1))
        ctx.line_to(qah.Vector(x2, y2))
        ctx.stroke()
    
    # Start a new path to avoid unintended connections
    ctx.new_path()

def drawText(ctx, size, x, y, text, ftype="ocrb"):
    """
    Draws text at a specified location with given size and font type.
    
    Parameters:
    - ctx: Qahirah context.
    - size: Font size.
    - x, y: Coordinates for text position.
    - text: The text to draw.
    - ftype: Font type (optional, default is "ocrb").
    """
    text = str(text)
    point1 = snapCoords(x, y)
    # Create a font face object
    if ftype == "ocra":
        try:
            font = qah.FontFace.create_for_file(fontpathocra)
        except OSError:
            font = qah.FontFace.create_for_file(fontpathocraalt)
    elif ftype == "ocrb":
        try:
            font = qah.FontFace.create_for_file(fontpathocrb)
        except OSError:
            font = qah.FontFace.create_for_file(fontpathocrbalt)
    else:
        font = None  # Default font
    if font is not None:
        ctx.set_font_face(font)
    ctx.set_font_size(size)
    fo = qah.FontOptions()
    fo.antialias = qah.Antialias.DEFAULT
    fo.hint_style = qah.HintStyle.FULL
    fo.hint_metrics = qah.HintMetrics.ON
    ctx.set_font_options(fo)
    ctx.move_to(qah.Vector(point1[0], point1[1]))
    ctx.show_text(text)
    ctx.stroke()
    return True

def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    """
    Draws colored text at a specified location with given size, color, and font type.
    
    Parameters:
    - ctx: Qahirah context.
    - size: Font size.
    - x, y: Coordinates for text position.
    - text: The text to draw.
    - color: Tuple of (R, G, B) with values in [0, 255].
    - ftype: Font type (optional, default is "ocrb").
    """
    text = str(text)
    ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    drawText(ctx, size, x, y, text, ftype)
    return True

def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, line_width=1):
    """
    Draws an outlined rectangle from (x1, y1) to (x2, y2) with the specified color and line width.
    
    Parameters:
    - ctx: Qahirah context.
    - x1, y1: Coordinates of the top-left corner.
    - x2, y2: Coordinates of the bottom-right corner.
    - color: Tuple of (R, G, B) with values in [0, 255].
    - line_width: Width of the outline (default is 1).
    """
    # Set the outline color (scaling RGB values to [0, 1])
    ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    
    # Set the line width for the outline
    ctx.set_line_width(line_width)
    
    # Define the rectangle path
    width_rect = x2 - x1
    height_rect = y2 - y1
    ctx.rectangle(qah.Rect(qah.Vector(x1, y1), qah.Vector(width_rect, height_rect)))
    
    # Stroke the rectangle outline
    ctx.stroke()
    
    # Start a new path to avoid unintended connections
    ctx.new_path()

    return True

# Define valid Qahirah output formats
cairo_valid_extensions = {"SVG", "PDF", "PS", "EPS"}

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files in Qahirah-compatible formats. Returns a tuple (filename, EXTENSION)
    or the original `outfile` if it's of type None, bool, or a file object.
    Defaults to "PNG" if the extension is not supported by Qahirah.
    
    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.
    
    Returns:
        tuple or original `outfile` or False if invalid.
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile
    
    # Handle file objects directly
    if isinstance(outfile, file):
        return (outfile, "PNG")
    
    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)
    
        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
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
    
        # Check if extension is supported by Qahirah
        if outfileext not in cairo_valid_extensions:
            outfileext = "PNG"
    
        return (outfile, outfileext)
    
    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            # Invalid tuple/list length
            return False
    
        filename, ext = outfile
    
        # Allow file objects as the first item in tuple
        if isinstance(filename, file):
            filename = filename  # fileobj is valid as-is
        elif isinstance(filename, str):
            filename = filename.strip()
        else:
            return False
    
        # Ensure the extension is a valid string
        if not isinstance(ext, str):
            return False
    
        ext = ext.strip().upper()
        # Check if extension is supported by Qahirah
        if ext not in cairo_valid_extensions:
            ext = "PNG"
    
        return (filename, ext)
    
    # Unsupported type
    return False