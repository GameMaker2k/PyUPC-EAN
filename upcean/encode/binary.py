# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: binary.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.encode.predraw import *
import re
import sys
import upcean.support
try:
    file
except NameError:
    from io import IOBase as file
try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO
import upcean.encode.ean2
import upcean.encode.ean5
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
svgwritesupport = upcean.support.check_for_svgwrite()
if(pilsupport or pillowsupport):
    import upcean.encode.predraw.prepil
    from PIL import PngImagePlugin
if(cairosupport):
    import upcean.encode.predraw.precairo
if(svgwritesupport):
    import upcean.encode.predraw.presvgwrite


def get_binary_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    upc_size_add_wo_shift = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    upc_size_add_w_shift = (len([item for sublist in upc['code'] for item in sublist]) + shiftxy[0]) * (barwidth[0] * int(resize))
    reswoshift = (upc_size_add_wo_shift, (barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize))
    reswshift = (upc_size_add_w_shift, ((barheightadd + shiftxy[1]) + ((upc['heightadd'] + shiftxy[1]) * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_binary_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(inimage is None):
        upc_img = None
        upc_preimg = None
    else:
        upc_img = inimage[0]
        upc_preimg = inimage[1]
    imageoutlib = None
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and inimage != "none" and inimage is not None):
        imageoutlib = None
    elif(inimage == "none" or inimage is None):
        imageoutlib = None
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwrite and imageoutlib == "svgwrite")):
        pil_addon_fix = 0
        cairo_addon_fix = (9 * (int(resize) * barwidth[1]))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    cairo_addon_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_size_add = (len([item for sublist in upc['code'] for item in sublist]) + shiftxy[0]) * (barwidth[0] * int(resize))
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], upc_size_add, ((barheightadd + shiftxy[1]) + ((upc['heightadd'] + shiftxy[1]) * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    bari = 0
    barmax = len(upc['code'])
    LineStart = shiftxy[0]
    while(bari < barmax):
        subbari = 0
        subbarmax = len(upc['code'][bari])
        while(subbari < subbarmax):
            if(hidetext):
                LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            else:
                LineSizeNum = upc['barsize'][bari][subbari]
                LineSize = (barheight[LineSizeNum] + shiftxy[1]) * int(resize)
            if(upc['code'][bari][subbari] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            elif(upc['code'][bari][subbari] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            subbari += 1
            LineStart += barwidth[0] * int(resize)
        bari += 1
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
    txtbari = 0
    txtbarmax = len(upc['text']['text'])
    LineStart = shiftxy[0]
    while(txtbari < txtbarmax):
        texthidden = False
        if hidetext or (upc['text']['type'][txtbari] == "sn" and (hidesn is None or hidesn)) or (upc['text']['type'][txtbari] == "cd" and (hidecd is None or hidecd)):
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (shiftxy[0] + (upc['text']['location'][txtbari] * int(resize))) * barwidth[0], cairo_addon_fix + (
            barheight[0] * int(resize)) + pil_addon_fix, upc['text']['text'][txtbari], barcolor[1], "ocrb", imageoutlib)
        txtbari += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc
    else:
        return [upc_img, upc_preimg, imageoutlib]

def draw_binary_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "svgwrite"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "svgwrite"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "svgwrite"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "svgwrite"
    if(not pilsupport and not cairosupport):
        imageoutlib = "svgwrite"
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    upc_size_add = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", ((upc_size_add, (barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize)) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(upc_size_add), float((barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize)) * int(resize)))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(upc_size_add, (barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize)) * int(resize))
        upc_preimg.close()
    imgout = encode_binary_barcode((upc_img, upc_preimg), upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, upc]

def create_binary_barcode(upc, outfile="./binary.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "svgwrite"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "svgwrite"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "svgwrite"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "svgwrite"
    if(not pilsupport and not cairosupport):
        imageoutlib = "svgwrite"
    if(outfile is None):
        if(imageoutlib == "cairosvg"):
            oldoutfile = None
            outfile = None
            outfileext = "SVG"
        else:
            oldoutfile = None
            outfile = None
            outfileext = None
    else:
        oldoutfile = upcean.encode.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    imgout = draw_binary_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': upc['type']+"; "+upc['upc']}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(outfileext == "WEBP"):
            exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
        if(outfileext == "HEIC"):
            exargdict.update({'lossless': True, 'quality': 100})
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 100, 'optimize': True, 'progressive': True})
        elif(outfileext == "GIF"):
            exargdict.update(
                {'optimize': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9, 'quality': 100})
            if(pilsupport):
                # Add a comment to the image
                info = PngImagePlugin.PngInfo()
                info.add_text("Comment", upc['type']+"; "+upc['upc'])
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': upc['type']+"; "+upc['upc']}
        if(svgwritesupport and imageoutlib == "svgwrite"):
                if isinstance(outfile, file):
                    upc_img.write(outfile, True)
                else:
                    upc_img.saveas(outfile, True)
        if(pilsupport and imageoutlib == "pillow"):
            if outfileext == "XPM":
                # XPM supports only palette-based images ("P" mode)
                upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            elif outfileext == "XBM":
                # XBM supports only 1-bit images ("1" mode)
                upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
            elif outfileext == "PBM":
                # PBM (Portable Bitmap) supports only monochrome (1-bit) images ("1" mode)
                upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
            elif outfileext == "PGM":
                # PGM (Portable Graymap) supports only grayscale images ("L" mode)
                upc_preimg.convert(mode="L").save(outfile, outfileext, **exargdict)
            elif outfileext == "GIF":
                # GIF supports only palette-based images with a maximum of 256 colors ("P" mode)
                upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            elif outfileext == "ICO":
                # ICO generally supports "L", "P", and "RGBA" but not direct "RGB".
                # Convert to RGBA for transparency support if available, or "P" otherwise.
                if "A" in upc_preimg.getbands():  # Check if alpha channel is present
                    upc_preimg.convert(mode="RGBA").save(outfile, outfileext, **exargdict)
                else:
                    upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            else:
                # If image is RGBA, convert to RGB to discard transparency; otherwise, save as-is
                if upc_preimg.mode == "RGBA":
                    upc_preimg.convert(mode="RGB").save(outfile, outfileext, **exargdict)
                else:
                    upc_preimg.save(outfile, outfileext, **exargdict)
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            x, y, width, height = upc_preimg.ink_extents()
            if(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                if(outfileext == "SVG" or imageoutlib == "cairosvg"):
                    # Create an ImageSurface with the exact dimensions of the recorded content
                    image_surface = cairo.SVGSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
                elif(outfileext == "PDF"):
                    # Create an ImageSurface with the exact dimensions of the recorded content
                    image_surface = cairo.PDFSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
                elif(outfileext == "PS" or outfileext == "EPS"):
                    # Create an PDFSurface with the exact dimensions of the recorded content
                    image_surface = cairo.PSSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    if(outfileext == "EPS"):
                        image_surface.set_eps(True)
                    else:
                        image_surface.set_eps(False)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
            else:
                # Create an ImageSurface with the exact dimensions of the recorded content
                image_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, int(width), int(height))
                image_context = cairo.Context(image_surface)
                # Transfer the content from the RecordingSurface to the ImageSurface
                image_context.set_source_surface(upc_preimg, -x, -y)
                image_context.paint()
                image_surface.flush()
                # Save as PNG
                image_surface.write_to_png(outfile)
                image_surface.finish()
                return True
    return True
