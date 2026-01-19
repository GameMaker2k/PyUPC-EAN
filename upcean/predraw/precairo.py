# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2025 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: precairo.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts

try:
    import cairo
except ImportError:
    import cairocffi as cairo

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
    from io import BytesIO
except ImportError:  # old Py2
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

# -------------------------
# Font paths (from upcean)
# -------------------------
fontpathocra = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt
fontpath = upcean.fonts.fontpath  # kept for compatibility

# -------------------------
# Constants / regex
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_DOT_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_COLON_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

# Define valid Cairo output formats (keep your set)
cairo_valid_extensions = set(["SVG", "PDF", "PS", "EPS", "RAW", "CAIRO", "QAHIRAH"])


# --- optional freetype support (runtime-detected) ---
try:
    import freetype  # pip install freetype-py
except Exception:
    freetype = None

# Cache: (abspath, face_index) -> (cairo_face, ft_face) OR None
_FT_FONTFACE_CACHE = {}

def _cairo_font_face_from_ttf(ttf_path, face_index=0):
    """
    Best-effort: create a cairo.FontFace from a font file without installing it.

    Returns:
        - cairocffi.FontFace on success
        - None if freetype/cairo-ft bridge not available or creation fails

    Important:
        We cache BOTH the cairo_face and the freetype Face object so the underlying
        FT_Face stays alive for as long as the cairo_face might be used.
    """
    if not ttf_path:
        return None

    ttf_path = os.path.abspath(ttf_path)
    key = (ttf_path, int(face_index))

    # Cache hit
    cached = _FT_FONTFACE_CACHE.get(key, None)
    if cached is None and key in _FT_FONTFACE_CACHE:
        # explicitly cached failure
        return None
    if cached is not None:
        cairo_face, ft_face = cached  # keep ft_face referenced via cache
        return cairo_face

    # No freetype -> cannot do FT loading
    if freetype is None:
        _FT_FONTFACE_CACHE[key] = None
        return None

    # Need cairocffi + cairo-ft bridge
    try:
        import cairocffi
        from cairocffi import ffi, lib
    except Exception:
        _FT_FONTFACE_CACHE[key] = None
        return None

    if not hasattr(lib, "cairo_ft_font_face_create_for_ft_face"):
        _FT_FONTFACE_CACHE[key] = None
        return None

    try:
        # freetype-py Face supports different signatures depending on version.
        # Prefer using the requested face_index if supported.
        try:
            ft_face = freetype.Face(ttf_path, index=int(face_index))
        except TypeError:
            ft_face = freetype.Face(ttf_path)
            # If we couldn't pass index, try selecting a face if API provides it
            # (not always available). Safe no-op if missing.
            try:
                ft_face.face_index = int(face_index)
            except Exception:
                pass

        cairo_face_ptr = lib.cairo_ft_font_face_create_for_ft_face(
            ffi.cast("FT_Face", ft_face._FT_Face),
            0  # load_flags; keep 0 unless you know you need FT_LOAD_* flags
        )

        # Wrap pointer into a cairocffi FontFace object
        cairo_face = cairocffi.FontFace._from_pointer(cairo_face_ptr, incref=False)

        # Cache both to keep FT_Face alive
        _FT_FONTFACE_CACHE[key] = (cairo_face, ft_face)
        return cairo_face

    except Exception:
        _FT_FONTFACE_CACHE[key] = None
        return None

def _set_rgb_255(ctx, color):
    """Set cairo source RGB from (R,G,B) in 0..255."""
    ctx.set_source_rgb(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)


def snapCoords(x, y):
    """
    Snaps coords to nearest half-pixel for crisp rendering.
    (Source mentioned in your original: stevehanov.ca)
    """
    return (round(x) + 0.5, round(y) + 0.5)


def drawColorRectangle(ctx, x1, y1, x2, y2, color):
    """Draw filled rectangle with RGB color in [0,255]."""
    _set_rgb_255(ctx, color)
    w = x2 - x1
    h = y2 - y1
    ctx.rectangle(x1, y1, w, h)
    ctx.fill()
    ctx.new_path()
    return True


