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

    $FileInfo: predrawlib.py - Last Update: 6/27/2025 Ver. 2.20.0 RC 1 - Author: cooldude2k $
'''

from drawlib.apis import (
    clear, config, rectangle, line, text, save,
    ShapeStyle, LineStyle, TextStyle, Colors, FontFile
)
from upcean.xml.downloader import upload_file_to_internet_file
import os, re
try:
    from io import BytesIO, IOBase
except ImportError:
    from StringIO import StringIO as BytesIO
    from StringIO import StringIO as IOBase
import upcean.fonts

# font paths
fontpathocra    = upcean.fonts.fontpathocra
fontpathocraalt = upcean.fonts.fontpathocraalt
fontpathocrb    = upcean.fonts.fontpathocrb
fontpathocrbalt = upcean.fonts.fontpathocrbalt

class DrawlibContext(object):
    """Dummy context so existing code can unpack ctx, img and draw into drawlib."""
    def __init__(self):
        pass
    def user_to_device(self, x, y):
        return x, y
    def rectangle(self, coords, fill=None, outline=None):
        (x1, y1), (x2, y2) = coords
        w = x2 - x1; h = y2 - y1
        if fill is not None:
            style = ShapeStyle(halign="left", valign="top", fcolor=fill, lwidth=0)
        else:
            style = ShapeStyle(halign="left", valign="top", fcolor=Colors.Transparent, lcolor=outline, lwidth=1)
        rectangle(xy=(x1, y1), width=w, height=h, style=style)
    def line(self, pts, fill, width):
        (x1, y1), (x2, y2) = pts
        style = LineStyle(width=max(1, int(width)), color=fill)
        line((x1, y1), (x2, y2), style=style)
    def text(self, pos, txt, font=None, fill=None, size=None):
        x, y = pos
        style = TextStyle(color=fill, font=font)
        if size is not None:
            style.size = size  # <-- this line ensures sizing works
        text(xy=(x, y), text=str(txt), style=style)


def snapCoords(ctx, x, y):
    return round(x) + 0.5, round(y) + 0.5


def drawColorRectangle(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], fill=color)
    return True


def drawColorLine(ctx, x1, y1, x2, y2, width, color, imageoutlib=None):
    ctx.line([(x1, y1), (x2, y2)], fill=color, width=width)
    return True


def drawColorText(ctx, size, x, y, txt, color, ftype="ocrb", imageoutlib=None):
    if ftype.lower() == "ocra":
        ttf = fontpathocra if os.path.exists(fontpathocra) else fontpathocraalt
    else:
        ttf = fontpathocrb if os.path.exists(fontpathocrb) else fontpathocrbalt

    font_file = FontFile(ttf)

    ctx.text((x, y), str(txt), font=font_file, fill=color, size=size)
    return True


def drawColorRectangleAlt(ctx, x1, y1, x2, y2, color, imageoutlib=None):
    ctx.rectangle([(x1, y1), (x2, y2)], outline=color)
    return True


def get_save_filename(outfile, imageoutlib=None):
    if outfile is None or isinstance(outfile, bool):
        return outfile
    if isinstance(outfile, IOBase) or outfile == "-":
        return (outfile, "png")
    if isinstance(outfile, str):
        s = outfile.strip()
        if s == "" or s == "-":
            return (s, "png")
        if re.match("^(ftp|ftps|sftp):\\/\\/", s):
            return (s, "png")
        base, ext = os.path.splitext(s)
        if ext:
            ext = ext.lstrip(".").lower()
        else:
            m = re.match("^(.+):([A-Za-z]+)$", s)
            if m:
                base, ext = m.group(1), m.group(2).lower()
            else:
                ext = "png"
        return (base, ext)
    if isinstance(outfile, (tuple, list)) and len(outfile) == 2:
        return (outfile[0], str(outfile[1]).lower())
    return False


get_save_file = get_save_filename


def new_image_surface(sizex, sizey, bgcolor, imageoutlib=None):
    # clear old canvas, init new one
    clear()
    config(width=sizex, height=sizey, background_color=bgcolor)
    return [DrawlibContext(), None]


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode", imageoutlib=None):
    upload_target = None
    is_bytes_out = False
    # handle remote upload
    if isinstance(outfile, str) and re.match("^(ftp|ftps|sftp):\\/\\/", outfile):
        upload_target = outfile
        outfile = BytesIO()
    elif outfile == "-":
        outfile = BytesIO()
        is_bytes_out = True
    # normalize path
    if isinstance(outfile, str):
        outfile = os.path.expanduser(outfile)
        outfile = os.path.expandvars(outfile)
        outfile = os.path.abspath(outfile)
        # attach extension if missing
        if not outfile.lower().endswith("." + str(outfileext).lower()):
            outfile = outfile + "." + str(outfileext).lower()
    # drawlib save: positional args
    save(file=outfile, format=str(outfileext).lower())
    # handle remote upload
    if upload_target:
        outfile.seek(0)
        upload_file_to_internet_file(outfile, upload_target)
        outfile.close()
        return True
    # return bytes for "-"
    if is_bytes_out:
        outfile.seek(0)
        data = outfile.read()
        outfile.close()
        return data
    return True


def save_to_filename(imgout, outfile, imgcomment="barcode", imageoutlib=None):
    parsed = get_save_filename(outfile, imageoutlib)
    if not parsed or isinstance(parsed, bool):
        return False if parsed is False else [None, None, imageoutlib]
    name, ext = parsed
    return save_to_file(imgout, name, ext, imgcomment, imageoutlib)
