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

    $FileInfo: code32.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.encode.predraw import *
import re
import sys
import upcean.support
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
    import upcean.encode.prepil
if(cairosupport):
    import upcean.encode.precairo
if(svgwritesupport):
    import upcean.encode.presvg

def encode_code32_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    imageoutlib = imageoutlib.lower()
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
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    if(len(upc) < 1):
        return False
    if(not re.findall("([0-9a-zB-DF-HJ-NP-Z\\-\\.\\$\\/\\+% ]+)", upc)):
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
    upc = upc.upper()
    upc_matches = list(upc)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], (((50 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'code': []}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                     0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    LineStart = shiftxy[0]
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    NumZero = 0
    while (NumZero < len(upc_matches)):
        left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "0"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "1"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "2"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "3"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "4"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "5"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "6"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "7"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "8"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "9"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "B"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "C"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "D"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "F"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "G"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "H"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "J"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "K"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "L"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "M"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "N"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "P"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "Q"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "R"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "S"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "T"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "U"):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "V"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "W"):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "X"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "Y"):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "Z"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
        InnerUPCNum = 0
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
            InnerUPCNum += 1
        drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize,
                      barwidth[0], barcolor[2], imageoutlib)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
        NumZero += 1
    end_barcode = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0,
                   1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    if(not hidetext):
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((14 + shiftxy[1]) * int(resize)) * barwidth[0], cairo_addon_fix + (barheight[0] + (
            barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), "A", barcolor[1], "ocrb", imageoutlib)
        NumTxtZero = 0
        LineTxtStart = 30 * int(resize)
        while (NumTxtZero < len(upc_matches)):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (int(resize) - 1)) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), upc_matches[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
            LineTxtStart += 16 * int(resize)
            NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    return [upc_img, upc_preimg, {'inimage': inimage, 'upc': upc, 'resize': resize, 'shiftxy': shiftxy, 'barheight': barheight, 'barwidth': barwidth, 'barcolor': barcolor, 'hideinfo': hideinfo, 'imageoutlib': imageoutlib}, upc_array]


def draw_code32_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    upc_matc = upc.upper()
    upc_matches = list(upc_matc)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(((50 * barwidth[0]) + upc_size_add) * int(resize)), float((barheightadd + (9 * barwidth[1])) * int(resize))))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
    imgout = encode_code32_barcode((upc_img, upc_preimg), upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, {'upc': upc, 'resize': resize, 'barheight': barheight, 'barwidth': barwidth, 'barcolor': barcolor, 'hideinfo': hideinfo, 'imageoutlib': imageoutlib}, imgout[3]]

def create_code32_barcode(upc, outfile="./code32.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    imgout = draw_code32_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': upc}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, {'upc': upc, 'outfile': outfile, 'resize': resize, 'barheight': barheight, 'barwidth': barwidth, 'barcolor': barcolor, 'hideinfo': hideinfo, 'imageoutlib': imageoutlib}, imgout[3]]
    else:
        if(outfileext == "WEBP"):
            exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 95, 'optimize': True, 'progressive': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9})
        else:
            exargdict = {'comment': upc}
        try:
            if(svgwritesupport and imageoutlib == "svgwrite"):
                    upc_preimg.close()
                    upc_img.saveas(outfile, True)
            if(pilsupport and imageoutlib == "pillow"):
                if(outfileext == "XBM"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.get_data().tobytes())
                elif(outfileext == "XPM"):
                    upc_preimg.convert(mode="P").save(
                        outfile, outfileext, **exargdict)
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
        except Exception as e:
            return False
    return True
