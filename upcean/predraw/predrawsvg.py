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

    $FileInfo: presvgwrite.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

from upcean.downloader import upload_file_to_internet_file
import upcean.support

import drawsvg
import os
import re
import base64

try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase
    file = IOBase

try:
    from io import IOBase, StringIO, BytesIO
except ImportError:  # Py2
    from StringIO import StringIO
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO
    try:
        from io import IOBase
    except Exception:
        IOBase = object

# CairoSVG optional conversion
cairosvgsupport = False
svgwrite_valid_extensions = set(["SVG"])
if upcean.support.cairosvgsupport:
    try:
        import cairosvg
        cairosvgsupport = True
        svgwrite_valid_extensions = set(["SVG", "PDF", "PS", "EPS", "PNG"])
    except ImportError:
        cairosvgsupport = False
        svgwrite_valid_extensions = set(["SVG"])

# regex/constants
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")


def _is_file_like(x):
    return hasattr(x, "write") or isinstance(x, (file, IOBase))


def _rgb_to_svg(color):
    """Convert (R,G,B) tuples to 'rgb(r,g,b)' strings; pass-through strings."""
    if isinstance(color, tuple):
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        return "rgb({0},{1},{2})".format(r, g, b)
    return color


def _drawing_to_svg_text(dwg):
    """
    Return SVG XML text from a drawsvg.Drawing instance across versions.
    drawsvg 2.x: as_svg(); older: asSvg()/to_svg()/toSvg().
    """
    if hasattr(dwg, "as_svg"):
        return dwg.as_svg()
    if hasattr(dwg, "asSvg"):
        return dwg.asSvg()
    if hasattr(dwg, "to_svg"):
        return dwg.to_svg()
    if hasattr(dwg, "toSvg"):
        return dwg.toSvg()
    return str(dwg)


def _svg_bytes_from_dwg(dwg):
    s = _drawing_to_svg_text(dwg)
    if isinstance(s, bytes):
        return s
    return s.encode("utf-8")


def _convert_svg_bytes(svg_bytes, fmt, out_fp):
    """
    Convert SVG bytes to fmt using CairoSVG, writing into out_fp (file-like or filename).
    """
    b = BytesIO(svg_bytes)
    b.seek(0)
    fmt = (fmt or "SVG").upper()

    if fmt == "PNG":
        cairosvg.svg2png(file_obj=b, write_to=out_fp)
    elif fmt == "PDF":
        cairosvg.svg2pdf(file_obj=b, write_to=out_fp)
    elif fmt == "PS":
        cairosvg.svg2ps(file_obj=b, write_to=out_fp)
    elif fmt == "EPS":
        cairosvg.svg2eps(file_obj=b, write_to=out_fp)
    elif fmt == "SVG":
        cairosvg.svg2svg(file_obj=b, write_to=out_fp)
    else:
        raise ValueError("Unsupported CairoSVG format: {0}".format(fmt))

    try:
        b.close()
    except Exception:
        pass


def get_save_filename(outfile):
    """
    Determine (filename, EXT) where EXT is one of svgwrite_valid_extensions.
    Supports:
      - None/bool -> passthrough
      - file-like or "-" -> (outfile, "SVG")
      - "name.ext" or "name:EXT" -> parsed
      - (name, ext) -> validated
    """
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if _is_file_like(outfile) or outfile == "-":
        return (outfile, "SVG")

    if isinstance(outfile, basestring):
        s = outfile.strip()
        if s in ("", "-"):
            return (s, "SVG")

        base, ext = os.path.splitext(s)
        if ext:
            m = _RE_EXT.match(ext)
            outfileext = m.group("ext").upper() if m else None
            name = s  # preserve full string like your originals
        else:
            m = _RE_NAME_EXT.match(s)
            if m:
                name = m.group("name")
                outfileext = m.group("ext").upper()
            else:
                name = s
                outfileext = None

        if not outfileext:
            outfileext = "SVG"
        if outfileext not in svgwrite_valid_extensions:
            outfileext = "SVG"
        return (name, outfileext)

    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False
        filename, ext = outfile
        if not (_is_file_like(filename) or isinstance(filename, basestring)):
            return False
        if not isinstance(ext, basestring):
            return False
        ext = ext.strip().upper() or "SVG"
        if ext not in svgwrite_valid_extensions:
            ext = "SVG"
        return (filename, ext)

    return False


def get_save_file(outfile):
    return get_save_filename(outfile)


def new_image_surface(sizex, sizey, bgcolor):
    """
    Create a new drawsvg.Drawing and paint a solid background rectangle.
    """
    dwg = drawsvg.Drawing(sizex, sizey)
    drawColorRectangle(dwg, 0, 0, sizex, sizey, bgcolor)
    return [dwg, None]


def drawColorRectangleAlt(dwg, x1, y1, x2, y2, color):
    w = x2 - x1
    h = y2 - y1
    stroke = _rgb_to_svg(color)
    rect = drawsvg.Rectangle(
        x1, y1, w, h,
        fill="none",
        stroke=stroke,
        stroke_width=1
    )
    dwg.append(rect)
    return True


def drawColorRectangle(dwg, x1, y1, x2, y2, color):
    w = x2 - x1
    h = y2 - y1
    fill = _rgb_to_svg(color)
    rect = drawsvg.Rectangle(
        x1, y1, w, h,
        fill=fill,
        stroke="none"
    )
    dwg.append(rect)
    return True


def drawColorLine(dwg, x1, y1, x2, y2, width, color):
    width = max(1, int(width))
    stroke = _rgb_to_svg(color)
    ln = drawsvg.Line(
        x1, y1, x2, y2,
        stroke=stroke,
        stroke_width=width
    )
    dwg.append(ln)
    return True


