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

    $FileInfo: upca.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
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


def create_upca_barcode(upc, outfile="./upca.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
    if(len(upc) > 12 or len(upc) < 12):
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
        cairo_addon_fix = (8 * (int(resize)))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    upc_matches = re.findall("(\\d{1})(\\d{5})(\\d{5})(\\d{1})", upc)
    if(len(upc_matches) <= 0):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(str(upc_matches[0])+str(upc_matches[1]))
    RightDigit = list(str(upc_matches[2])+str(upc_matches[3]))
    CheckDigit = upc_matches[3]
    addonsize = 0
    if(supplement is not None and len(supplement) == 2):
        addonsize = 29 * barwidth[0]
    if(supplement is not None and len(supplement) == 5):
        addonsize = 56 * barwidth[0]
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", ((113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1])))
        upc_img = ImageDraw.Draw(upc_preimg)
        upc_img.rectangle([(0, 0), ((113 * barwidth[0]) + addonsize,
                          barheightadd + (9 * barwidth[1]))], fill=barcolor[2])
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(outfileext == "SVG"):
            upc_preimg = cairo.SVGSurface(
                None, (113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]))
        elif(outfileext == "PDF"):
            upc_preimg = cairo.PDFSurface(
                None, (113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]))
        elif(outfileext == "PS" or outfileext == "EPS"):
            upc_preimg = cairo.PSSurface(
                None, (113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]))
            if(outfileext == "EPS"):
                upc_preimg.set_eps(True)
            else:
                upc_preimg.set_eps(False)
        else:
            upc_preimg = cairo.ImageSurface(
                cairo.FORMAT_RGB24, (113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
        upc_img.rectangle(
            0, 0, (113 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]))
        upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2])
        upc_img.fill()
    upc_array = {'upc': upc, 'code': []}
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    upc_array['code'].append([1, 0, 1])
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    LineStart = 0
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = barheight[0]
    if(hidetext):
        LineSize = barheight[1]
    while(BarNum < start_bc_num_end):
        if(BarNum < 9):
            LineSize = barheight[0]
        else:
            LineSize = barheight[1]
        if(hidetext):
            LineSize = barheight[1]
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[2], imageoutlib)
        LineStart += barwidth[0]
        BarNum += 1
    NumZero = 0
    while (NumZero < len(LeftDigit)):
        if(NumZero > 0):
            LineSize = barheight[0]
        if(NumZero == 0):
            LineSize = barheight[1]
        if(hidetext):
            LineSize = barheight[1]
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
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, 10, LineStart,
                              LineSize, barwidth[0], barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 10, LineStart,
                              LineSize, barwidth[0], barcolor[2], imageoutlib)
            LineStart += barwidth[0]
            BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    upc_array['code'].append([0, 1, 0, 1, 0])
    mid_barcode = [0, 1, 0, 1, 0]
    mid_bc_num = 0
    mid_bc_num_end = len(mid_barcode)
    LineSize = barheight[1]
    while(mid_bc_num < mid_bc_num_end):
        if(mid_barcode[mid_bc_num] == 1):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[0], imageoutlib)
        if(mid_barcode[mid_bc_num] == 0):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[2], imageoutlib)
        mid_bc_num += 1
        LineStart += barwidth[0]
        BarNum += 1
    NumZero = 0
    while (NumZero < len(RightDigit)):
        if(NumZero != 5):
            LineSize = barheight[0]
        if(NumZero == 5):
            LineSize = barheight[1]
        if(hidetext):
            LineSize = barheight[1]
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
                drawColorLine(upc_img, LineStart, 10, LineStart,
                              LineSize, barwidth[0], barcolor[0], imageoutlib)
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 10, LineStart,
                              LineSize, barwidth[0], barcolor[2], imageoutlib)
            LineStart += barwidth[0]
            BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    upc_array['code'].append([1, 0, 1])
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    end_barcode = [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    LineSize = barheight[1]
    while(end_bc_num < end_bc_num_end):
        if(end_bc_num < 4):
            LineSize = barheight[1]
        else:
            LineSize = barheight[0]
        if(hidetext):
            LineSize = barheight[1]
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, 10, LineStart,
                          LineSize, barwidth[0], barcolor[2], imageoutlib)
        end_bc_num += 1
        LineStart += barwidth[0]
        BarNum += 1
    if(pilsupport and imageoutlib == "pillow"):
        new_upc_img = upc_preimg.resize((((113 * barwidth[0]) + addonsize) * int(
            resize), (barheightadd + (9 * barwidth[1])) * int(resize)), Image.NEAREST)
        del(upc_img)
        del(upc_preimg)
        upc_img = ImageDraw.Draw(new_upc_img)
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        upc_imgpat = cairo.SurfacePattern(upc_preimg)
        scaler = cairo.Matrix()
        scaler.scale(1/int(resize), 1/int(resize))
        upc_imgpat.set_matrix(scaler)
        upc_imgpat.set_filter(cairo.FILTER_NEAREST)
        if(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS"):
            if(outfile is None):
                imgoutfile = None
            else:
                if(sys.version[0] == "2"):
                    imgoutfile = StringIO()
                if(sys.version[0] >= "3"):
                    imgoutfile = BytesIO()
            if(outfileext == "SVG"):
                new_upc_preimg = cairo.SVGSurface(imgoutfile, ((
                    113 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
            elif(outfileext == "PDF"):
                new_upc_preimg = cairo.PDFSurface(imgoutfile, ((
                    113 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
            elif(outfileext == "PS" or outfileext == "EPS"):
                new_upc_preimg = cairo.PSSurface(imgoutfile, ((
                    113 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
                if(outfileext == "EPS"):
                    new_upc_preimg.set_eps(True)
                else:
                    new_upc_preimg.set_eps(False)
            else:
                new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((
                    113 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        else:
            new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((
                113 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        new_upc_img = cairo.Context(new_upc_preimg)
        new_upc_img.set_source(upc_imgpat)
        new_upc_img.paint()
        upc_img = new_upc_img
    if(not hidetext):
        if(hidesn is not None and not hidesn):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (1 + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[0] * int(resize)), upc_matches[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (22 + (23 * (int(resize) - 1)) - (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (28 + (28 * (int(resize) - 1)) - (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (34 + (33 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
            barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (40 + (38 * (int(resize) - 1)) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (46 + (43 * (int(resize) - 1)) + (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[4], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (61 + (63 * (int(resize) - 1)) - (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[0], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (67 + (68 * (int(resize) - 1)) - (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[1], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (73 + (73 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
            barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[2], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (79 + (78 * (int(resize) - 1)) + (2 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[3], barcolor[1], "ocrb", imageoutlib)
        drawColorText(upc_img, 10 * int(resize * barwidth[1]), (85 + (83 * (int(resize) - 1)) + (4 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
            barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[2])[4], barcolor[1], "ocrb", imageoutlib)
        if(hidecd is not None and not hidecd):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (105 + (104 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (
                barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[2] * int(resize)), upc_matches[3], barcolor[1], "ocrb", imageoutlib)
    del(upc_img)
    if(pilsupport and imageoutlib == "pillow"):
        if(supplement is not None and len(supplement) == 2):
            upc_sup_img = upcean.encode.ean2.draw_ean2sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            if(upc_sup_img):
                new_upc_img.paste(
                    upc_sup_img, ((113 * barwidth[0]) * int(resize), 0))
                del(upc_sup_img)
        if(supplement is not None and len(supplement) == 5):
            upc_sup_img = upcean.encode.ean5.draw_ean5sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            if(upc_sup_img):
                new_upc_img.paste(
                    upc_sup_img, ((113 * barwidth[0]) * int(resize), 0))
                del(upc_sup_img)
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(supplement != None and len(supplement) == 2):
            upc_sup_img = upcean.encode.ean2.draw_ean2sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            new_upc_img.set_source_surface(
                upc_sup_img, (113 * barwidth[0]) * int(resize), 0)
            new_upc_img.paint()
            del(upc_sup_img)
        if(supplement != None and len(supplement) == 5):
            upc_sup_img = upcean.encode.ean5.draw_ean5sup_barcode(
                supplement, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
            new_upc_img.set_source_surface(
                upc_sup_img, (113 * barwidth[0]) * int(resize), 0)
            new_upc_img.paint()
            del(upc_sup_img)
    exargdict = {}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        if(pilsupport and imageoutlib == "pillow"):
            return new_upc_img
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            return new_upc_preimg
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
                        stdoutfile.write(new_upc_img.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            new_upc_img.convert(mode="1").tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        new_upc_img.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        new_upc_img.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(new_upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        new_upc_preimg.flush()
                        new_upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        new_upc_preimg.write_to_png(stdoutfile)
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
                        stdoutfile.write(new_upc_img.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            new_upc_img.convert(mode='1').tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        new_upc_img.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        new_upc_img.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(new_upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        new_upc_preimg.flush()
                        new_upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        new_upc_preimg.write_to_png(stdoutfile)
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
                        f.write(new_upc_img.tobytes())
                elif(outfileext == "XBM"):
                    with open(outfile, 'wb+') as f:
                        f.write(new_upc_preimg.get_data().tobytes())
                elif(outfileext == "XPM"):
                    new_upc_img.convert(mode="P").save(
                        outfile, outfileext, **exargdict)
                else:
                    new_upc_img.save(outfile, outfileext, **exargdict)
            if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                if(outfileext == "BYTES"):
                    with open(outfile, 'wb+') as f:
                        f.write(new_upc_preimg.get_data().tobytes())
                    return True
                elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                    new_upc_preimg.flush()
                    new_upc_preimg.finish()
                    imgoutfile.seek(0)
                    svgouttext = imgoutfile.read()
                    with open(outfile, 'wb+') as f:
                        f.write(svgouttext)
                    return True
                else:
                    new_upc_preimg.write_to_png(outfile)
                    return True
        except:
            return False
    return True


def create_ean12_barcode(upc, outfile="./ean12.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_upca_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def create_gtin12_barcode(upc, outfile="./gtin12.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_upca_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def create_ucc12_barcode(upc, outfile="./ucc12.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_upca_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_upca_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_upca_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_gtin12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_gtin12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_ean12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_ucc12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ucc12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_upca_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_upca_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_ean12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ean12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_gtin12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_gtin12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_ucc12_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_ucc12_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
