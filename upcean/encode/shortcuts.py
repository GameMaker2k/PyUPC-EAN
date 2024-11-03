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

    $FileInfo: shortcuts.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean.encode.barcode
import upcean.xml.files
import upcean.support

''' // Shortcut Codes by Kazuki Przyborowski '''


def encode_barcode(bctype, inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.encode.barcode, "encode_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "encode_"+bctype+"_barcode"))):
        return getattr(upcean.encode.barcode, "encode_"+bctype+"_barcode")(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    if(not hasattr(upcean.encode.barcode, "encode_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "encode_"+bctype+"_barcode"))):
        return False
    return False


def draw_barcode(bctype, upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.encode.barcode, "draw_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "draw_"+bctype+"_barcode"))):
        return getattr(upcean.encode.barcode, "draw_"+bctype+"_barcode")(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    if(not hasattr(upcean.encode.barcode, "draw_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "draw_"+bctype+"_barcode"))):
        return False
    return False


def create_barcode(bctype, upc, outfile="./barcode.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.encode.barcode, "create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "create_"+bctype+"_barcode"))):
        return getattr(upcean.encode.barcode, "create_"+bctype+"_barcode")(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    if(not hasattr(upcean.encode.barcode, "create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "create_"+bctype+"_barcode"))):
        return False
    return False


def validate_encode_barcode(bctype, inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "validate_encode_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "validate_encode_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "validate_encode_"+bctype+"_barcode")(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "validate_encode_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "validate_encode_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return encode_barcode(bctype, inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_barcode(bctype, upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "validate_draw_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "validate_draw_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "validate_draw_"+bctype+"_barcode")(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "validate_draw_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "validate_draw_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return draw_barcode(bctype, upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_barcode(bctype, upc, outfile="./barcode.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode")(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return create_barcode(bctype, upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_barcode(bctype, inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "fix_encode_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "fix_encode_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "fix_encode_"+bctype+"_barcode")(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "fix_encode_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "fix_encode_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return encode_barcode(bctype, inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_barcode(bctype, upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "fix_draw_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "fix_draw_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "fix_draw_"+bctype+"_barcode")(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "fix_draw_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "fix_draw_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return draw_barcode(bctype, upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_barcode(bctype, upc, outfile="./barcode.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(bctype == "upca" or bctype == "goodwill" or bctype == "upce" or bctype == "ean13" or bctype == "ean8" or bctype == "itf" or bctype == "itf6" or bctype == "itf14"):
        if(hasattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode"))):
            return getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode")(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
        if(not hasattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode"))):
            return False
        return False
    if(bctype != "upca" and bctype != "goodwill" and bctype != "upce" and bctype != "ean13" and bctype != "ean8" and bctype != "itf" and bctype != "itf6" and bctype != "itf14"):
        return create_barcode(bctype, upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
