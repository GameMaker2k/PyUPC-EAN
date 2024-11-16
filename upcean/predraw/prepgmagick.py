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

    $FileInfo: prepgmagick.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
from upcean.xml.downloader import upload_file_to_internet_file
import pgmagick
import os
import re
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

# Supported extensions for pgmagick (GraphicsMagick)
PGMAGICK_SUPPORTED_EXTENSIONS = {
    'PNG', 'JPG', 'JPEG', 'GIF', 'WEBP', 'BMP', 'ICO', 'TIFF', 'HEIC', 'XPM', 'XBM', 'PBM', 'PGM'
}

def snapCoords(x, y):
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(image, x1, y1, x2, y2, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = pgmagick.Color('#{:02x}{:02x}{:02x}'.format(*color))
    else:
        color = pgmagick.Color(color)
    draw = pgmagick.DrawableRectangle(x1, y1, x2, y2)
    dlist = pgmagick.DrawableList()
    dlist.append(draw)
    image.fillColor(color)
    image.draw(dlist)
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = pgmagick.Color('#{:02x}{:02x}{:02x}'.format(*color))
    else:
        color = pgmagick.Color(color)
    image.strokeColor(color)
    image.strokeWidth(width)
    draw = pgmagick.DrawableLine(x1, y1, x2, y2)
    dlist = pgmagick.DrawableList()
    dlist.append(draw)
    image.draw(dlist)
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    # If color is a tuple of RGB values in the range 0-255
    if isinstance(color, tuple) and len(color) == 3:
        # Scale the color components to 0-65535
        r, g, b = [int(c * 257) for c in color]
        color = pgmagick.Color(r, g, b)
    else:
        color = pgmagick.Color(color)  # For color names or hex strings

    if ftype == "ocrb":
        font_path = fontpathocrb
    else:
        font_path = fontpathocra

    # Set the fill color, stroke color, and stroke width
    image.fillColor(color)
    image.strokeColor('none')  # Disable stroke color
    image.strokeWidth(0)       # Set stroke width to zero

    image.fontPointsize(size)
    image.font(font_path)

    draw = pgmagick.DrawableText(x, y, text)
    dlist = pgmagick.DrawableList()
    dlist.append(draw)
    image.draw(dlist)
    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    # Alternate rectangle drawing
    return drawColorRectangle(image, x1, y1, x2, y2, color)

def new_image_surface(sizex, sizey, bgcolor):
    if isinstance(bgcolor, tuple) and len(bgcolor) == 3:
        bgcolor = pgmagick.Color('#{:02x}{:02x}{:02x}'.format(*bgcolor))
    else:
        bgcolor = pgmagick.Color(bgcolor)
    geometry = pgmagick.Geometry(sizex, sizey)
    upc_img = pgmagick.Image(geometry, bgcolor)
    upc_img.type(pgmagick.ImageType.TrueColorType)
    upc_img.colorSpace(pgmagick.ColorspaceType.sRGBColorspace)
    upc_img.depth(24)
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
        if not ext or ext not in PGMAGICK_SUPPORTED_EXTENSIONS:
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
        if ext not in PGMAGICK_SUPPORTED_EXTENSIONS:
            ext = "PNG"  # Default to PNG if unsupported
        return (filename, ext)
    # Unsupported type
    return False

def get_save_file(outfile):
    return get_save_filename(outfile)

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the given image to a file or other output, optionally adding metadata.

    Parameters:
        inimage (tuple): Tuple containing the main image and pre-image (if any).
        outfile (str or file): Output file path, file object, or variable destination.
        outfileext (str): The image format (e.g., 'PNG', 'JPEG').
        imgcomment (str): Comment or metadata to embed in the image.
    """
    upc_img = inimage[0]
    # upc_preimg = inimage[1]  # Not used in this context
    uploadfile = None
    outfiletovar = False
    # Handle output destinations
    if re.match(r"^(ftp|ftps|sftp):\/\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()
    # Set specific options for formats
    outfileext_upper = outfileext.upper()
    upc_img.quality(100)  # Set default quality
    if outfileext_upper == "PNG":
        upc_img.magick('PNG')
        upc_img.interlaceType(pgmagick.InterlaceType.LineInterlace)
    elif outfileext_upper in ['JPG', 'JPEG', 'JPE']:
        upc_img.magick('JPEG')
        upc_img.interlaceType(pgmagick.InterlaceType.PlaneInterlace)
    elif outfileext_upper == "WEBP":
        upc_img.magick('WEBP')
        upc_img.interlaceType(pgmagick.InterlaceType.PlaneInterlace)
        upc_img.quality(100)
        upc_img.defineValue('webp', 'lossless', 'true')
    elif outfileext_upper == "TIFF":
        upc_img.magick('TIFF')
        upc_img.compression(pgmagick.CompressionType.LZWCompression)
        upc_img.interlaceType(pgmagick.InterlaceType.LineInterlace)
    elif outfileext_upper == 'BMP':
        upc_img.magick('BMP')
        upc_img.depth(24)
    elif outfileext_upper == 'GIF':
        upc_img.magick('GIF')
        upc_img.type(pgmagick.ImageType.PaletteType)
        upc_img.interlaceType(pgmagick.InterlaceType.LineInterlace)
    else:
        upc_img.magick(outfileext_upper)
    # Add comment
    upc_img.attribute('comment', imgcomment)
    # Save image
    try:
        if isinstance(outfile, file) or isinstance(outfile, IOBase):
            blob = pgmagick.Blob()
            upc_img.write(blob)
            outfile.write(blob.data)
        else:
            upc_img.write(outfile)
    except Exception as e:
        raise RuntimeError("Failed to save image: {0}".format(e))
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
    oldoutfile = get_save_filename(outfile)
    if isinstance(oldoutfile, tuple):
        outfile, outfileext = oldoutfile
    else:
        return [imgout, "pgmagick"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
