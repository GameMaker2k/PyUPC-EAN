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

    $FileInfo: code93.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
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
drawlibsupport = upcean.support.check_for_drawlib()
imagelibsupport = upcean.support.imagelibsupport
defaultdraw = upcean.support.defaultdraw


def get_code93_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
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
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    reswoshift = (((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((37 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code93_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if((pilsupport and imageoutlib == "pillow") or (drawlibsupport and imageoutlib == "drawlib")):
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
    if(len(upc_matches) <= 0):
        return False
    Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
                   24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"}
    Code93Values = dict(zip(Code93Array.values(), Code93Array))
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((37 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code93", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]
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
        left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "0"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "1"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "2"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "3"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "4"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "5"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "6"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "7"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "8"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "9"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "A"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "B"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "C"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "D"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "E"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "F"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "G"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "H"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "I"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "J"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "K"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "L"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "M"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "N"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "O"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "P"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Q"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "R"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "S"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "T"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "U"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "V"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "W"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "X"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Y"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Z"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "-"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "."):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == " "):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "$"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "/"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "+"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "%"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "($)"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "(%)"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "(/)"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "(+)"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 0]
        ''' Unused barcodes
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0];
  '''
        InnerUPCNum = 0
        upc_array['code'].append(left_barcolor)
        barsizeloop = []
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            barsizeloop.append(LineSizeType)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    end_barcode = [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(end_barcode)
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
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
    NumTxtZero = 0
    LineTxtStart = ((shiftxy[0] + 18) * int(resize))
    LineTxtStartNorm = 18
    if(tkintersupport and imageoutlib == "tkinter"):
        LineTxtStart += (4 * int(resize))
    elif(svgwritesupport and not cairosvgsupport and imageoutlib == "svgwrite"):
        LineTxtStart += (1 * int(resize))
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
        LineTxtStart += 9 * int(resize)
        LineTxtStartNorm += 9
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_code93_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    upc_up = upc.upper()
    upc_matches = list(upc_up)
    if(len(upc_matches) <= 0):
        return False
    Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
                   24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"}
    Code93Values = dict(zip(Code93Array.values(), Code93Array))
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code93_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_code93_barcode(upc, outfile="./code93.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
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
    imgout = draw_code93_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "code93; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True

def draw_code93_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
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
    upc_img, upc_preimg = upcean.predraw.new_image_surface((((50 * barwidth[0]) + upc_size_add) * int(resize)) * int(numxy[0]), ((barheightadd + (9 * barwidth[1])) * int(resize)) * int(numxy[1]), barcolor[2], imageoutlib)
    shift_x = 0
    shift_y = 0
    shift_x_pos = 0
    shift_y_pos = 0
    for shift_y in range(numxy[1]):
        for shift_x in range(numxy[0]):
            imgout = encode_code93_barcode([upc_img, upc_preimg], upc, resize, (shift_x_pos, shift_y_pos), barheight, barwidth, barcolor, hideinfo, imageoutlib)
            shift_x_pos += ((50 * barwidth[0]) + upc_size_add)
        shift_y_pos += (barheightadd + (9 * barwidth[1]))
        shift_x_pos = 0
    return [upc_img, upc_preimg, imageoutlib]

def create_code93_barcode_sheet(upc, outfile="./code93.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
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
    imgout = draw_code93_barcode_sheet(upc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "code93; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True

def get_code93extended_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
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
    pattern = '\\(\\$\\)|\\(%\\)|\\(/\\)|\\(\\+\\)|[0-9A-Z\\-\\. \\$\\/\\+%]'
    upc_matches = re.findall(pattern, upc)
    if(len(upc_matches) <= 0):
        return False
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    reswoshift = (((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((37 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code93extended_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if((pilsupport and imageoutlib == "pillow") or (drawlibsupport and imageoutlib == "drawlib")):
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
    pattern = '\\(\\$\\)|\\(%\\)|\\(/\\)|\\(\\+\\)|[0-9A-Z\\-\\. \\$\\/\\+%]'
    upc_matches = re.findall(pattern, upc)
    if(len(upc_matches) <= 0):
        return False
    Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
                   24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"}
    Code93Values = dict(zip(Code93Array.values(), Code93Array))
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((37 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code93", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]
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
        left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "0"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "1"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "2"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "3"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "4"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "5"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "6"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "7"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "8"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "9"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "A"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "B"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "C"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "D"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "E"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "F"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "G"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "H"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "I"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "J"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "K"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "L"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "M"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "N"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "O"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "P"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Q"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "R"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "S"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "T"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "U"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "V"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "W"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "X"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Y"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "Z"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "-"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "."):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == " "):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "$"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "/"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "+"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "%"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "($)"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "(%)"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "(/)"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "(+)"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 0]
        ''' Unused barcodes
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0];
  '''
        InnerUPCNum = 0
        upc_array['code'].append(left_barcolor)
        barsizeloop = []
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            barsizeloop.append(LineSizeType)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        upc_array['barsize'].append(barsizeloop)
        NumZero += 1
    end_barcode = [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
        barsizeloop.append(LineSizeType)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    code93extended = {'(%)U': " ", '($)A': " ", '($)B': " ", '($)C': " ", '($)D': " ", '($)E': " ", '($)F': " ", '($)G': " ", '($)H': " ", '($)I': " ", '($)J': " ", '($)K': " ", '($)L': " ", '($)M': " ", '($)N': " ", '($)O': " ", '($)P': " ", '($)Q': " ", '($)R': " ", '($)S': " ", '($)T': " ", '($)U': " ", '($)V': " ", '($)W': " ", '($)X': " ", '($)Y': " ", '($)Z': " ", '(%)A': " ", '(%)B': " ", '(%)C': " ", '(%)D': " ", '(%)E': " ", ' ': " ", '(/)A': "!", '(/)B': "\"", '(/)C': "#", '($)': "$", '(/)F': "&", '(/)G': "'", '(/)H': "(", '(/)I': "", '(/)J': "*", '(/)L': ",", '-': "-", '.': ".", '0': "0", '1': "1", '2': "2", '3': "3", '4': "4", '5': "5", '6': "6", '7': "7", '8': "8", '9': "9", '(/)Z': ":", '(/)': "/", '(%)F': ";", '(%)G': "<", '(%)H': "=", '(%)I': ">", '(%)J': "?",
                      '(%)V': "@", '(%)K': "[", '(%)L': "\\", '(%)M': "]", '(%)N': "^", '(%)O': "_", '(%)W': "`", '(+)A': "a", '(+)B': "b", '(+)C': "c", '(+)D': "d", '(+)E': "e", '(+)F': "f", '(+)G': "g", '(+)H': "h", '(+)I': "i", '(+)J': "j", '(+)K': "k", '(+)L': "l", '(+)M': "m", '(+)N': "n", '(+)O': "o", '(+)P': "p", '(+)Q': "q", '(+)R': "r", '(+)S': "s", '(+)T': "t", '(+)U': "u", '(+)V': "v", '(+)W': "w", '(+)X': "x", '(+)Y': "y", '(+)Z': "z", '(+)': "+", '(%)P': "{", '(%)Q': "|", '(%)R': "}", '(%)S': "~", '(%)T': " ", '(%)X': " ", '(%)Y': " ", '(%)Z': " ", '(%)': "%"}
    NumTxtZero = 0
    LineTxtStart = ((shiftxy[0] + 18) * int(resize))
    LineTxtStartNorm = 18
    if(tkintersupport and imageoutlib == "tkinter"):
        LineTxtStart += (4 * int(resize))
    elif(svgwritesupport and not cairosvgsupport and imageoutlib == "svgwrite"):
        LineTxtStart += (1 * int(resize))
    while (NumTxtZero < len(upc_matches)):
        texthidden = False
        if(len(upc_matches[NumTxtZero])==3):
            NumTxtZeroNext = NumTxtZero + 1
            nextchar = code93extended.get(upc_matches[NumTxtZero]+upc_matches[NumTxtZeroNext], "  ")
            LineTxtStart += 9 * int(resize)
            LineTxtStartNorm += 9
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  nextchar, barcolor[1], "ocrb", imageoutlib)
            NumTxtZero += 1
        else:
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  code93extended.get(upc_matches[NumTxtZero], upc_matches[NumTxtZero]), barcolor[1], "ocrb", imageoutlib)
            #print(upc_matches[NumTxtZero], NumTxtZero)
        if hidetext:
            texthidden = True
        upc_array['text']['location'].append(LineTxtStartNorm)
        upc_array['text']['text'].append(upc_matches[NumTxtZero])
        upc_array['text']['type'].append("txt")
        LineTxtStart += 9 * int(resize)
        LineTxtStartNorm += 9
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    return [upc_img, upc_preimg, imageoutlib, upc_array]


def draw_code93extended_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    upc = upc.upper()
    pattern = '\\(\\$\\)|\\(%\\)|\\(/\\)|\\(\\+\\)|[0-9A-Z\\-\\. \\$\\/\\+%]'
    upc_matches = re.findall(pattern, upc)
    if(len(upc_matches) <= 0):
        return False
    Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N",
                   24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"}
    Code93Values = dict(zip(Code93Array.values(), Code93Array))
    upc_size_add = (len(upc_matches) * 9) * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code93extended_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_code93extended_barcode(upc, outfile="./code93.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
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
    imgout = draw_code93extended_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "code93; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True

''' Old code that works will check and fix other functions '''

def create_code93alt_barcode(upc,outfile="./code93.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 imageoutlib = imageoutlib.lower();
 barheightadd = barheight[1];
 if(barheight[0] >= barheight[1]):
  barheightadd = barheight[0] + 6;
 else:
  barheightadd = barheight[1];
 if(not pilsupport and imageoutlib=="pillow"):
  imageoutlib = "cairo";
 if(not cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  imageoutlib = "pillow";
 if(not cairosupport and imageoutlib=="cairosvg"):
  imageoutlib = "pillow";
 if(imageoutlib!="pillow" and imageoutlib!="cairo" and imageoutlib!="cairosvg"):
  imageoutlib = "pillow";
 if(not pilsupport and not cairosupport):
  return False;
 if(outfile is None):
  if(imageoutlib=="cairosvg"):
   oldoutfile = None;
   outfile = None;
   outfileext = "SVG";
  else:
   oldoutfile = None;
   outfile = None;
   outfileext = None;
 else:
  oldoutfile = upcean.encode.predraw.get_save_filename(outfile, imageoutlib);
  if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
   del(outfile);
   outfile = oldoutfile[0];
   outfileext = oldoutfile[1];
   if(cairosupport and imageoutlib=="cairo" and outfileext=="SVG"):
    imageoutlib = "cairosvg";
   if(cairosupport and imageoutlib=="cairosvg" and outfileext!="SVG"):
    imageoutlib = "cairo";
 if(len(upc) < 1):
  return False;
 if(not re.findall(r"([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 if(not re.findall(r"^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(pilsupport and imageoutlib=="pillow"):
  try:
   pil_ver = Image.PILLOW_VERSION;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
   pil_is_pillow = True;
  except AttributeError:
   try:
    pil_ver = Image.VERSION;
    pil_is_pillow = False;
   except AttributeError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except NameError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
  except NameError:
   try:
    pil_ver = Image.VERSION;
    pil_is_pillow = False;
   except AttributeError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except NameError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
  pil_prevercheck = [str(x) for x in pil_ver];
  pil_vercheck = int(pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2]);
  if(pil_is_pillow and pil_vercheck>=210 and pil_vercheck<220):
   pil_addon_fix = int(resize) * 2;
   cairo_addon_fix = 0;
 elif(pilsupport and imageoutlib=="pillow"):
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
 elif(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  pil_addon_fix = 0;
  cairo_addon_fix = (8 * (int(resize) ) );
 else:
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
 upc = upc.upper();
 upc_matches = list(upc);
 upc_print = upc_matches;
 if(len(upc_matches)<=0):
  return False;
 Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"};
 Code93Values = dict(zip(Code93Array.values(),Code93Array));
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 upc_print = list(upc_matches);
 UPC_Count = 0;
 UPC_Weight = 1;
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>20):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1;
  UPC_Weight += 1;
 upc_matches.append(Code93Array[UPC_Sum % 47]);
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 UPC_Count = 0;
 UPC_Weight = 1;
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>15):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1;
  UPC_Weight += 1;
 upc_matches.append(Code93Array[UPC_Sum % 47]);
 upc_size_add = (len(upc_matches) * 9) * barwidth[0];
 if(pilsupport and imageoutlib=="pillow"):
  upc_preimg = Image.new("RGB", ((37 * barwidth[0]) + upc_size_add, barheightadd + (9 * barwidth[1])));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((37 * barwidth[0]) + upc_size_add, barheightadd + (9 * barwidth[1]))], fill=barcolor[2]);
 if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  if(outfileext=="SVG"):
   upc_preimg = cairo.SVGSurface(None, (37 * barwidth[0]) + upc_size_add, barheightadd + (9 * barwidth[1]));
  elif(outfileext=="PDF"):
   upc_preimg = cairo.PDFSurface(None, (37 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
  elif(outfileext=="PS" or outfileext=="EPS"):
   upc_preimg = cairo.PSSurface(None, (37 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
   if(outfileext=="EPS"):
    upc_preimg.set_eps(True);
   else:
    upc_preimg.set_eps(False);
  else:
   upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (37 * barwidth[0]) + upc_size_add, barheightadd + (9 * barwidth[1]));
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (37 * barwidth[0]) + upc_size_add, barheightadd + (9 * barwidth[1]));
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0];
 LineStart = 0;
 BarNum = 0;
 start_bc_num_end = len(start_barcode);
 while(BarNum < start_bc_num_end):
  if(start_barcode[BarNum]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
  if(start_barcode[BarNum]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
  LineStart += barwidth[0];
  BarNum += 1;
 NumZero = 0;
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 0, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="A"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="B"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="C"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="D"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="E"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="F"):
   left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="G"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="H"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="I"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="J"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="K"):
   left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="L"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="M"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="N"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="O"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="P"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Q"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="R"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="S"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="T"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="U"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="V"):
   left_barcolor = [1, 1, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="W"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="X"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Y"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Z"):
   left_barcolor = [1, 0, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="-"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="."):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="$"):
   left_barcolor = [1, 1, 1, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="/"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="+"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="%"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="($)"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="(%)"):
   left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="(/)"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="(+)"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 0];
  ''' Unused barcodes
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0];
  '''
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
   LineStart += barwidth[0];
   BarNum += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 end_barcode = [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_bc_num_end = len(end_barcode);
 while(end_bc_num < end_bc_num_end):
  if(end_barcode[end_bc_num]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
  if(end_barcode[end_bc_num]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
  end_bc_num += 1;
  LineStart += barwidth[0];
  BarNum += 1;
 if(pilsupport and imageoutlib=="pillow"):
  new_upc_img = upc_preimg.resize((((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize)), Image.NEAREST); # use nearest neighbour
  del(upc_img);
  del(upc_preimg);
  upc_img = ImageDraw.Draw(new_upc_img);
 if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  upc_imgpat = cairo.SurfacePattern(upc_preimg);
  scaler = cairo.Matrix();
  scaler.scale(1/int(resize),1/int(resize));
  upc_imgpat.set_matrix(scaler);
  upc_imgpat.set_filter(cairo.FILTER_NEAREST);
  if(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS"):
   if(outfile is None):
    imgoutfile = None;
   else:
    if(sys.version[0]=="2"):
     imgoutfile = StringIO();
    if(sys.version[0]>="3"):
     imgoutfile = BytesIO();
   if(outfileext=="SVG"):
    new_upc_preimg = cairo.SVGSurface(imgoutfile, ((37 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PDF"):
    new_upc_preimg = cairo.PDFSurface(imgoutfile, ((37 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PS" or outfileext=="EPS"):
    new_upc_preimg = cairo.PSSurface(imgoutfile, ((37 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
    if(outfileext=="EPS"):
     new_upc_preimg.set_eps(True);
    else:
     new_upc_preimg.set_eps(False);
   else:
    new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
  else:
   new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((37 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
  new_upc_img = cairo.Context(new_upc_preimg);
  new_upc_img.set_source(upc_imgpat);
  new_upc_img.paint();
  upc_img = new_upc_img;
 if(not hidetext):
  NumTxtZero = 0;
  LineTxtStart = 18;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (19 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib);
   LineTxtStart += 9 * int(resize);
   NumTxtZero += 1;
 del(upc_img);
 exargdict = {};
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  if(pilsupport and imageoutlib=="pillow"):
   return new_upc_img;
  if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
   return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   stdoutfile = StringIO();
   if(outfileext=="WEBP"):
    exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
   elif(outfileext=="JPEG"):
    exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
   elif(outfileext=="PNG"):
    exargdict.update( { 'optimize': True, 'compress_level': 9 } );
   else:
    exargdict = {};
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_img.tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XBM"):
      stdoutfile.write(new_upc_img.convert(mode="1").tobitmap());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XPM"):
      new_upc_img.convert(mode="P").save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_img.save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
    if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_preimg.get_data().tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
      new_upc_preimg.flush();
      new_upc_preimg.finish();
      imgoutfile.seek(0);
      svgouttext = imgoutfile.read();
      stdoutfile.write(svgouttext);
      imgoutfile.close();
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_preimg.write_to_png(stdoutfile);
      stdoutfile.seek(0);
      return stdoutfile;
   except:
    return False;
 if(sys.version[0]>="3"):
  stdoutfile = BytesIO();
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   if(outfileext=="WEBP"):
    exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
   elif(outfileext=="JPEG"):
    exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
   elif(outfileext=="PNG"):
    exargdict.update( { 'optimize': True, 'compress_level': 9 } );
   else:
    exargdict = {};
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_img.tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XBM"):
      stdoutfile.write(new_upc_img.convert(mode='1').tobitmap());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XPM"):
      new_upc_img.convert(mode="P").save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_img.save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
    if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_preimg.get_data().tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
      new_upc_preimg.flush();
      new_upc_preimg.finish();
      imgoutfile.seek(0);
      svgouttext = imgoutfile.read();
      stdoutfile.write(svgouttext);
      imgoutfile.close();
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_preimg.write_to_png(stdoutfile);
      stdoutfile.seek(0);
      return stdoutfile;
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  if(outfileext=="WEBP"):
   exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
  elif(outfileext=="JPEG"):
   exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
  elif(outfileext=="PNG"):
   exargdict.update( { 'optimize': True, 'compress_level': 9 } );
  else:
   exargdict = {};
  try:
   if(pilsupport and imageoutlib=="pillow"):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_img.tobytes());
    elif(outfileext=="XBM"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_preimg.get_data().tobytes());
    elif(outfileext=="XPM"):
     new_upc_img.convert(mode="P").save(outfile, outfileext, **exargdict);
    else:
     new_upc_img.save(outfile, outfileext, **exargdict);
   if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_preimg.get_data().tobytes());
     return True;
    elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
     new_upc_preimg.flush();
     new_upc_preimg.finish();
     imgoutfile.seek(0);
     svgouttext = imgoutfile.read();
     with open(outfile, 'wb+') as f:
      f.write(svgouttext);
     return True;
    else:
     new_upc_preimg.write_to_png(outfile);
     return True;
  except:
   return False;
 return True;
 
def draw_code93alt_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code93alt_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code93alt_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code93alt_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
