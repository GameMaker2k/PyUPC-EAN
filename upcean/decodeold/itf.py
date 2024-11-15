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

    $FileInfo: itf.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
from upcean.encode.predraw import *
import re
import upcean.encode.predraw.getsfname
import upcean.support
try:
    from PIL import Image, UnidentifiedImageError
    hasuie = True
except ImportError:
    from PIL import Image
    hasuie = False
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
if(cairosupport):
    import cairo


def decode_itf_barcode(infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    if(not re.findall(r"^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(isinstance(infile, Image.Image)):
        upc_img = infile.convert('RGB')
    elif(cairosupport and isinstance(infile, cairo.ImageSurface)):
        if(sys.version[0] == "2"):
            stdoutfile = StringIO()
        if(sys.version[0] >= "3"):
            stdoutfile = BytesIO()
        infile.write_to_png(stdoutfile)
        stdoutfile.seek(0)
        upc_img = Image.open(stdoutfile).convert('RGB')
    else:
        try:
            infile.seek(0)
            if(hasuie):
                try:
                    upc_img = Image.open(infile).convert('RGB')
                except UnidentifiedImageError:
                    return False
                    '''upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
            else:
                try:
                    upc_img = Image.open(infile).convert('RGB')
                except IOError:
                    return False
                    '''upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
        except AttributeError:
            if(hasuie):
                try:
                    upc_img = Image.open(infile).convert('RGB')
                except UnidentifiedImageError:
                    return False
                    '''prefile = open(infile, "rb");
     upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
     prefile.close();'''
            else:
                try:
                    upc_img = Image.open(infile).convert('RGB')
                except IOError:
                    return False
                    '''prefile = open(infile, "rb");
     upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
     prefile.close();'''
    threewidebar = True
    barsize = barwidth[0] * int(resize)
    starty = (int(upc_img.size[1] / 2) - ((barwidth[1] - 1) * 9)) + shiftxy[1]
    left_barcode_dict = {'00110': "0", '10001': "1", '01001': "2", '11000': "3",
                         '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9"}
    right_barcode_dict = {'00110': "0", '10001': "1", '01001': "2", '11000': "3",
                          '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9"}
    startx = 17
    if(shiftcheck):
        prestartx = shiftxy[0]
        startx = shiftxy[0]
        gotvalue = False
        barcodesize = 0
        while(prestartx < upc_img.size[0]):
            inprestartx = prestartx
            substartx = prestartx + (4 * (barwidth[0] * int(resize)))
            curpixelist = []
            if(upc_img.getpixel((inprestartx, starty)) == barcolor[0]):
                if(inprestartx+(4 * (barwidth[0] * int(resize))) > upc_img.size[0]):
                    return False
                if(threewidebar):
                    icount = 0
                    imaxc = 4
                    while(icount < imaxc):
                        curpixelist.append(upc_img.getpixel(
                            (inprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                        icount += 1
                    if((curpixelist[0] == barcolor[0] and curpixelist[1] == barcolor[2] and curpixelist[2] == barcolor[0] and curpixelist[3] == barcolor[2])):
                        preinprestartx = inprestartx + \
                            (4 * (barwidth[0] * int(resize)))
                        precurpixelist = []
                        while(preinprestartx < upc_img.size[0]):
                            precurpixelist = []
                            if((preinprestartx+(9 * (barwidth[0] * int(resize))) > upc_img.size[0])):
                                return False
                            icount = 0
                            imaxc = 9
                            while(icount < imaxc):
                                precurpixelist.append(upc_img.getpixel(
                                    (preinprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                                icount += 1
                            preinprestartx += (9 * (barwidth[0] * int(resize)))
                            barcodesize += 1
                            if((precurpixelist[0] == barcolor[0] and precurpixelist[1] == barcolor[0] and precurpixelist[2] == barcolor[0] and precurpixelist[3] == barcolor[2] and precurpixelist[4] == barcolor[0] and precurpixelist[5] == barcolor[2] and precurpixelist[6] == barcolor[2] and precurpixelist[7] == barcolor[2] and precurpixelist[8] == barcolor[2])):
                                break
                        barcodesize = int((barcodesize) / 2)
                        inprestartx += (4 + (barcodesize * 18)) * \
                            (barwidth[0] * int(resize))
                        icount = 0
                        imaxc = 5
                        while(icount < imaxc):
                            curpixelist.append(upc_img.getpixel(
                                (inprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                            icount += 1
                        if((curpixelist[0] == barcolor[0] and curpixelist[1] == barcolor[2] and curpixelist[2] == barcolor[0] and curpixelist[3] == barcolor[2]) and (curpixelist[4] == barcolor[0] and curpixelist[5] == barcolor[0] and curpixelist[6] == barcolor[0] and curpixelist[7] == barcolor[2] and curpixelist[8] == barcolor[0])):
                            startx = substartx
                            break
                else:
                    icount = 0
                    imaxc = 4
                    while(icount < imaxc):
                        curpixelist.append(upc_img.getpixel(
                            (inprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                        icount += 1
                    if((curpixelist[0] == barcolor[0] and curpixelist[1] == barcolor[2] and curpixelist[2] == barcolor[0] and curpixelist[3] == barcolor[2])):
                        preinprestartx = inprestartx + \
                            (4 * (barwidth[0] * int(resize)))
                        precurpixelist = []
                        while(preinprestartx < upc_img.size[0]):
                            precurpixelist = []
                            if((preinprestartx+(7 * (barwidth[0] * int(resize))) > upc_img.size[0])):
                                return False
                            icount = 0
                            imaxc = 7
                            while(icount < imaxc):
                                precurpixelist.append(upc_img.getpixel(
                                    (preinprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                                icount += 1
                            preinprestartx += (7 * (barwidth[0] * int(resize)))
                            barcodesize += 1
                            if((precurpixelist[0] == barcolor[0] and precurpixelist[1] == barcolor[0] and precurpixelist[2] == barcolor[2] and precurpixelist[3] == barcolor[0] and precurpixelist[4] == barcolor[2] and precurpixelist[5] == barcolor[2] and precurpixelist[6] == barcolor[2])):
                                break
                        barcodesize = int((barcodesize) / 2)
                        inprestartx += (4 + (barcodesize * 14)) * \
                            (barwidth[0] * int(resize))
                        icount = 0
                        imaxc = 4
                        while(icount < imaxc):
                            curpixelist.append(upc_img.getpixel(
                                (inprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                            icount += 1
                        if((curpixelist[0] == barcolor[0] and curpixelist[1] == barcolor[2] and curpixelist[2] == barcolor[0] and curpixelist[3] == barcolor[2]) and (curpixelist[4] == barcolor[0] and curpixelist[5] == barcolor[0] and curpixelist[6] == barcolor[2] and curpixelist[7] == barcolor[0])):
                            startx = substartx
                            break
            prestartx += 1
        shiftxy = (0, shiftxy[1])
    else:
        startx = ((17 * (barwidth[0] * int(resize))) + shiftxy[0])
        preinprestartx = startx
        precurpixelist = []
        barcodesize = 0
        while(preinprestartx < upc_img.size[0]):
            precurpixelist = []
            if(threewidebar):
                if((preinprestartx+(8 * (barwidth[0] * int(resize))) > upc_img.size[0])):
                    return False
                icount = 0
                imaxc = 9
                while(icount < imaxc):
                    precurpixelist.append(upc_img.getpixel(
                        (preinprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                    icount += 1
                preinprestartx += (9 * (barwidth[0] * int(resize)))
                barcodesize += 1
                if((precurpixelist[0] == barcolor[0] and precurpixelist[1] == barcolor[0] and precurpixelist[2] == barcolor[0] and precurpixelist[3] == barcolor[2] and precurpixelist[4] == barcolor[0] and precurpixelist[5] == barcolor[2] and precurpixelist[6] == barcolor[2] and precurpixelist[7] == barcolor[2] and precurpixelist[8] == barcolor[2])):
                    break
            else:
                if((preinprestartx+(6 * (barwidth[0] * int(resize))) > upc_img.size[0])):
                    return False
                icount = 0
                imaxc = 7
                while(icount < imaxc):
                    precurpixelist.append(upc_img.getpixel(
                        (preinprestartx+(icount * (barwidth[0] * int(resize))), starty)))
                    icount += 1
                preinprestartx += (7 * (barwidth[0] * int(resize)))
                barcodesize += 1
                if((precurpixelist[0] == barcolor[0] and precurpixelist[1] == barcolor[0] and precurpixelist[2] == barcolor[2] and precurpixelist[3] == barcolor[0] and precurpixelist[4] == barcolor[2] and precurpixelist[5] == barcolor[2] and precurpixelist[6] == barcolor[2])):
                    break
        barcodesize = int((barcodesize) / 2)
    endx = int(startx + ((barcodesize * 18) * (barwidth[0] * int(resize))))
    if(locatebarcode):
        endx -= (1 * (barwidth[0] * int(resize)))
    if(threewidebar):
        if(locatebarcode):
            postendx = endx + (5 * (barwidth[0] * int(resize)))
        endx = int(startx + ((barcodesize * 18) * (barwidth[0] * int(resize))))
    else:
        if(locatebarcode):
            postendx = endx + (4 * (barwidth[0] * int(resize)))
        endx = int(startx + ((barcodesize * 14) * (barwidth[0] * int(resize))))
    if(locatebarcode):
        prestartx = startx - (4 * (barwidth[0] * int(resize)))
        endx -= (1 * (barwidth[0] * int(resize)))
        countyup = starty
        while(countyup >= 0):
            curonepixel = upc_img.getpixel((prestartx, countyup))
            curtwopixel = upc_img.getpixel(
                (prestartx + (1 * (barwidth[0] * int(resize))), countyup))
            if(curonepixel == barcolor[2] or curtwopixel == barcolor[0]):
                break
            countyup += 1
        countyup -= 1
        countydown = starty
        while(countydown <= upc_img.size[1]):
            curonepixel = upc_img.getpixel((prestartx, countydown))
            curtwopixel = upc_img.getpixel(
                (prestartx + (1 * (barwidth[0] * int(resize))), countydown))
            if(curonepixel == barcolor[2] or curtwopixel == barcolor[0]):
                break
            countydown -= 1
        countydown -= 1
        return ("itf", prestartx, startx, 0, 0, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, (barcodesize * 2))
    listcount = 0
    pre_upc_whole_left = []
    pre_upc_whole_right = []
    pre_upc_list_left = []
    pre_upc_list_right = []
    skiptwo = False
    while(startx < endx):
        listcount = 0
        curpixel = upc_img.getpixel((startx, starty))
        if(curpixel == barcolor[0]):
            incount = 0
            inbarwidth = barwidth[0] - 1
            while(incount <= inbarwidth):
                incurpixel = upc_img.getpixel((startx + incount, starty))
                if(incurpixel != barcolor[0]):
                    return False
                incount += 1
            nexpixel = upc_img.getpixel(
                (startx + (1 * (barwidth[0] * int(resize))), starty))
            if(nexpixel == barcolor[0] and startx < (endx - (2 * (barwidth[0] * int(resize))) + 1)):
                incount = 0
                inbarwidth = barwidth[0] - 1
                while(incount <= inbarwidth):
                    incurpixel = upc_img.getpixel(
                        ((startx + (1 * (barwidth[0] * int(resize)))) + incount, starty))
                    if(incurpixel != barcolor[0]):
                        return False
                    incount += 1
                if(threewidebar):
                    incount = 0
                    inbarwidth = barwidth[0] - 1
                    while(incount <= inbarwidth):
                        incurpixel = upc_img.getpixel(
                            ((startx + (2 * (barwidth[0] * int(resize)))) + incount, starty))
                        if(incurpixel != barcolor[0]):
                            return False
                        incount += 1
                pre_upc_list_left.append("1")
                skiptwo = True
            else:
                pre_upc_list_left.append("0")
                skiptwo = False
        if(curpixel == barcolor[2]):
            incount = 0
            inbarwidth = barwidth[0] - 1
            while(incount <= inbarwidth):
                incurpixel = upc_img.getpixel((startx + incount, starty))
                if(incurpixel != barcolor[2]):
                    return False
                incount += 1
            nexpixel = upc_img.getpixel(
                (startx + (1 * (barwidth[0] * int(resize))), starty))
            if(nexpixel == barcolor[2] and startx < (endx - (2 * (barwidth[0] * int(resize))) + 1)):
                incount = 0
                inbarwidth = barwidth[0] - 1
                while(incount <= inbarwidth):
                    incurpixel = upc_img.getpixel(
                        ((startx + (1 * (barwidth[0] * int(resize)))) + incount, starty))
                    if(incurpixel != barcolor[2]):
                        return False
                    incount += 1
                if(threewidebar):
                    incount = 0
                    inbarwidth = barwidth[0] - 1
                    while(incount <= inbarwidth):
                        incurpixel = upc_img.getpixel(
                            ((startx + (2 * (barwidth[0] * int(resize)))) + incount, starty))
                        if(incurpixel != barcolor[2]):
                            return False
                        incount += 1
                pre_upc_list_right.append("1")
                skiptwo = True
            else:
                pre_upc_list_right.append("0")
                skiptwo = False
        if(skiptwo):
            if(threewidebar):
                startx += 3 * (barwidth[0] * int(resize))
            else:
                startx += 2 * (barwidth[0] * int(resize))
        else:
            startx += 1 * (barwidth[0] * int(resize))
    pre_upc_whole_left = "".join(pre_upc_list_left)
    pre_upc_whole_right = "".join(pre_upc_list_right)
    upc_img.close()
    pre_upc_whole_left_re = re.findall(r"([0-9]{5})", pre_upc_whole_left)
    pre_upc_whole_right_re = re.findall(r"([0-9]{5})", pre_upc_whole_right)
    countlist = barcodesize
    listcount = 0
    barcode_list = []
    fist_number_list = []
    while(listcount < countlist):
        left_barcode_value = left_barcode_dict.get(
            pre_upc_whole_left_re[listcount], False)
        if(not left_barcode_value):
            return False
        barcode_list.append(left_barcode_value)
        right_barcode_value = right_barcode_dict.get(
            pre_upc_whole_right_re[listcount], False)
        if(not right_barcode_value):
            return False
        barcode_list.append(right_barcode_value)
        listcount += 1
        upc = "".join(barcode_list)
    return upc


def get_itf_barcode_location(infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_itf_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_code25_interleaved_barcode(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_itf_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_code25_interleaved_barcode_location(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_code25_interleaved_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
