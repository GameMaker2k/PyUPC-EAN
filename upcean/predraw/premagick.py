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
from io import BytesIO
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

# Font paths for different font types
fontpathocra = upcean.fonts.fontpathocra
fontpathocrb = upcean.fonts.fontpathocrb

# Common file extensions supported by PythonMagick
PYTHONMAGICK_SUPPORTED_EXTENSIONS = {
    'PNG': 'PNG', 'JPG': 'JPEG', 'JPEG': 'JPEG', 'GIF': 'GIF', 'WEBP': 'WEBP',
    'BMP': 'BMP', 'ICO': 'ICO', 'TIFF': 'TIFF', 'HEIC': 'HEIC', 'XPM': 'XPM',
    'XBM': 'XBM', 'PBM': 'PBM', 'PGM': 'PGM'
}

def snapCoords(ctx, x, y):
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(image, x1, y1, x2, y2, color):
    """Draws a filled rectangle on the image."""
    r, g, b = [int(c * 257) for c in color]
    draw_color = PythonMagick.Color(r, g, b)
    image.fillColor(draw_color)
    image.strokeColor("none")  # No border
    drawable = PythonMagick.DrawableRectangle(x1, y1, x2, y2)
    image.draw(drawable)
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    """Draws a line on the image."""
    r, g, b = [int(c * 257) for c in color]
    stroke_color = PythonMagick.Color(r, g, b)
    image.strokeColor(stroke_color)
    image.strokeWidth(width)
    drawable = PythonMagick.DrawableLine(x1, y1, x2, y2)
    image.draw(drawable)
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    """Draws text on the image with the specified color and minimal bold effect."""
    # Convert color to "rgb(r, g, b)" format for PythonMagick
    r, g, b = color
    text_color = PythonMagick.Color("rgb({},{},{})".format(r, g, b))
    
    # Set font and size
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra
    image.font(font_path)
    image.fontPointsize(size)
    
    # Set fill color for the text and apply a minimal stroke width
    image.fillColor(text_color)
    image.strokeColor(text_color)  # Use the same color for stroke
    image.strokeWidth(0.5)  # Set a very thin stroke width

    # Draw the text
    drawable_text = PythonMagick.DrawableText(x, y, text)
    image.draw(drawable_text)

    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    """Draws a rectangle outline on the image."""
    r, g, b = [int(c * 257) for c in color]
    stroke_color = PythonMagick.Color(r, g, b)
    image.fillColor("none")  # No fill
    image.strokeColor(stroke_color)
    drawable = PythonMagick.DrawableRectangle(x1, y1, x2, y2)
    image.draw(drawable)
    return True

def new_image_surface(sizex, sizey, bgcolor):
    """Creates a new image surface with the given dimensions and background color."""
    r, g, b = [int(c * 257) for c in bgcolor]
    background_color = PythonMagick.Color(r, g, b)
    geometry = PythonMagick.Geometry(sizex, sizey)
    upc_img = PythonMagick.Image(geometry, background_color)
    upc_img.depth(24)
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, None]

def get_save_filename(outfile):
    """Processes the `outfile` parameter to determine a suitable filename and extension."""
    if outfile is None or isinstance(outfile, bool):
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
    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile
        if isinstance(filename, str):
            filename = filename.strip()
        ext = ext.strip().upper()
        if ext in PYTHONMAGICK_SUPPORTED_EXTENSIONS:
            ext = PYTHONMAGICK_SUPPORTED_EXTENSIONS[ext]
        else:
            ext = "PNG"
        return (filename, ext)
    return False

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the given image to a file with the specified format.

    Parameters:
        inimage (list): List containing the main image and pre-image (if any).
        outfile (str or file): Output file path or file-like object.
        outfileext (str): The image format (e.g., 'PNG', 'JPEG').
        imgcomment (str): Comment or metadata to embed in the image.
    """
    upc_img = inimage[0]  # Extract the main image (PythonMagick.Image)
    upc_preimg = inimage[1]  # This may be None or additional image data

    # Set the comment for the image
    upc_img.comment(imgcomment)
    upc_img.magick(outfileext.upper())

    # Handle output destinations
    if isinstance(outfile, file):
        upc_img.write(outfile)  # Save to a file-like object
    else:
        upc_img.write(outfile)  # Save to a file path

    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """Saves the image to a filename."""
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, tuple):
        outfile, outfileext = oldoutfile
    else:
        return [imgout, "pythonmagick"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
