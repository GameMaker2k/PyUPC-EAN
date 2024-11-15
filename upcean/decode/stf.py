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

    $FileInfo: stf.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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


def decode_stf_barcode(infile="./stf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    # Validate resize input
    if not isinstance(resize, (int, float)) or int(resize) < 1:
        resize = 1

    # Load image
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

    # Define barcode dictionary for decoding
    barcode_dict = {
        '10101110111010': "0", '11101010101110': "1", '10111010101110': "2",
        '11101110101010': "3", '10101110101110': "4", '11101011101010': "5",
        '10111011101010': "6", '10101011101110': "7", '11101010111010': "8",
        '10111010111010': "9"
    }

    # Calculate barsize and starty position
    barsize = barwidth[0] * int(resize)
    starty = (int(upc_img.size[1] / 2) - ((barwidth[1] - 1) * 9)) + shiftxy[1]

    # Determine startx based on shiftcheck
    if shiftcheck:
        prestartx = shiftxy[0]
        startx = shiftxy[0]
        gotvalue = False
        while prestartx < upc_img.size[0]:
            inprestartx = prestartx
            substartx = prestartx + (8 * (barwidth[0] * int(resize)))
            curpixelist = []
            if upc_img.getpixel((inprestartx, starty)) == barcolor[0]:
                if inprestartx + (8 * (barwidth[0] * int(resize))) > upc_img.size[0]:
                    return False
                # Extract pixel list for decoding
                for i in range(8):
                    curpixelist.append(upc_img.getpixel((inprestartx + (i * (barwidth[0] * int(resize))), starty)))
                # Condition to match the startx position
                if curpixelist[0] == barcolor[0] and curpixelist[7] == barcolor[2]:
                    startx = substartx
                    break
            prestartx += 1
        shiftxy = (0, shiftxy[1])
    else:
        startx = ((21 * (barwidth[0] * int(resize))) + shiftxy[0])

    # Calculate barcode size
    barcodesize = 12
    endx = startx + (barcodesize * 14 * barsize)

    # If locatebarcode is enabled
    if locatebarcode:
        prestartx = startx - (8 * (barwidth[0] * int(resize)))
        countyup = starty
        while countyup >= 0:
            if upc_img.getpixel((prestartx, countyup)) == barcolor[2]:
                break
            countyup -= 1
        countydown = starty
        while countydown < upc_img.size[1]:
            if upc_img.getpixel((prestartx, countydown)) == barcolor[2]:
                break
            countydown += 1
        return ("stf", prestartx, startx, 0, 0, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, barcodesize)

    # Decode the barcode
    binary_sequence = []
    while startx < endx:
        curpixelist = []
        for _ in range(14):
            curpixel = upc_img.getpixel((startx, starty))
            if curpixel == barcolor[0]:
                curpixelist.append("1")
            elif curpixel == barcolor[2]:
                curpixelist.append("0")
            startx += barsize
        binary_sequence.append("".join(curpixelist))

    # Close the image
    upc_img.close()

    # Decode binary sequences into barcode digits
    decoded_digits = []
    for binary_seq in binary_sequence:
        digit = barcode_dict.get(binary_seq, False)
        if not digit:
            return False
        decoded_digits.append(digit)

    # Join digits into final barcode
    return "".join(decoded_digits)


def get_stf_barcode_location(infile="./stf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_stf_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_code25_barcode(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_stf_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_code25_barcode_location(infile="./code25.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_code25_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
