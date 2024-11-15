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

    $FileInfo: oopfuncs.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean.validate
import upcean.convert
import upcean.getprefix
import upcean.support
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or cairosupport or svgwritesupport):
    import upcean.fonts
    import upcean.xml
    import upcean.encode
if(pilsupport):
    import upcean.decode

''' // Object-oriented classes and functions by Kazuki Przyborowski '''


class encode:
    ''' // Barcode Types '''
    EAN2 = "ean2"
    UPCS2 = "ean2"
    EAN5 = "ean5"
    UPCS5 = "ean5"
    UPCA = "upca"
    GOODWILL = "goodwill"
    UPCE = "upce"
    EAN13 = "ean13"
    EAN8 = "ean8"
    STF = "stf"
    ITF = "itf"
    ITF14 = "itf14"
    CODE11 = "code11"
    CODE39 = "code39"
    CODE93 = "code93"
    CODE128 = "code128"
    CODABAR = "codabar"
    MSI = "msi"
    bctype_dict = upcean.support.bctype_dict
    bctype_dict_alt = upcean.support.bctype_dict_alt
    bctype_list = upcean.support.bctype_list
    bctype_tuple = upcean.support.bctype_tuple
    bctype_name = upcean.support.bctype_name

    def __init__(self, type=None, code=None):
        if(type is not None):
            self.type = type
        if(code is not None):
            self.code = code
        self.filename = "./barcode.png"
        self.inimage = None
        self.size = 1
        self.hidesn = False
        self.hidecd = False
        self.hidetext = False
        self.shiftxy = (0, 0)
        self.barheight = (48, 54)
        self.barwidth = (1, 1)
        self.barcolor = (0, 0, 0)
        self.textcolor = (0, 0, 0)
        self.bgcolor = (255, 255, 255)
        self.imageoutlib = "pillow"
        self.return_check = False
        self.return_type = "dict"
    ''' // support.py funtions '''

    def supported_barcodes(self, return_type=None):
        if(return_type is None):
            return_type = self.return_type
        return upcean.support.supported_barcodes(return_type)

    def barcode_support(self, return_type=None):
        if(return_type is None):
            return_type = self.return_type
        return upcean.support.barcode_support(return_type)

    def get_barcode_name(self, barcode_type=None):
        if(barcode_type is None):
            barcode_type = self.type
        return upcean.support.get_barcode_name(barcode_type)

    def check_for_pil(self):
        return upcean.support.check_for_pil()

    def check_for_pillow(self):
        return upcean.support.check_for_pillow()

    def get_pil_version(self, barcode_type=None):
        if(barcode_type is None):
            barcode_type = self.type
        return upcean.support.get_pil_version()

    def get_pillow_version(self, barcode_type=None):
        if(barcode_type is None):
            barcode_type = self.type
        return upcean.support.get_pillow_version()

    def get_python_info(self, barcode_type=None):
        if(barcode_type is None):
            barcode_type = self.type
        return upcean.support.get_pillow_version()
    ''' // barcodes/__init__.py funtions '''
    if(pilsupport or cairosupport or svgwritesupport):
        def create_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            return upcean.encode.create_barcode(self.type, self.code, filename, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def validate_create_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            return upcean.encode.validate_create_barcode(self.type, self.code, filename, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def fix_create_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            return upcean.encode.fix_create_barcode(self.type, self.code, filename, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def draw_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.draw_barcode(self.type, self.code, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def validate_draw_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.validate_draw_barcode(self.type, self.code, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def fix_draw_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.fix_draw_barcode(self.type, self.code, size, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext), self.imageoutlib)

        def encode_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.encode_barcode(self.type, self.inimage, self.code, size, self.shiftxy, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext))

        def validate_encode_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.validate_encode_barcode(self.type, self.inimage, self.code, size, self.shiftxy, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext))

        def fix_encode_barcode(self, size=None):
            if(size is None):
                size = self.size
            return upcean.encode.fix_encode_barcode(self.type, self.inimage, self.code, size, self.shiftxy, self.barheight, self.barwidth, (self.barcolor, self.textcolor, self.bgcolor), (self.hidesn, self.hidecd, self.hidetext))
    ''' // validate/__init__.py funtions '''

    def validate_checksum(self):
        return upcean.validate.validate_checksum(self.type, self.code, self.return_check)

    def validate_luhn_checksum(self):
        return upcean.validate.validate_luhn_checksum(self.code, self.codelen, self.return_check)

    def validate_usps_checksum(self):
        return upcean.validate.validate_usps_checksum(self.code, self.return_check)

    def validate_ups_checksum(self):
        return upcean.validate.validate_ups_checksum(self.code, self.return_check)

    def validate_fedex_checksum(self):
        return upcean.validate.validate_fedex_checksum(self.code, self.return_check)

    def validate_imei_checksum(self):
        return upcean.validate.validate_imei_checksum(self.code, self.return_check)

    def validate_bcn_checksum(self):
        return upcean.validate.validate_bcn_checksum(self.code, self.return_check)

    def get_checksum(self):
        return upcean.validate.get_checksum(self.type, self.code)

    def get_luhn_checksum(self):
        return upcean.validate.get_luhn_checksum(self.code, self.codelen)

    def get_code11_checksum(self):
        return upcean.validate.get_code11_checksum(self.code)

    def get_code93_checksum(self):
        return upcean.validate.get_code93_checksum(self.code)

    def get_code128_checksum(self):
        return upcean.validate.get_code128_checksum(self.code)

    def get_digital_root(self):
        return upcean.validate.get_digital_root(self.number)

    def get_usps_checksum(self):
        return upcean.validate.get_usps_checksum(self.code)

    def get_ups_checksum(self):
        return upcean.validate.get_ups_checksum(self.code)

    def get_fedex_checksum(self):
        return upcean.validate.get_fedex_checksum(self.code)

    def get_imei_checksum(self):
        return upcean.validate.get_imei_checksum(self.code)

    def get_bcn_checksum(self):
        return upcean.validate.get_bcn_checksum(self.code)

    def fix_checksum(self):
        return upcean.validate.fix_checksum(self.type, self.code)

    def fix_luhn_checksum(self):
        return upcean.validate.fix_luhn_checksum(self.code, self.codelen)

    def fix_usps_checksum(self):
        return upcean.validate.fix_usps_checksum(self.code)

    def fix_ups_checksum(self):
        return upcean.validate.fix_ups_checksum(self.code)

    def fix_fedex_checksum(self):
        return upcean.validate.fix_fedex_checksum(self.code)

    def fix_imei_checksum(self):
        return upcean.validate.fix_imei_checksum(self.code)

    def fix_bcn_checksum(self):
        return upcean.validate.fix_bcn_checksum(self.code)
    ''' // convert/__init__.py funtions '''

    def convert_barcode(self, outtype=None):
        if(outtype is None):
            outtype = self.outtype
        return upcean.convert.convert_barcode(self.type, outtype, self.code)

    def print_convert_barcode(self, outtype=None):
        if(outtype is None):
            outtype = self.outtype
        return upcean.convert.print_convert_barcode(self.type, outtype, self.code)

    def make_barcode(self, numbersystem, manufacturer, product):
        if(numbersystem is None):
            numbersystem = self.numbersystem
        if(manufacturer is None):
            manufacturer = self.manufacturer
        if(product is None):
            product = self.product
        return upcean.convert.make_barcode(self.type, self.numbersystem, self.manufacturer, self.product)
    ''' // getsfname.py funtions '''
    if(pilsupport or cairosupport):
        def get_save_filename(self, filename=None):
            if(filename is None):
                filename = self.filename
            return upcean.predraw.get_save_filename(self.filename)
    ''' // getprefix/__init__.py funtions '''

    def get_barcode_info(self):
        return upcean.getprefix.get_barcode_info(self.type, self.code)


barcode = encode

''' // Object-oriented classes and functions by Kazuki Przyborowski '''


class decode:
    ''' // Barcode Types '''
    EAN2 = "ean2"
    UPCS2 = "ean2"
    EAN5 = "ean5"
    UPCS5 = "ean5"
    UPCA = "upca"
    GOODWILL = "goodwill"
    UPCE = "upce"
    EAN13 = "ean13"
    EAN8 = "ean8"
    STF = "stf"
    ITF = "itf"
    ITF14 = "itf14"
    CODE11 = "code11"
    CODE39 = "code39"
    CODE93 = "code93"
    CODE128 = "code128"
    CODABAR = "codabar"
    MSI = "msi"
    bctype_dict = upcean.support.bctype_dict
    bctype_dict_alt = upcean.support.bctype_dict_alt
    bctype_list = upcean.support.bctype_list
    bctype_tuple = upcean.support.bctype_tuple
    bctype_name = upcean.support.bctype_name

    def __init__(self, type=None, filename=None):
        if(type is not None):
            self.type = type
        if(filename is not None):
            self.filename = filename
        self.code = None
        self.info = None
        self.size = 1
        self.barheight = (48, 54)
        self.barwidth = (1, 1)
        self.shiftxy = (0, 0)
        self.barcolor = (0, 0, 0)
        self.textcolor = (0, 0, 0)
        self.bgcolor = (255, 255, 255)
        self.imageoutlib = "pillow"
        self.return_check = False
        self.return_type = "dict"
        self.locatebarcode = False
        self.shiftcheck = False
    if(pilsupport):
        def decode_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            self.code = upcean.decode.decode_barcode(self.type, filename, size, self.barheight, self.barwidth, self.shiftcheck, self.shiftxy, (
                self.barcolor, self.textcolor, self.bgcolor), self.locatebarcode, self.imageoutlib)
            return self.code

        def get_barcode_info(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            self.info = upcean.decode.get_barcode_location(self.type, filename, size, self.barheight, self.barwidth,
                                                           self.shiftcheck, self.shiftxy, (self.barcolor, self.textcolor, self.bgcolor), self.imageoutlib)
            return self.info

        def get_barcode_location(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            self.info = upcean.decode.get_barcode_location(self.type, filename, size, self.barheight, self.barwidth,
                                                           self.shiftcheck, self.shiftxy, (self.barcolor, self.textcolor, self.bgcolor), self.imageoutlib)
            return self.info

        def validate_decode_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            self.code = upcean.decode.decode_barcode(self.type, filename, size, self.barheight, self.barwidth, self.shiftcheck, self.shiftxy, (
                self.barcolor, self.textcolor, self.bgcolor), self.locatebarcode, self.imageoutlib)
            return self.code

        def fix_decode_barcode(self, filename=None, size=None):
            if(filename is None):
                filename = self.filename
            if(size is None):
                size = self.size
            self.code = upcean.decode.fix_decode_barcode(self.type, filename, size, self.barheight, self.barwidth, self.shiftcheck, self.shiftxy, (
                self.barcolor, self.textcolor, self.bgcolor), self.locatebarcode, self.imageoutlib)
            return self.code
