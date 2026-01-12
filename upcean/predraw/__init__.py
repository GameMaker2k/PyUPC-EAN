# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: predraw.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

import logging

import upcean.support
from upcean.predraw.prefuncs import *  # existing project uses these globals

logger = logging.getLogger(__name__)

# Py2/3 compatibility shims
try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase
    file = IOBase


class UnsupportedLibraryError(Exception):
    """Raised when no supported image output library is available."""
    pass


# Prefer SVG-ish outputs first (generally easiest to support), then bitmap backends.
_FALLBACK_ORDER = (
    "svgwrite",
    "drawsvg",
    "cairo",     # cairo is also used for cairosvg path
    "qahirah",
    "pillow",
    "pil",
    "wand",
    "magick",
    "pgmagick",
    "cv2",
    "skimage",
    "tkinter",
    "drawlib",
)

# Cache for selection results (Py2/3 friendly)
_SELECT_CACHE = {}

# Cache backend module imports
_MODULE_CACHE = {}


def _available_libs():
    """
    Return the authoritative list of usable backends.
    support.py populates imagelibsupport only when imports/checks succeed.
    """
    libs = getattr(upcean.support, "imagelibsupport", None)
    if not libs:
        return []
    # normalize strings to lower
    out = []
    for x in libs:
        try:
            out.append(x.lower())
        except Exception:
            pass
    return out


def select_image_output_lib(imageoutlib="pillow"):
    """
    Choose backend based on preference + upcean.support.imagelibsupport.

    Returns:
        str: selected backend name or "none"
    Raises:
        UnsupportedLibraryError if nothing usable exists.
    """
    if imageoutlib == "none" or imageoutlib is None:
        return "none"

    try:
        pref = imageoutlib.lower()
    except Exception:
        pref = None

    libs = _available_libs()
    if not libs:
        raise UnsupportedLibraryError("No supported image output library available.")

    # If requested is available, use it
    if pref and pref in libs:
        return pref

    # Special case: user asks "cairosvg" but imagelibsupport may include it only when cairo is present
    # (your support.py adds both "cairo" and "cairosvg" if cairo is found).
    if pref == "cairosvg" and "cairosvg" in libs:
        return "cairosvg"

    # Otherwise fall back
    for candidate in _FALLBACK_ORDER:
        if candidate in libs:
            return candidate

    # Last resort: use whatever is available (stable deterministic pick)
    return libs[0]


def _select_cached(imageoutlib):
    key = "none" if imageoutlib is None else imageoutlib
    if key in _SELECT_CACHE:
        return _SELECT_CACHE[key]
    val = select_image_output_lib(imageoutlib)
    _SELECT_CACHE[key] = val
    return val


def _get_backend_module(lib):
    """
    Lazy-load the backend module for the selected library.
    This prevents import-order issues and speeds startup.
    """
    if lib in _MODULE_CACHE:
        return _MODULE_CACHE[lib]

    # Map library -> module path
    # Note: cairosvg uses cairo drawing module for most operations; saving may differ in that module.
    mod = None
    try:
        if lib in ("pillow", "pil"):
            from upcean.predraw import prepil as mod
        elif lib in ("cairo", "cairosvg"):
            from upcean.predraw import precairo as mod
        elif lib == "qahirah":
            from upcean.predraw import preqahirah as mod
        elif lib == "drawsvg":
            from upcean.predraw import predrawsvg as mod
        elif lib == "svgwrite":
            from upcean.predraw import presvgwrite as mod
        elif lib == "wand":
            from upcean.predraw import prewand as mod
        elif lib == "magick":
            from upcean.predraw import premagick as mod
        elif lib == "pgmagick":
            from upcean.predraw import prepgmagick as mod
        elif lib == "cv2":
            from upcean.predraw import precv2 as mod
        elif lib == "skimage":
            from upcean.predraw import preskimage as mod
        elif lib == "tkinter":
            from upcean.predraw import pretkinter as mod
        elif lib == "drawlib":
            from upcean.predraw import predrawlib as mod
        else:
            mod = None
    except Exception as e:
        logger.error("Failed importing backend module for %r: %s", lib, e)
        mod = None

    _MODULE_CACHE[lib] = mod
    return mod


def _call_backend(fn_name, imageoutlib, args, none_return=True):
    """
    Generic dispatcher to call a backend function.

    Parameters:
        fn_name (str): function name in backend module
        imageoutlib: preferred backend name
        args (tuple): positional args for the function call
        none_return: what to return when lib is "none"

    Returns:
        whatever backend returns, or False on error (legacy-compatible)
    """
    try:
        lib = _select_cached(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("%s failed: %s", fn_name, e)
        return False

    if lib in (None, "none"):
        return none_return

    mod = _get_backend_module(lib)
    if mod is None:
        logger.error("%s: Backend module unavailable for %r", fn_name, lib)
        return False

    func = getattr(mod, fn_name, None)
    if func is None:
        logger.error("%s: Backend %r missing function %s", fn_name, lib, fn_name)
        return False

    return func(*args)


# -----------------------------
# Drawing wrappers (no-op returns True for "none")
# -----------------------------
def snapCoords(ctx, x, y, imageoutlib=defaultdraw):
    return _call_backend("snapCoords", imageoutlib, (ctx, x, y), none_return=True)


def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib=defaultdraw):
    return _call_backend("drawColorLine", imageoutlib, (ctx, x1, y1, x2, y2, width, color), none_return=True)


def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib=defaultdraw):
    return _call_backend("drawColorRectangle", imageoutlib, (ctx, x1, y1, x2, y2, color), none_return=True)


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb", imageoutlib=defaultdraw):
    return _call_backend("drawColorText", imageoutlib, (ctx, size, x, y, text, color, ftype), none_return=True)


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib=defaultdraw):
    return _call_backend("drawColorRectangleAlt", imageoutlib, (ctx, x1, y1, x2, y2, color), none_return=True)


# -----------------------------
# Functions that must return real values
# For "none", return False (prevents unpack errors)
# -----------------------------
def get_save_filename(outfile, imageoutlib=defaultdraw):
    return _call_backend("get_save_filename", imageoutlib, (outfile,), none_return=False)


def get_save_file(outfile, imageoutlib=defaultdraw):
    return get_save_filename(outfile, imageoutlib)


def new_image_surface(sizex, sizey, bgcolor, imageoutlib=defaultdraw):
    # Must return (ctx, surface) for most callers; so "none" should not pretend success.
    return _call_backend("new_image_surface", imageoutlib, (sizex, sizey, bgcolor), none_return=False)


def embed_font(dwg, font_path, font_family, imageoutlib=defaultdraw):
    # Only meaningful for SVG backends. Others no-op True.
    try:
        lib = _select_cached(imageoutlib)
    except UnsupportedLibraryError as e:
        logger.error("embed_font failed: %s", e)
        return False

    if lib in (None, "none"):
        return True
    if lib not in ("drawsvg", "svgwrite"):
        return True

    return _call_backend("embed_font", lib, (dwg, font_path, font_family), none_return=True)


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode", imageoutlib=defaultdraw):
    return _call_backend("save_to_file", imageoutlib, (inimage, outfile, outfileext, imgcomment), none_return=False)
