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
import upcean.fonts
import upcean.support

enable_internal_svgwrite = upcean.support.enable_internal_svgwrite
# Initialize support flags
tkintersupport = upcean.support.check_for_tkinter()
tkintersupport = upcean.support.check_for_tkinter()
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
cv2support = upcean.support.check_for_cv2()
skimagesupport = upcean.support.check_for_skimage()
imagelibsupport = upcean.support.imagelibsupport
defaultdraw = upcean.support.defaultdraw

if tkintersupport:
    try:
        import tkinter
        from tkinter import font as tkFont
    except ImportError:
        import Tkinter as tkinter
        import tkFont
    import upcean.predraw.pretkinter

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
        logger.warning("pgmagick support failed to initialize.")

# Initialize Cairo support if available
if cv2support:
    try:
        import cv2
        import numpy as np
        import upcean.predraw.precv2
    except ImportError:
        magicksupport = False
        logger.warning("cv2 support failed to initialize.")

# Initialize Cairo support if available
if skimagesupport:
    try:
        import numpy as np
        import skimage
        import upcean.predraw.preskimage
    except ImportError:
        magicksupport = False
        logger.warning("skimage support failed to initialize.")

# Initialize svgwrite support if available
if svgwritesupport and not enable_internal_svgwrite:
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
else:
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
