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

    $FileInfo: barcode.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.encode.msi import *
from upcean.encode.plessey import *
from upcean.encode.codabar import *
from upcean.encode.code128 import *
from upcean.encode.code93 import *
from upcean.encode.code39 import *
from upcean.encode.code32 import *
from upcean.encode.code11 import *
from upcean.encode.itf14 import *
from upcean.encode.itf import *
from upcean.encode.stf import *
from upcean.encode.ean8 import *
from upcean.encode.ean13 import *
from upcean.encode.upce import *
from upcean.encode.goodwill import *
from upcean.encode.upca import *
from upcean.encode.ean5 import *
from upcean.encode.ean2 import *
import upcean.support
import upcean.getprefix.getprefix

''' // Code for making EAN-2 supplement by Kazuki Przyborowski '''
''' // Code for making EAN-5 supplement by Kazuki Przyborowski '''
''' // Code for making UPC-A by Kazuki Przyborowski '''
try:
    import upcean.encode.upca as gtin12
    import upcean.encode.upca as ucc12
except:
    pass
''' // Code for making Goodwill Barcodes by Kazuki Przyborowski '''
''' // Code for making UPC-E by Kazuki Przyborowski '''
''' // Code for making EAN-13 by Kazuki Przyborowski '''
try:
    import upcean.encode.ean13 as gtin13
    import upcean.encode.ean13 as ucc13
except:
    pass
''' // Code for making EAN-8 by Kazuki Przyborowski '''
try:
    import upcean.encode.ean8 as gtin8
    import upcean.encode.ean8 as ucc8
except:
    pass
''' // Code for making Standard 2 of 5 by Kazuki Przyborowski '''
try:
    import upcean.encode.stf as code25
except:
    pass
''' // Code for making Interleaved 2 of 5 by Kazuki Przyborowski '''
''' // Code for making ITF-14 by Kazuki Przyborowski '''
try:
    import upcean.encode.itf14 as itf6
except:
    pass
''' // Code for making Code 11 by Kazuki Przyborowski '''
''' // Code for making Code 32 by Kazuki Przyborowski '''
try:
    import upcean.encode.code32 as pharmacode
except:
    pass
''' // Code for making Code 39 by Kazuki Przyborowski '''
''' // Code for making Code 93 by Kazuki Przyborowski '''
''' // Code for making Code 128 by Kazuki Przyborowski '''
''' // Code for making Codabar by Kazuki Przyborowski '''
''' // Code for making Plessey by Kazuki Przyborowski '''
''' // Code for making Modified Plessey by Kazuki Przyborowski '''


