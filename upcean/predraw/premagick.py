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

    $FileInfo: premagick.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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
    # If color is a tuple of RGB values in the range 0-255
    if isinstance(color, tuple) and len(color) == 3:
        # Scale the color components to 0-65535 (assuming 16-bit QuantumRange)
        r, g, b = [int(c * 257) for c in color]
        fill_color = PythonMagick.Color(r, g, b)
    else:
        fill_color = PythonMagick.Color(color)  # For color names or hex strings

    if ftype == "ocrb":
        font_path = fontpathocrb
    else:
        font_path = fontpathocra

    # Set the fill color, stroke color, and stroke width
    image.fillColor(fill_color)
    image.strokeColor('none')  # Disable stroke color (outline)
    image.strokeWidth(0)       # Set stroke width to zero

    image.fontPointsize(size)
    image.font(font_path)

    draw = PythonMagick.DrawableText(x, y, text)
    image.draw(draw)
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
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Returns a tuple (filename, EXTENSION),
    the original `outfile` if it's of type None, bool, or a file object, or
    False for unsupported input types.
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile
    # Handle file objects directly
    if isinstance(outfile, file) or isinstance(outfile, IOBase) or outfile == "-":
        return (outfile, "PNG")
    # Handle string types
    if isinstance(outfile, basestring):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")
        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            ext = ext[1:].upper()  # Remove the dot and convert to uppercase
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match("^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                ext = custom_match.group('ext').upper()
            else:
                ext = None

        # Default to "PNG" if no valid extension was found or if unsupported
        if not ext or ext not in PYTHONMAGICK_SUPPORTED_EXTENSIONS:
            ext = "PNG"
        return (outfile, ext)
    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile
        # Allow file objects or strings as the first element
        if isinstance(filename, file) or filename == "-":
            pass  # file object is valid as-is
        elif isinstance(filename, basestring):
            filename = filename.strip()
        else:
            return False  # Invalid first element type
        # Ensure the extension is a valid string
        if not isinstance(ext, basestring):
            return False

        ext = ext.strip().upper()
        if ext not in PYTHONMAGICK_SUPPORTED_EXTENSIONS:
            ext = "PNG"  # Default to PNG if unsupported
        return (filename, ext)
    # Unsupported type
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
    uploadfile = None
    outfiletovar = False
    if re.match("^(ftp|ftps|sftp):\\/\\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Handle output destinations
    if isinstance(outfile, file) or isinstance(outfile, IOBase):
        blob = PythonMagick.Blob()
        upc_img.write(blob)
        data = blob.data
        outfile.write(data)  # Save to a file-like object
    else:
        upc_img.write(outfile)  # Save to a file path

    # Handle FTP uploads or variable output
    if uploadfile:
        outfile.seek(0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
    elif outfiletovar:
        outfile.seek(0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """Saves the image to a filename."""
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, tuple):
        outfile, outfileext = oldoutfile
    else:
        return [imgout, "pythonmagick"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
