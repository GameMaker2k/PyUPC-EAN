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

    $FileInfo: prepygame2.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import pygame
import upcean.fonts

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    unicode  # Py2
except NameError:  # Py3
    unicode = str

try:
    basestring  # Py2
except NameError:  # Py3
    basestring = str


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
    return (round(x) + 0.5, round(y) + 0.5)


def _safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def _rect_from_coords(x1, y1, x2, y2):
    # Preserve original behavior: width/height are (x2-x1)/(y2-y1) (no normalization).
    return pygame.Rect(_safe_int(x1), _safe_int(y1), _safe_int(x2 - x1), _safe_int(y2 - y1))


def _to_text(s):
    # Keep behavior: bytes -> decode; otherwise str()
    if isinstance(s, bytes):
        try:
            return s.decode("utf-8")
        except Exception:
            return s.decode("latin-1", "replace")
    return str(s)


def _pick_font_paths(ftype):
    if ftype == "ocra":
        return (fontpathocra, fontpathocraalt)
    if ftype == "ocrb":
        return (fontpathocrb, fontpathocrbalt)
    return (fontpath, None)


def _first_existing_path(paths):
    for p in paths:
        if p and isinstance(p, basestring) and os.path.isfile(p):
            return p
    return None


# -------------------------
# Font loader (Pygame 2 friendly)
# -------------------------
_HAS_FREETYPE = False
try:
    import pygame.freetype as _pgft
    _HAS_FREETYPE = True
except Exception:
    _pgft = None
    _HAS_FREETYPE = False

# Simple cache: {(backend, path_or_None, size): fontobj}
_FONT_CACHE = {}


def _get_font(size, ftype):
    """
    Returns (backend, fontobj) where backend is either 'freetype' or 'font'.
    Uses pygame.freetype when available (preferred for Pygame 2).
    """
    size = _safe_int(size, 12)
    if size <= 0:
        size = 12

    primary, alt = _pick_font_paths(ftype)
    chosen = _first_existing_path([primary, alt])

    # Prefer freetype on pygame 2
    if _HAS_FREETYPE:
        key = ("freetype", chosen, size)
        font = _FONT_CACHE.get(key)
        if font is None:
            # pygame.freetype.Font accepts None -> default font
            font = _pgft.Font(chosen, size)
            _FONT_CACHE[key] = font
        return ("freetype", font)

    # Fallback to pygame.font (works in pygame 1/2)
    key = ("font", chosen, size)
    font = _FONT_CACHE.get(key)
    if font is None:
        # pygame.font.Font accepts None -> default font
        font = pygame.font.Font(chosen, size)
        _FONT_CACHE[key] = font
    return ("font", font)


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(surface, x1, y1, x2, y2, color, filled=True):
    rect = _rect_from_coords(x1, y1, x2, y2)
    if filled:
        pygame.draw.rect(surface, color, rect)
    else:
        pygame.draw.rect(surface, color, rect, 1)
    return True


def drawColorLine(surface, x1, y1, x2, y2, width, color):
    w = _safe_int(width, 1)
    if w < 1:
        w = 1
    pygame.draw.line(
        surface,
        color,
        (_safe_int(x1), _safe_int(y1)),
        (_safe_int(x2), _safe_int(y2)),
        w
    )
    return True


def drawColorText(surface, size, x, y, text, color, ftype="ocrb"):
    """
    Pygame 2 compatible text drawing:
    - Prefer pygame.freetype.Font.render_to (no need to blit a returned surface manually)
    - Fallback to pygame.font.Font.render + blit if freetype not available

    Keeps your original semantics: draw at (x,y) using the chosen OCR font.
    """
    t = _to_text(text)
    x = _safe_int(x)
    y = _safe_int(y)

    backend, font = _get_font(size, ftype)

    if backend == "freetype":
        # render_to draws directly onto the surface at the given position
        # antialias=True matches typical rendered look; Pygame 1/2 differences exist anyway.
        font.render_to(surface, (x, y), t, fgcolor=color)
        return True

    # pygame.font fallback
    text_surface = font.render(t, True, color)
    surface.blit(text_surface, (x, y))
    return True


def drawColorRectangleAlt(surface, x1, y1, x2, y2, color):
    rect = _rect_from_coords(x1, y1, x2, y2)
    pygame.draw.rect(surface, color, rect, 1)
    return True
