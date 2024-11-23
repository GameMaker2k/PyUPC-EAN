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

    $FileInfo: binary.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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

import upcean.encode.ean2
import upcean.encode.ean5
pilsupport = upcean.support.check_for_pil()
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


def get_binary_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    upc_size_add_wo_shift = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    upc_size_add_w_shift = (len([item for sublist in upc['code'] for item in sublist]) + shiftxy[0]) * (barwidth[0] * int(resize))
    reswoshift = (upc_size_add_wo_shift, (barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize))
    reswshift = (upc_size_add_w_shift, ((barheightadd + shiftxy[1]) + ((upc['heightadd'] + shiftxy[1]) * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_binary_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
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
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
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
    upc_size_add = (len([item for sublist in upc['code'] for item in sublist]) + shiftxy[0]) * (barwidth[0] * int(resize))
    drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), upc_size_add, ((barheightadd + shiftxy[1]) + ((upc['heightadd'] + shiftxy[1]) * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    bari = 0
    barmax = len(upc['code'])
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    while(bari < barmax):
        subbari = 0
        subbarmax = len(upc['code'][bari])
        while(subbari < subbarmax):
            if(hidetext):
                LineSize = (barheight[1] + shiftxy[1]) * int(resize)
            else:
                LineSizeNum = upc['barsize'][bari][subbari]
                LineSize = (barheight[LineSizeNum] + shiftxy[1]) * int(resize)
            if(upc['code'][bari][subbari] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            elif(upc['code'][bari][subbari] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            subbari += 1
            LineStart += barwidth[0] * int(resize)
        bari += 1
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
    txtbari = 0
    txtbarmax = len(upc['text']['text'])
    LineFixTxtStart = 0
    if(tkintersupport and imageoutlib == "tkinter"):
        LineFixTxtStart = 4
    elif(svgwritesupport and not cairosvgsupport and imageoutlib == "svgwrite"):
        LineTxtStart = 1
    while(txtbari < txtbarmax):
        texthidden = False
        if hidetext or (upc['text']['type'][txtbari] == "sn" and (hidesn is None or hidesn)) or (upc['text']['type'][txtbari] == "cd" and (hidecd is None or hidecd)):
            texthidden = True
        if(not texthidden):
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (shiftxy[0] + ((upc['text']['location'][txtbari] + LineFixTxtStart) * int(resize))) * barwidth[0], vertical_text_fix + (barheight[0] * int(resize)),  upc['text']['text'][txtbari], barcolor[1], "ocrb", imageoutlib)

        txtbari += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc
    else:
        return [upc_img, upc_preimg, imageoutlib]

def draw_binary_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(imageoutlib not in imagelibsupport):
        imageoutlib = defaultdraw
    upc_size_add = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    upc_img, upc_preimg = upcean.predraw.new_image_surface(upc_size_add, (barheightadd + (upc['heightadd'] * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_binary_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo, imageoutlib)
    return [upc_img, upc_preimg, imageoutlib]

def create_binary_barcode(upc, outfile="./binary.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
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
    imgout = draw_binary_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        if(imagecomment is None):
            imagecomment = upc['type']+"; "+upc['upc']
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, imagecomment, imageoutlib)
    return True
