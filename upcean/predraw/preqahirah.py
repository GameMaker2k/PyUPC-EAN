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

    $FileInfo: preqahirah.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.xml.downloader import upload_file_to_internet_file
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
    # Set the color as a tuple for qahirah
    ctx.set_source_colour(color)
    
    # Calculate width and height from the given coordinates
    width = x2 - x1
    height = y2 - y1
    
    # Define the rectangle using the top-left corner and dimensions
    ctx.rectangle(qah.Rect(x1, y1, width, height))
    ctx.fill()

def drawColorLine(ctx, x1, y1, x2, y2, width, color):
    # Set the color as a tuple for qahirah
    ctx.set_source_colour(color)
    
    # Calculate width and height for the rectangle based on coordinates
    rect_x = min(x1, x2)
    rect_y = min(y1, y2)
    rect_width = abs(x2 - x1) if x1 != x2 else width
    rect_height = abs(y2 - y1) if y1 != y2 else width

    # Define the rectangle directly with x, y, width, and height
    ctx.rectangle(qah.Rect(rect_x, rect_y, rect_width, rect_height))
    ctx.fill()

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
    fo.antialias = qah.CAIRO.ANTIALIAS_DEFAULT
    fo.hint_style = qah.CAIRO.HINT_METRICS_OFF
    fo.hint_metrics = qah.CAIRO.HINT_STYLE_NONE
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
    ctx.set_source_colour((color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))
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
    ctx.set_source_colour((color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))
    
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
cairo_valid_extensions = {"SVG", "PDF", "PS", "EPS", "RAW", "CAIRO"}

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
    if isinstance(outfile, file) or isinstance(outfile, IOBase) or outfile=="-":
        return (outfile, "PNG")

    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")
    
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

def get_save_file(outfile):
    return get_save_filename(outfile)

def new_image_surface(sizex, sizey, bgcolor):
    # Define the content type and create a Rect for the extents
    content_type = qah.CAIRO.CONTENT_COLOR  # Use COLOR if you don't need transparency; use COLOR_ALPHA if you do
    extents = qah.Rect(0, 0, sizex, sizey)
    # Create the RecordingSurface using the create method
    upc_preimg = qah.RecordingSurface.create(content=content_type, extents=extents)
    # Create a drawing context
    upc_img = qah.Context.create(upc_preimg)
    # Disable antialiasing
    upc_img.set_antialias(qah.CAIRO.ANTIALIAS_NONE)
    # Draw the colored rectangle (assumes drawColorRectangle is defined)
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, upc_preimg]

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    # Access the Rect properties individually
    rect = upc_preimg.ink_extents
    x = rect.left
    y = rect.top
    width = rect.width
    height = rect.height
    uploadfile = None
    outfiletovar = False
    if re.findall("^(ftp|ftps|sftp):\\/\\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile=="-":
        outfiletovar = True
        outfile = BytesIO()
    if outfileext == "SVG":
        # Instantiate SVGSurface with only the file path
        image_surface = qah.SVGSurface.create(outfile, (int(width), int(height)))
        image_context = qah.Context.create(image_surface)
        image_context.set_source_surface(upc_preimg, (-x, -y))
        image_context.paint()
        image_surface.flush()
    elif outfileext == "PDF":
        image_surface = qah.PDFSurface.create(outfile, (int(width), int(height)))
        image_context = qah.Context.create(image_surface)
        image_context.set_source_surface(upc_preimg, (-x, -y))
        image_context.paint()
        image_surface.flush()
    elif outfileext == "PS" or outfileext == "EPS":
        image_surface = qah.PSSurface.create(outfile, (int(width), int(height)))
        image_context = qah.Context.create(image_surface)
        image_surface.set_eps(outfileext == "EPS")
        image_context.set_source_surface(upc_preimg, (-x, -y))
        image_context.paint()
        image_surface.flush()
    if outfileext == "CAIRO":
        # Step 1: Create the ScriptDevice, specifying the output file
        script_device = qah.ScriptDevice.create(outfile)
        # Step 2: Create a proxy surface linked to the ScriptDevice
        # The proxy surface acts as an intermediary for drawing operations
        proxy_surface = script_device.surface_create_for_target(upc_preimg)
        # Step 3: Create a context for the proxy surface and draw as usual
        image_context = qah.Context.create(proxy_surface)
        image_context.set_source_surface(upc_preimg, (-x, -y))
        image_context.paint()
    elif(outfileext == "RAW"):
        # Create an ImageSurface with the exact dimensions of the recorded content
        image_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, int(width), int(height))
        image_context = cairo.Context(image_surface)
        # Transfer the content from the RecordingSurface to the ImageSurface
        image_context.set_source_surface(upc_preimg, -x, -y)
        image_context.paint()
        image_surface.flush()
        # Save as PNG
        data = image_surface.get_data()
        if isinstance(outfile, file) or isinstance(outfile, IOBase):
            outfile.write(data)
        else:
            dataout = open(outfile, "wb")
            dataout.write(data)
            dataout.close()
        image_surface.finish()
    else:
        # Default to ImageSurface with FORMAT_RGB24 for RGB output
        image_surface = qah.ImageSurface.create(format=qah.CAIRO.FORMAT_RGB24, dimensions=(int(width), int(height)))
        image_context = qah.Context.create(image_surface)
        image_context.set_source_surface(upc_preimg, (-x, -y))
        image_context.paint()
        image_surface.flush()
        image_surface.write_to_png(outfile)
    if re.findall("^(ftp|ftps|sftp):\\/\\/", str(uploadfile)):
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
    elif outfiletovar:
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
        return [upc_img, upc_preimg, "cairo"]
    save_to_file(imgout, outfile, outfileext, imgcomment)
    return True
