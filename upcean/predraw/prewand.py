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

    $FileInfo: prewand.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
from wand.image import Image as wImage
from wand.drawing import Drawing as wDrawing
from wand.color import Color as wColor
from wand.version import formats as wformats
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

# Common file extensions supported by ImageMagick and Wand
WAND_SUPPORTED_EXTENSIONS = {
    'PNG': 'png', 'JPG': 'jpeg', 'JPEG': 'jpeg', 'GIF': 'gif', 'WEBP': 'webp',
    'BMP': 'bmp', 'ICO': 'ico', 'TIFF': 'tiff', 'HEIC': 'heic', 'XPM': 'xpm',
    'XBM': 'xbm', 'PBM': 'pbm', 'PGM': 'pgm'
}

def snapCoords(ctx, x, y):
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(image, x1, y1, x2, y2, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with wDrawing() as draw:
        draw.fill_color = wColor(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(image)  # Apply drawing to the `image` (which should be an Image instance)
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with wDrawing() as draw:
        draw.stroke_color = wColor(color)
        draw.stroke_width = width
        draw.line((x1, y1), (x2, y2))
        draw(image)  # Apply drawing to the `image`
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    font_path = fontpathocrb if ftype == "ocrb" else fontpathocra
    with wDrawing() as draw:
        draw.font = font_path
        draw.font_size = size
        draw.fill_color = wColor(color)
        draw.text(x, y, text)
        draw(image)  # Apply drawing to the `image`
    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    if isinstance(color, tuple) and len(color) == 3:
        color = '#{:02x}{:02x}{:02x}'.format(*color)
    with wDrawing() as draw:
        draw.stroke_color = wColor(color)
        draw.rectangle(left=x1, top=y1, width=x2 - x1, height=y2 - y1)
        draw(image)  # Apply drawing to the `image`
    return True

def new_image_surface(sizex, sizey, bgcolor):
    if isinstance(bgcolor, tuple) and len(bgcolor) == 3:
        bgcolor = '#{:02x}{:02x}{:02x}'.format(*bgcolor)
    upc_img = wImage(width=sizex, height=sizey, background=wColor(bgcolor))
    preupc_img = wDrawing()
    upc_img.alpha_channel = False  # Disable alpha channel
    upc_img.type = 'truecolor'  # Force truecolor (RGB)
    upc_img.colorspace = 'rgb'  # Set colorspace explicitly
    upc_img.depth = 24  # Set bit depth to 8
    upc_img.options['png:color-type'] = '2'  # Force PNG to use truecolor (RGB)
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, preupc_img]

def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files. Returns a tuple (filename, EXTENSION),
    the original `outfile` if it's of type None, bool, or a file object, or
    False for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple: (filename, EXTENSION) or False if invalid.
    """
    # Get supported formats from wand and convert them to uppercase for comparison
    wand_supported_formats = {fmt.upper() for fmt in wformats()}

    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly (using the cross-version file compatibility you've defined)
    if isinstance(outfile, file) or isinstance(outfile, IOBase) or outfile == "-":
        return (outfile, "PNG")

    # Handle string types
    if isinstance(outfile, (str, unicode) if 'unicode' in globals() else str):
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
        if not ext or ext not in wand_supported_formats:
            ext = "PNG"

        return (outfile, ext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        filename, ext = outfile

        # Allow file objects or strings as the first element
        if isinstance(filename, file) or filename == "-":
            filename = filename  # file object is valid as-is
        elif isinstance(filename, (str, unicode) if 'unicode' in globals() else str):
            filename = filename.strip()
        else:
            return False  # Invalid first element type

        # Ensure the extension is a valid string
        if not isinstance(ext, (str, unicode) if 'unicode' in globals() else str):
            return False

        ext = ext.strip().upper()
        if ext not in wand_supported_formats:
            ext = "PNG"  # Default to PNG if unsupported

        return (filename, ext)

    # Unsupported type
    return False


def get_save_file(outfile):
    return get_save_filename

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
    upc_preimg = inimage[1]

    upc_img.format = outfileext.lower()

    # Set image comment
    upc_img.metadata["comment"] = imgcomment

    # Handle output destinations
    uploadfile = None
    outfiletovar = False
    if re.match("^(ftp|ftps|sftp):\\/\\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Set specific options for formats
    if outfileext.lower() == "png":
        upc_img.depth = 24  # Set bit depth
        upc_img.interlace_scheme = "line"  # Use LINE interlacing for PNG
        upc_img.compression_quality = 100  # Set to high quality for PNG
    elif outfileext.lower() in ["jpg", "jpeg", "jpe"]:
        upc_img.interlace_scheme = "plane"  # Use PLANE interlacing for JPEG
        upc_img.compression_quality = 100  # Set high quality for JPEG
    elif outfileext.lower() == "webp":
        upc_img.compression_quality = 100  # Set high quality for WEBP
        # Note: Lossless WEBP support depends on Wand/ImageMagick version.
    elif outfileext.lower() == "tiff":
        upc_img.compression = "lzw"  # Use LZW compression for TIFF
        upc_img.interlace_scheme = "line"  # Use LINE interlacing for TIFF
    elif outfileext.lower() == "bmp":
        upc_img.depth = 24  # Set bit depth to 24 for BMP
    elif outfileext.lower() == "gif":
        upc_img.type = "palette"  # Set to palette type for GIF

    # Save the image
    try:
        if isinstance(outfile, file) or isinstance(outfile, IOBase):
            upc_img.save(file=outfile)  # Save to a file-like object
        else:
            upc_img.save(filename=outfile)  # Save to a file path
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
        return [imgout, "wand"]

    return save_to_file(imgout, outfile, outfileext, imgcomment)
