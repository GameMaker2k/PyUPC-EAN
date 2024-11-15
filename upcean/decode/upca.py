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

    $FileInfo: upca.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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


def decode_upca_barcode(infile, resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, cairosupport=False):
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
    starty = (upc_img.size[1] // 2) - ((barwidth[1] - 1) * 6) + shiftxy[1]
    left_barcode_dict = {
        '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3",
        '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", 
        '0110111': "8", '0001011': "9"
    }
    right_barcode_dict = {
        '1110010': "0", '1100110': "1", '1101100': "2", '1000010': "3",
        '1011100': "4", '1001110': "5", '1010000': "6", '1000100': "7", 
        '1001000': "8", '1110100': "9"
    }

    # Define start and end positions for scanning
    startx = 12 * barsize + shiftxy[0]
    jumpcode = 54 * barsize + shiftxy[0]
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
        return ("upca", prestartx, startx, jumpcode, jumpcodeend, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, 12)

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
        for i, binary in enumerate(binary_list):
            if i < 6:  # Left side encoding
                decoded = left_barcode_dict.get(binary)
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
    
    # Decode the binary values into a valid UPC-A barcode
    upc = decode_barcode(binary_barcode)
    return upc if upc else False


def get_upca_barcode_location(infile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_upca_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_ean12_barcode(infile="./ean12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_upca_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def decode_gtin12_barcode(infile="./gtin12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_upca_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_ean12_barcode_location(infile="./ean12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_ean12_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def get_gtin12_barcode_location(infile="./gtin12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_gtin12_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)


def decode_ucc12_barcode(infile="./ucc12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    return decode_upca_barcode(infile, resize, barheight, barwidth, barcolor, locatebarcode, imageoutlib)


def get_ucc12_barcode_location(infile="./ucc12.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return decode_ucc12_barcode(infile, resize, barheight, barwidth, shiftcheck, shiftxy, barcolor, True, imageoutlib)