def drawColorText(dwg, size, x, y, text, color, ftype="ocrb"):
    fill = _rgb_to_svg(color)
    ft = (ftype or "").lower()
    if ft == "ocrb":
        font_family = "OCRB"
    elif ft == "ocra":
        font_family = "OCR-A"
    else:
        font_family = "Monospace"

    t = drawsvg.Text(
        str(text),
        size,
        x, y,
        fill=fill,
        font_family=font_family
    )
    dwg.append(t)
    return True


def embed_font(dwg, font_path, font_family):
    """
    Embeds a custom font into the SVG via an @font-face block once per Drawing.
    Safe to call many times.

    drawsvg API differences:
      - some versions support dwg.append_def(...)
      - some expose dwg.defs
      - fallback: dwg.append(...)
    """
    # per-drawing cache
    cache = getattr(dwg, "_embedded_fonts", None)
    if cache is None:
        cache = set()
        setattr(dwg, "_embedded_fonts", cache)

    try:
        fam = unicode(font_family)  # Py2
    except Exception:
        fam = str(font_family)

    key = (os.path.abspath(font_path), fam)
    if key in cache:
        return
    cache.add(key)

    # read font file
    f = open(font_path, "rb")
    try:
        font_data = f.read()
    finally:
        f.close()

    # base64 encode
    b64 = base64.b64encode(font_data)
    if not isinstance(b64, str):
        b64 = b64.decode("ascii")

    # determine format
    ext = os.path.splitext(font_path)[1].lower()
    if ext == ".ttf":
        fmt = "truetype"
        mime = "font/ttf"
    elif ext == ".otf":
        fmt = "opentype"
        mime = "font/otf"
    else:
        raise ValueError("Unsupported font format: {0}".format(ext))

    # CSS wrapped in CDATA for SVG
    css = (
        '<style type="text/css"><![CDATA[\n'
        '@font-face {\n'
        "  font-family: '%(family)s';\n"
        "  src: url(data:%(mime)s;base64,%(b64)s) format('%(fmt)s');\n"
        '  font-weight: normal;\n'
        '  font-style: normal;\n'
        '}\n'
        ']]></style>\n'
    ) % {"family": fam, "mime": mime, "b64": b64, "fmt": fmt}

    raw = drawsvg.Raw(css)

    # attach to defs (best-effort)
    if hasattr(dwg, "append_def"):
        try:
            dwg.append_def(raw)
            return
        except Exception:
            pass
    if hasattr(dwg, "defs"):
        try:
            dwg.defs.append(raw)
            return
        except Exception:
            pass
    try:
        dwg.append(raw)
    except Exception:
        return


def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    """
    Save drawsvg.Drawing to:
      - SVG directly, or
      - PNG/PDF/PS/EPS via CairoSVG (when available)

    Behaviors preserved:
      - outfile "-" => return bytes/text
      - ftp/ftps/sftp upload
      - file-like objects supported
    """
    dwg = inimage[0]
    fmt = (outfileext or "SVG").upper()
    if fmt not in svgwrite_valid_extensions:
        fmt = "SVG"

    upload_target = None
    return_to_var = False

    # Decide destination
    if isinstance(outfile, basestring) and _RE_URL.match(str(outfile)):
        upload_target = outfile
        # Use BytesIO when converting (CairoSVG) else StringIO is fine
        outfp = BytesIO() if (cairosvgsupport and fmt != "SVG") else StringIO()
    elif outfile == "-":
        return_to_var = True
        outfp = BytesIO() if (cairosvgsupport and fmt != "SVG") else StringIO()
    else:
        outfp = outfile  # filename or file-like

    # Write/convert
    if cairosvgsupport and fmt in ("PNG", "PDF", "PS", "EPS", "SVG"):
        _convert_svg_bytes(_svg_bytes_from_dwg(dwg), fmt, outfp)
    else:
        # Plain SVG
        svg_text = _drawing_to_svg_text(dwg)

        if _is_file_like(outfp):
            # If it's a binary buffer, write bytes
            if isinstance(outfp, BytesIO):
                outfp.write(svg_text.encode("utf-8") if not isinstance(svg_text, bytes) else svg_text)
            else:
                try:
                    outfp.write(svg_text)
                except TypeError:
                    outfp.write(svg_text.encode("utf-8"))
        else:
            # filename path
            if hasattr(dwg, "save_svg") and fmt == "SVG":
                dwg.save_svg(outfp)
            else:
                # Py2: no encoding arg in open()
                f = open(outfp, "wb")
                try:
                    b = svg_text if isinstance(svg_text, bytes) else svg_text.encode("utf-8")
                    f.write(b)
                finally:
                    f.close()

    # Upload
    if upload_target:
        if isinstance(outfp, BytesIO):
            outfp.seek(0)
            upload_file_to_internet_file(outfp, upload_target)
            outfp.close()
        else:
            outfp.seek(0)
            b = BytesIO(outfp.getvalue().encode("utf-8"))
            outfp.close()
            b.seek(0)
            upload_file_to_internet_file(b, upload_target)
            b.close()
        return True

    # "-" returns
    if return_to_var:
        outfp.seek(0)
        data = outfp.read()
        outfp.close()
        return data

    return True


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    upc_img = imgout[0]
    upc_preimg = imgout[1]

    if outfile is None:
        return [upc_img, upc_preimg, "drawsvg"]

    parsed = get_save_filename(outfile)
    if isinstance(parsed, (tuple, list)):
        outname, ext = parsed[0], parsed[1]
    else:
        return [upc_img, upc_preimg, "drawsvg"]

    save_to_file(imgout, outname, ext, imgcomment)
    return True
