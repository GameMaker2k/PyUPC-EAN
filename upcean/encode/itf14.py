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

    $FileInfo: itf14.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
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

def encode_itf14_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    threewidebar = True
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(len(upc) % 2):
        return False
    if(len(upc) < 6):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwrite and imageoutlib == "svgwrite")):
        pil_addon_fix = 0
        cairo_addon_fix = (8 * (int(resize) * barwidth[1]))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    cairo_addon_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], (((44 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (15 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'barsize': [], 'code': []}
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
    upc_array['code'].append(start_barcode)
    LineStart = shiftxy[0]
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 0
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        LineStart += barwidth[0] * int(resize)
        barsizeloop.append(LineSizeType)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    barsizeloop = []
    LineSizeType = 0
    subcode = []
    while (NumZero < len(upc_matches)):
        ArrayDigit = list(upc_matches[NumZero])
        left_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[0]) == 0):
            left_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[0]) == 1):
            left_barcolor = [1, 0, 0, 0, 1]
        if(int(ArrayDigit[0]) == 2):
            left_barcolor = [0, 1, 0, 0, 1]
        if(int(ArrayDigit[0]) == 3):
            left_barcolor = [1, 1, 0, 0, 0]
        if(int(ArrayDigit[0]) == 4):
            left_barcolor = [0, 0, 1, 0, 1]
        if(int(ArrayDigit[0]) == 5):
            left_barcolor = [1, 0, 1, 0, 0]
        if(int(ArrayDigit[0]) == 6):
            left_barcolor = [0, 1, 1, 0, 0]
        if(int(ArrayDigit[0]) == 7):
            left_barcolor = [0, 0, 0, 1, 1]
        if(int(ArrayDigit[0]) == 8):
            left_barcolor = [1, 0, 0, 1, 0]
        if(int(ArrayDigit[0]) == 9):
            left_barcolor = [0, 1, 0, 1, 0]
        right_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[1]) == 0):
            right_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[1]) == 1):
            right_barcolor = [1, 0, 0, 0, 1]
        if(int(ArrayDigit[1]) == 2):
            right_barcolor = [0, 1, 0, 0, 1]
        if(int(ArrayDigit[1]) == 3):
            right_barcolor = [1, 1, 0, 0, 0]
        if(int(ArrayDigit[1]) == 4):
            right_barcolor = [0, 0, 1, 0, 1]
        if(int(ArrayDigit[1]) == 5):
            right_barcolor = [1, 0, 1, 0, 0]
        if(int(ArrayDigit[1]) == 6):
            right_barcolor = [0, 1, 1, 0, 0]
        if(int(ArrayDigit[1]) == 7):
            right_barcolor = [0, 0, 0, 1, 1]
        if(int(ArrayDigit[1]) == 8):
            right_barcolor = [1, 0, 0, 1, 0]
        if(int(ArrayDigit[1]) == 9):
            right_barcolor = [0, 1, 0, 1, 0]
        InnerUPCNum = 0
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(1)
                BarNum += 1
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(1)
                BarNum += 1
                if(threewidebar):
                    drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                                  LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                    LineStart += barwidth[0] * int(resize)
                    barsizeloop.append(LineSizeType)
                    subcode.append(1)
                    BarNum += 1
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(1)
                BarNum += 1
            if(right_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(0)
                BarNum += 1
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(0)
                BarNum += 1
                if(threewidebar):
                    drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                                  LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                    LineStart += barwidth[0] * int(resize)
                    barsizeloop.append(LineSizeType)
                    subcode.append(0)
                    BarNum += 1
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                barsizeloop.append(LineSizeType)
                subcode.append(0)
                BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    upc_array['code'].append(subcode)
    upc_array['barsize'].append(barsizeloop)
    if(threewidebar):
        end_barcode = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        end_barcode = [1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(end_barcode)
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    barsizeloop = []
    LineSizeType = 0
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        end_bc_num += 1
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    RectAltLoop = 4 * resize
    RectAltLoopSpin = 1
    while(RectAltLoopSpin <= RectAltLoop):
        RectAltLoopSpinAlt = RectAltLoopSpin + 10
        RectAltLoopSpinDown = RectAltLoopSpin - 1
        drawColorRectangleAlt(upc_img, RectAltLoopSpinDown + shiftxy[0], RectAltLoopSpinDown + shiftxy[1], ((
        ((44 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize)) - RectAltLoopSpin, ((barheight[0] + ((15 + shiftxy[1]) * barwidth[0])) - RectAltLoopSpinAlt), barcolor[0], imageoutlib)
        RectAltLoopSpin += 1
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
        NumTxtZero = 0
        LineTxtStart = 23
        if(not threewidebar):
            LineTxtStart -= 2
        while (NumTxtZero < len(upc_matches)):
            ArrayDigit = list(upc_matches[NumTxtZero])
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (24 * (int(resize) - 1))) * barwidth[0], (barheight[0] + (4 * (int(
                resize))) + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), ArrayDigit[0], barcolor[1], "ocrb", imageoutlib)
            if(threewidebar):
                LineTxtStart += 9 * int(resize)
            else:
                LineTxtStart += 7 * int(resize)
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (24 * (int(resize) - 1))) * barwidth[0], (barheight[0] + (4 * (int(
                resize))) + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), ArrayDigit[1], barcolor[1], "ocrb", imageoutlib)
            if(threewidebar):
                LineTxtStart += 9 * int(resize)
            else:
                LineTxtStart += 7 * int(resize)
            NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    return [upc_img, upc_preimg, imageoutlib, upc_array]


def draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    threewidebar = True
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((44 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[1])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(((44 * barwidth[0]) + upc_size_add) * int(resize)), float((barheightadd + (15 * barwidth[1])) * int(resize))))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(((44 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[1])) * int(resize)))
        upc_preimg.close()
    imgout = encode_itf14_barcode((upc_img, upc_preimg), upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, imgout[3]]

def create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
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
    imgout = draw_itf14_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': "itf14; "+upc}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib, imgout[3]]
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
                info.add_text("Comment", "itf14; "+upc)
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': "itf14; "+upc}
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

def encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
 return encode_itf14_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)

def draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
 return draw_itf14_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)

def create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    return create_itf14_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
