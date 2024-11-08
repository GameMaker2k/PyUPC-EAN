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

    $FileInfo: presvgwrite.py - Last Update: 04/27/2024 Ver. 1.0.0 - Author: ChatGPT $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import svgwrite
import os
import re
import base64
import io  # For file object type checking

try:
    file
except NameError:
    from io import IOBase as file

# Define helper functions

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding file extension for saving SVG files.
    Returns a tuple (filename, "SVG") or the original `outfile` if it's of type None, bool, or a file object.
    Defaults to "SVG" as the extension if none is provided or if an unsupported extension is detected.
    Returns False for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple: (filename, "SVG") or False if invalid.
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly
    if isinstance(outfile, file):
        return (outfile, "SVG")

    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, None)

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            ext_match = re.match("^\\.(?P<ext>[A-Za-z]+)$", ext)
            if ext_match:
                outfileext = ext_match.group('ext').upper()
            else:
                outfileext = None
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match("^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                outfileext = custom_match.group('ext').upper()
            else:
                outfileext = None

        # Default to "SVG" if no valid extension was found or if it's not SVG
        if outfileext != "SVG":
            outfileext = "SVG"

        return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False  # Invalid tuple/list length

        filename, ext = outfile

        # Allow file objects or strings as the first element
        if isinstance(filename, file):
            filename = filename  # file object is valid as-is
        elif isinstance(filename, str):
            filename = filename.strip()
        else:
            return False  # Invalid first element type

        # Ensure the extension is a valid string
        if not isinstance(ext, str):
            return False

        ext = ext.strip().upper()
        # Ensure the extension is SVG
        if ext != "SVG":
            ext = "SVG"

        return (filename, ext)

    # Unsupported type
    return False

def drawColorRectangleAlt(dwg, x1, y1, x2, y2, color):
    """
    Draws a rectangle with only an outline (no fill) from (x1, y1) to (x2, y2) with the specified color.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B) or a valid SVG color string.

    Returns:
    - True if the rectangle is drawn successfully.
    """
    width_rect = x2 - x1
    height_rect = y2 - y1

    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        # Ensure RGB values are within 0-255
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        color = 'rgb({},{},{})'.format(r, g, b)

    # Create and add the rectangle with no fill and specified stroke color
    rectangle = dwg.rect(
        insert=(x1, y1),
        size=(width_rect, height_rect),
        fill='none',
        stroke=color,
        stroke_width=1  # Default stroke width; modify as needed
    )
    dwg.add(rectangle)

    return True

def drawColorRectangle(dwg, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B) or a valid SVG color string.

    Returns:
    - True if the rectangle is drawn successfully.
    """
    width_rect = x2 - x1
    height_rect = y2 - y1

    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        # Ensure RGB values are within 0-255
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        color = 'rgb({},{},{})'.format(r, g, b)

    # Create and add the rectangle to the drawing
    rectangle = dwg.rect(
        insert=(x1, y1),
        size=(width_rect, height_rect),
        fill=color,
        stroke='none'  # No outline
    )
    dwg.add(rectangle)

    return True

def drawColorLine(dwg, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple representing (R, G, B) or a valid SVG color string.

    Returns:
    - True if the line is drawn successfully.
    """
    width = max(1, int(width))

    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        # Ensure RGB values are within 0-255
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        color = 'rgb({},{},{})'.format(r, g, b)

    # Create and add the line to the drawing
    line = dwg.line(
        start=(x1, y1),
        end=(x2, y2),
        stroke=color,
        stroke_width=width
    )
    dwg.add(line)

    return True

def drawColorText(dwg, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text at (x, y) with the specified size, color, and font type.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - size: Font size (e.g., 20).
    - x, y: Coordinates where the text starts.
    - text: The string to be drawn.
    - color: Tuple representing (R, G, B) or a valid SVG color string.
    - ftype: Font type (e.g., "ocrb"). Note: Custom fonts require embedding or system availability.

    Returns:
    - True if the text is drawn successfully.
    """
    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        # Ensure RGB values are within 0-255
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        color = 'rgb({},{},{})'.format(r, g, b)

    # Define font family based on ftype
    if ftype.lower() == "ocrb":
        font_family = "OCRB"
    elif ftype.lower() == "ocra":
        font_family = "OCR-A"
    else:
        font_family = "Monospace"
    # Create and add the text to the drawing
    text_element = dwg.text(
        text,
        insert=(x, y),
        fill=color,
        font_size=size,
        font_family=font_family
    )
    dwg.add(text_element)

    return True

def embed_font(dwg, font_path, font_family):
    """
    Embeds a custom font into the SVG.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - font_path: Path to the font file (e.g., .ttf or .otf).
    - font_family: The name to assign to the font family.
    """
    # Read the font file
    with open(font_path, 'rb') as f:
        font_data = f.read()

    # Encode the font data in base64
    font_base64 = base64.b64encode(font_data).decode('utf-8')

    # Determine the font format based on the file extension
    ext = os.path.splitext(font_path)[1].lower()
    if ext == '.ttf':
        font_format = 'truetype'
    elif ext == '.otf':
        font_format = 'opentype'
    else:
        raise ValueError("Unsupported font format.")

    # Create the @font-face CSS
    font_face = """
    @font-face {{
        font-family: '{0}';
        src: url(data:font/{1};base64,{2}) format('{1}')
        font-weight: normal;
        font-style: normal;
    }}
    """.format(font_family, font_format, font_base64)

    # Add the style to the SVG
    dwg.defs.add(dwg.style(font_face))
