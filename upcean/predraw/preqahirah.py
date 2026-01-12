# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Cool Dude 2k
    Copyright 2011-2025 Game Maker 2k
    Copyright 2011-2025 Kazuki Przyborowski

    $FileInfo: preqahirah.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

from upcean.downloader import upload_file_to_internet_file
import upcean.fonts

import qahirah as qah

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

cairo_valid_extensions = set(["SVG", "PDF", "PS", "EPS", "RAW", "CAIRO", "QAHIRAH"])


# -------------------------
# Helpers (Cairo-compatible)
# -------------------------
def snapCoords(x, y):
    """Snap to half-pixels for crisp rendering (Cairo style)."""
    return (round(x) + 0.5, round(y) + 0.5)


def _set_rgb_255(ctx, color):
    """Set Qahirah source colour from (R,G,B) in 0..255."""
    ctx.set_source_colour((color[0] / 255.0, color[1] / 255.0, color[2] / 255.0))


def _get_cairo_const(*names):
    """
    Qahirah exposes Cairo constants under qah.CAIRO, but exact naming can vary by build/version.
    Try a list of candidate attribute names and return the first found.
    """
    for n in names:
        if hasattr(qah.CAIRO, n):
            return getattr(qah.CAIRO, n)
    return None


def _toy_slant_weight_normal():
    """
    Return (slant_normal, weight_normal) constants for select_font_face,
    with fallbacks across possible constant names.
    """
    slant = _get_cairo_const("FONT_SLANT_NORMAL", "FontSlant_NORMAL", "FontSlantNormal")
    weight = _get_cairo_const("FONT_WEIGHT_NORMAL", "FontWeight_NORMAL", "FontWeightNormal")
    return slant, weight


def _select_font_family_string(ftype):
    """
    Match the Cairo backend *as written*:
    it fed a string into ToyFontFace(...). That API expects a family name,
    but the code supplies a path. We'll supply the same string here.
    """
    if ftype == "ocra":
        primary, alt = fontpathocra, fontpathocraalt
    else:
        primary, alt = fontpathocrb, fontpathocrbalt

    # Try to use primary, fall back to alt if primary path doesn't exist/readable.
    # (Cairo code caught OSError on ToyFontFace creation; here we approximate by checking existence.)
    try:
        if primary and os.path.exists(primary):
            return primary
    except Exception:
        pass
    return alt or primary


def _apply_font_options(ctx):
    """Match Cairo backend font options."""
    fo = qah.FontOptions()
    fo.antialias = qah.CAIRO.ANTIALIAS_DEFAULT
    fo.hint_style = qah.CAIRO.HINT_STYLE_NONE
    fo.hint_metrics = qah.CAIRO.HINT_METRICS_OFF
    ctx.set_font_options(fo)


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(ctx, x1, y1, x2, y2, color):
    _set_rgb_255(ctx, color)
    w = x2 - x1
    h = y2 - y1
    ctx.rectangle(qah.Rect(x1, y1, w, h))
    ctx.fill()
    ctx.new_path()
    return True


def drawColorLine(ctx, x1, y1, x2, y2, width, color):
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
        ctx.rectangle(qah.Rect(rect_x, rect_y, rect_w, rect_h))
        ctx.fill()
    elif y1 == y2:
        rect_x = min(x1, x2)
        rect_y = y1 - width / 2.0
        rect_w = abs(x2 - x1)
        rect_h = float(width)
        ctx.rectangle(qah.Rect(rect_x, rect_y, rect_w, rect_h))
        ctx.fill()
    else:
        ctx.set_line_width(float(width))
        ctx.move_to(qah.Vector(x1, y1))
        ctx.line_to(qah.Vector(x2, y2))
        ctx.stroke()

    ctx.new_path()
    return True


def drawText(ctx, size, x, y, text, ftype="ocrb"):
    """
    Text rendering aligned to Cairo backend:
    - Prefer toy API: select_font_face(family_string, NORMAL, NORMAL)
    - If not available, fall back to file font face
    """
    text = str(text)
    px, py = snapCoords(x, y)

    family = _select_font_family_string(ftype)
    slant, weight = _toy_slant_weight_normal()

    used_toy = False
    if hasattr(ctx, "select_font_face") and slant is not None and weight is not None:
        try:
            ctx.select_font_face(family, slant, weight)
            used_toy = True
        except Exception:
            used_toy = False

    if not used_toy:
        # Fallback: load the font file directly (still keeps OCR-A/OCR-B intent).
        # This is NOT toy-font behavior, but ensures the function works everywhere.
        try:
            font_face = qah.FontFace.create_for_file(family)
        except OSError:
            # last-resort: try the other path explicitly
            if ftype == "ocra":
                font_face = qah.FontFace.create_for_file(fontpathocraalt)
            else:
                font_face = qah.FontFace.create_for_file(fontpathocrbalt)
        ctx.set_font_face(font_face)

    ctx.set_font_size(size)
    _apply_font_options(ctx)

    ctx.move_to(qah.Vector(px, py))
    ctx.show_text(text)
    ctx.stroke()
    return True


