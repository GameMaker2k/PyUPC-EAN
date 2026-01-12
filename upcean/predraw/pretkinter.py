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

    $FileInfo: pretkinter.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

try:
    import tkinter
    from tkinter import font as tkFont
except ImportError:  # Py2
    import Tkinter as tkinter
    import tkFont

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
try:
    basestring  # Py2
except NameError:  # Py3
    basestring = str

try:
    file  # Py2
except NameError:  # Py3
    from io import IOBase as file  # alias

from io import IOBase

try:
    from io import StringIO
except ImportError:  # Py2
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

# -------------------------
# Regex / constants
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_PS_EXT = "PS"


# -------------------------
# Helpers
# -------------------------
def color_to_hex(color):
    """
    Accepts:
    - (R,G,B) tuple (0..255)
    - string like "#RRGGBB" or color names
    """
    if isinstance(color, tuple):
        return '#%02x%02x%02x' % color
    if isinstance(color, basestring):
        return color
    raise ValueError("Color must be a tuple or string.")


def _safe_destroy(root):
    try:
        root.destroy()
    except Exception:
        pass


def _canvas_dimensions(canvas):
    # canvas['width'] and ['height'] are strings; normalize to int
    return int(canvas['width']), int(canvas['height'])


def _pick_font(size, ftype):
    """
    Reuse the same fallback list idea, but avoid recreating fonts more than needed.
    Note: Tk font lookup can still vary by platform; this matches original intent.
    """
    families = []
    if ftype == "ocra":
        families.extend(["OCR A Extended", "OCR A"])
    elif ftype == "ocrb":
        families.append("OCR B")

    families.extend(["Monospace", "Courier New", "Courier", "Consolas", "Lucida Console"])

    for fam in families:
        try:
            return tkFont.Font(family=fam, size=size)
        except Exception:
            continue

    return tkFont.Font(size=size)


# -------------------------
# Drawing API
# -------------------------
def drawColorRectangle(canvas, x1, y1, x2, y2, color):
    c = color_to_hex(color)
    canvas.create_rectangle(x1, y1, x2, y2, fill=c, outline=c)
    return True


def drawColorLine(canvas, x1, y1, x2, y2, width, color):
    try:
        width = int(width)
    except Exception:
        width = 1
    if width < 1:
        width = 1

    c = color_to_hex(color)
    canvas.create_line(x1, y1, x2, y2, fill=c, width=width)
    return True


def drawColorText(canvas, size, x, y, text, color, ftype="ocrb"):
    text = str(text)
    c = color_to_hex(color)
    font = _pick_font(size, ftype)
    canvas.create_text(x, y, text=text, fill=c, font=font)
    return True


def drawColorRectangleAlt(canvas, x1, y1, x2, y2, color):
    c = color_to_hex(color)
    canvas.create_rectangle(x1, y1, x2, y2, outline=c)
    return True


def new_image_surface(sizex, sizey, bgcolor):
    """
    Returns [canvas, root] like the original.
    Root is hidden (withdrawn).
    """
    bg = color_to_hex(bgcolor)
    root = tkinter.Tk()
    root.withdraw()
    canvas = tkinter.Canvas(root, width=sizex, height=sizey)
    canvas.pack()
    canvas.create_rectangle(0, 0, sizex, sizey, fill=bg, outline=bg)
    return [canvas, root]


# -------------------------
# Saving helpers
# -------------------------
def get_save_filename(outfile):
    """
    Only PS output is supported.
    Returns:
    - None/bool passthrough
    - (outfile, "PS") for file-like or "-" or string paths
    - False for invalid types
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # file-like or "-"
    if outfile == "-" or hasattr(outfile, 'write') or isinstance(outfile, (file, IOBase)):
        return (outfile, _PS_EXT)

    if isinstance(outfile, basestring):
        out = outfile.strip()
        if out in ("", "-"):
            return (out, _PS_EXT)

        base, ext = os.path.splitext(out)
        # force PS regardless of what was provided
        return (out, _PS_EXT)

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Saves PostScript via canvas.postscript.
    Preserves original branching:
    - outfile is a URL => NotImplementedError (FTP upload not implemented)
    - outfile == "-" => return PS string
    - outfile is None => return PS string
    - outfile is file-like => write PS string and return True
    - outfile is string path => write to that file path and return True
    """
    canvas, root = inimage[0], inimage[1]
    try:
        c_width, c_height = _canvas_dimensions(canvas)

        # enforce PS only (same as original expectation)
        if (outfileext or _PS_EXT).upper() != _PS_EXT:
            raise ValueError("Only PS output is supported")

        # outfile None => return PS string
        if outfile is None:
            return canvas.postscript(width=c_width, height=c_height)

        # string destinations
        if isinstance(outfile, basestring):
            if _RE_URL.match(outfile):
                ps_data = canvas.postscript(width=c_width, height=c_height)
                raise NotImplementedError("FTP upload not implemented in this code")
            if outfile == "-":
                return canvas.postscript(width=c_width, height=c_height)

            # path
            canvas.postscript(file=outfile, width=c_width, height=c_height)
            return True

        # file-like destinations
        if hasattr(outfile, 'write') or isinstance(outfile, (file, IOBase)):
            ps_data = canvas.postscript(width=c_width, height=c_height)
            outfile.write(ps_data)
            return True

        raise ValueError("Invalid outfile type")
    finally:
        _safe_destroy(root)


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    """
    Wrapper consistent with original:
    - parse outfile via get_save_filename
    - enforce PS
    - delegate to save_to_file
    """
    if outfile is None:
        outdest, outfmt = None, None
    else:
        info = get_save_filename(outfile)
        if isinstance(info, (tuple, list)):
            outdest, outfmt = info[0], info[1]
        else:
            outdest, outfmt = None, None

    if (outfmt or _PS_EXT).upper() != _PS_EXT:
        raise ValueError("Only PS output is supported")

    return save_to_file(imgout, outdest, _PS_EXT, imgcomment)
