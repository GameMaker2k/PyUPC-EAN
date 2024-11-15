# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: prepysdl2.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import re
import ctypes

# Compatibility for Python 2 and 3
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

# Import PySDL2 modules
import sdl2
import sdl2.ext
import sdl2.sdlttf

import upcean.fonts

# Load font paths from upcean.fonts
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

def snapCoords(x, y):
    """
    Snaps the coordinates to the nearest integer plus 0.5.

    Parameters:
    - x, y: Original coordinates.

    Returns:
    - (snapped_x, snapped_y)
    """
    snapped_x = round(x) + 0.5
    snapped_y = round(y) + 0.5
    return (snapped_x, snapped_y)

def drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=True):
    """
    Draws a filled or outlined rectangle on the given renderer.

    Parameters:
    - renderer: SDL_Renderer object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B, A).
    - filled: If True, draws a filled rectangle. If False, draws only the outline.
    """
    rect = sdl2.SDL_Rect(int(x1), int(y1), int(x2 - x1), int(y2 - y1))
    sdl2.SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], color[3])
    if filled:
        sdl2.SDL_RenderFillRect(renderer, rect)
    else:
        sdl2.SDL_RenderDrawRect(renderer, rect)
    return True  # Optional

def drawColorLine(renderer, x1, y1, x2, y2, width, color):
    """
    Draws a line on the given renderer.

    Parameters:
    - renderer: SDL_Renderer object.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple representing (R, G, B, A).
    """
    # SDL2 does not support line width directly. To emulate width, draw multiple lines offset.
    sdl2.SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], color[3])
    for i in range(width):
        offset = i - width // 2
        adjusted_y1 = y1 + offset
        adjusted_y2 = y2 + offset
        sdl2.SDL_RenderDrawLine(renderer, int(x1), int(adjusted_y1), int(x2), int(adjusted_y2))
    return True  # Optional

def load_font(font_type, size):
    """
    Loads the specified font type with the given size.

    Parameters:
    - font_type: "ocra" or "ocrb".
    - size: Font size.

    Returns:
    - TTF_Font pointer.
    """
    if font_type == "ocra":
        try:
            font = sdl2.sdlttf.TTF_OpenFont(fontpathocra.encode('utf-8'), size)
            if not font:
                raise IOError
        except IOError:
            font = sdl2.sdlttf.TTF_OpenFont(fontpathocraalt.encode('utf-8'), size)
            if not font:
                raise IOError("Failed to load ocra fonts.")
    elif font_type == "ocrb":
        try:
            font = sdl2.sdlttf.TTF_OpenFont(fontpathocrb.encode('utf-8'), size)
            if not font:
                raise IOError
        except IOError:
            font = sdl2.sdlttf.TTF_OpenFont(fontpathocrbalt.encode('utf-8'), size)
            if not font:
                raise IOError("Failed to load ocrb fonts.")
    else:
        try:
            font = sdl2.sdlttf.TTF_OpenFont(fontpath.encode('utf-8'), size)
            if not font:
                raise IOError
        except IOError:
            font = sdl2.sdlttf.TTF_OpenFont(None, size)  # Default font
            if not font:
                raise IOError("Failed to load default font.")
    return font

def drawColorText(renderer, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text on the given renderer with the specified font and color.

    Parameters:
    - renderer: SDL_Renderer object.
    - size: Font size.
    - x, y: Position to draw the text.
    - text: The text string to render.
    - color: Tuple representing (R, G, B, A).
    - ftype: Font type ("ocra" or "ocrb").
    """
    try:
        font = load_font(ftype, size)
    except IOError as e:
        print(e)
        return False

    # Ensure text is a Unicode string in Python 2
    if isinstance(text, bytes):
        text = text.decode('utf-8')

    # Render text to surface
    text_surface = sdl2.sdlttf.TTF_RenderUTF8_Blended(font, text.encode('utf-8'), sdl2.SDL_Color(color[0], color[1], color[2], color[3]))
    if not text_surface:
        print("TTF_RenderUTF8_Blended Error: {}".format(sdl2.sdlttf.TTF_GetError()))
        sdl2.sdlttf.TTF_CloseFont(font)
        return False

    # Create texture from surface
    texture = sdl2.SDL_CreateTextureFromSurface(renderer, text_surface)
    if not texture:
        print("SDL_CreateTextureFromSurface Error: {}".format(sdl2.SDL_GetError()))
        sdl2.SDL_FreeSurface(text_surface)
        sdl2.sdlttf.TTF_CloseFont(font)
        return False

    # Get text dimensions
    text_rect = sdl2.SDL_Rect(x, y, text_surface.contents.w, text_surface.contents.h)

    # Render the texture
    sdl2.SDL_RenderCopy(renderer, texture, None, text_rect)

    # Clean up
    sdl2.SDL_DestroyTexture(texture)
    sdl2.SDL_FreeSurface(text_surface)
    sdl2.sdlttf.TTF_CloseFont(font)
    return True

def drawColorRectangleAlt(renderer, x1, y1, x2, y2, color):
    """
    Draws an outlined rectangle on the given renderer.

    Parameters:
    - renderer: SDL_Renderer object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B, A).
    """
    return drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=False)

def clear_renderer(renderer, color=(255, 255, 255, 255)):
    """
    Clears the renderer with the specified color.

    Parameters:
    - renderer: SDL_Renderer object.
    - color: Tuple representing (R, G, B, A).
    """
    sdl2.SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], color[3])
    sdl2.SDL_RenderClear(renderer)

def present_renderer(renderer):
    """
    Presents the current rendering on the screen.

    Parameters:
    - renderer: SDL_Renderer object.
    """
    sdl2.SDL_RenderPresent(renderer)