def drawColorText(ctx, size, x, y, text, color, ftype="ocrb"):
    _set_rgb_255(ctx, color)
    return drawText(ctx, size, x, y, text, ftype)


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, line_width=1):
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
    ctx.rectangle(qah.Rect(x1, y1, w, h))
    ctx.stroke()
    ctx.new_path()
    return True


# -------------------------
# Saving helpers
# -------------------------
def get_save_filename(outfile):
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


def new_image_surface(sizex, sizey, bgcolor):
    content_type = qah.CAIRO.CONTENT_COLOR
    extents = qah.Rect(0, 0, sizex, sizey)
    surface = qah.RecordingSurface.create(content=content_type, extents=extents)
    ctx = qah.Context.create(surface)
    ctx.set_antialias(qah.CAIRO.ANTIALIAS_NONE)
    drawColorRectangle(ctx, 0, 0, sizex, sizey, bgcolor)
    return [ctx, surface]


def _recording_ink_extents(rec_surface):
    rect = rec_surface.ink_extents
    return rect.left, rect.top, rect.width, rect.height


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    rec = inimage[1]
    outfileext = (outfileext or "PNG").upper()

    x, y, w, h = _recording_ink_extents(rec)
    iw, ih = int(w), int(h)

    uploadfile = None
    outfiletovar = False
    if outfile is not None and _RE_URL.search(str(outfile)):
        uploadfile = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO()

    if outfileext == "SVG":
        surface = qah.SVGSurface.create(outfile, (iw, ih))
        ctx = qah.Context.create(surface)
        ctx.set_source_surface(rec, (-x, -y))
        ctx.paint()
        surface.flush()

    elif outfileext == "PDF":
        surface = qah.PDFSurface.create(outfile, (iw, ih))
        ctx = qah.Context.create(surface)
        ctx.set_source_surface(rec, (-x, -y))
        ctx.paint()
        surface.flush()

    elif outfileext in ("PS", "EPS"):
        surface = qah.PSSurface.create(outfile, (iw, ih))
        surface.set_eps(outfileext == "EPS")
        ctx = qah.Context.create(surface)
        ctx.set_source_surface(rec, (-x, -y))
        ctx.paint()
        surface.flush()

    elif outfileext in ("CAIRO", "QAHIRAH"):
        script_device = qah.ScriptDevice.create(outfile)
        proxy_surface = script_device.surface_create_for_target(rec)
        ctx = qah.Context.create(proxy_surface)
        ctx.set_source_surface(rec, (-x, -y))
        ctx.paint()

    elif outfileext == "RAW":
        # Keep your original approach: use cairo/cairocffi to extract raw bytes.
        try:
            import cairo
        except ImportError:
            import cairocffi as cairo

        image_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, iw, ih)
        image_ctx = cairo.Context(image_surface)
        image_ctx.set_source_surface(rec, -x, -y)
        image_ctx.paint()
        image_surface.flush()

        data = image_surface.get_data()
        if isinstance(outfile, (file, IOBase)):
            outfile.write(data)
        else:
            f = open(outfile, "wb")
            try:
                f.write(data)
            finally:
                f.close()
        image_surface.finish()

    else:
        surface = qah.ImageSurface.create(format=qah.CAIRO.FORMAT_RGB24, dimensions=(iw, ih))
        ctx = qah.Context.create(surface)
        ctx.set_source_surface(rec, (-x, -y))
        ctx.paint()
        surface.flush()
        surface.write_to_png(outfile)

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
    upc_img = imgout[0]
    upc_preimg = imgout[1]

    oldoutfile = None if outfile is None else get_save_filename(outfile)

    if oldoutfile is None or isinstance(oldoutfile, bool):
        # keep your original return marker for compatibility
        return [upc_img, upc_preimg, "cairo"]

    if not isinstance(oldoutfile, (tuple, list)) or len(oldoutfile) != 2:
        return False

    outdest, outfmt = oldoutfile
    return save_to_file(imgout, outdest, outfmt, imgcomment)
