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

    $FileInfo: upce.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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


def decode_upce_barcode(infile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
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
        # Handle Cairo ImageSurface input
        stdoutfile = BytesIO()
        infile[1].write_to_png(stdoutfile)
        stdoutfile.seek(0)
        upc_img = Image.open(stdoutfile).convert('RGB')
    else:
        # Assume input is a file path or file-like object
        try:
            infile.seek(0)  # Reset file pointer if file-like object
            upc_img = Image.open(infile).convert('RGB')
        except (AttributeError, UnidentifiedImageError, IOError):
            try:
                upc_img = Image.open(infile).convert('RGB')  # File path case
            except (UnidentifiedImageError, IOError):
                return False

    # Precompute common values
    barsize = barwidth[0] * resize
    starty = (upc_img.size[1] // 2) - ((barwidth[1] - 1) * 9) + shiftxy[1]
    
    fist_number_dict = {
        'EEEOOO': "0", 'EEOEOO': "0", 'EEOOEO': "0", 'EEOOOE': "0",
        'EOEEOO': "0", 'EOOEEO': "0", 'EOOOEE': "0", 'EOEOEO': "0",
        'EOEOOE': "0", 'EOOEOE': "0", 'OOOEEE': "1", 'OOEOEE': "1",
        'OOEEOE': "1", 'OOEEEO': "1", 'OEOOEE': "1", 'OEEOOE': "1",
        'OEEEOO': "1", 'OEOEOE': "1", 'OEOEEO': "1", 'OEEOEO': "9"
    }
    last_number_dict = {
        'EEEOOO': "0", 'EEOEOO': "1", 'EEOOEO': "2", 'EEOOOE': "3",
        'EOEEOO': "4", 'EOOEEO': "5", 'EOOOEE': "6", 'EOEOEO': "7",
        'EOEOOE': "8", 'EOOEOE': "9", 'OOOEEE': "0", 'OOEOEE': "1",
        'OOEEOE': "2", 'OOEEEO': "3", 'OEOOEE': "4", 'OEEOOE': "5",
        'OEEEOO': "6", 'OEOEOE': "7", 'OEOEEO': "8", 'OEEOEO': "9"
    }
    left_barcode_o_dict = {
        '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3",
        '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", 
        '0110111': "8", '0001011': "9"
    }
    left_barcode_e_dict = {
        '0100111': "0", '0110011': "1", '0011011': "2", '0100001': "3",
        '0011101': "4", '0111001': "5", '0000101': "6", '0010001': "7", 
        '0001001': "8", '0010111': "9"
    }

    # Define start and end positions for scanning
    startx = 12 * barsize + shiftxy[0]
    endx = 42 * barsize

    # If shiftcheck is enabled, adjust startx dynamically by checking pixel values
    if shiftcheck:
        prestartx = shiftxy[0]
        while prestartx < upc_img.size[0]:
            curpixel = upc_img.getpixel((prestartx, starty))
            if curpixel == barcolor[0]:  # Checking for a potential barcode start
                substartx = prestartx + (3 * barsize)
                pixel_list = [upc_img.getpixel((substartx + (i * barsize), starty)) for i in range(3)]
                # Validate the sequence of pixels to ensure it's the start of the barcode
                if pixel_list[0] == barcolor[0] and pixel_list[1] == barcolor[2] and pixel_list[2] == barcolor[0]:
                    startx = substartx  # Found the start
                    break
            prestartx += 1

    # Locate the barcode without decoding
    if locatebarcode:
        prestartx = startx - (3 * barsize)
        endx = startx + (42 * barsize)
        postendx = endx + (6 * barsize)

        # Scan vertically to find the barcode height
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

        # Return barcode location information
        return ("upce", prestartx, startx, 0, 0, endx, postendx, countyup, round(countyup / 2), round(countydown * 2), countydown, 8)

    # Extract the binary pattern from the barcode image
    def extract_barcode(startx):
        binary_values = []
        startxalt = 0
        
        while startxalt < endx:
            pre_upc_list = []
            for _ in range(7):
                curpixel = upc_img.getpixel((startx, starty))
                if curpixel == barcolor[0]:
                    incount = 0
                    inbarwidth = barwidth[0] - 1
                    while incount <= inbarwidth:
                        incurpixel = upc_img.getpixel((startx + incount, starty))
                        if incurpixel != barcolor[0]:
                            return False
                        incount += 1
                    pre_upc_list.append("1")
                elif curpixel == barcolor[2]:
                    incount = 0
                    inbarwidth = barwidth[0] - 1
                    while incount <= inbarwidth:
                        incurpixel = upc_img.getpixel((startx + incount, starty))
                        if incurpixel != barcolor[2]:
                            return False
                        incount += 1
                    pre_upc_list.append("0")
                startx += barsize
                startxalt += barsize
            binary_values.append("".join(pre_upc_list))
        
        return binary_values

    # Decode the binary list into digits
    def decode_barcode(binary_list):
        barcode = []
        parity_pattern_list = []
        for i, binary in enumerate(binary_list):
            if left_barcode_o_dict.get(binary) is not None:
                parity_pattern_list.append("O")
                barcode.append(left_barcode_o_dict[binary])
            elif left_barcode_e_dict.get(binary) is not None:
                parity_pattern_list.append("E")
                barcode.append(left_barcode_e_dict[binary])
            else:
                return False
        get_parity_pattern = "".join(parity_pattern_list)
        barcode.insert(0, fist_number_dict.get(get_parity_pattern, "0"))
        barcode.append(last_number_dict.get(get_parity_pattern, "0"))
        return "".join(barcode)

    # Extract the barcode binary data
    binary_barcode = extract_barcode(startx)
    
    if not binary_barcode:
        return False
    
    # Decode the binary values into a valid UPC-E barcode
    upce = decode_barcode(binary_barcode)
    return upce if upce else False


def get_upce_barcode_location(infile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_upce_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