def drawColorLine(ctx, x1, y1, x2, y2, width, color):
    """
    Draw a colored line. For perfectly vertical/horizontal lines, draw a filled rectangle
    for consistent thickness; otherwise stroke a cairo line.
    """
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    _set_rgb_255(ctx, color)

    x1, y1 = snapCoords(x1, y1)
    x2, y2 = snapCoords(x2, y2)

    if x1 == x2:
        rect_x = x1 - width / 2.0
        rect_y = min(y1, y2)
        rect_w = float(width)
        rect_h = abs(y2 - y1)
        ctx.rectangle(rect_x, rect_y, rect_w, rect_h)
        ctx.fill()
    elif y1 == y2:
        rect_x = min(x1, x2)
        rect_y = y1 - width / 2.0
        rect_w = abs(x2 - x1)
        rect_h = float(width)
        ctx.rectangle(rect_x, rect_y, rect_w, rect_h)
        ctx.fill()
    else:
        ctx.set_line_width(width)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

    ctx.new_path()
    return True


def _select_toy_font(ftype):
    """
    Select a Cairo ToyFontFace with fallback paths.
    Keeps your behavior (try primary else alt).
    """
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    else:
        primary, alt = fontpathocrb, fontpathocrbalt

    try:
        return cairo.ToyFontFace(primary)
    except OSError:
        return cairo.ToyFontFace(alt)


def _select_font_face(ctx, ftype):
    """
    Prefer a real FT font face from a font file if possible.
    Fall back to ToyFontFace with family names if not.
    """
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
        family_fallback = "OCR-A"
    else:
        primary, alt = fontpathocrb, fontpathocrbalt
        family_fallback = "OCRB"

    # pick an existing file path
    path = primary if (primary and os.path.isfile(primary)) else alt

    # Try FT font face from file
    face = _cairo_font_face_from_ttf(path) if path else None
    if face is not None:
        # IMPORTANT: this face is a cairocffi FontFace; it works with cairocffi Context.
        # If you're using pycairo Context, it may not accept it.
        try:
            ctx.set_font_face(face)
            return True
        except Exception:
            pass

    # Fall back: family-name based toy face
    try:
        ctx.set_font_face(cairo.ToyFontFace(family_fallback))
    except Exception:
        ctx.select_font_face(family_fallback)
    return False


def _apply_font_options(ctx):
    """Apply font options matching your original settings."""
    fo = cairo.FontOptions()
    fo.set_antialias(cairo.ANTIALIAS_DEFAULT)
    fo.set_hint_style(cairo.HINT_STYLE_NONE)
    fo.set_hint_metrics(cairo.HINT_METRICS_OFF)
    ctx.set_font_options(fo)


def drawText(ctx, size, x, y, text, ftype="ocrb"):
    """Draw text (uncolored) at snapped coords."""
    text = str(text)
    px, py = snapCoords(x, y)

    _select_font_face(ctx, ftype)
    ctx.set_font_size(size)
    _apply_font_options(ctx)

    ctx.move_to(px, py)
    ctx.show_text(text)
    return True


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    """Draw colored text at position."""
    _set_rgb_255(ctx, color)
    return drawText(ctx, size, x, y, text, ftype)


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, line_width=1):
    """Draw outlined rectangle."""
    _set_rgb_255(ctx, color)
    try:
        lw = float(line_width)
    except Exception:
        lw = 1.0
    if lw <= 0:
        lw = 1.0
    ctx.set_line_width(lw)

    w = x2 - x1
    h = y2 - y1
    ctx.rectangle(x1, y1, w, h)
    ctx.stroke()
    ctx.new_path()
    return True


