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

    $FileInfo: prepysdl2.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import sdl2
import sdl2.ext
import sdl2.sdlttf

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


def _rgba(color):
    """
    Ensure (R,G,B,A). If 3-tuple is passed, assume opaque.
    """
    if isinstance(color, tuple) and len(color) == 4:
        return (int(color[0]), int(color[1]), int(color[2]), int(color[3]))
    if isinstance(color, tuple) and len(color) == 3:
        return (int(color[0]), int(color[1]), int(color[2]), 255)
    # best effort fallback
    return (255, 255, 255, 255)


def _to_text(s):
    """
    Ensure we have a unicode text string (works in Py2/Py3).
    """
    if isinstance(s, bytes):
        try:
            return s.decode("utf-8")
        except Exception:
            return s.decode("latin-1", "replace")
    return str(s)


def _fs_path_bytes(path):
    """
    SDL_ttf expects a bytes path in most bindings; keep behavior robust.
    """
    if path is None:
        return None
    if isinstance(path, bytes):
        return path
    try:
        return path.encode("utf-8")
    except Exception:
        # last resort
        return str(path).encode("utf-8")


def _pick_font_path(ftype):
    """
    Match your original preference:
    - ocra: primary then alt
    - ocrb: primary then alt
    - else: fontpath, else None
    """
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    elif ftype == "ocrb":
        primary, alt = fontpathocrb, fontpathocrbalt
    else:
        primary, alt = fontpath, None

    if primary and os.path.isfile(primary):
        return primary
    if alt and os.path.isfile(alt):
        return alt
    return primary  # may be None/invalid, caller handles


# -------------------------
# Font caching
# -------------------------
_FONT_CACHE = {}  # {(ftype, size): TTF_Font*}


def close_cached_fonts():
    """
    Optional: call at shutdown to release cached fonts.
    """
    for k, font in list(_FONT_CACHE.items()):
        try:
            if font:
                sdl2.sdlttf.TTF_CloseFont(font)
        except Exception:
            pass
        _FONT_CACHE.pop(k, None)


def load_font(font_type, size):
    """
    Loads the specified font type with the given size.
    Now cached per (font_type, size) to reduce overhead.
    Returns: TTF_Font pointer, or raises IOError on failure.
    """
    try:
        size_i = int(size)
    except Exception:
        size_i = 12
    if size_i <= 0:
        size_i = 12

    key = (font_type, size_i)
    cached = _FONT_CACHE.get(key)
    if cached:
        return cached

    path = _pick_font_path(font_type)

    # Fall back logic mirrors your original intent.
    if font_type == "ocra":
        candidates = [fontpathocra, fontpathocraalt]
    elif font_type == "ocrb":
        candidates = [fontpathocrb, fontpathocrbalt]
    else:
        candidates = [fontpath, None]

    font = None
    for p in candidates:
        if p is None:
            continue
        b = _fs_path_bytes(p)
        try:
            font = sdl2.sdlttf.TTF_OpenFont(b, size_i)
        except Exception:
            font = None
        if font:
            break

    if not font:
        # As in your original: try "default font" by passing None (may fail depending on platform)
        try:
            font = sdl2.sdlttf.TTF_OpenFont(None, size_i)
        except Exception:
            font = None

    if not font:
        raise IOError("Failed to load font type={!r} size={!r}".format(font_type, size_i))

    _FONT_CACHE[key] = font
    return font


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=True):
    r, g, b, a = _rgba(color)
    rect = sdl2.SDL_Rect(_safe_int(x1), _safe_int(y1), _safe_int(x2 - x1), _safe_int(y2 - y1))
    sdl2.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    if filled:
        sdl2.SDL_RenderFillRect(renderer, rect)
    else:
        sdl2.SDL_RenderDrawRect(renderer, rect)
    return True


def drawColorLine(renderer, x1, y1, x2, y2, width, color):
    """
    SDL2 doesn't support line width directly; emulate by drawing multiple offset lines.
    Keeps your approach, but makes width coercion safer and offsets symmetric.
    """
    r, g, b, a = _rgba(color)
    w = _safe_int(width, 1)
    if w < 1:
        w = 1

    sdl2.SDL_SetRenderDrawColor(renderer, r, g, b, a)

    x1i, y1i, x2i, y2i = _safe_int(x1), _safe_int(y1), _safe_int(x2), _safe_int(y2)

    # Symmetric offsets: for width=1 -> [0], width=2 -> [-1,0], width=3 -> [-1,0,1], etc.
    start = -(w // 2)
    end = start + w
    for off in range(start, end):
        sdl2.SDL_RenderDrawLine(renderer, x1i, y1i + off, x2i, y2i + off)

    return True


def drawColorText(renderer, size, x, y, text, color, ftype="ocrb"):
    """
    Render text with SDL_ttf to a surface, convert to texture, copy to renderer.
    Preserves your behavior, but:
    - uses cached fonts
    - centralizes utf-8 conversion
    - ensures cleanup on all failure paths
    """
    try:
        font = load_font(ftype, size)
    except IOError:
        return False

    t = _to_text(text)
    r, g, b, a = _rgba(color)
    sdl_color = sdl2.SDL_Color(r, g, b, a)

    # Render text surface
    surf = sdl2.sdlttf.TTF_RenderUTF8_Blended(font, t.encode("utf-8"), sdl_color)
    if not surf:
        return False

    tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
    if not tex:
        sdl2.SDL_FreeSurface(surf)
        return False

    try:
        w = surf.contents.w
        h = surf.contents.h
        dst = sdl2.SDL_Rect(_safe_int(x), _safe_int(y), w, h)
        sdl2.SDL_RenderCopy(renderer, tex, None, dst)
    finally:
        sdl2.SDL_DestroyTexture(tex)
        sdl2.SDL_FreeSurface(surf)

    return True


def drawColorRectangleAlt(renderer, x1, y1, x2, y2, color):
    return drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=False)


def clear_renderer(renderer, color=(255, 255, 255, 255)):
    r, g, b, a = _rgba(color)
    sdl2.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    sdl2.SDL_RenderClear(renderer)


def present_renderer(renderer):
    sdl2.SDL_RenderPresent(renderer)
