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

    $FileInfo: predraw.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import re
import logging
import upcean.fonts
import upcean.support

# Configure logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Initialize support flags
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
defaultdraw = upcean.support.defaultdraw

# Initialize Pillow support if available
if pilsupport:
    try:
        from PIL import Image, ImageDraw, ImageFont
        pilsupport = True  # Confirm support
        # Handle resampling filter compatibility for Pillow 10+ and older versions
        try:
            from PIL import Resampling  # Pillow 10+
            NEAREST = Resampling.NEAREST
        except ImportError:
            NEAREST = Image.NEAREST  # Older versions of Pillow
    except ImportError:
        pilsupport = False
        NEAREST = None  # If Pillow isn't available, NEAREST isn't needed
    else:
        import upcean.predraw.prepil

# Initialize Cairo support if available
if cairosupport:
    try:
        import cairo
        import upcean.predraw.precairo
    except ImportError:
        cairosupport = False
        logger.warning("Cairo support failed to initialize.")

# Initialize Cairo support if available
if qahirahsupport:
    try:
        import qahirah as qah
        import upcean.predraw.preqahirah
    except ImportError:
        qahirahsupport = False
        logger.warning("Qahirah support failed to initialize.")

# Initialize Cairo support if available
if wandsupport:
    try:
        from wand.image import Image as wImage
        from wand.drawing import Drawing
        from wand.color import Color
        import upcean.predraw.prewand
    except ImportError:
        wandsupport = False
        logger.warning("Wand support failed to initialize.")

# Initialize Cairo support if available
if magicksupport:
    try:
        import PythonMagick
        import upcean.predraw.premagick
    except ImportError:
        magicksupport = False
        logger.warning("PythonMagick support failed to initialize.")

# Initialize Cairo support if available
if pgmagicksupport:
    try:
        import pgmagick
        import upcean.predraw.prepgmagick
    except ImportError:
        magicksupport = False
        logger.warning("PythonMagick support failed to initialize.")

# Initialize svgwrite support if available
if svgwritesupport:
    try:
        import svgwrite
        import upcean.predraw.presvgwrite
    except ImportError:
        try:
            import upcean.svgcreate as svgwrite
            import upcean.predraw.presvgwrite
        except ImportError:
            svgwritesupport = False
            logger.warning("svgwrite support failed to initialize.")

# Initialize pkg_resources support
try:
    import pkg_resources
    pkgres = True
except ImportError:
    pkgres = False

# Initialize font paths
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

class UnsupportedLibraryError(Exception):
    """Exception raised when no supported image output library is available."""
    pass

def select_image_output_lib(imageoutlib="pillow"):
    """
    Selects the appropriate image output library based on support flags and user preference.

    Parameters:
        imageoutlib (str): Preferred image output library. Options: 'pillow', 'cairo', 'cairosvg'.

    Returns:
        str: Selected image output library ('pillow', 'cairo', 'cairosvg').

    Raises:
        UnsupportedLibraryError: If neither Pillow nor Cairo is supported.
    """

    if imageoutlib == "none" or imageoutlib == None:
        return "none"

    imageoutlib = imageoutlib.lower()

    # Adjust imageoutlib based on support flags
    if not pilsupport and imageoutlib == "pillow":
        imageoutlib = "svgwrite"
        logger.info("Pillow not supported. Switching to svgwrite.")
    if not cairosupport and imageoutlib in ["cairo", "cairosvg"]:
        imageoutlib = "svgwrite"
        logger.info("Cairo not supported. Switching to svgwrite.")
    if not qahirahsupport and imageoutlib == "qahirah":
        imageoutlib = "svgwrite"
        logger.info("Qahirah not supported. Switching to svgwrite.")
    if not svgwritesupport and imageoutlib == "svgwrite":
        imageoutlib = "svgwrite"
        logger.info("svgwrite not supported. Switching to svgwrite.")
    if not wandsupport and imageoutlib == "wand":
        imageoutlib = "svgwrite"
        logger.info("svgwrite not supported. Switching to svgwrite.")
    if not magicksupport and imageoutlib == "magick":
        imageoutlib = "svgwrite"
    if not pgmagicksupport and imageoutlib == "pgmagick":
        imageoutlib = "svgwrite"
        logger.info("svgwrite not supported. Switching to svgwrite.")
    if imageoutlib not in ["pillow", "cairo", "qahirah", "cairosvg", "svgwrite", "wand", "magick", "pgmagick"]:
        imageoutlib = "svgwrite"
        logger.info("Invalid library specified. Defaulting to svgwrite.")

    # If neither library is supported, log the issue and raise an exception
    if not pilsupport and not cairosupport and not qahirahsupport and not svgwritesupport:
        logger.error("Neither Pillow nor Cairo is supported.")
        raise UnsupportedLibraryError("Neither Pillow nor Cairo is supported.")

    logger.info("Selected image output library: {}".format(imageoutlib))
    return imageoutlib

