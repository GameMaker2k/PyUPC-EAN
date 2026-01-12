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
# drawsvg (Python package) docs: https://pypi.org/project/drawsvg/
import drawsvg
import os
import re
import base64
import io  # For file object type checking

try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

# CairoSVG optional (used here for PDF/PS/EPS/PNG conversion exactly like original script)
if upcean.support.cairosvgsupport:
    try:
        import cairosvg
        cairosvgsupport = True
        # Define valid CairoSVG output formats
        svgwrite_valid_extensions = {"SVG", "PDF", "PS", "EPS", "PNG"}
    except ImportError:
        cairosvgsupport = False
        svgwrite_valid_extensions = {"SVG"}
else:
    cairosvgsupport = False
    svgwrite_valid_extensions = {"SVG"}


def _rgb_to_svg(color):
    """Convert (R,G,B) tuples to 'rgb(r,g,b)' strings; pass-through strings."""
    if isinstance(color, tuple):
        r = min(max(int(color[0]), 0), 255)
        g = min(max(int(color[1]), 0), 255)
        b = min(max(int(color[2]), 0), 255)
        return 'rgb({},{},{})'.format(r, g, b)
    return color


def _drawing_to_svg_text(dwg):
    """
    Return SVG XML text from a drawsvg.Drawing instance across drawsvg versions.
    drawsvg 2.x uses d.as_svg(); older 1.x used camelCase methods.
    """
    if hasattr(dwg, 'as_svg'):
        return dwg.as_svg()
    if hasattr(dwg, 'asSvg'):
        return dwg.asSvg()
    if hasattr(dwg, 'to_svg'):
        return dwg.to_svg()
    if hasattr(dwg, 'toSvg'):
        return dwg.toSvg()
    # Last resort: try str()
    return str(dwg)


