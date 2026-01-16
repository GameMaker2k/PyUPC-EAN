# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: prepygame.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

import pygame
import upcean.fonts

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    basestring  # Py2
except NameError:  # Py3
    basestring = str

try:
    unicode  # Py2
except NameError:  # Py3
    unicode = str

try:
    file  # Py2
except NameError:  # Py3
    from io import IOBase as file  # alias

from io import IOBase

try:
    from io import BytesIO, StringIO
except ImportError:  # old Py2
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

# -------------------------
# Fonts (from upcean.fonts)
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath


# -------------------------
# Helpers
# -------------------------
def snapCoords(x, y):
    """Snap to integer + 0.5 (kept behavior)."""
    return (round(x) + 0.5, round(y) + 0.5)


def _safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def _rect_from_coords(x1, y1, x2, y2):
    """
    Create a pygame.Rect from endpoints.
    Preserves original behavior (no normalization): width/height are (x2-x1)/(y2-y1).
    """
    return pygame.Rect(_safe_int(x1), _safe_int(y1), _safe_int(x2 - x1), _safe_int(y2 - y1))


def _to_text(s):
    """
    Ensure we hand pygame a str/unicode appropriate for Py2/Py3.
    - Py3: bytes -> decode utf-8
    - Py2: 'bytes' is str; keep as-is unless it's actually a bytes object from Py3 (rare)
    """
    if isinstance(s, bytes):
        try:
            return s.decode("utf-8")
        except Exception:
            return s.decode("latin-1", "replace")
    return str(s)


def _load_font(ftype, size):
    """
    Load OCR font with fallback paths (kept logic).
    Uses IOError/OSError catch to cover platform differences.
    """
    size = _safe_int(size, 12)
    if size <= 0:
        size = 12

    if ftype == "ocra":
        try:
            return pygame.font.Font(fontpathocra, size)
        except (IOError, OSError):
            return pygame.font.Font(fontpathocraalt, size)

    if ftype == "ocrb":
        try:
            return pygame.font.Font(fontpathocrb, size)
        except (IOError, OSError):
            return pygame.font.Font(fontpathocrbalt, size)

    # Default font path if unknown ftype
    return pygame.font.Font(fontpath, size)


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(surface, x1, y1, x2, y2, color, filled=True):
    """
    Draw filled or outlined rectangle.
    Keeps:
    - filled=True draws filled rect
    - filled=False draws 1px outline
    """
    rect = _rect_from_coords(x1, y1, x2, y2)
    if filled:
        pygame.draw.rect(surface, color, rect)
    else:
        pygame.draw.rect(surface, color, rect, 1)
    return True


def drawColorLine(surface, x1, y1, x2, y2, width, color):
    """Draw a line; width coerced to int >= 1 (kept behavior)."""
    w = _safe_int(width, 1)
    if w < 1:
        w = 1
    pygame.draw.line(surface, color, (_safe_int(x1), _safe_int(y1)), (_safe_int(x2), _safe_int(y2)), w)
    return True


def drawColorText(surface, size, x, y, text, color, ftype="ocrb"):
    """Render text and blit onto surface at (x,y)."""
    font = _load_font(ftype, size)
    t = _to_text(text)
    text_surface = font.render(t, True, color)
    surface.blit(text_surface, (_safe_int(x), _safe_int(y)))
    return True


def drawColorRectangleAlt(surface, x1, y1, x2, y2, color):
    """Outlined rectangle (1px), kept behavior."""
    rect = _rect_from_coords(x1, y1, x2, y2)
    pygame.draw.rect(surface, color, rect, 1)
    return True
