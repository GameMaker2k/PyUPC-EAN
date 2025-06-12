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

    $FileInfo: predrawlib.py - Last Update: 6/11/2025 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from drawlib.apis import (
    config, rectangle, line, text, save,
    ShapeStyle, LineStyle, TextStyle, Colors
)
from upcean.xml.downloader import upload_file_to_internet_file
from io import BytesIO, IOBase
import os, re
import upcean.fonts
from PIL import ImageFont  # only for font loading

# font paths
fontpathocra    = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb    = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt

def snapCoords(x, y):
    """Snap to the nearest half-pixel grid."""
    return (round(x) + 0.5, round(y) + 0.5)

def drawColorRectangle(x1, y1, x2, y2, color):
    """Filled rectangle from (x1,y1) to (x2,y2)."""
    w = x2 - x1
    h = y2 - y1
    style = ShapeStyle(
        halign="left", valign="top",
        fcolor=color,
        lwidth=0
    )
    rectangle(xy=(x1, y1), width=w, height=h, style=style)
    return True

def drawColorLine(x1, y1, x2, y2, width, color):
    """Line from (x1,y1) to (x2,y2)."""
    style = LineStyle(
        width=max(1, int(width)),
        color=color
    )
    line((x1, y1), (x2, y2), style=style)
    return True

def drawColorText(size, x, y, txt, color, ftype="ocrb"):
    """Draw text at (x,y) with OCR-style font."""
    # pick the right font file
    if ftype.lower() == "ocra":
        path = fontpathocra if os.path.exists(fontpathocra) else fontpathocraalt
    else:
        path = fontpathocrb if os.path.exists(fontpathocrb) else fontpathocrbalt
    font = ImageFont.truetype(path, size)
    style = TextStyle(color=color, font=font)
    text(xy=(x, y), text=str(txt), style=style)
    return True

def drawColorRectangleAlt(x1, y1, x2, y2, color):
    """Outline-only rectangle."""
    w = x2 - x1
    h = y2 - y1
    style = ShapeStyle(
        halign="left", valign="top",
        fcolor=Colors.Transparent,
        lcolor=color,
        lwidth=1
    )
    rectangle(xy=(x1, y1), width=w, height=h, style=style)
    return True

def setup_canvas(width, height, bgcolor=(255,255,255)):
    """
    Initialize the global drawlib canvas.
    """
    config(width=width, height=height, background_color=bgcolor)

def get_save_filename(outfile):
    """
    Parse `outfile` into (filename, format) or return None/False.
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile
    # file-object or stdout
    if isinstance(outfile, IOBase) or outfile == "-":
        return (outfile, "png")
    # string path or URL
    if isinstance(outfile, str):
        s = outfile.strip()
        # stdout
        if s in ("", "-"):
            return (s, "png")
        # FTP/SFTP upload
        if re.match(r"^(ftp|ftps|sftp)://", s):
            return (s, "png")
        base, ext = os.path.splitext(s)
        if ext:
            ext = ext.lstrip(".").lower()
        else:
            # custom "name:EXT" syntax
            m = re.match(r"^(.+):([A-Za-z]+)$", s)
            if m:
                base, ext = m.group(1), m.group(2).lower()
            else:
                ext = "png"
        return (base, ext)
    # tuple/list
    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        name, ext = outfile
        if not isinstance(ext, str):
            return False
        ext = ext.strip().lower()
        return (name, ext)
    return False

# alias
get_save_file = get_save_filename

def new_image_surface(sizex, sizey, bgcolor=(255,255,255)):
    """
    Create+clear the canvas.
    """
    setup_canvas(sizex, sizey, bgcolor)

def save_to_file(outfile, fmt=None, imgcomment=None):
    """
    Save global canvas to `outfile`.
    Supports FTP URLs and "-" (returns bytes).
    """
    target = outfile
    upload_dest = None
    is_stdout = False

    # handle FTP
    if isinstance(outfile, str) and re.match(r"^(ftp|ftps|sftp)://", outfile):
        upload_dest = outfile
        target = BytesIO()
    # handle stdout
    elif outfile == "-":
        target = BytesIO()
        is_stdout = True

    # default format
    fmt = (fmt or "png").lower()
    save(file=target, format=fmt)

    # perform upload if needed
    if upload_dest:
        target.seek(0)
        upload_file_to_internet_file(target, upload_dest)
        target.close()
        return True

    # return bytes on stdout
    if is_stdout:
        target.seek(0)
        data = target.read()
        target.close()
        return data

    return True

def save_to_filename(outfile, imgcomment=None):
    """
    Figure out filename+format, then call save_to_file().
    """
    parsed = get_save_filename(outfile)
    if not parsed or isinstance(parsed, bool):
        # e.g. None or False
        return False if parsed is False else [None, None, "drawlib"]
    name, fmt = parsed
    return save_to_file(name, fmt, imgcomment)
