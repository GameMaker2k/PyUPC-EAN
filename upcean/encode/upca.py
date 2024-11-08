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

    $FileInfo: upca.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
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

def encode_upca_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    upc_pieces = None
    supplement = None
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
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
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
    upc_matches = re.findall("(\\d{1})(\\d{5})(\\d{5})(\\d{1})", upc)
    if(len(upc_matches) <= 0):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(str(upc_matches[0])+str(upc_matches[1]))
    RightDigit = list(str(upc_matches[2])+str(upc_matches[3]))
    CheckDigit = upc_matches[3]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    if(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], (((113 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'barsize': [], 'code': []}
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    LineStart = shiftxy[0]
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 0
    while(BarNum < start_bc_num_end):
        if(BarNum < 9):
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        else:
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    LineSizeType = 0
    while (NumZero < len(LeftDigit)):
        if(NumZero > 0):
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        if(NumZero == 0):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        left_barcolor = [0, 0, 0, 0, 0, 0, 0]
        if(int(LeftDigit[NumZero]) == 0):
            left_barcolor = [0, 0, 0, 1, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 1):
            left_barcolor = [0, 0, 1, 1, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 2):
            left_barcolor = [0, 0, 1, 0, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 3):
            left_barcolor = [0, 1, 1, 1, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 4):
            left_barcolor = [0, 1, 0, 0, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 5):
            left_barcolor = [0, 1, 1, 0, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 6):
            left_barcolor = [0, 1, 0, 1, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 7):
            left_barcolor = [0, 1, 1, 1, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 8):
            left_barcolor = [0, 1, 1, 0, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 9):
            left_barcolor = [0, 0, 0, 1, 0, 1, 1]
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            LineStart += barwidth[0] * int(resize)
            barsizeloop.append(LineSizeType)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    upc_array['code'].append([0, 1, 0, 1, 0])
    mid_barcode = [0, 1, 0, 1, 0]
    mid_bc_num = 0
    mid_bc_num_end = len(mid_barcode)
    LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    LineSizeType = 1
    barsizeloop = []
    while(mid_bc_num < mid_bc_num_end):
        if(mid_barcode[mid_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(mid_barcode[mid_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        mid_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    LineSizeType = 0
    while (NumZero < len(RightDigit)):
        if(NumZero != 5):
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        if(NumZero == 5):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        right_barcolor = [0, 0, 0, 0, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 0):
            right_barcolor = [1, 1, 1, 0, 0, 1, 0]
        if(int(RightDigit[NumZero]) == 1):
            right_barcolor = [1, 1, 0, 0, 1, 1, 0]
        if(int(RightDigit[NumZero]) == 2):
            right_barcolor = [1, 1, 0, 1, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 3):
            right_barcolor = [1, 0, 0, 0, 0, 1, 0]
        if(int(RightDigit[NumZero]) == 4):
            right_barcolor = [1, 0, 1, 1, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 5):
            right_barcolor = [1, 0, 0, 1, 1, 1, 0]
        if(int(RightDigit[NumZero]) == 6):
            right_barcolor = [1, 0, 1, 0, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 7):
            right_barcolor = [1, 0, 0, 0, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 8):
            right_barcolor = [1, 0, 0, 1, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 9):
            right_barcolor = [1, 1, 1, 0, 1, 0, 0]
        upc_array['code'].append(right_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
        while (InnerUPCNum < len(right_barcolor)):
            if(right_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            LineStart += barwidth[0] * int(resize)
            barsizeloop.append(LineSizeType)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    upc_array['code'].append([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    end_barcode = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    LineSizeType = 1
    barsizeloop = []
    while(end_bc_num < end_bc_num_end):
        if(end_bc_num < 4):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        else:
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
        if(hidesn is not None and not hidesn):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((1 + shiftxy[0]) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), upc_matches[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((22 + shiftxy[0]) + (23 * (int(resize) - 1)) - (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((28 + shiftxy[0]) + (28 * (int(resize) - 1)) - (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((34 + shiftxy[0]) + (33 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
            barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((40 + shiftxy[0]) + (38 * (int(resize) - 1)) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((46 + shiftxy[0]) + (43 * (int(resize) - 1)) + (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((61 + shiftxy[0]) + (63 * (int(resize) - 1)) - (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((67 + shiftxy[0]) + (68 * (int(resize) - 1)) - (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((73 + shiftxy[0]) + (73 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
            barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((79 + shiftxy[0]) + (78 * (int(resize) - 1)) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((85 + shiftxy[0]) + (83 * (int(resize) - 1)) + (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[4], barcolor[1], "ocrb", imageoutlib)
        if(hidecd is not None and not hidecd):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((105 + shiftxy[0]) + (104 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), upc_matches[3], barcolor[1], "ocrb", imageoutlib)
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(supplement is not None and len(supplement) == 2):
        supout = upcean.encode.ean2.encode_upc2_barcode((upc_img, upc_preimg), supplement, resize, (((113 + shiftxy[0]) * barwidth[0]) * int(resize), shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
        upc_array['code'] += supout[3]['code']
        upc_array['barsize'] += supout[3]['barsize']
    if(supplement is not None and len(supplement) == 5):
        supout = upcean.encode.ean5.encode_upc5_barcode((upc_img, upc_preimg), supplement, resize, (((113 + shiftxy[0]) * barwidth[0]) * int(resize), shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
        upc_array['code'] += supout[3]['code']
        upc_array['barsize'] += supout[3]['barsize']
    return [upc_img, upc_preimg, imageoutlib, upc_array]


def draw_upca_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    elif(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((113 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(((113 * barwidth[0]) + upc_size_add) * int(resize)), float((barheightadd + (9 * barwidth[1])) * int(resize))))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(((113 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_preimg.close()
    imgout = encode_upca_barcode((upc_img, upc_preimg), fullupc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, imgout[3]]

def create_upca_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    imgout = draw_upca_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': "upca; "+upc}
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
                info.add_text("Comment", "upca; "+upc)
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': "upca; "+upc}
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


def encode_upcaean_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    upc_pieces = None
    supplement = None
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
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
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
    upc_matches = re.findall("(\\d{1})(\\d{5})(\\d{5})(\\d{1})", upc)
    if(len(upc_matches) <= 0):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(str(upc_matches[0])+str(upc_matches[1]))
    RightDigit = list(str(upc_matches[2])+str(upc_matches[3]))
    CheckDigit = upc_matches[3]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    if(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], (((115 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'barsize': [], 'code': []}
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    LineStart = shiftxy[0]
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 1
    while(BarNum < start_bc_num_end):
        if(BarNum < 10):
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        else:
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    LineSizeType = 0
    while (NumZero < len(LeftDigit)):
        LineSize = (barheight[0] + shiftxy[1]) * int(resize)
        LineSizeType = 0
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        left_barcolor = [0, 0, 0, 0, 0, 0, 0]
        if(int(LeftDigit[NumZero]) == 0):
            left_barcolor = [0, 0, 0, 1, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 1):
            left_barcolor = [0, 0, 1, 1, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 2):
            left_barcolor = [0, 0, 1, 0, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 3):
            left_barcolor = [0, 1, 1, 1, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 4):
            left_barcolor = [0, 1, 0, 0, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 5):
            left_barcolor = [0, 1, 1, 0, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 6):
            left_barcolor = [0, 1, 0, 1, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 7):
            left_barcolor = [0, 1, 1, 1, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 8):
            left_barcolor = [0, 1, 1, 0, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 9):
            left_barcolor = [0, 0, 0, 1, 0, 1, 1]
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            barsizeloop.append(LineSizeType)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    upc_array['code'].append([0, 1, 0, 1, 0])
    mid_barcode = [0, 1, 0, 1, 0]
    mid_bc_num = 0
    mid_bc_num_end = len(mid_barcode)
    LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 1
    while(mid_bc_num < mid_bc_num_end):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        if(mid_barcode[mid_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(mid_barcode[mid_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        mid_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    LineSizeType = 0
    while (NumZero < len(RightDigit)):
        if(NumZero != 6):
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        if(NumZero == 6):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
        right_barcolor = [0, 0, 0, 0, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 0):
            right_barcolor = [1, 1, 1, 0, 0, 1, 0]
        if(int(RightDigit[NumZero]) == 1):
            right_barcolor = [1, 1, 0, 0, 1, 1, 0]
        if(int(RightDigit[NumZero]) == 2):
            right_barcolor = [1, 1, 0, 1, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 3):
            right_barcolor = [1, 0, 0, 0, 0, 1, 0]
        if(int(RightDigit[NumZero]) == 4):
            right_barcolor = [1, 0, 1, 1, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 5):
            right_barcolor = [1, 0, 0, 1, 1, 1, 0]
        if(int(RightDigit[NumZero]) == 6):
            right_barcolor = [1, 0, 1, 0, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 7):
            right_barcolor = [1, 0, 0, 0, 1, 0, 0]
        if(int(RightDigit[NumZero]) == 8):
            right_barcolor = [1, 0, 0, 1, 0, 0, 0]
        if(int(RightDigit[NumZero]) == 9):
            right_barcolor = [1, 1, 1, 0, 1, 0, 0]
        upc_array['code'].append(right_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
        while (InnerUPCNum < len(right_barcolor)):
            if(right_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            LineStart += barwidth[0] * int(resize)
            barsizeloop.append(LineSizeType)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    upc_array['code'].append([1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    end_barcode = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 1
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.encode.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
        if(hidesn is not None and not hidesn):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((2 + shiftxy[0]) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), "0", barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((17 + shiftxy[0]) + (20 * (int(resize) - 1)) - (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), upc_matches[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((23 + shiftxy[0]) + (25 * (int(resize) - 1)) - (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((29 + shiftxy[0]) + (30 * (int(resize) - 1)) - (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((35 + shiftxy[0]) + (35 * (int(resize) - 1)) + (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((41 + shiftxy[0]) + (40 * (int(resize) - 1)) + (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((47 + shiftxy[0]) + (45 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[1])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((63 + shiftxy[0]) + (65 * (int(resize) - 1)) - (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((69 + shiftxy[0]) + (70 * (int(resize) - 1)) - (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((75 + shiftxy[0]) + (75 * (int(resize) - 1)) - (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((81 + shiftxy[0]) + (80 * (int(resize) - 1)) + (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((87 + shiftxy[0]) + (85 * (int(resize) - 1)) + (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), list(upc_matches[2])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((93 + shiftxy[0]) + (90 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), upc_matches[3], barcolor[1], "ocrb", imageoutlib)
        if(hidecd is not None and not hidecd):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), ((107 + shiftxy[0]) + (103 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
                barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + int(resize), ">", barcolor[1], "ocrb", imageoutlib)
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(supplement is not None and len(supplement) == 2):
        upcean.encode.ean2.encode_upc2_barcode((upc_img, upc_preimg), supplement, resize, (((115 + shiftxy[0]) * barwidth[0]) * int(resize), shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
    if(supplement is not None and len(supplement) == 5):
        upcean.encode.ean5.encode_upc5_barcode((upc_img, upc_preimg), supplement, resize, (((115 + shiftxy[0]) * barwidth[0]) * int(resize), shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, upc_array]


def draw_upcaean_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    elif(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((115 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(((115 * barwidth[0]) + upc_size_add) * int(resize)), float((barheightadd + (9 * barwidth[1])) * int(resize))))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(((115 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_preimg.close()
    imgout = encode_upcaean_barcode((upc_img, upc_preimg), fullupc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, imgout[3]]

def create_upcaean_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
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
    imgout = draw_upcaean_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': "upca; "+upc}
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
                info.add_text("Comment", "upca; "+upc)
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': "upca; "+upc}
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

