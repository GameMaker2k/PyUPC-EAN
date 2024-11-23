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

    $FileInfo: codabar.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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


def get_codabar_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) < 1):
        return False
    if(barwidth[0] < 1):
        barwidth[0] = 1
    if(not re.findall("^([a-dA-DeEnN\\*tT])([0-9\\-\\$\\:\\/\\.\\+]+)([a-dA-DeEnN\\*tT])$", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    pre_upc_matches = upc_matches = re.findall(
        "^([a-dA-DeEnN\\*tT])([0-9\\-\\$\\:\\/\\.\\+]+)([a-dA-DeEnN\\*tT])$", upc)
    pre_upc_matches = pre_upc_matches[0]
    upc_matches = list(pre_upc_matches[1])
    bcsize9 = len(re.findall("([0-9\\-\\$])", "".join(upc_matches)))
    bcsize10 = len(re.findall("([\\:\\/\\.])", "".join(upc_matches)))
    bcsize12 = len(re.findall("([\\+])", "".join(upc_matches)))
    upc_size_add = ((bcsize9 * 9) + (bcsize10 * 10) +
                    (bcsize12 * 12) + len(upc_matches) - 1) * barwidth[0]
    reswoshift = (((40 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((40 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_codabar_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if(barwidth[0] < 1):
        barwidth[0] = 1
    if(not re.findall("^([a-dA-DeEnN\\*tT])([0-9\\-\\$\\:\\/\\.\\+]+)([a-dA-DeEnN\\*tT])$", upc)):
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
    pre_upc_matches = upc_matches = re.findall(
        "^([a-dA-DeEnN\\*tT])([0-9\\-\\$\\:\\/\\.\\+]+)([a-dA-DeEnN\\*tT])$", upc)
    pre_upc_matches = pre_upc_matches[0]
    upc_matches = list(pre_upc_matches[1])
    bcsize9 = len(re.findall("([0-9\\-\\$])", "".join(upc_matches)))
    bcsize10 = len(re.findall("([\\:\\/\\.])", "".join(upc_matches)))
    bcsize12 = len(re.findall("([\\+])", "".join(upc_matches)))
    upc_size_add = ((bcsize9 * 9) + (bcsize10 * 10) +
                    (bcsize12 * 12) + len(upc_matches) - 1) * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((40 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "codabar", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if(pre_upc_matches[0] == "A" or pre_upc_matches[0] == "T"):
        start_barcode = [0, 0, 0, 0, 0, 0, 0, 0,
                         0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0]
    if(pre_upc_matches[0] == "B" or pre_upc_matches[0] == "N"):
        start_barcode = [0, 0, 0, 0, 0, 0, 0, 0,
                         0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0]
    if(pre_upc_matches[0] == "C" or pre_upc_matches[0] == "*"):
        start_barcode = [0, 0, 0, 0, 0, 0, 0, 0,
                         0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0]
    if(pre_upc_matches[0] == "D" or pre_upc_matches[0] == "E"):
        start_barcode = [0, 0, 0, 0, 0, 0, 0, 0,
                         0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0]
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
        left_barcolor = [1, 0, 1, 0, 1, 0, 0, 1, 1]
        if(upc_matches[NumZero] == "0"):
            left_barcolor = [1, 0, 1, 0, 1, 0, 0, 1, 1]
        if(upc_matches[NumZero] == "1"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 1]
        if(upc_matches[NumZero] == "2"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 0, 1, 1]
        if(upc_matches[NumZero] == "3"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "4"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 1]
        if(upc_matches[NumZero] == "5"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 1]
        if(upc_matches[NumZero] == "6"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 0, 1, 1]
        if(upc_matches[NumZero] == "7"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "8"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "9"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == "-"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "$"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 1]
        if(upc_matches[NumZero] == ":"):
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1]
        if(upc_matches[NumZero] == "/"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
        if(upc_matches[NumZero] == "."):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1]
        if(upc_matches[NumZero] == "+"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
        upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
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
        drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize,
                      barwidth[0], barcolor[2], imageoutlib)
        upc_array['code'].append([0])
        upc_array['barsize'].append(barsizeloop)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
        NumZero += 1
    end_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if(pre_upc_matches[2] == "A" or pre_upc_matches[2] == "T"):
        end_barcode = [1, 0, 1, 1, 0, 0, 1, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if(pre_upc_matches[2] == "B" or pre_upc_matches[2] == "N"):
        end_barcode = [1, 0, 0, 1, 0, 0, 1, 0, 1,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if(pre_upc_matches[2] == "C" or pre_upc_matches[2] == "*"):
        end_barcode = [1, 0, 1, 0, 0, 1, 0, 0, 1,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if(pre_upc_matches[2] == "D" or pre_upc_matches[2] == "E"):
        end_barcode = [1, 0, 1, 0, 0, 1, 1, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    LineTxtStart = ((shiftxy[0] + 20) * int(resize))
    LineTxtStartNorm = 20
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
        LineTxtStart += 11 * int(resize)
        LineTxtStartNorm += 11
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_codabar_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    pre_upc_matches = upc_matches = re.findall(
        "^([a-dA-DeEnN\\*tT])([0-9\\-\\$\\:\\/\\.\\+]+)([a-dA-DeEnN\\*tT])$", upc)
    pre_upc_matches = pre_upc_matches[0]
    upc_matches = list(pre_upc_matches[1])
    bcsize9 = len(re.findall("([0-9\\-\\$])", "".join(upc_matches)))
    bcsize10 = len(re.findall("([\\:\\/\\.])", "".join(upc_matches)))
    bcsize12 = len(re.findall("([\\+])", "".join(upc_matches)))
    upc_size_add = ((bcsize9 * 9) + (bcsize10 * 10) +
                    (bcsize12 * 12) + len(upc_matches) - 1) * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((40 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_codabar_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_codabar_barcode(upc, outfile="./codabar.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
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
    imgout = draw_codabar_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = "codabar; "+upc
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True
