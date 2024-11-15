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

    $FileInfo: ean13.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.predraw import *
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
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or pillowsupport):
    import upcean.predraw.prepil
if(cairosupport):
    import upcean.predraw.precairo
if(qahirahsupport):
    import upcean.predraw.preqahirah
if(svgwritesupport):
    import upcean.predraw.presvgwrite


def get_upcaean_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
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
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    if(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    reswoshift = (((115 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((115 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_ean13_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
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
    upc_pieces = None
    supplement = None
    imageoutlib = None
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif qahirahsupport and isinstance(upc_img, qah.Context) and isinstance(upc_preimg, qah.Surface):
        imageoutlib = "qahirah"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif wandsupport and isinstance(upc_img, Image):
        imageoutlib = "wand"
    elif magicksupport and isinstance(upc_img, PythonMagick.Image):
        imageoutlib = "magick"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and imageoutlib != "wand" and imageoutlib != "magick" and inimage != "none" and inimage is not None):
        imageoutlib = None
    elif(inimage == "none" or inimage is None):
        imageoutlib = None
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    elif(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        pil_addon_fix = 0
        cairo_addon_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick")):
        pil_addon_fix = 0
        cairo_addon_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and imageoutlib == "svgwrite"):
        pil_addon_fix = 0
        cairo_addon_fix = (8 * (int(resize) * barwidth[1]))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    cairo_addon_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_matches = re.findall("(\\d{1})(\\d{6})(\\d{6})", upc)
    if(len(upc_matches) <= 0):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(upc_matches[1])
    RightDigit = list(upc_matches[2])
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    elif(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((115 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "ean13", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    upc_array['code'].append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1])
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    barsizeloop = []
    LineSizeType = 0
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
        if(hidetext):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
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
    barsizeloop = []
    LineSizeType = 1
    while(mid_bc_num < mid_bc_num_end):
        if(mid_bc_num < 4):
            LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            LineSizeType = 1
        else:
            LineSize = (barheight[0] + shiftxy[1]) * int(resize)
            LineSizeType = 0
        if(hidetext):
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
        LineSize = (barheight[0] + shiftxy[1]) * int(resize)
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
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
    NumTxtZero = 0
    LineTxtStart = ((shiftxy[0] + 2) * int(resize))
    LineTxtStartNorm = 2
    upc_print = list(re.findall("(\\d{13})", upc)[0])+[">"]
    while (NumTxtZero < len(upc_print)):
        texthidden = False
        if hidetext or (NumTxtZero == 0 and (hidesn is None or hidesn)) or (NumTxtZero == 13 and (hidecd is None or hidecd)):
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], cairo_addon_fix + (
            barheight[0] * int(resize)) + pil_addon_fix, upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(upc_print[NumTxtZero])
        if(NumTxtZero == 0):
         upc_array['text']['type'].append("sn")
        elif(NumTxtZero == 9):
         upc_array['text']['type'].append("cd")
        else:
         upc_array['text']['type'].append("txt")
        if(NumTxtZero==0):
            LineTxtStart += 5 * int(resize)
            LineTxtStartNorm += 5
        if(NumTxtZero==6):
            LineTxtStart += 4 * int(resize)
            LineTxtStartNorm += 4
        if(NumTxtZero==12):
            LineTxtStart += 5 * int(resize)
            LineTxtStartNorm += 5
        LineTxtStart += 7 * int(resize)
        LineTxtStartNorm += 7
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(supplement is not None and len(supplement) == 2):
        if(imageoutlib is None):
            supimgout = None
        else:
            supimgout = (upc_img, upc_preimg)
        supout = upcean.encode.ean2.encode_ean2_barcode(supimgout, supplement, resize, (115, shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
        if(imageoutlib is None):
            upc_array['code'] += supout['code']
            upc_array['barsize'] += supout['barsize']
            # Add 115 to every 0th element in each sublist of upc_array['text']['location']
            upc_array['text']['location'] += [x + 115 for x in supout['text']['location']]
            upc_array['text']['location'] += supout['text']['location']
            upc_array['text']['type'] += supout['text']['type']
            upc_array['text']['text'] += supout['text']['text']
    elif(supplement is not None and len(supplement) == 5):
        if(imageoutlib is None):
            supimgout = None
        else:
            supimgout = (upc_img, upc_preimg)
        supout = upcean.encode.ean5.encode_ean5_barcode(supimgout, supplement, resize, (115, shiftxy[1]), barheight, barwidth, barcolor, hideinfo)
        if(imageoutlib is None):
            upc_array['code'] += supout['code']
            upc_array['barsize'] += supout['barsize']
            # Add 115 to every 0th element in each sublist of upc_array['text']['location']
            upc_array['text']['location'] += [x + 115 for x in supout['text']['location']]
            upc_array['text']['location'] += supout['text']['location']
            upc_array['text']['type'] += supout['text']['type']
            upc_array['text']['text'] += supout['text']['text']
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_ean13_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
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
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    elif(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29 * barwidth[0]
    elif(supplement is not None and len(supplement) == 5):
        upc_size_add = 56 * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((115 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_ean13_barcode([upc_img, upc_preimg], fullupc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib]

def create_ean13_barcode(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "svgwrite"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "svgwrite"
    if(not qahirahsupport and imageoutlib == "qahirah"):
        imageoutlib = "svgwrite"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "svgwrite"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "svgwrite"
    if(not wandsupport and imageoutlib == "wand"):
        imageoutlib = "svgwrite"
    if(not magicksupport and imageoutlib == "magick"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "svgwrite"):
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
        oldoutfile = upcean.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    imgout = draw_ean13_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, "ean13; "+upc, imageoutlib)
    return True
