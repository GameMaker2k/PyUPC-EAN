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

    $FileInfo: prepygame.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import pygame
import os
import re
import upcean.fonts

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

def drawColorRectangle(surface, x1, y1, x2, y2, color, filled=True):
    """
    Draws a filled or outlined rectangle on the given surface.

    Parameters:
    - surface: Pygame Surface object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B).
    - filled: If True, draws a filled rectangle. If False, draws only the outline.
    """
    rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
    if filled:
        pygame.draw.rect(surface, color, rect)
    else:
        pygame.draw.rect(surface, color, rect, 1)  # 1 pixel border
    return True  # Optional

def drawColorLine(surface, x1, y1, x2, y2, width, color):
    """
    Draws a line on the given surface.

    Parameters:
    - surface: Pygame Surface object.
    - x1, y1: Starting coordinates.
    - x2, y2: Ending coordinates.
    - width: Line width (integer >= 1).
    - color: Tuple representing (R, G, B).
    """
    width = max(1, int(width))
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)
    return True  # Optional

def drawColorText(surface, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text on the given surface with the specified font and color.

    Parameters:
    - surface: Pygame Surface object.
    - size: Font size.
    - x, y: Position to draw the text.
    - text: The text string to render.
    - color: Tuple representing (R, G, B).
    - ftype: Font type ("ocra" or "ocrb").
    """
    if ftype == "ocra":
        try:
            font = pygame.font.Font(fontpathocra, size)
        except IOError:
            font = pygame.font.Font(fontpathocraalt, size)
    elif ftype == "ocrb":
        try:
            font = pygame.font.Font(fontpathocrb, size)
        except IOError:
            font = pygame.font.Font(fontpathocrbalt, size)
    else:
        font = pygame.font.Font(fontpath, size)  # Default font

    # Ensure text is a Unicode string in Python 2
    if isinstance(text, bytes):
        text = text.decode('utf-8')

    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
    return True

def drawColorRectangleAlt(surface, x1, y1, x2, y2, color):
    """
    Draws an outlined rectangle on the given surface.

    Parameters:
    - surface: Pygame Surface object.
    - x1, y1: Top-left corner coordinates.
    - x2, y2: Bottom-right corner coordinates.
    - color: Tuple representing (R, G, B).
    """
    rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
    pygame.draw.rect(surface, color, rect, 1)  # 1 pixel border
    return True
