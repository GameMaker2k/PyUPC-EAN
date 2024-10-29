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

    $FileInfo: ean13.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
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
import upcean.encode.ean2
import upcean.encode.ean5
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
if(pilsupport or pillowsupport):
    import upcean.encode.prepil
if(cairosupport):
    import upcean.encode.precairo


def create_ean13_barcode(upc, outfile="./ean13.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
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
    upc_pieces = None
    supplement = None
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
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        try:
            pil_ver = Image.PILLOW_VERSION
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
            pil_is_pillow = True
        except AttributeError:
            try:
                pil_ver = Image.VERSION
                pil_is_pillow = False
            except AttributeError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            except NameError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
        except NameError:
            try:
                pil_ver = Image.VERSION
                pil_is_pillow = False
            except AttributeError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            except NameError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
        pil_addon_fix = 0
        cairo_addon_fix = 0
        pil_prevercheck = [str(x) for x in pil_ver]
        pil_vercheck = int(
            pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2])
        if(pil_is_pillow and pil_vercheck >= 210 and pil_vercheck < 220):
            pil_addon_fix = int(resize) * 2
            cairo_addon_fix = 0
    elif(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        pil_addon_fix = 0
        cairo_addon_fix = 8
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    upc_matches = re.findall("(\\d{1})(\\d{6})(\\d{6})", upc)
    if(len(upc_matches) <= 0):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(upc_matches[1])
    RightDigit = list(upc_matches[2])
    addonsize = 0
    if(supplement is not None and len(supplement) == 2):
        addonsize = 29 * barwidth[0]
    if(supplement is not None and len(supplement) == 5):
        addonsize = 56 * barwidth[0]
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
        upc_img.rectangle([(0, 0), (((115 * barwidth[0]) + addonsize) * int(resize),
                          (barheightadd + (9 * barwidth[1])) * int(resize))], fill=barcolor[2])
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(outfileext == "SVG"):
            upc_preimg = cairo.SVGSurface(
                None, ((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        elif(outfileext == "PDF"):
            upc_preimg = cairo.PDFSurface(
                None, ((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        elif(outfileext == "PS" or outfileext == "EPS"):
            upc_preimg = cairo.PSSurface(
                None, ((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
            if(outfileext == "EPS"):
                upc_preimg.set_eps(True)
            else:
                upc_preimg.set_eps(False)
        else:
            upc_preimg = cairo.ImageSurface(
                cairo.FORMAT_RGB24, ((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
        upc_img.rectangle(
            0, 0, ((115 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2])
        upc_img.fill()
    upc_array = {'upc': upc, 'code': []}
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    upc_array['code'].append([1, 0, 1])
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    LineStart = 0
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = barheight[1] * int(resize)
    while(BarNum < start_bc_num_end):
        if(BarNum < 10):
            LineSize = barheight[0] * int(resize)
        else:
            LineSize = barheight[1] * int(resize)
        if(hidetext):
            LineSize = barheight[1] * int(resize)
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    NumZero = 0
    while (NumZero < len(LeftDigit)):
        LineSize = barheight[0] * int(resize)
        if(hidetext):
            LineSize = barheight[1] * int(resize)
        left_barcolor_l = [0, 0, 0, 0, 0, 0, 0]
        left_barcolor_g = [1, 1, 1, 1, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 0):
            left_barcolor_l = [0, 0, 0, 1, 1, 0, 1]
            left_barcolor_g = [0, 1, 0, 0, 1, 1, 1]
        if(int(LeftDigit[NumZero]) == 1):
            left_barcolor_l = [0, 0, 1, 1, 0, 0, 1]
            left_barcolor_g = [0, 1, 1, 0, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 2):
            left_barcolor_l = [0, 0, 1, 0, 0, 1, 1]
            left_barcolor_g = [0, 0, 1, 1, 0, 1, 1]
        if(int(LeftDigit[NumZero]) == 3):
            left_barcolor_l = [0, 1, 1, 1, 1, 0, 1]
            left_barcolor_g = [0, 1, 0, 0, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 4):
            left_barcolor_l = [0, 1, 0, 0, 0, 1, 1]
            left_barcolor_g = [0, 0, 1, 1, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 5):
            left_barcolor_l = [0, 1, 1, 0, 0, 0, 1]
            left_barcolor_g = [0, 1, 1, 1, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 6):
            left_barcolor_l = [0, 1, 0, 1, 1, 1, 1]
            left_barcolor_g = [0, 0, 0, 0, 1, 0, 1]
        if(int(LeftDigit[NumZero]) == 7):
            left_barcolor_l = [0, 1, 1, 1, 0, 1, 1]
            left_barcolor_g = [0, 0, 1, 0, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 8):
            left_barcolor_l = [0, 1, 1, 0, 1, 1, 1]
            left_barcolor_g = [0, 0, 0, 1, 0, 0, 1]
        if(int(LeftDigit[NumZero]) == 9):
            left_barcolor_l = [0, 0, 0, 1, 0, 1, 1]
            left_barcolor_g = [0, 0, 1, 0, 1, 1, 1]
        left_barcolor = left_barcolor_l
        if(int(upc_matches[0]) == 1):
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 4):
                left_barcolor = left_barcolor_g
            if(NumZero == 5):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 2):
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 3):
                left_barcolor = left_barcolor_g
            if(NumZero == 5):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 3):
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 3):
                left_barcolor = left_barcolor_g
            if(NumZero == 4):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 4):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 4):
                left_barcolor = left_barcolor_g
            if(NumZero == 5):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 5):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 5):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 6):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 3):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 7):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 3):
                left_barcolor = left_barcolor_g
            if(NumZero == 5):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 8):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 3):
                left_barcolor = left_barcolor_g
            if(NumZero == 4):
                left_barcolor = left_barcolor_g
        if(int(upc_matches[0]) == 9):
            if(NumZero == 1):
                left_barcolor = left_barcolor_g
            if(NumZero == 2):
                left_barcolor = left_barcolor_g
            if(NumZero == 4):
                left_barcolor = left_barcolor_g
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    upc_array['code'].append([0, 1, 0, 1, 0])
    mid_barcode = [0, 1, 0, 1, 0]
    mid_bc_num = 0
    mid_bc_num_end = len(mid_barcode)
    LineSize = barheight[1] * int(resize)
    while(mid_bc_num < mid_bc_num_end):
        if(mid_bc_num < 4):
            LineSize = barheight[1] * int(resize)
        else:
            LineSize = barheight[0] * int(resize)
        if(hidetext):
            LineSize = barheight[1] * int(resize)
        if(mid_barcode[mid_bc_num] == 1):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(mid_barcode[mid_bc_num] == 0):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        mid_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    NumZero = 0
    while (NumZero < len(RightDigit)):
        LineSize = barheight[0] * int(resize)
        if(hidetext):
            LineSize = barheight[1] * int(resize)
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
        while (InnerUPCNum < len(right_barcolor)):
            if(right_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    upc_array['code'].append([1, 0, 1])
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    end_barcode = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    LineSize = barheight[1] * int(resize)
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, 10 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    if(not hidetext):
        if(hidesn is not None and not hidesn):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (2 + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[0] * int(resize)), upc_matches[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (17 + (20 * (int(resize) - 1)) - (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (23 + (25 * (int(resize) - 1)) - (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (29 + (30 * (int(resize) - 1)) - (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (35 + (35 * (int(resize) - 1)) + (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (41 + (40 * (int(resize) - 1)) + (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (47 + (45 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[5], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (63 + (65 * (int(resize) - 1)) - (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (69 + (70 * (int(resize) - 1)) - (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (75 + (75 * (int(resize) - 1)) - (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (81 + (80 * (int(resize) - 1)) + (1 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (87 + (85 * (int(resize) - 1)) + (3 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (93 + (90 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[5], barcolor[1], "ocrb", imageoutlib)
        if(hidecd is not None and not hidecd):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (107 + (103 * (int(resize) - 1)) + (5 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
                barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[0] * int(resize)), ">", barcolor[1], "ocrb", imageoutlib)
    if(supplement is not None and len(supplement) == 2):
        upcean.encode.ean2.create_ean2sup_barcode(
            supplement, upc_img, (115 * barwidth[0]) * int(resize), resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
    if(supplement is not None and len(supplement) == 5):
        upcean.encode.ean5.create_ean5sup_barcode(
            supplement, upc_img, (115 * barwidth[0]) * int(resize), resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(supplement != None and len(supplement) == 2):
            upc_sup_img = upcean.encode.ean2.draw_ean2sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            upc_img.set_source_surface(
                upc_sup_img, (115 * barwidth[0]) * int(resize), 0)
            upc_img.paint()
            del(upc_sup_img)
        if(supplement != None and len(supplement) == 5):
            upc_sup_img = upcean.encode.ean5.draw_ean5sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            upc_img.set_source_surface(
                upc_sup_img, (115 * barwidth[0]) * int(resize), 0)
            upc_img.paint()
            del(upc_sup_img)
    exargdict = {}
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS"):
            if(outfile is None):
                imgoutfile = None
            else:
                if(sys.version[0] == "2"):
                    imgoutfile = StringIO()
                if(sys.version[0] >= "3"):
                    imgoutfile = BytesIO()
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        if(pilsupport and imageoutlib == "pillow"):
            return upc_preimg
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            return upc_preimg
    if(sys.version[0] == "2"):
        if(outfile == "-" or outfile == "" or outfile == " " or outfile is None):
            stdoutfile = StringIO()
            if(outfileext == "WEBP"):
                exargdict.update(
                    {'lossless': True, 'quality': 100, 'method': 6})
            elif(outfileext == "JPEG"):
                exargdict.update(
                    {'quality': 95, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {}
            try:
                if(pilsupport and imageoutlib == "pillow"):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            upc_preimg.convert(mode="1").tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        upc_preimg.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        upc_preimg.flush()
                        upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.write_to_png(stdoutfile)
                        stdoutfile.seek(0)
                        return stdoutfile
            except:
                return False
    if(sys.version[0] >= "3"):
        stdoutfile = BytesIO()
        if(outfile == "-" or outfile == "" or outfile == " " or outfile is None):
            if(outfileext == "WEBP"):
                exargdict.update(
                    {'lossless': True, 'quality': 100, 'method': 6})
            elif(outfileext == "JPEG"):
                exargdict.update(
                    {'quality': 95, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {}
            try:
                if(pilsupport and imageoutlib == "pillow"):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            upc_preimg.convert(mode='1').tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        upc_preimg.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        upc_preimg.flush()
                        upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.write_to_png(stdoutfile)
                        stdoutfile.seek(0)
                        return stdoutfile
            except:
                return False
    if(outfile != "-" and outfile != "" and outfile != " "):
        if(outfileext == "WEBP"):
            exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 95, 'optimize': True, 'progressive': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9})
        else:
            exargdict = {}
        try:
            if(pilsupport and imageoutlib == "pillow"):
                if(outfileext == "BYTES"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.tobytes())
                elif(outfileext == "XBM"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.get_data().tobytes())
                elif(outfileext == "XPM"):
                    upc_preimg.convert(mode="P").save(
                        outfile, outfileext, **exargdict)
                else:
                    upc_preimg.save(outfile, outfileext, **exargdict)
            if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                if(outfileext == "BYTES"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.get_data().tobytes())
                    return True
                elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                    upc_preimg.flush()
                    upc_preimg.finish()
                    imgoutfile.seek(0)
                    svgouttext = imgoutfile.read()
                    with open(outfile, 'wb+') as f:
                        f.write(svgouttext)
                    return True
                else:
                    upc_preimg.write_to_png(outfile)
                    return True
        except:
            return False
    return True


def create_gtin13_barcode(upc, outfile="./gtin13.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_barcode(upc, outfile, resize, hideinfo, barheight, textxy, barcolor, imageoutlib)


def create_ucc13_barcode(upc, outfile="./ucc13.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_barcode(upc, outfile, resize, hideinfo, barheight, textxy, barcolor, imageoutlib)


def create_ean13_from_upca_barcode(upc, outfile="./upca.png", resize=1, hideinfo=(True, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    if(len(upc) > 13 or len(upc) < 12):
        return False
    if(len(upc) < 13):
        upc = "0"+str(upc)
    return create_ean13_barcode(upc, outfile, resize, hideinfo, barheight, textxy, barcolor, imageoutlib)


def draw_ean13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_gtin13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_gtin13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_ucc13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ucc13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_ean13_from_upca_barcode(upc, resize=1, hideinfo=(True, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_from_upca_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_ean13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_gtin13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_gtin13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_ucc13_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ucc13_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_ean13_from_upca_barcode(upc, resize=1, hideinfo=(True, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean13_from_upca_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
