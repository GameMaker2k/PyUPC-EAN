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

    $FileInfo: predraw.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean.fonts
import upcean.support
pilsupport = upcean.support.check_for_pil()
if(pilsupport):
    try:
        from PIL import Image, ImageDraw, ImageFont
        pilsupport = True
        # Handle resampling filter compatibility for Pillow 10+ and older versions
        try:
            from PIL import Resampling  # Pillow 10+
            NEAREST = Resampling.NEAREST
        except ImportError:
            NEAREST = Image.NEAREST  # Older versions of Pillow
    except ImportError:
        pilsupport = False
        NEAREST = None  # If Pillow isn't available, NEAREST isn't needed
    import upcean.encode.prepil
cairosupport = upcean.support.check_for_cairo()
if(cairosupport):
    import cairo
    import upcean.encode.precairo

try:
    import pkg_resources
    pkgres = True
except ImportError:
    pkgres = False

try:
    basestring
except NameError:
    basestring = str

pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()

fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

''' // Source: http://stevehanov.ca/blog/index.php?id=28 '''


def snapCoords(ctx, x, y, imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.snapCoords(ctx, x, y)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.snapCoords(ctx, x, y)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False


def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.drawColorLine(ctx, x1, y1, x2, y2, width, color)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False


def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.drawColorRectangle(ctx, x1, y1, x2, y2, color)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb", imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.drawColorText(ctx, size, x, y, text, color, ftype)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.drawColorText(ctx, size, x, y, text, color, ftype)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.drawColorRectangleAlt(ctx, x1, y1, x2, y2, color)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False


def get_save_filename(outfile, imageoutlib="pillow"):
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        return upcean.encode.prepil.get_save_filename(outfile)
    if(not pilsupport and imageoutlib == "pillow"):
        return False
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return upcean.encode.precairo.get_save_filename(outfile)
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        return False
    return False
