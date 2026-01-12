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

# PySDL3 module names vary depending on how your environment packages them.
# Aermoss/PySDL3 typically exposes `sdl3` and `sdl3_ttf`. :contentReference[oaicite:3]{index=3}
try:
    import sdl3 as sdl
except ImportError:
    import sdl3  # noqa
    sdl = sdl3

try:
    import sdl3_ttf as ttf
except ImportError:
    # Some setups might put ttf under a different name; keep a clear error if not found.
    ttf = None

import upcean.fonts

# Font paths from upcean
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath

# Python 2/3 compatibility
try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase as file  # type: ignore

from io import IOBase


# -----------------------------
# Small helpers
# -----------------------------
def _is_file_like(obj):
    return hasattr(obj, "write") or isinstance(obj, (file, IOBase))


def _to_utf8_bytes(text):
    # Keep behavior: accept bytes or str/unicode; SDL_ttf expects UTF-8 bytes.
    if text is None:
        text = ""
    # Python 2: unicode exists; Python 3: this NameError except path is fine.
    try:
        unicode  # noqa
        is_py2 = True
    except NameError:
        is_py2 = False

    if isinstance(text, bytes):
        return text
    if is_py2:
        # unicode_literals means "str" might be unicode in py2; still safe.
        try:
            return text.encode("utf-8")
        except Exception:
            return unicode(text).encode("utf-8")  # noqa
    # py3
    return str(text).encode("utf-8")


def snapCoords(x, y):
    """Snap to half-pixel for crisp 1px lines (classic trick)."""
    return (round(x) + 0.5, round(y) + 0.5)


def _ensure_rgba(color):
    """Accept (R,G,B) or (R,G,B,A); default A=255."""
    if color is None:
        return (0, 0, 0, 255)
    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            return (int(color[0]), int(color[1]), int(color[2]), 255)
        if len(color) == 4:
            return (int(color[0]), int(color[1]), int(color[2]), int(color[3]))
    # fallback
    return (0, 0, 0, 255)


def _pick_font_path(ftype):
    if ftype == "ocra":
        return fontpathocra if os.path.isfile(fontpathocra) else fontpathocraalt
    if ftype == "ocrb":
        return fontpathocrb if os.path.isfile(fontpathocrb) else fontpathocrbalt
    return fontpath


# -----------------------------
# Font cache (big speed win)
# -----------------------------
_FONT_CACHE = {}  # (font_path, ptsize_float) -> TTF_Font*


def ttf_init():
    """Call once before drawColorText if you haven't already initialized SDL_ttf."""
    if ttf is None:
        raise ImportError("sdl3_ttf module not available (install/enable SDL3_ttf bindings).")
    # SDL3_ttf uses TTF_Init / TTF_Quit like SDL2_ttf (same naming in the C API). :contentReference[oaicite:4]{index=4}
    if ttf.TTF_WasInit() == 0:
        if ttf.TTF_Init() < 0:
            # Keep it simple; caller can also inspect TTF_GetError if available.
            raise RuntimeError("TTF_Init failed")


def ttf_quit(close_cached_fonts=True):
    """Optionally close cached fonts and quit SDL_ttf."""
    if ttf is None:
        return
    if close_cached_fonts:
        for _k, f in list(_FONT_CACHE.items()):
            try:
                ttf.TTF_CloseFont(f)
            except Exception:
                pass
        _FONT_CACHE.clear()
    if ttf.TTF_WasInit() != 0:
        ttf.TTF_Quit()


def _get_font(ftype, size):
    """Open (or reuse) a font. SDL3_ttf uses float ptsize. :contentReference[oaicite:5]{index=5}"""
    ttf_init()
    font_path = _pick_font_path(ftype)
    ptsize = float(size)
    key = (font_path, ptsize)
    f = _FONT_CACHE.get(key)
    if f:
        return f

    # PySDL3 is ctypes-based; it generally accepts Python strings for const char*,
    # but on some platforms passing bytes is safer.
    path_arg = _to_utf8_bytes(font_path) if isinstance(font_path, basestring) else font_path
    f = ttf.TTF_OpenFont(path_arg, ptsize)
    if not f:
        # fall back: try default fontpath if OCR font is missing
        if font_path != fontpath:
            path_arg = _to_utf8_bytes(fontpath)
            f = ttf.TTF_OpenFont(path_arg, ptsize)
    if not f:
        raise IOError("Failed to load font for ftype=%s size=%s" % (ftype, size))

    _FONT_CACHE[key] = f
    return f


