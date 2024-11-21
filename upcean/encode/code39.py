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

    $FileInfo: code39.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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

tkintersupport = upcean.support.check_for_tkinter()
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
cv2support = upcean.support.check_for_cv2()
skimagesupport = upcean.support.check_for_skimage()
imagelibsupport = upcean.support.imagelibsupport
defaultdraw = upcean.support.defaultdraw


def get_code39_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) < 1):
        return False
    if(not re.findall("([0-9a-zA-Z\\-\\.\\$\\/\\+% ]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    upc = upc.upper()
    upc_matches = list(upc)
    if(len(upc_matches) <= 0):
        return False
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    reswoshift = (((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((50 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code39_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if(imageoutlib not in imagelibsupport and imageoutlib is not None):
        imageoutlib = defaultdraw
    if(imageoutlib is not None):
        inimage = None
    if(len(upc) < 1):
        return False
    if(not re.findall("([0-9a-zA-Z\\-\\.\\$\\/\\+% ]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        vertical_text_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        vertical_text_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick") or (pgmagicksupport and imageoutlib == "pgmagick")):
        vertical_text_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and not cairosvgsupport and imageoutlib == "svgwrite"):
        vertical_text_fix = (8 * (int(resize) * barwidth[1]))
    elif(tkintersupport and imageoutlib == "tkinter"):
        vertical_text_fix = (5 * (int(resize) * barwidth[1]))
    else:
        vertical_text_fix = 0
    vertical_text_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc = upc.upper()
    upc_matches = list(upc)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((50 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code39", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                     0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    upc_array['code'].append(start_barcode)
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    barsizeloop = []
    LineSizeType = 0
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
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
        if(upc_matches[NumZero] == "A"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "B"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "C"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "D"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "E"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "F"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "G"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "H"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "I"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
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
        if(upc_matches[NumZero] == "O"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1]
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
        if(upc_matches[NumZero] == "-"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "."):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == " "):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "$"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "/"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "+"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "%"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
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
            barsizeloop.append(LineSizeType)
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize,
                      barwidth[0], barcolor[2], imageoutlib)
        upc_array['code'].append([0])
        upc_array['barsize'].append([LineSizeType])
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
        NumZero += 1
    end_barcode = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0,
                   1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(end_barcode)
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    barsizeloop = []
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
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
    LineTxtStart = ((shiftxy[0] + 15) * int(resize))
    LineTxtStartNorm = 15
    if(tkintersupport and imageoutlib == "tkinter"):
        LineTxtStart += (4 * int(resize))
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        LineTxtStart += (1 * int(resize))
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  "*", barcolor[1], "ocrb", imageoutlib)
    upc_array['text']['location'].append(LineTxtStartNorm)
    upc_array['text']['text'].append("*")
    upc_array['text']['type'].append("sn")
    LineTxtStart += 15 * int(resize)
    LineTxtStartNorm += 15
    while (NumTxtZero < len(upc_matches)):
        texthidden = False
        if hidetext:
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  upc_matches[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(upc_matches[NumTxtZero])
        upc_array['text']['type'].append("txt")
        LineTxtStart += 16 * int(resize)
        LineTxtStartNorm += 16
        NumTxtZero += 1
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  "*", barcolor[1], "ocrb", imageoutlib)
    upc_array['text']['location'].append(LineTxtStartNorm)
    upc_array['text']['text'].append("*")
    upc_array['text']['type'].append("cd")
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_code39_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    upc_up = upc.upper()
    upc_matches = list(upc_up)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code39_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_code39_barcode(upc, outfile="./code39.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
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
    imgout = draw_code39_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "code39; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True

def get_code39extended_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) < 1):
        return False
    if(not re.findall("([0-9a-zA-Z\\-\\.\\$\\/\\+% ]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    upc = upc.upper()
    upc_matches = list(upc)
    if(len(upc_matches) <= 0):
        return False
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    reswoshift = (((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((50 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code39extended_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if(imageoutlib not in imagelibsupport and imageoutlib is not None):
        imageoutlib = defaultdraw
    if(imageoutlib is not None):
        inimage = None
    if(len(upc) < 1):
        return False
    if(not re.findall("([0-9a-zA-Z\\-\\.\\$\\/\\+% ]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        vertical_text_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        vertical_text_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick") or (pgmagicksupport and imageoutlib == "pgmagick")):
        vertical_text_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and not cairosvgsupport and imageoutlib == "svgwrite"):
        vertical_text_fix = (8 * (int(resize) * barwidth[1]))
    elif(tkintersupport and imageoutlib == "tkinter"):
        vertical_text_fix = (5 * (int(resize) * barwidth[1]))
    else:
        vertical_text_fix = 0
    vertical_text_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc = upc.upper()
    upc_matches = list(upc)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((50 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code39", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                     0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
    upc_array['code'].append(start_barcode)
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    BarNum = 0
    barsizeloop = []
    LineSizeType = 0
    start_bc_num_end = len(start_barcode)
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
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
        if(upc_matches[NumZero] == "A"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "B"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "C"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "D"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "E"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "F"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "G"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "H"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "I"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
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
        if(upc_matches[NumZero] == "O"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1]
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
        if(upc_matches[NumZero] == "-"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1]
        if(upc_matches[NumZero] == "."):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == " "):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "$"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "/"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "+"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        if(upc_matches[NumZero] == "%"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
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
            barsizeloop.append(LineSizeType)
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize,
                      barwidth[0], barcolor[2], imageoutlib)
        upc_array['code'].append([0])
        upc_array['barsize'].append(barsizeloop)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
        NumZero += 1
    end_barcode = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0,
                   1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(end_barcode)
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    barsizeloop = []
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    code39extended = {'%U': " ", '$A': " ", '$B': " ", '$C': " ", '$D': " ", '$E': " ", '$F': " ", '$G': " ", '$H': " ", '$I': " ", '$J': " ", '$K': " ", '$L': " ", '$M': " ", '$N': " ", '$O': " ", '$P': " ", '$Q': " ", '$R': " ", '$S': " ", '$T': " ", '$U': " ", '$V': " ", '$W': " ", '$X': " ", '$Y': " ", '$Z': " ", '%A': " ", '%B': " ", '%C': " ", '%D': " ", '%E': " ", ' ': " ", '/A': "!", '/B': "\"", '/C': "#", '/D': "$", '/E': "%", '/F': "&", '/G': "'",
                          '/H': "(", '/I': ")", '/J': "*", '/K': "+", '/L': ",", '/M': "-", '/N': ".", '/O': "/", '-': "-", '.': ".", '0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9", '/Z': ":", '%F': ";", '%G': "<", '%H': "=", '%I': ">", '%J': "?", '%V': "@", 'A': "A", 'B': "B", 'C': "C", 'D': "D", 'E': "E", 'F': "F", 'G': "G", 'H': "H", 'I': "I", 'J': "J", 'K': "K", 'L': "L", 'M': "M", 'N': "N", 'O': "O", 'P': "P", 'Q': "Q", 'R': "R", 'S': "S", 'T': "T", 'U': "U", 'V': "V", 'W': "W", 'X': "X", 'Y': "Y", 'Z': "Z", '%K': "[", '%L': "\\", '%M': "]", '%N': "^", '%O': "_", '%W': "`", '+A': "a", '+B': "b", '+C': "c", '+D': "d", '+E': "e", '+F': "f", '+G': "g", '+H': "h", '+I': "i", '+J': "j", '+K': "k", '+L': "l", '+M': "m", '+N': "n", '+O': "o", '+P': "p", '+Q': "q", '+R': "r", '+S': "s", '+T': "t", '+U': "u", '+V': "v", '+W': "w", '+X': "x", '+Y': "y", '+Z': "z", '%P': "{", '%Q': "|", '%R': "}", '%S': "~", '%T': " ", '%X': " ", '%Y': " ", '%Z': " "}
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
    NumTxtZero = 0
    LineTxtStart = ((shiftxy[0] + 15) * int(resize))
    LineTxtStartNorm = 15
    if(tkintersupport and imageoutlib == "tkinter"):
        LineTxtStart += (4 * int(resize))
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        LineTxtStart += (1 * int(resize))
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  "*", barcolor[1], "ocrb", imageoutlib)
    upc_array['text']['location'].append(LineTxtStartNorm)
    upc_array['text']['text'].append("*")
    upc_array['text']['type'].append("sn")
    LineTxtStart += 15 * int(resize)
    LineTxtStartNorm += 15
    while (NumTxtZero < len(upc_matches)):
        texthidden = False
        NumTxtZeroNext = NumTxtZero + 1
        if(NumTxtZeroNext < len(upc_matches) and code39extended.get(upc_matches[NumTxtZero]+upc_matches[NumTxtZeroNext], False)):
            LineTxtStart += 16 * int(resize)
            LineTxtStartNorm += 16
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  code39extended.get(upc_matches[NumTxtZero]+upc_matches[NumTxtZeroNext], " "), barcolor[1], "ocrb", imageoutlib)
            NumTxtZero += 1
        else:
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  code39extended.get(upc_matches[NumTxtZero], upc_matches[NumTxtZero]), barcolor[1], "ocrb", imageoutlib)
        if hidetext:
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  upc_matches[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(upc_matches[NumTxtZero])
        upc_array['text']['type'].append("txt")
        LineTxtStart += 16 * int(resize)
        LineTxtStartNorm += 16
        NumTxtZero += 1
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  "*", barcolor[1], "ocrb", imageoutlib)
    upc_array['text']['location'].append(LineTxtStartNorm)
    upc_array['text']['text'].append("*")
    upc_array['text']['type'].append("cd")
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_code39extended_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    upc_up = upc.upper()
    upc_matches = list(upc_up)
    upc_size_add = ((len(upc_matches) * 15) +
                    (len(upc_matches) + 1)) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((50 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code39extended_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_code39extended_barcode(upc, outfile="./code39.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
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
    imgout = draw_code39extended_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': upc}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "code39; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True