def get_save_filename(outfile):
    """
    Processes the `outfile` parameter to determine a suitable filename and its corresponding file extension.
    Returns a tuple (filename, "SVG") or the original `outfile` if it's of type None, bool, or a file object.
    Defaults to "SVG" as the extension if none is provided or if an unsupported extension is detected.
    Returns False for unsupported input types.

    Parameters:
        outfile (str, tuple, list, None, bool, file): The output file specification.

    Returns:
        tuple: (filename, "SVG") or False if invalid.
    """
    # Handle None or boolean types directly
    if outfile is None or isinstance(outfile, bool):
        return outfile

    # Handle file objects directly
    if isinstance(outfile, file) or isinstance(outfile, IOBase) or outfile == "-":
        return (outfile, "SVG")

    # Handle string types
    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "SVG")

        # Extract extension using os.path.splitext
        base, ext = os.path.splitext(outfile)
        if ext:
            ext_match = re.match(r"^\.(?P<ext>[A-Za-z]+)$", ext)
            if ext_match:
                outfileext = ext_match.group('ext').upper()
            else:
                outfileext = None
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match(r"^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                outfileext = custom_match.group('ext').upper()
            else:
                outfileext = None

        # Default to "SVG" if no valid extension was found
        if not outfileext:
            outfileext = "SVG"

        # Check if extension is supported
        if outfileext not in svgwrite_valid_extensions:
            outfileext = "SVG"

        return (outfile, outfileext)

    # Handle tuple or list types
    if isinstance(outfile, (tuple, list)):
        if len(outfile) != 2:
            return False

        filename, ext = outfile

        # Allow file objects as the first item in tuple
        if isinstance(filename, file) or isinstance(filename, IOBase):
            filename = filename
        elif isinstance(filename, str):
            filename = filename.strip()
        else:
            return False

        # Ensure the extension is a valid string
        if not isinstance(ext, str):
            return False

        ext = ext.strip().upper()
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
    upc_img = drawsvg.Drawing(sizex, sizey)  # y-axis matches SVG coordinate system in drawsvg 2.x
    drawColorRectangle(upc_img, 0, 0, sizex, sizey, bgcolor)
    return [upc_img, None]


def drawColorRectangleAlt(dwg, x1, y1, x2, y2, color):
    """
    Draws a rectangle with only an outline (no fill) from (x1, y1) to (x2, y2).
    """
    width_rect = x2 - x1
    height_rect = y2 - y1
    color = _rgb_to_svg(color)

    rect = drawsvg.Rectangle(
        x1, y1, width_rect, height_rect,
        fill='none',
        stroke=color,
        stroke_width=1
    )
    dwg.append(rect)
    return True


def drawColorRectangle(dwg, x1, y1, x2, y2, color):
    """
    Draws a filled rectangle from (x1, y1) to (x2, y2).
    """
    width_rect = x2 - x1
    height_rect = y2 - y1
    color = _rgb_to_svg(color)

    rect = drawsvg.Rectangle(
        x1, y1, width_rect, height_rect,
        fill=color,
        stroke='none'
    )
    dwg.append(rect)
    return True


def drawColorLine(dwg, x1, y1, x2, y2, width, color):
    """
    Draws a line from (x1, y1) to (x2, y2) with the specified width and color.
    """
    width = max(1, int(width))
    color = _rgb_to_svg(color)

    line = drawsvg.Line(
        x1, y1, x2, y2,
        stroke=color,
        stroke_width=width
    )
    dwg.append(line)
    return True


def drawColorText(dwg, size, x, y, text, color, ftype="ocrb"):
    """
    Draws text at (x, y) with the specified size, color, and font type.
    """
    color = _rgb_to_svg(color)

    if ftype.lower() == "ocrb":
        font_family = "OCRB"
    elif ftype.lower() == "ocra":
        font_family = "OCR-A"
    else:
        font_family = "Monospace"

    t = drawsvg.Text(
        text,
        size,
        x, y,
        fill=color,
        font_family=font_family
    )
    dwg.append(t)
    return True


def embed_font(dwg, font_path, font_family):
    """
    Embeds a custom font into the SVG via an @font-face style block,
    but only once per drawing (safe to call many times).
    """
    import os
    import base64
    import drawsvg

    # ---- per-drawing cache ----
    cache = getattr(dwg, "_embedded_fonts", None)
    if cache is None:
        cache = set()
        setattr(dwg, "_embedded_fonts", cache)

    key = (os.path.abspath(font_path), str(font_family))
    if key in cache:
        return
    cache.add(key)

    # ---- read font file ----
    with open(font_path, 'rb') as f:
        font_data = f.read()

    # ---- base64 encode ----
    font_base64 = base64.b64encode(font_data)
    if not isinstance(font_base64, str):
        font_base64 = font_base64.decode('ascii')

    # ---- determine format ----
    ext = os.path.splitext(font_path)[1].lower()
    if ext == '.ttf':
        font_format = 'truetype'
        mime = 'font/ttf'
    elif ext == '.otf':
        font_format = 'opentype'
        mime = 'font/otf'
    else:
        raise ValueError("Unsupported font format: %s" % ext)

    # ---- build CSS (NOTE: braces are literal, no .format() here) ----
    font_face_css = (
        '<style type="text/css"><![CDATA[\n'
        '@font-face {\n'
        "  font-family: '%(family)s';\n"
        "  src: url(data:%(mime)s;base64,%(b64)s) format('%(fmt)s');\n"
        '  font-weight: normal;\n'
        '  font-style: normal;\n'
        '}\n'
        ']]></style>\n'
    ) % {
        'family': font_family,
        'mime': mime,
        'b64': font_base64,
        'fmt': font_format,
    }

    raw = drawsvg.Raw(font_face_css)

    # ---- attach to defs (best-effort across drawsvg versions) ----
    if hasattr(dwg, 'append_def'):
        dwg.append_def(raw)
        return
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
    while preserving the original script’s behaviors for:
      - outfile "-" => return bytes/text
      - ftp/ftps/sftp upload
      - file-like objects
    """
    upc_img = inimage[0]
    uploadfile = None
    outfiletovar = False

    # Handle upload targets and stdout-to-variable targets
    if re.findall(r"^(ftp|ftps|sftp):\/\/", str(outfile)):
        uploadfile = outfile
        outfile = BytesIO() if cairosvgsupport else StringIO()
    elif outfile == "-":
        outfiletovar = True
        outfile = BytesIO() if cairosvgsupport else StringIO()

    svg_text = _drawing_to_svg_text(upc_img)

    def _write_svg_to_filelike(fobj):
        # If binary stream, write bytes
        try:
            if isinstance(fobj, (BytesIO,)) or 'b' in getattr(fobj, 'mode', 'b'):
                fobj.write(svg_text.encode('utf-8'))
            else:
                fobj.write(svg_text)
        except TypeError:
            # If it refuses str, try bytes
            fobj.write(svg_text.encode('utf-8'))

    # If outfile is file-like
    if isinstance(outfile, file) or isinstance(outfile, IOBase):
        if cairosvgsupport and outfileext in {"PNG", "PDF", "PS", "EPS", "SVG"}:
            # CairoSVG wants bytes file_obj
            byte_buffer = BytesIO(svg_text.encode("utf-8"))
            byte_buffer.seek(0, 0)

            if outfileext == "PNG":
                cairosvg.svg2png(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "PDF":
                cairosvg.svg2pdf(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "PS":
                cairosvg.svg2ps(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "EPS":
                cairosvg.svg2eps(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "SVG":
                cairosvg.svg2svg(file_obj=byte_buffer, write_to=outfile)

            byte_buffer.close()
        else:
            # Plain SVG only
            _write_svg_to_filelike(outfile)
    else:
        # outfile is a filename/path string
        if cairosvgsupport and outfileext in {"PNG", "PDF", "PS", "EPS", "SVG"}:
            byte_buffer = BytesIO(svg_text.encode("utf-8"))
            byte_buffer.seek(0, 0)

            if outfileext == "PNG":
                cairosvg.svg2png(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "PDF":
                cairosvg.svg2pdf(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "PS":
                cairosvg.svg2ps(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "EPS":
                cairosvg.svg2eps(file_obj=byte_buffer, write_to=outfile)
            elif outfileext == "SVG":
                cairosvg.svg2svg(file_obj=byte_buffer, write_to=outfile)

            byte_buffer.close()
        else:
            # Save SVG directly
            if hasattr(upc_img, 'save_svg'):
                upc_img.save_svg(outfile)
            else:
                with open(outfile, 'w', encoding='utf-8') as f:
                    f.write(svg_text)

    # Upload to internet file if needed
    if re.findall(r"^(ftp|ftps|sftp):\/\/", str(uploadfile)):
        if cairosvgsupport:
            # outfile is BytesIO from above conversions or SVG bytes; ensure pointer reset
            try:
                outfile.seek(0, 0)
                upload_file_to_internet_file(outfile, uploadfile)
                outfile.close()
            except Exception:
                # fallback: re-encode from svg_text
                byte_buffer = BytesIO(svg_text.encode("utf-8"))
                byte_buffer.seek(0, 0)
                upload_file_to_internet_file(byte_buffer, uploadfile)
                byte_buffer.close()
        else:
            outfile.seek(0, 0)
            byte_buffer = BytesIO(outfile.getvalue().encode("utf-8"))
            outfile.close()
            byte_buffer.seek(0, 0)
            upload_file_to_internet_file(byte_buffer, uploadfile)
            byte_buffer.close()

    # Return-to-variable behavior ("-")
    elif outfiletovar:
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    return True


def save_to_filename(imgout, outfile, imgcomment="barcode"):
    upc_img = imgout[0]
    upc_preimg = imgout[1]

    if outfile is None:
        oldoutfile = None
        outfile = None
        outfileext = None
    else:
        oldoutfile = get_save_filename(outfile)
        if isinstance(oldoutfile, (tuple, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]

    if oldoutfile is None or isinstance(oldoutfile, bool):
        return [upc_img, upc_preimg, "drawsvg"]

    save_to_file(imgout, outfile, outfileext, imgcomment)
    return True
