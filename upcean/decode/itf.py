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

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.predraw import *
import re
import upcean.predraw.getsfname
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
    # Validate resize value (should be a positive number greater than or equal to 1)
    try:
        resize = float(resize)
        if resize < 1:
            resize = 1
    except ValueError:
        resize = 1

    # Check if input is a Pillow Image, Cairo ImageSurface, or file path
    if isinstance(infile, list) and isinstance(infile[1], Image.Image):
        upc_img = infile[1].convert('RGB')
    elif cairosupport and isinstance(infile, list) and isinstance(infile[0], cairo.Context):
        stdoutfile = io.BytesIO()
        infile[1].write_to_png(stdoutfile)
        stdoutfile.seek(0)
        upc_img = Image.open(stdoutfile).convert('RGB')
    else:
        try:
            infile.seek(0)
            upc_img = Image.open(infile).convert('RGB')
        except (AttributeError, IOError):
            return False

    # Precompute common values
    barsize = barwidth[0] * resize
    starty = (upc_img.size[1] // 2) - ((barwidth[1] - 1) * 9) + shiftxy[1]
    
    left_barcode_dict = {
        '00110': "0", '10001': "1", '01001': "2", '11000': "3",
        '00101': "4", '10100': "5", '01100': "6", '00011': "7", 
        '10010': "8", '01010': "9"
    }
    right_barcode_dict = {
        '00110': "0", '10001': "1", '01001': "2", '11000': "3",
        '00101': "4", '10100': "5", '01100': "6", '00011': "7", 
        '10010': "8", '01010': "9"
    }

    # Determine barcode type and calculate end positions
    startx = 17 * barsize + shiftxy[0]
    preinprestartx = startx
    barcodesize = 0

    # If shiftcheck is enabled, adjust startx dynamically by checking pixel values
    if shiftcheck:
        prestartx = shiftxy[0]
        while prestartx < upc_img.size[0]:
            curpixel = upc_img.getpixel((prestartx, starty))
            if curpixel == barcolor[0]:
                substartx = prestartx + (4 * barsize)
                pixel_list = [upc_img.getpixel((substartx + (i * barsize), starty)) for i in range(4)]
                if pixel_list[0] == barcolor[0] and pixel_list[1] == barcolor[2] and pixel_list[2] == barcolor[0] and pixel_list[3] == barcolor[2]:
                    startx = substartx
                    break
            prestartx += 1

    # Calculate the endx value based on barcodesize
    preinprestartx = startx
    precurpixelist = []
    barcodesize = 0
    while preinprestartx < upc_img.size[0]:
        precurpixelist = []
        if (preinprestartx + (9 * barsize)) > upc_img.size[0]:
            return False
        icount = 0
        imaxc = 9
        while icount < imaxc:
            precurpixelist.append(upc_img.getpixel((preinprestartx + (icount * barsize), starty)))
            icount += 1
        preinprestartx += (9 * barsize)
        barcodesize += 1
        if (precurpixelist[0] == barcolor[0] and precurpixelist[1] == barcolor[0] and precurpixelist[2] == barcolor[0] and precurpixelist[3] == barcolor[2] and precurpixelist[4] == barcolor[0] and precurpixelist[5] == barcolor[2] and precurpixelist[6] == barcolor[2] and precurpixelist[7] == barcolor[2] and precurpixelist[8] == barcolor[2]):
            break
    barcodesize = int(barcodesize / 2)
    endx = int(startx + ((barcodesize * 18) * barsize))

    # Adjust for locating the barcode without decoding
    if locatebarcode:
        prestartx = startx - (4 * barsize)
        countyup = starty
        while countyup >= 0:
            curonepixel = upc_img.getpixel((prestartx, countyup))
            curtwopixel = upc_img.getpixel((prestartx + barsize, countyup))
            if curonepixel == barcolor[2] or curtwopixel == barcolor[0]:
                break
            countyup -= 1

        countydown = starty
        while countydown < upc_img.size[1]:
            curonepixel = upc_img.getpixel((prestartx, countydown))
            curtwopixel = upc_img.getpixel((prestartx + barsize, countydown))
            if curonepixel == barcolor[2] or curtwopixel == barcolor[0]:
                break
            countydown += 1

        return ("itf", prestartx, startx, 0, 0, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, (barcodesize * 2))

    # Extract the binary pattern from the barcode image, considering wide/narrow bars
    def extract_barcode(startx, endx):
        pre_upc_list_left = []
        pre_upc_list_right = []
        skiptwo = False

        def detect_bar_width(startx):
            """ Detect if the bar is wide or narrow """
            cur_width = 1
            while (startx + cur_width < upc_img.size[0] and
                   upc_img.getpixel((startx, starty)) == upc_img.getpixel((startx + cur_width, starty))):
                cur_width += 1
            return cur_width

        while startx < endx:
            curpixel = upc_img.getpixel((startx, starty))
            bar_width = detect_bar_width(startx)

            if curpixel == barcolor[0]:  # Black bar
                if bar_width > barsize:  # Wide bar
                    pre_upc_list_left.append("1")
                else:  # Narrow bar
                    pre_upc_list_left.append("0")
            elif curpixel == barcolor[2]:  # White bar (space)
                if bar_width > barsize:  # Wide space
                    pre_upc_list_right.append("1")
                else:  # Narrow space
                    pre_upc_list_right.append("0")

            # Move forward based on the width of the current bar/space
            startx += bar_width

        pre_upc_whole_left = "".join(pre_upc_list_left)
        pre_upc_whole_right = "".join(pre_upc_list_right)

        return pre_upc_whole_left, pre_upc_whole_right

    # Decode the binary list into digits
    def decode_barcode(pre_upc_whole_left, pre_upc_whole_right):
        pre_upc_whole_left_re = re.findall("([01]{5})", pre_upc_whole_left)
        pre_upc_whole_right_re = re.findall("([01]{5})", pre_upc_whole_right)

        barcode_list = []

        for left_part, right_part in zip(pre_upc_whole_left_re, pre_upc_whole_right_re):
            left_barcode_value = left_barcode_dict.get(left_part)
            right_barcode_value = right_barcode_dict.get(right_part)

            if not left_barcode_value or not right_barcode_value:
                return False

            barcode_list.append(left_barcode_value)
            barcode_list.append(right_barcode_value)

        return "".join(barcode_list)

    # Extract and decode the barcode
    pre_upc_whole_left, pre_upc_whole_right = extract_barcode(startx, endx)

    if not pre_upc_whole_left or not pre_upc_whole_right:
        return False

    # Decode the binary values into a valid ITF barcode
    itf_barcode = decode_barcode(pre_upc_whole_left, pre_upc_whole_right)
    
    if not itf_barcode:
        return False
    
    return itf_barcode


def get_itf_barcode_location(infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_itf_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_code25_interleaved_barcode(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_itf_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_code25_interleaved_barcode_location(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_code25_interleaved_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