def snapCoords(ctx, x, y, imageoutlib=defaultdraw):
    """
    Snaps coordinates using the selected image output library.

    Parameters:
        ctx: Context object required by the underlying library.
        x (float): X-coordinate.
        y (float): Y-coordinate.
        imageoutlib (str): Preferred image output library.

    Returns:
        Result from the corresponding library's snapCoords method.

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("snapCoords failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.snapCoords(ctx, x, y)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.snapCoords(ctx, x, y)
    if selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.snapCoords(ctx, x, y)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.snapCoords(ctx, x, y)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.snapCoords(ctx, x, y)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.snapCoords(ctx, x, y)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.snapCoords(ctx, x, y)

    logger.error("snapCoords: Selected library is not supported.")
    return False

def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib=defaultdraw):
    """
    Draws a colored line using the selected image output library.

    Parameters:
        ctx: Context object required by the underlying library.
        x1, y1, x2, y2 (float): Coordinates defining the line.
        width (float): Width of the line.
        color (tuple or str): Color of the line.
        imageoutlib (str): Preferred image output library.

    Returns:
        Result from the corresponding library's drawColorLine method.

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("drawColorLine failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.drawColorLine(ctx, x1, y1, x2, y2, width, color)

    logger.error("drawColorLine: Selected library is not supported.")
    return False

def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib=defaultdraw):
    """
    Draws a colored rectangle using the selected image output library.

    Parameters:
        ctx: Context object required by the underlying library.
        x1, y1, x2, y2 (float): Coordinates defining the rectangle.
        color (tuple or str): Color of the rectangle.
        imageoutlib (str): Preferred image output library.

    Returns:
        Result from the corresponding library's drawColorRectangle method.

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("drawColorRectangle failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.drawColorRectangle(ctx, x1, y1, x2, y2, color)

    logger.error("drawColorRectangle: Selected library is not supported.")
    return False

def drawColorText(ctx, size, x, y, text, color, ftype="ocrb", imageoutlib=defaultdraw):
    """
    Draws colored text using the selected image output library.

    Parameters:
        ctx: Context object required by the underlying library.
        size (int): Font size.
        x, y (float): Coordinates for the text.
        text (str): Text to draw.
        color (tuple or str): Color of the text.
        ftype (str): Font type.
        imageoutlib (str): Preferred image output library.

    Returns:
        Result from the corresponding library's drawColorText method.

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("drawColorText failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.drawColorText(ctx, size, x, y, text, color, ftype)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.drawColorText(ctx, size, x, y, text, color, ftype)

    logger.error("drawColorText: Selected library is not supported.")
    return False

def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib=defaultdraw):
    """
    Draws an alternative colored rectangle using the selected image output library.

    Parameters:
        ctx: Context object required by the underlying library.
        x1, y1, x2, y2 (float): Coordinates defining the rectangle.
        color (tuple or str): Color of the rectangle.
        imageoutlib (str): Preferred image output library.

    Returns:
        Result from the corresponding library's drawColorRectangleAlt method.

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("drawColorRectangleAlt failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.precairo.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)

    logger.error("drawColorRectangleAlt: Selected library is not supported.")
    return False

def get_save_filename(outfile, imageoutlib=defaultdraw):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding
    file extension for saving files (e.g., images). Returns a tuple (filename, EXTENSION)
    or the original `outfile` if it's of type None, bool, or a file object. Returns False
    for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.
        imageoutlib (str): Preferred image output library.

    Returns:
        tuple or original `outfile` or False

    Raises:
        UnsupportedLibraryError: If no supported image output library is available.
    """
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("get_save_filename failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.get_save_filename(outfile)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.get_save_filename(outfile)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.get_save_filename(outfile)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.get_save_filename(outfile)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.get_save_filename(outfile)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.get_save_filename(outfile)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.get_save_filename(outfile)

    logger.error("get_save_filename: Selected library is not supported.")
    return False

def get_save_file(outfile, imageoutlib=defaultdraw):
    return get_save_filename(outfile, imageoutlib)

def new_image_surface(sizex, sizey, bgcolor, imageoutlib=defaultdraw):
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("new_image_surface failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.new_image_surface(sizex, sizey, bgcolor)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.new_image_surface(sizex, sizey, bgcolor)

    logger.error("save_to_file: Selected library is not supported.")
    return False

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode", imageoutlib=defaultdraw):
    try:
        selected_lib = select_image_output_lib(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("save_to_file failed: {}".format(e))
        return False

    if selected_lib == "none" or selected_lib == None:
        return True
    if selected_lib == "pillow" and pilsupport:
        return upcean.predraw.prepil.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib in ["cairo", "cairosvg"] and cairosupport:
        return upcean.predraw.precairo.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib == "qahirah" and qahirahsupport:
        return upcean.predraw.preqahirah.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib == "svgwrite" and svgwritesupport:
        return upcean.predraw.presvgwrite.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib == "wand" and wandsupport:
        return upcean.predraw.prewand.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib == "magick" and magicksupport:
        return upcean.predraw.premagick.save_to_file(inimage, outfile, outfileext, imgcomment)
    elif selected_lib == "pgmagick" and pgmagicksupport:
        return upcean.predraw.prepgmagick.save_to_file(inimage, outfile, outfileext, imgcomment)

    logger.error("save_to_file: Selected library is not supported.")
    return False

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    imageoutlib = None
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif qahirahsupport and isinstance(upc_img, qah.Context) and isinstance(upc_preimg, qah.Surface):
        imageoutlib = "qahirah"
    elif wandsupport and isinstance(upc_img, wImage):
        imageoutlib = "wand"
    elif magicksupport and isinstance(upc_img, PythonMagick.Image):
        imageoutlib = "magick"
    elif pgmagicksupport and isinstance(upc_img, pgmagick.Image):
        imageoutlib = "magick"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and imgout != "none" and imgout is not None):
        imageoutlib = None
    elif(imgout == "none" or imgout is None):
        return False
    elif(not pilsupport and not cairosupport and not qahirahsupport and not svgwritesupport):
        return False
    else:
        return False
    if(outfile is None):
        if(imageoutlib == "cairosvg"):
            oldoutfile = None
            outfile = None
            outfileext = "SVG"
        else:
            oldoutfile = None
            outfile = None
            outfileext = None
    else:
        oldoutfile = get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib] 
    return save_to_file(imgout, outfile, outfileext, imgcomment, imageoutlib)
