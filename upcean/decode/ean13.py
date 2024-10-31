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
from upcean.encode.predraw import *
import re
import upcean.encode.getsfname
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


def decode_ean13_barcode(infile, resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, cairosupport=False):
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
        'LLLLLL': "0", 'LLGLGG': "1", 'LLGGLG': "2", 'LLGGGL': "3",
        'LGLLGG': "4", 'LGGLLG': "5", 'LGGGLL': "6", 'LGLGLG': "7", 
        'LGLGGL': "8", 'LGGLGL': "9"
    }
    left_barcode_l_dict = {
        '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3",
        '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", 
        '0110111': "8", '0001011': "9"
    }
    left_barcode_g_dict = {
        '0100111': "0", '0110011': "1", '0011011': "2", '0100001': "3",
        '0011101': "4", '0111001': "5", '0000101': "6", '0010001': "7", 
        '0001001': "8", '0010111': "9"
    }
    right_barcode_dict = {
        '1110010': "0", '1100110': "1", '1101100': "2", '1000010': "3",
        '1011100': "4", '1001110': "5", '1010000': "6", '1000100': "7", 
        '1001000': "8", '1110100': "9"
    }

    # Define start and end positions for scanning
    startx = 14 * barsize + shiftxy[0]
    jumpcode = 56 * barsize + shiftxy[0]
    endx = (42 + 42) * barsize

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
        jumpcodeend = jumpcode + (4 * barsize)
        endx = startx + ((42 + 4 + 42) * barsize)
        postendx = endx + (3 * barsize)

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
        return ("ean13", prestartx, startx, jumpcode, jumpcodeend, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, 13)

    # Extract the binary pattern from the barcode image
    def extract_barcode(startx):
        binary_values = []
        startxalt = 0
        
        while startxalt < endx:
            pre_upc_list = []
            for _ in range(7):
                if startx == jumpcode:
                    startx += 5 * barsize
                
                curpixel = upc_img.getpixel((startx, starty))
                if curpixel == barcolor[0]:
                    pre_upc_list.append("1")
                elif curpixel == barcolor[2]:
                    pre_upc_list.append("0")
                else:
                    return False
                startx += barsize
                startxalt += barsize
            binary_values.append("".join(pre_upc_list))
        
        return binary_values

    # Decode the binary list into digits
    def decode_barcode(binary_list):
        barcode = []
        fist_number_list = []
        for i, binary in enumerate(binary_list):
            if i < 6:  # Left side encoding
                if left_barcode_l_dict.get(binary) is not None:
                    fist_number_list.append("L")
                    barcode.append(left_barcode_l_dict[binary])
                elif left_barcode_g_dict.get(binary) is not None:
                    fist_number_list.append("G")
                    barcode.append(left_barcode_g_dict[binary])
                else:
                    return False
            elif i == 6:  # Get the first digit
                get_fist_number = "".join(fist_number_list)
                first_num_value = fist_number_dict.get(get_fist_number, False)
                if not first_num_value:
                    return False
                barcode.insert(0, first_num_value)
            else:  # Right side encoding
                decoded = right_barcode_dict.get(binary)
                if decoded is None:
                    return False
                barcode.append(decoded)
        return "".join(barcode)

    # Extract the barcode binary data
    binary_barcode = extract_barcode(startx)
    
    if not binary_barcode:
        return False
    
    # Decode the binary values into a valid EAN-13 barcode
    ean13 = decode_barcode(binary_barcode)
    return ean13 if ean13 else False


def get_ean13_barcode_location(infile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_ean13_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_gtin13_barcode(infile="./gtin13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_ean13_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_gtin13_barcode_location(infile="./gtin13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_gtin13_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_ucc13_barcode(infile="./ucc13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_ean13_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_ucc13_barcode_location(infile="./ucc13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_ucc13_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
