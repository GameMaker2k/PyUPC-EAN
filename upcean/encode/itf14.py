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

    $FileInfo: itf14.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.predraw import *
import re
import sys
import upcean.support

import io
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

pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or pillowsupport):
    import upcean.predraw.prepil
if(cairosupport):
    import upcean.predraw.precairo
if(qahirahsupport):
    import upcean.predraw.preqahirah
if(svgwritesupport):
    import upcean.predraw.presvgwrite
if(wandsupport):
    import upcean.predraw.prewand
if(magicksupport):
    import upcean.predraw.premagick


def get_itf14_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    threewidebar = True
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) % 2):
        return False
    if(len(upc) < 6):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    reswoshift = (((44 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[1])) * int(resize))
    reswshift = ((((44 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (15 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


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
    elif qahirahsupport and isinstance(upc_img, qah.Context) and isinstance(upc_preimg, qah.Surface):
        imageoutlib = "qahirah"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif wandsupport and isinstance(upc_img, wImage):
        imageoutlib = "wand"
    elif magicksupport and isinstance(upc_img, PythonMagick.Image):
        imageoutlib = "magick"
    elif pgmagicksupport and isinstance(upc_img, pgmagick.Image):
        imageoutlib = "pgmagick"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and inimage != "none" and inimage is not None):
        imageoutlib = None
    elif(inimage == "none" or inimage is None):
        imageoutlib = None
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
        vertical_text_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        vertical_text_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick") or (pgmagicksupport and imageoutlib == "pgmagick")):
        vertical_text_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and imageoutlib == "svgwrite"):
        vertical_text_fix = (8 * (int(resize) * barwidth[1]))
    else:
        vertical_text_fix = 0
    vertical_text_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((44 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (15 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 15, 'type': "itf14", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
    upc_array['code'].append(start_barcode)
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
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
        subcode = []
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
        upc_array['code'].append(subcode)
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
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
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
    NumTxtZero = 0
    LineTxtStart = shiftxy[0] * int(resize) + (23 * int(resize))
    LineTxtStartNorm = 23
    while (NumTxtZero < len(upc_matches)):
        ArrayDigit = list(upc_matches[NumTxtZero])
        texthidden = False
        if hidetext or (NumTxtZero == 0 and (hidesn is None or hidesn)) or (NumTxtZero == 11 and (hidecd is None or hidecd)):
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  ArrayDigit[0], barcolor[1], "ocrb", imageoutlib)
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(ArrayDigit[0])
        upc_array['text']['type'].append("txt")
        if(threewidebar):
            LineTxtStart += 9 * int(resize)
            LineTxtStartNorm += 9
        else:
            LineTxtStart += 7 * int(resize)
            LineTxtStartNorm += 7
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  ArrayDigit[1], barcolor[1], "ocrb", imageoutlib)
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(ArrayDigit[1])
        upc_array['text']['type'].append("txt")
        if(threewidebar):
            LineTxtStart += 9 * int(resize)
            LineTxtStartNorm += 9
        else:
            LineTxtStart += 7 * int(resize)
            LineTxtStartNorm += 7
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
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
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((44 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_itf14_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib]

def create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
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
    if(not pgmagicksupport and imageoutlib == "pgmagick"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and imageoutlib != "svgwrite"):
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
    imgout = draw_itf14_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, "itf14; "+upc, imageoutlib)
    return True

def encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
 return encode_itf14_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)

def draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
 return draw_itf14_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)

def create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    return create_itf14_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
