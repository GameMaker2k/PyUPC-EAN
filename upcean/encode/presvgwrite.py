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

import os
import re
import base64

from upcean.downloader import upload_file_to_internet_file
import upcean.support

# choose svgwrite implementation
enable_internal_svgwrite = upcean.support.enable_internal_svgwrite
if not enable_internal_svgwrite:
    try:
        import upcean.svgwrite as svgwrite
    except ImportError:
        import upcean.svgcreate as svgwrite
else:
    import upcean.svgcreate as svgwrite

# -------------------------
# Py2 / Py3 compatibility
# -------------------------
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

# -------------------------
# CairoSVG optional
# -------------------------
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

# -------------------------
# regex/constants
# -------------------------
_RE_URL = re.compile(r"^(ftp|ftps|sftp)://", re.IGNORECASE)
_RE_EXT = re.compile(r"^\.(?P<ext>[A-Za-z]+)$")
_RE_NAME_EXT = re.compile(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$")

# -------------------------
# helpers
# -------------------------
def _is_file_like(x):
    return hasattr(x, "write") or isinstance(x, (file, IOBase))

def _rgb_to_svg(color):
    """Accept (R,G,B) tuples 0..255 or pass through SVG color strings."""
    if isinstance(color, tuple):
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        return "rgb({0},{1},{2})".format(r, g, b)
    return color

def _svg_text_from_dwg(dwg):
    """
    Return SVG as unicode text.
    Uses dwg.write(StringIO, pretty=True) which both svgwrite/svgcreate usually support.
    """
    buf = StringIO()
    try:
        # signature differs in some svgwrite forks; keep True like original
        dwg.write(buf, True)
    except TypeError:
        # fallback: some use 'pretty=True'
        try:
            dwg.write(buf)
        except Exception:
            # last fallback: tostring
            return dwg.tostring()
    val = buf.getvalue()
    buf.close()
    return val

def _svg_bytes_from_dwg(dwg):
    """Return UTF-8 encoded bytes for the SVG document."""
    s = _svg_text_from_dwg(dwg)
    if isinstance(s, bytes):
        return s
    return s.encode("utf-8")

def _convert_svg_bytes(svg_bytes, fmt, out_fp):
    """
    Convert SVG bytes to fmt using CairoSVG, writing into out_fp (file-like or filename).
    """
    b = BytesIO(svg_bytes)
    b.seek(0)
    fmt = fmt.upper()
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
        # should not happen due to validation
        raise ValueError("Unsupported CairoSVG format: {0}".format(fmt))
    try:
        b.close()
    except Exception:
        pass

# -------------------------
# API functions
# -------------------------
def get_save_filename(outfile):
    """
    Returns:
      - outfile unchanged if None/bool
      - (outfile, "SVG") for file-like or "-"
      - (path_or_url_or_name, EXT) for strings / (name, ext)
      - False on invalid
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
            name = s  # keep original full string (path) like your code
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
    # Use a live in-memory file-like for svgwrite Drawing initialization
    dummy = StringIO()
    dwg = svgwrite.Drawing(dummy, profile="full", size=(sizex, sizey))
    # background
    drawColorRectangle(dwg, 0, 0, sizex, sizey, bgcolor)
    try:
        dummy.close()
    except Exception:
        pass
    return [dwg, None]

def drawColorRectangleAlt(dwg, x1, y1, x2, y2, color):
    w = x2 - x1
    h = y2 - y1
    stroke = _rgb_to_svg(color)
    dwg.add(dwg.rect(insert=(x1, y1), size=(w, h), fill="none", stroke=stroke, stroke_width=1))
    return True

def drawColorRectangle(dwg, x1, y1, x2, y2, color):
    w = x2 - x1
    h = y2 - y1
    fill = _rgb_to_svg(color)
    dwg.add(dwg.rect(insert=(x1, y1), size=(w, h), fill=fill, stroke="none"))
    return True

def drawColorLine(dwg, x1, y1, x2, y2, width, color):
    width = max(1, int(width))
    stroke = _rgb_to_svg(color)
    dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=stroke, stroke_width=width))
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

    dwg.add(dwg.text(
        str(text),
        insert=(x, y),
        fill=fill,
        font_size=size,
        font_family=font_family
    ))
    return True

def embed_font(dwg, font_path, font_family):
    """
    Embed a local TTF/OTF into <defs><style> once per drawing.
    Safe Py2/Py3.
    """
    # per-drawing cache
    try:
        cache = dwg._embedded_fonts
    except AttributeError:
        cache = set()
        dwg._embedded_fonts = cache

    try:
        fam = unicode(font_family)  # Py2
    except Exception:
        fam = str(font_family)

    key = (os.path.abspath(font_path), fam)
    if key in cache:
        return
    cache.add(key)

    f = open(font_path, "rb")
    try:
        font_data = f.read()
    finally:
        f.close()

    b64 = base64.b64encode(font_data)
    if not isinstance(b64, str):
        b64 = b64.decode("ascii")

    ext = os.path.splitext(font_path)[1].lower()
    if ext == ".ttf":
        fmt = "truetype"
        mime = "font/ttf"
    elif ext == ".otf":
        fmt = "opentype"
        mime = "font/otf"
    else:
        raise ValueError("Unsupported font format: {0}".format(ext))

    css = (
        "@font-face {{\n"
        "  font-family: '{family}';\n"
        "  src: url(data:{mime};base64,{b64}) format('{fmt}');\n"
        "  font-weight: normal;\n"
        "  font-style: normal;\n"
        "}}\n"
    ).format(family=fam, mime=mime, b64=b64, fmt=fmt)

    style_el = dwg.style(css)
    try:
        style_el.update(id="fontface-{0}".format(fam))
    except Exception:
        pass
    dwg.defs.add(style_el)

def save_to_file(inimage, outfile, outfileext, imgcomment="barcode"):
    dwg = inimage[0]
    fmt = (outfileext or "SVG").upper()
    if fmt not in svgwrite_valid_extensions:
        fmt = "SVG"

    upload_target = None
    return_to_var = False

    # Decide destination: URL upload / "-" / file-like / filename
    if isinstance(outfile, basestring) and _RE_URL.match(str(outfile)):
        upload_target = outfile
        # For cairo conversions we want bytes; otherwise text is OK but we upload bytes anyway.
        outfp = BytesIO() if cairosvgsupport and fmt != "SVG" else StringIO()
    elif outfile == "-":
        return_to_var = True
        outfp = BytesIO() if cairosvgsupport and fmt != "SVG" else StringIO()
    else:
        outfp = outfile  # file-like or filename

    # Write or convert
    if cairosvgsupport and fmt in ("PNG", "PDF", "PS", "EPS", "SVG"):
        svg_bytes = _svg_bytes_from_dwg(dwg)
        # ensure binary output target for cairo conversion when writing to file-like
        if _is_file_like(outfp) and isinstance(outfp, StringIO):
            # shouldn't happen in our branches, but keep safe
            outfp = BytesIO()
        _convert_svg_bytes(svg_bytes, fmt, outfp)
    else:
        # Plain SVG write
        if _is_file_like(outfp):
            # svgwrite wants text stream; if we were handed a binary stream, write bytes ourselves
            if isinstance(outfp, BytesIO):
                outfp.write(_svg_bytes_from_dwg(dwg))
            else:
                dwg.write(outfp, True)
        else:
            # filename path
            try:
                dwg.saveas(outfp, True)
            except TypeError:
                dwg.saveas(outfp)

    # Upload to URL
    if upload_target:
        # We must upload bytes
        if isinstance(outfp, BytesIO):
            outfp.seek(0)
            upload_file_to_internet_file(outfp, upload_target)
            outfp.close()
        else:
            # StringIO -> bytes
            outfp.seek(0)
            b = BytesIO(outfp.getvalue().encode("utf-8"))
            outfp.close()
            b.seek(0)
            upload_file_to_internet_file(b, upload_target)
            b.close()
        return True

    # Return to variable for "-"
    if return_to_var:
        outfp.seek(0)
        data = outfp.read()
        outfp.close()
        return data

    return True

def save_to_filename(imgout, outfile, imgcomment="barcode"):
    if outfile is None:
        # match your convention: return [dwg, preimg, "svgwrite"]
        return [imgout[0], imgout[1], "svgwrite"]

    parsed = get_save_filename(outfile)
    if not parsed or isinstance(parsed, bool):
        return False

    outname, ext = parsed
    save_to_file(imgout, outname, ext, imgcomment)
    return True
