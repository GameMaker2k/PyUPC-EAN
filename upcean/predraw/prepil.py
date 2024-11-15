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

    $FileInfo: prepil.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
from PIL import Image, ImageDraw, ImageFont
from PIL import PngImagePlugin
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
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly (using the cross-version file compatibility you've defined)
    if isinstance(outfile, file) or isinstance(outfile, IOBase) or outfile=="-":
        return (outfile, "PNG")

    # Handle string types
    if isinstance(outfile, (str, unicode) if 'unicode' in globals() else str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            # Match extension pattern and extract if valid
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

        # Default to "PNG" if no valid extension was found
        if not outfileext:
            outfileext = "PNG"
        if ext.strip().upper()==".RAW":
            return (outfile, outfileext)
        # Check if the extension is supported by Pillow's registered extensions
        pil_extensions = {ext[1:].upper(): fmt.upper() for ext, fmt in Image.registered_extensions().items()}
        if outfileext in pil_extensions:
            outfileext = pil_extensions[outfileext]
        else:
            outfileext = "PNG"  # Default to PNG if unsupported

        return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False  # Invalid tuple/list length

        filename, ext = outfile

        # Allow file objects or strings as the first element
        if isinstance(filename, file):
            filename = filename  # file object is valid as-is
        elif isinstance(filename, (str, unicode) if 'unicode' in globals() else str):
            filename = filename.strip()
        else:
            return False  # Invalid first element type

        # Ensure the extension is a valid string
        if not isinstance(ext, (str, unicode) if 'unicode' in globals() else str):
            return False

        ext = ext.strip().upper()
        if ext=="RAW":
            return (filename, "RAW")
        # Check if the extension is supported by Pillow's registered extensions
        pil_extensions = {ext[1:].upper(): fmt.upper() for ext, fmt in Image.registered_extensions().items()}
        if ext in pil_extensions:
            ext = pil_extensions[ext]
        else:
            ext = "PNG"  # Default to PNG if unsupported

        return (filename, ext)

    # Unsupported type
    return False

def get_save_file(outfile):
    return get_save_filename(outfile)

def new_image_surface(sizex, sizey, bgcolor):
    upc_preimg = Image.new("RGB", (sizex, sizey))
    upc_img = ImageDraw.Draw(upc_preimg)
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, upc_preimg]

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    exargdict = {'comment': imgcomment}
    if(outfileext == "WEBP"):
        exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
    if(outfileext == "HEIC"):
        exargdict.update({'lossless': True, 'quality': 100})
    elif(outfileext == "JPEG"):
        exargdict.update(
            {'quality': 100, 'optimize': True, 'progressive': True})
    elif(outfileext == "GIF"):
        exargdict.update(
            {'optimize': True})
    elif(outfileext == "PNG"):
        exargdict.update({'optimize': True, 'compress_level': 9, 'quality': 100})
        # Add a comment to the image
        info = PngImagePlugin.PngInfo()
        info.add_text("Comment", imgcomment)
        exargdict.update({'pnginfo': info})
    else:
        exargdict = {'comment': imgcomment}
    uploadfile = None
    outfiletovar = False
    if(re.findall("^(ftp|ftps|sftp):\\/\\/", str(outfile))):
        uploadfile = outfile
        outfile = BytesIO()
    elif(outfile=="-"):
        outfiletovar = True
        outfile = BytesIO()
    if outfileext == "XPM":
        # XPM supports only palette-based images ("P" mode)
        upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
    elif outfileext == "XBM":
        # XBM supports only 1-bit images ("1" mode)
        upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
    elif outfileext == "PBM":
        # PBM (Portable Bitmap) supports only monochrome (1-bit) images ("1" mode)
        upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
    elif outfileext == "PGM":
        # PGM (Portable Graymap) supports only grayscale images ("L" mode)
        upc_preimg.convert(mode="L").save(outfile, outfileext, **exargdict)
    elif outfileext == "GIF":
        # GIF supports only palette-based images with a maximum of 256 colors ("P" mode)
        upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
    elif outfileext == "ICO":
        # ICO generally supports "L", "P", and "RGBA" but not direct "RGB".
        # Convert to RGBA for transparency support if available, or "P" otherwise.
        if "A" in upc_preimg.getbands():  # Check if alpha channel is present
            upc_preimg.convert(mode="RGBA").save(outfile, outfileext, **exargdict)
        else:
            upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
    else:
        # If image is RGBA, convert to RGB to discard transparency; otherwise, save as-is
        if upc_preimg.mode == "RGBA":
            upc_preimg.convert(mode="RGB").save(outfile, outfileext, **exargdict)
        elif(outfileext=="RAW"):
            data = upc_preimg.tobytes()
            if isinstance(outfile, file) or isinstance(outfile, IOBase):
                outfile.write(data)
            else:
                dataout = open(outfile, "wb")
                dataout.write(data)
                dataout.close()
        else:
            upc_preimg.save(outfile, outfileext, **exargdict)
    if(re.findall("^(ftp|ftps|sftp):\\/\\/", str(uploadfile))):
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
    elif(outfiletovar):
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte
    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(outfile is None):
        oldoutfile = None
        outfile = None
        outfileext = None
    else:
        oldoutfile = get_save_filename(
            outfile)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, "pillow"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