# -----------------------------
# Drawing API
# -----------------------------
def drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=True):
    r, g, b, a = _ensure_rgba(color)
    rect = sdl.SDL_FRect(float(x1), float(y1), float(x2 - x1), float(y2 - y1))
    sdl.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    if filled:
        sdl.SDL_RenderFillRect(renderer, rect)
    else:
        sdl.SDL_RenderRect(renderer, rect)
    return True


def drawColorRectangleAlt(renderer, x1, y1, x2, y2, color):
    return drawColorRectangle(renderer, x1, y1, x2, y2, color, filled=False)


def drawColorLine(renderer, x1, y1, x2, y2, width, color):
    """
    SDL3 renderer API still draws 1px lines; emulate width by drawing multiple offset lines.
    Mirrors your SDL2 behavior.
    """
    r, g, b, a = _ensure_rgba(color)
    width = max(1, int(width))

    sdl.SDL_SetRenderDrawColor(renderer, r, g, b, a)

    # Center the offsets, like the SDL2 version
    half = width // 2

    # If vertical-ish, offset in x; otherwise offset in y (matches typical thick-line hack).
    dx = abs(int(x2) - int(x1))
    dy = abs(int(y2) - int(y1))
    if dx <= dy:
        # mostly vertical: vary x
        for i in range(width):
            off = i - half
            sdl.SDL_RenderLine(renderer, float(x1 + off), float(y1), float(x2 + off), float(y2))
    else:
        # mostly horizontal: vary y
        for i in range(width):
            off = i - half
            sdl.SDL_RenderLine(renderer, float(x1), float(y1 + off), float(x2), float(y2 + off))

    return True


def drawColorText(renderer, size, x, y, text, color, ftype="ocrb"):
    """
    Render text using SDL3_ttf:
      surface = TTF_RenderText_Blended(font, text, length, color) :contentReference[oaicite:6]{index=6}
      texture = SDL_CreateTextureFromSurface(renderer, surface)
      SDL_RenderTexture(renderer, texture, None, &dstrect) :contentReference[oaicite:7]{index=7}
    """
    if ttf is None:
        raise ImportError("sdl3_ttf module not available (install/enable SDL3_ttf bindings).")

    r, g, b, a = _ensure_rgba(color)
    font = _get_font(ftype, size)

    txt = _to_utf8_bytes(text)
    # SDL3_ttf takes explicit length. :contentReference[oaicite:8]{index=8}
    length = len(txt)

    fg = sdl.SDL_Color(r, g, b, a)
    surface = ttf.TTF_RenderText_Blended(font, txt, length, fg)
    if not surface:
        return False

    texture = sdl.SDL_CreateTextureFromSurface(renderer, surface)
    if not texture:
        sdl.SDL_DestroySurface(surface)
        return False

    # Query surface size
    w = int(surface.contents.w)
    h = int(surface.contents.h)

    dst = sdl.SDL_FRect(float(x), float(y), float(w), float(h))
    # SDL3 uses SDL_RenderTexture (subpixel precision). :contentReference[oaicite:9]{index=9}
    ok = sdl.SDL_RenderTexture(renderer, texture, None, dst)

    sdl.SDL_DestroyTexture(texture)
    sdl.SDL_DestroySurface(surface)

    return bool(ok)


def clear_renderer(renderer, color=(255, 255, 255, 255)):
    r, g, b, a = _ensure_rgba(color)
    sdl.SDL_SetRenderDrawColor(renderer, r, g, b, a)
    sdl.SDL_RenderClear(renderer)


def present_renderer(renderer):
    sdl.SDL_RenderPresent(renderer)
