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

    $FileInfo: barcode.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
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
from upcean.encode.binary import *
from upcean.encode.upca import *
from upcean.encode.upcavar import *
from upcean.encode.ean5 import *
from upcean.encode.ean2 import *
import upcean.support
import upcean.getprefix.getprefix
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
drawlibsupport = upcean.support.check_for_drawlib()
imagelibsupport = upcean.support.imagelibsupport
defaultdraw = upcean.support.defaultdraw

def validate_create_upca_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upca_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upca_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upca_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_upca_barcode_sheet(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upca_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upca_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upca_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)

def validate_encode_upca_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return encode_upca_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_upcaean_barcode(upc, outfile="./goodwill.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upcaean_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upcaean_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upcaean_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_upcaean_barcode_sheet(upc, outfile="./goodwill.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return create_upcaean_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upcaean_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return draw_upcaean_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_upcaean_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    return encode_upcaean_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_upce_barcode(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return create_upce_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upce_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return draw_upce_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)

def validate_create_upce_barcode_sheet(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return create_upce_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_upce_barcod_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return draw_upce_barcode_sheet(fullfullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)

def validate_encode_upce_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    return encode_upce_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_ean13_barcode(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return create_ean13_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_ean13_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return draw_ean13_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_ean13_barcode_sheet(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return create_ean13_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_ean13_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return draw_ean13_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_ean13_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    return encode_ean13_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_ean8_barcode(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return create_ean8_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_ean8_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return draw_ean8_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_ean8_barcode_sheet(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return create_ean8_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_ean8_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return draw_ean8_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_ean8_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    return encode_ean8_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf_barcode(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf_barcode_sheet(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf_barcode_sheet(fullfullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_itf_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return encode_itf_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return create_itf6_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return draw_itf6_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf6_barcode_sheet(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return create_itf6_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf6_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return draw_itf6_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 6 or len(upc) < 6):
        return False
    if(not upcean.validate.validate_itf6_checksum(upc)):
        return False
    return encode_itf6_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf14_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf14_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def validate_create_itf14_barcode_sheet(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return create_itf14_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def validate_draw_itf14_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return draw_itf14_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def validate_encode_itf14_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    return encode_itf14_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upca_barcode(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upca_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upca_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upca_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upca_barcode_sheet(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upca_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upca_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upca_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def fix_encode_upca_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return encode_upca_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upcaean_barcode(upc, outfile="./goodwill.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upcaean_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upcaean_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upcaean_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upcaean_barcode_sheet(upc, outfile="./upca.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upcaean_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upcaean_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upcaean_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def fix_encode_upcaean_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 11):
        return False
    upc = upcean.validate.fix_upca_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return encode_upcaean_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upce_barcode(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upce_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upce_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upce_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_upce_barcode_sheet(upc, outfile="./upce.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_upce_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_upce_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_upce_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def fix_encode_upce_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_upce_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return encode_upce_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_ean13_barcode(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_ean13_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_ean13_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_ean13_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_ean13_barcode_sheet(upc, outfile="./ean13.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_ean13_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_ean13_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_ean13_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def fix_encode_ean13_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 13 or len(upc) < 12):
        return False
    upc = upcean.validate.fix_ean13_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return encode_ean13_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_ean8_barcode(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_ean8_barcode(fullupc, outfile, resize, barheight, barwidth, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_ean8_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_ean8_barcode(fullupc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_ean8_barcode_sheet(upc, outfile="./ean8.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return create_ean8_barcode_sheet(fullupc, outfile, resize, barheight, barwidth, numxy, barcolor, hideinfo, imagecomment, imageoutlib)


def fix_draw_ean8_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return draw_ean8_barcode_sheet(fullupc, resize, barheight, barwidth, numxy, barcolor, hideinfo, imageoutlib)


def fix_encode_ean8_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    upc_pieces = None
    supplement = None
    fullupc = upc
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 8 or len(upc) < 7):
        return False
    upc = upcean.validate.fix_ean8_checksum(upc)
    if(supplement is not None):
        fullupc = upc+supplement
    else:
        fullupc = upc
    return encode_ean8_barcode(inimage, fullupc, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def fix_create_itf_barcode(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)

def fix_create_itf_barcode_sheet(upc, outfile="./itf.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_draw_itf_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_encode_itf_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return encode_itf_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf6_barcode(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return create_itf6_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf6_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return draw_itf6_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf6_barcode_sheet(upc, outfile="./itf6.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return create_itf6_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_draw_itf6_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return draw_itf6_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_encode_itf6_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 6 or len(upc) < 5):
        return False
    upc = upcean.validate.fix_itf6_checksum(upc)
    return encode_itf6_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf14_barcode(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf14_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_draw_itf14_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf14_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def fix_create_itf14_barcode_sheet(upc, outfile="./itf14.png", resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imagecomment=None, imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return create_itf14_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_draw_itf14_barcode_sheet(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), numxy=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return draw_itf14_barcode_sheet(fullupc, outfile, resize, hideinfo, barheight, barwidth, numxy, textxy, barcolor, imageoutlib)


def fix_encode_itf14_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=None):
    if(len(upc) > 14 or len(upc) < 13):
        return False
    upc = upcean.validate.fix_itf14_checksum(upc)
    return encode_itf14_barcode(fullupc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
