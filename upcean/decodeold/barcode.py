# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: barcode.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
from upcean.decodeold.stf import *
from upcean.decodeold.itf14 import *
from upcean.decodeold.itf import *
from upcean.decodeold.ean8 import *
from upcean.decodeold.ean13 import *
from upcean.decodeold.upce import *
from upcean.decodeold.upca import *
import upcean.support
import upcean.getprefix.getprefix

''' // Code for decoding UPC-A by Kazuki Przyborowski '''
try:
    import upcean.decodeold.upca as gtin12
    import upcean.decodeold.upca as ucc12
except:
    pass
''' // Code for decoding UPC-E by Kazuki Przyborowski '''
''' // Code for decoding EAN-13 by Kazuki Przyborowski '''
try:
    import upcean.decodeold.ean13 as gtin13
    import upcean.decodeold.ean13 as ucc13
except:
    pass
''' // Code for decoding EAN-8 by Kazuki Przyborowski '''
try:
    import upcean.decodeold.ean8 as gtin8
    import upcean.decodeold.ean8 as ucc8
except:
    pass
''' // Code for making Interleaved 2 of 5 by Kazuki Przyborowski '''
''' // Code for making ITF-14 by Kazuki Przyborowski '''
try:
    import upcean.decodeold.itf14 as itf6
except:
    pass
''' // Code for making Standard 2 of 5 by Kazuki Przyborowski '''
try:
    import upcean.decodeold.stf as code25
except:
    pass


def validate_decode_upca_barcode(infile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_upca_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return True


def validate_decode_upce_barcode(infile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_upce_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return True


def validate_decode_ean13_barcode(infile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_ean13_barcode(infile, resize, barheight, barwidth,
                               shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return True


def validate_decode_itf_barcode(infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_itf_barcode(infile, resize, barheight, barwidth,
                             shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return True


def validate_decode_itf6_barcode(infile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_itf6_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return True


def validate_decode_itf14_barcode(infile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), locatebarcode=False, imageoutlib="pillow"):
    upc = decode_itf14_barcode(infile, resize, barheight, barwidth,
                               shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return True


def fix_decode_upca_barcode(infile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_upca_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return upc


def fix_decode_upce_barcode(infile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_upce_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    return upc


def fix_decode_ean13_barcode(infile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_ean13_barcode(infile, resize, barheight, barwidth,
                               shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    return upc


def fix_decode_ean8_barcode(infile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_ean8_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    return upc


def fix_decode_itf_barcode(infile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_itf14_barcode(infile, resize, barheight, barwidth,
                               shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return upc


def fix_decode_itf6_barcode(infile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_itf6_barcode(infile, resize, barheight, barwidth,
                              shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return upc


def fix_decode_itf14_barcode(infile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), shiftcheck=False, shiftxy=(0, 0), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = decode_itf14_barcode(infile, resize, barheight, barwidth,
                               shiftcheck, shiftxy, barcolor, locatebarcode, imageoutlib)
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return upc