def get_save_filename(outfile):
    """
    Normalize outfile spec to (destination, EXT).
    Same behavior as your original:
    - None/bool passthrough
    - file-like or "-" -> (outfile, "PNG")
    - string -> supports "name.ext" and "name:EXT", defaults to PNG,
               and restricts to cairo_valid_extensions (else PNG)
    - tuple/list (filename, ext) -> validates ext similarly
    - invalid -> False
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if outfile == "-" or isinstance(outfile, (file, IOBase)):
        return (outfile, "PNG")

    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return (out, "PNG")

        base, ext = os.path.splitext(out)

        out_ext = None
        if ext:
            m = _RE_DOT_EXT.match(ext)
            if m:
                out_ext = m.group("ext").upper()
        else:
            m = _RE_NAME_COLON_EXT.match(out)
            if m:
                out = m.group("name")
                out_ext = m.group("ext").upper()

        if not out_ext:
            out_ext = "PNG"

        if out_ext not in cairo_valid_extensions:
            out_ext = "PNG"

        return (out, out_ext)

    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False
        filename, ext = outfile

        if isinstance(filename, (file, IOBase)):
            fn = filename
        elif isinstance(filename, basestring):
            fn = filename.strip()
        else:
            return False

        if not isinstance(ext, basestring):
            return False

        ext_u = ext.strip().upper()
        if ext_u not in cairo_valid_extensions:
            ext_u = "PNG"

        return (fn, ext_u)

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


def new_image_surface(sizex, sizey, bgcolor, imtype=None):
    """
    Create a RecordingSurface and a Context, fill background.
    Returns [ctx, recording_surface].
    """
    if(imtype is None):
        surface = cairo.RecordingSurface(
            cairo.CONTENT_COLOR, (0.0, 0.0, float(sizex), float(sizey))
        )
    elif(imtype=="image"):
        surface = cairo.ImageSurface(
            cairo.FORMAT_RGB24, float(sizex), float(sizey)
        )
    elif(imtype=="pdf"):
        surface = cairo.PDFSurface(
            None, float(sizex), float(sizey)
        )
    elif(imtype=="ps" or imtype=="eps"):
        surface = cairo.PSSurface(
            None, float(sizex), float(sizey)
        )
    elif(imtype=="svg"):
        surface = cairo.SVGSurface(
            None, float(sizex), float(sizey)
        )
    else:
        surface = cairo.RecordingSurface(
            cairo.CONTENT_COLOR, (0.0, 0.0, float(sizex), float(sizey))
        )
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_NONE)
    drawColorRectangle(ctx, 0, 0, sizex, sizey, bgcolor)
    return [ctx, surface]


def _paint_recording_to_surface(recording_surface, target_surface):
    """
    Paint the recorded content onto a concrete surface, accounting for ink extents.
    Returns (x, y) extents used so caller can apply offsets if needed.
    """
    x, y, w, h = recording_surface.ink_extents()
    ctx = cairo.Context(target_surface)
    ctx.set_source_surface(recording_surface, -x, -y)
    ctx.paint()
    return x, y, w, h


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Save recorded Cairo content.
    Keeps:
    - ftp/ftps/sftp upload
    - outfile == "-" returns bytes
    - SVG/PDF/PS/EPS/CAIRO/QAHIRAH/RAW/PNG behaviors
    """
    recording = inimage[1]
    outfileext = (outfileext or "PNG").upper()

    # Determine output destination mode
    uploadfile = None
    outfiletovar = False
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    # Ink extents give bounding box of drawn content
    x, y, w, h = recording.ink_extents()
    iw = int(w)
    ih = int(h)

    # Helper: create the right target surface, paint, flush, finish
    if outfileext == "SVG":
        surface = cairo.SVGSurface(outfile, iw, ih)
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        surface.finish()

    elif outfileext == "PDF":
        surface = cairo.PDFSurface(outfile, iw, ih)
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        surface.finish()

    elif outfileext in ("PS", "EPS"):
        surface = cairo.PSSurface(outfile, iw, ih)
        if outfileext == "EPS":
            surface.set_eps(True)
        else:
            surface.set_eps(False)
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        surface.finish()

    elif outfileext in ("CAIRO", "QAHIRAH"):
        # Script output
        surface = cairo.ScriptSurface(
            cairo.ScriptDevice(outfile),
            cairo.FORMAT_RGB24,
            iw,
            ih
        )
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        surface.finish()

    elif outfileext == "RAW":
        # Raw pixel bytes from an ImageSurface
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, iw, ih)
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        data = surface.get_data()

        if isinstance(outfile, (file, IOBase)):
            outfile.write(data)
        else:
            f = open(outfile, "wb")
            try:
                f.write(data)
            finally:
                f.close()

        surface.finish()

    else:
        # Default to PNG via ImageSurface.write_to_png
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, iw, ih)
        _paint_recording_to_surface(recording, surface)
        surface.flush()
        surface.write_to_png(outfile)
        surface.finish()

    # Upload / return bytes behavior
    if uploadfile is not None:
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
        return True

    if outfiletovar:
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    return True


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """
    Wrapper:
    - if outfile is None OR get_save_filename returns None/bool -> return [ctx, surface, "cairo"]
    - else save via save_to_file
    """
    upc_img = imgout[0]
    upc_preimg = imgout[1]

    if outfile is None:
        oldoutfile = None
    else:
        oldoutfile = get_save_filename(outfile)

    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [upc_img, upc_preimg, "cairo"]

    if not isinstance(oldoutfile, (tuple, list)) or len(oldoutfile) != 2:
        return False

    outdest, outfmt = oldoutfile
    return save_to_file(imgout, outdest, outfmt, imgcomment)
