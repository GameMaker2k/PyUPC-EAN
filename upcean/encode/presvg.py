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

    $FileInfo: svg_functions.py - Last Update: 04/27/2024 Ver. 1.0.0 - Author: ChatGPT $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import svgwrite
import os
import re
import base64
import io  # For file object type checking
import upcean.fonts

# Define helper functions

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding file extension for saving SVG files.
    Returns a tuple (filename, EXTENSION) or the original `outfile` if it's of type None, bool, or a file object.
    Returns False for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple or original `outfile` or False
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly
    if isinstance(outfile, io.IOBase):
        return outfile

    # Handle string types
    if isinstance(outfile, str):
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
            outfileext = "SVG"

        # Ensure the extension is SVG
        if outfileext != "SVG":
            outfileext = "SVG"

        return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            # Invalid tuple/list length
            return False
        filename, ext = outfile
        if not isinstance(filename, str) or not isinstance(ext, str):
            # Invalid types within tuple/list
            return False
        ext = ext.strip().upper()
        if ext != "SVG":
            # Default to SVG if not specified
            ext = "SVG"
        return (filename, ext)

    # Unsupported type
    return False

def drawColorRectangle(dwg, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color.

    Parameters:
    - dwg: svgwrite.Drawing object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B) or a valid SVG color string.
    """
    width_rect = x2 - x1
    height_rect = y2 - y1

    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        color = 'rgb({},{},{})'.format(*color)

    # Create and add the rectangle to the drawing
    rectangle = dwg.rect(insert=(x1, y1), size=(width_rect, height_rect), fill=color)
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
    """
    width = max(1, int(width))

    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        color = 'rgb({},{},{})'.format(*color)

    # Create and add the line to the drawing
    line = dwg.line(start=(x1, y1), end=(x2, y2), stroke=color, stroke_width=width)
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
    """
    # Convert RGB tuple to SVG color string if necessary
    if isinstance(color, tuple):
        color = 'rgb({},{},{})'.format(*color)

    # Define font family based on ftype
    if ftype.lower() == "ocrb":
        font_family = "OCRB"
    elif ftype.lower() == "ocra":
        font_family = "OCR-A"
    else:
        font_family = "Monospace"

    # Create and add the text to the drawing
    text_element = dwg.text(text, insert=(x, y), fill=color, font_size=size, font_family=font_family)
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
        src: url(data:font/{1};base64,{2}) format('{1}');
        font-weight: normal;
        font-style: normal;
    }}
    """.format(font_family, font_format, font_base64)

    # Add the style to the SVG
    dwg.defs.add(dwg.style(font_face))

def create_complex_svg(outfile='complex_example.svg', embed_custom_font=False, font_path=None):
    """
    Creates a complex SVG with a rectangle, a semi-transparent circle, a line, and text.

    Parameters:
    - outfile: The output SVG filename.
    - embed_custom_font: Boolean indicating whether to embed a custom font.
    - font_path: Path to the custom font file if embedding is desired.
    """
    # Process the outfile to ensure it has the correct extension
    save_info = get_save_filename(outfile)
    if not save_info:
        raise ValueError("Unsupported outfile format.")

    # Unpack filename and extension
    filename, ext = save_info

    if ext != "SVG":
        raise ValueError("Unsupported extension for SVG creation.")

    # Initialize the SVG drawing
    dwg = svgwrite.Drawing(filename, profile='full', size=(400, 400))

    # Optionally embed a custom font
    if embed_custom_font:
        if not font_path:
            raise ValueError("Font path must be provided to embed a custom font.")
        embed_font(dwg, font_path, 'OCRB')

    # Draw a rectangle
    drawColorRectangle(dwg, 50, 50, 350, 350, (0, 0, 0))  # Black rectangle

    # Draw a semi-transparent red circle
    circle = dwg.circle(center=(200, 200), r=100, fill='red', fill_opacity=0.5)
    dwg.add(circle)

    # Draw a blue line
    drawColorLine(dwg, 50, 50, 350, 350, 3, (0, 0, 255))  # Blue line

    # Draw green text
    drawColorText(dwg, 20, 150, 200, "Complex SVG", (0, 255, 0), ftype="ocrb")  # Green text

    # Save the SVG file
    dwg.save()
    print("SVG file '{}' created successfully.".format(filename))

# Example usage
if __name__ == "__main__":
    # Create a complex SVG without embedding a custom font
    create_complex_svg('complex_example.svg')

    # To embed a custom font, ensure you have the font file and provide the path
    # Example:
    # create_complex_svg('complex_with_font.svg', embed_custom_font=True, font_path='OCRB.ttf')
