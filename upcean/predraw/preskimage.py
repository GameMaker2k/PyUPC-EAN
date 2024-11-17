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

    $FileInfo: precv2.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
import numpy as np
import skimage
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import os
from io import BytesIO
from upcean.xml.downloader import upload_file_to_internet_file  # Assuming this function is available

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

def drawColorRectangle(img, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2) with the specified color using scikit-image.
    """
    rr, cc = skimage.draw.rectangle(start=(y1, x1), end=(y2 - 1, x2 - 1))
    img[rr, cc] = color
    return True

def drawColorLine(img, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color using scikit-image.
    """
    width = max(1, int(width))
    rr, cc = skimage.draw.line(y1, x1, y2, x2)
    for offset in range(-width // 2, width // 2 + 1):
        rr_offset = rr + offset
        cc_offset = cc + offset
        # Ensure indices are within image bounds
        valid_indices = (rr_offset >= 0) & (rr_offset < img.shape[0]) & (cc_offset >= 0) & (cc_offset < img.shape[1])
        img[rr_offset[valid_indices], cc_offset[valid_indices]] = color
    return True

def drawColorText(img, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text on the image using matplotlib.
    """
    # Map ftype to font file path
    if ftype == "ocra":
        fontpath = fontpathocra if os.path.isfile(fontpathocra) else fontpathocraalt
    elif ftype == "ocrb":
        fontpath = fontpathocrb if os.path.isfile(fontpathocrb) else fontpathocrbalt
    else:
        fontpath = fontpathocra
    # Check if font file exists
    if not os.path.isfile(fontpath):
        print("Font file not found:", fontpath)
        return False
    # Load the font
    font_prop = fm.FontProperties(fname=fontpath, size=size)
    # Create a matplotlib figure and render text
    h, w, _ = img.shape
    dpi = 100  # Dots per inch
    fig_h = h / dpi
    fig_w = w / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.imshow(img)
    ax.axis('off')
    # Invert y-axis to match image coordinates
    ax.invert_yaxis()
    # Draw text
    ax.text(x, y, text, fontproperties=font_prop, color=np.array(color) / 255.0, verticalalignment='top')
    # Render the figure to a numpy array
    fig.canvas.draw()
    text_image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    text_image = text_image.reshape((h, w, 3))
    plt.close(fig)
    # Merge the text image onto the original image
    img[...] = text_image
    return True

def drawColorRectangleAlt(img, x1, y1, x2, y2, color):
    """
    Draws a rectangle outline from (x1, y1) to (x2, y2) with the specified color using scikit-image.
    """
    # Draw top and bottom lines
    drawColorLine(img, x1, y1, x2, y1, 1, color)
    drawColorLine(img, x1, y2 - 1, x2, y2 - 1, 1, color)
    # Draw left and right lines
    drawColorLine(img, x1, y1, x1, y2, 1, color)
    drawColorLine(img, x2 - 1, y1, x2 - 1, y2, 1, color)
    return True

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

    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            # Match extension pattern and extract if valid
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
        if ext.strip().upper() == ".RAW":
            return (outfile, outfileext)
        # Supported formats
        supported_exts = ["PNG", "JPG", "JPEG", "BMP", "TIFF", "RAW"]
        if outfileext in supported_exts:
            return (outfile, outfileext)
        else:
            outfileext = "PNG"  # Default to PNG if unsupported
            return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False  # Invalid tuple/list length

        filename, ext = outfile

        # Ensure the extension is a valid string
        if not isinstance(ext, str):
            return False

        ext = ext.strip().upper()
        if ext == "RAW":
            return (filename, "RAW")
        # Supported formats
        supported_exts = ["PNG", "JPG", "JPEG", "BMP", "TIFF", "RAW"]
        if ext in supported_exts:
            return (filename, ext)
        else:
            ext = "PNG"  # Default to PNG if unsupported

        return (filename, ext)

    # Unsupported type
    return False

def new_image_surface(sizex, sizey, bgcolor):
    """
    Creates a new image surface with the specified background color using scikit-image.
    """
    img = np.zeros((sizey, sizex, 3), dtype=np.uint8)
    img[:, :] = bgcolor
    return [img, None]

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the image to a file or stream using imageio, with support for FTP uploads
    and returning image data when outfile is '-'.
    """
    img = inimage[1]
    uploadfile = None
    outfiletovar = False

    if re.match(r"^(ftp|ftps|sftp)://", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Prepare image saving parameters
    # Imageio supports saving images with various formats

    # Determine the file extension and format
    format = outfileext.lower()
    if format == "jpg":
        format = "jpeg"

    # Now, save the image
    if isinstance(outfile, str):
        # Save to file
        skimage.io.imsave(outfile, img, plugin='imageio', format=format)
    elif hasattr(outfile, 'write'):
        # outfile is a file-like object
        import imageio
        imageio.imwrite(outfile, img, format=format)
    else:
        # Unsupported outfile type
        return False

    if uploadfile is not None:
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
    """
    Processes the output filename and saves the image using save_to_file().
    """
    if outfile is None:
        oldoutfile = None
        outfile = None
        outfileext = None
    else:
        oldoutfile = get_save_filename(outfile)
        if isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list):
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
        else:
            return False
    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [imgout[0], imgout[1], "skimage"]
    return save_to_file(imgout, outfile, outfileext, imgcomment)