def validate_create_upca_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upca_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_upca_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upca_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_upca_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return encode_upca_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_upcaean_barcode(upc, outfile="./goodwill.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upcaean_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_upcaean_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upcaean_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_upcaean_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return encode_upcaean_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_upce_barcode(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return create_upce_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_upce_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return draw_upce_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)

def validate_encode_upce_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return encode_upce_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_ean13_barcode(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return create_ean13_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_ean13_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return draw_ean13_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)

def validate_encode_ean13_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return encode_ean13_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_ean8_barcode(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return create_ean8_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_ean8_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return draw_ean8_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_ean8_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return encode_ean8_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_itf_barcode(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_itf_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_itf_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return encode_itf_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return create_itf6_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return draw_itf6_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return encode_itf6_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def validate_create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf14_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf14_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_encode_itf14_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return encode_itf14_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_upca_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return create_upca_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_upca_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return draw_upca_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_upca_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return encode_upca_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_upcaean_barcode(upc, outfile="./goodwill.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return create_upcaean_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_upcaean_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return draw_upcaean_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_upcaean_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    return encode_upcaean_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_upce_barcode(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    return create_upce_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_upce_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    return draw_upce_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_upce_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    return encode_upce_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_ean13_barcode(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    return create_ean13_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_ean13_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    return draw_ean13_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_ean13_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    return encode_ean13_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_ean8_barcode(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    return create_ean8_barcode(upc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_draw_ean8_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    return draw_ean8_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_encode_ean8_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    return encode_ean8_barcode(inimage, upc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo)


def fix_create_itf_barcode(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_encode_itf_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return encode_itf_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return create_itf6_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return draw_itf6_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return encode_itf6_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf14_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf14_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)

def fix_encode_itf14_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return encode_itf14_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)

def encode_barcode_from_binary(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    upc_img = inimage[0]
    upc_preimg = inimage[1]
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwrite and imageoutlib == "svgwrite")):
        pil_addon_fix = 0
        cairo_addon_fix = (8 * (int(resize) * barwidth[1]))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    cairo_addon_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_size_add = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    drawColorRectangle(upc_img, 0 + shiftxy[0], 0 + shiftxy[1], upc_size_add, ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    bari = 0
    barmax = len(upc['code'])
    LineStart = shiftxy[0]
    while(bari < barmax):
        subbari = 0
        subbarmax = len(upc['code'][bari])
        while(subbari < subbarmax):
            if(upc['code'][bari][subbari] == 1):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          upc['barsize'][bari][subbari], barwidth[0] * int(resize), barcolor[0], imageoutlib)
            elif(upc['code'][bari][subbari] == 0):
                drawColorLine(upc_img, LineStart, (10 + shiftxy[1]) * int(resize), LineStart,
                          upc['barsize'][bari][subbari], barwidth[0] * int(resize), barcolor[2], imageoutlib)
            subbari += 1
            LineStart += barwidth[0] * int(resize)
        bari += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    return [upc_img, upc_preimg, imageoutlib, upc]


def draw_barcode_from_binary(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    upc_size_add = len([item for sublist in upc['code'] for item in sublist]) * (barwidth[0] * int(resize))
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", ((upc_size_add, (barheightadd + (9 * barwidth[1])) * int(resize))))
        upc_img = ImageDraw.Draw(upc_preimg)
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        upc_preimg = cairo.RecordingSurface(
                cairo.CONTENT_COLOR, (0.0, 0.0, float(upc_size_add), float((barheightadd + (9 * barwidth[1])) * int(resize))))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
    elif(svgwritesupport and imageoutlib=="svgwrite"):
        upc_preimg = StringIO()
        upc_img = svgwrite.Drawing(upc_preimg, profile='full', size=(upc_size_add, (barheightadd + (9 * barwidth[1])) * int(resize)))
        upc_preimg.close()
    imgout = encode_barcode_from_binary((upc_img, upc_preimg), upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib, upc]

def create_barcode_from_binary(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib="pillow"):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport and not svgwritesupport):
        return False
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
        oldoutfile = upcean.encode.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    imgout = draw_barcode_from_binary(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    exargdict = {'comment': "barcode; "+upc['upc']}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib, imgout[3]]
    else:
        if(outfileext == "WEBP"):
            exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
        if(outfileext == "HEIC"):
            exargdict.update({'lossless': True, 'quality': 100})
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 100, 'optimize': True, 'progressive': True})
        elif(outfileext == "GIF"):
            exargdict.update(
                {'optimize': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9, 'quality': 100})
            if(pilsupport):
                # Add a comment to the image
                info = PngImagePlugin.PngInfo()
                info.add_text("Comment", "upca; "+upc)
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': "barcode; "+upc['upc']}
        if(svgwritesupport and imageoutlib == "svgwrite"):
                if isinstance(outfile, file):
                    upc_img.write(outfile, True)
                else:
                    upc_img.saveas(outfile, True)
        if(pilsupport and imageoutlib == "pillow"):
            if outfileext == "XPM":
                # XPM supports only palette-based images ("P" mode)
                upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            elif outfileext == "XBM":
                # XBM supports only 1-bit images ("1" mode)
                upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
            elif outfileext == "PBM":
                # PBM (Portable Bitmap) supports only monochrome (1-bit) images ("1" mode)
                upc_preimg.convert(mode="1").save(outfile, outfileext, **exargdict)
            elif outfileext == "PGM":
                # PGM (Portable Graymap) supports only grayscale images ("L" mode)
                upc_preimg.convert(mode="L").save(outfile, outfileext, **exargdict)
            elif outfileext == "GIF":
                # GIF supports only palette-based images with a maximum of 256 colors ("P" mode)
                upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            elif outfileext == "ICO":
                # ICO generally supports "L", "P", and "RGBA" but not direct "RGB".
                # Convert to RGBA for transparency support if available, or "P" otherwise.
                if "A" in upc_preimg.getbands():  # Check if alpha channel is present
                    upc_preimg.convert(mode="RGBA").save(outfile, outfileext, **exargdict)
                else:
                    upc_preimg.convert(mode="P").save(outfile, outfileext, **exargdict)
            else:
                # If image is RGBA, convert to RGB to discard transparency; otherwise, save as-is
                if upc_preimg.mode == "RGBA":
                    upc_preimg.convert(mode="RGB").save(outfile, outfileext, **exargdict)
                else:
                    upc_preimg.save(outfile, outfileext, **exargdict)
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            x, y, width, height = upc_preimg.ink_extents()
            if(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                if(outfileext == "SVG" or imageoutlib == "cairosvg"):
                    # Create an ImageSurface with the exact dimensions of the recorded content
                    image_surface = cairo.SVGSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
                elif(outfileext == "PDF"):
                    # Create an ImageSurface with the exact dimensions of the recorded content
                    image_surface = cairo.PDFSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
                elif(outfileext == "PS" or outfileext == "EPS"):
                    # Create an PDFSurface with the exact dimensions of the recorded content
                    image_surface = cairo.PSSurface(outfile, int(width), int(height))
                    image_context = cairo.Context(image_surface)
                    # Transfer the content from the RecordingSurface to the ImageSurface
                    image_context.set_source_surface(upc_preimg, -x, -y)
                    if(outfileext == "EPS"):
                        image_surface.set_eps(True)
                    else:
                        image_surface.set_eps(False)
                    image_context.paint()
                    image_surface.flush()
                    image_surface.finish()
            else:
                # Create an ImageSurface with the exact dimensions of the recorded content
                image_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, int(width), int(height))
                image_context = cairo.Context(image_surface)
                # Transfer the content from the RecordingSurface to the ImageSurface
                image_context.set_source_surface(upc_preimg, -x, -y)
                image_context.paint()
                image_surface.flush()
                # Save as PNG
                image_surface.write_to_png(outfile)
                image_surface.finish()
                return True
    return True
