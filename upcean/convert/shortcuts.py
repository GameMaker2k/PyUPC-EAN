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

    $FileInfo: shortcuts.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean.convert
import upcean.support

'''
// Shortcut Codes by Kazuki Przyborowski
// convert
'''


def make_barcode(bctype, numbersystem, manufacturer, product):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.convert, "make_"+bctype+"_barcode") and callable(getattr(upcean.convert, "make_"+bctype+"_barcode"))):
        return getattr(upcean.convert, "make_"+bctype+"_barcode")(numbersystem, manufacturer, product)
    if(not hasattr(upcean.convert, "make_"+bctype+"_barcode") or not callable(getattr(upcean.convert, "make_"+bctype+"_barcode"))):
        return False
    return False


def convert_barcode(intype, outtype, upc):
    if(intype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(outtype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.convert, "convert_barcode_from_"+intype+"_to_"+outtype) and callable(getattr(upcean.convert, "convert_barcode_from_"+intype+"_to_"+outtype))):
        return getattr(upcean.convert, "convert_barcode_from_"+intype+"_to_"+outtype)(upc)
    if(not hasattr(upcean.convert, "convert_barcode_from_"+intype+"_to_"+outtype) or not callable(getattr(upcean.convert, "convert_barcode_from_"+intype+"_to_"+outtype))):
        return False
    return False


def print_barcode(bctype, upc):
    if(bctype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.convert, "print_"+bctype+"_barcode") and callable(getattr(upcean.convert, "print_"+bctype+"_barcode"))):
        return getattr(upcean.convert, "print_"+bctype+"_barcode")(upc)
    if(not hasattr(upcean.convert, "print_"+bctype+"_barcode") or not callable(getattr(upcean.convert, "print_"+bctype+"_barcode"))):
        return False
    return False


def print_convert_barcode(intype, outtype, upc):
    if(intype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(outtype not in upcean.support.supported_barcodes("tuple")):
        return False
    if(hasattr(upcean.convert, "print_convert_barcode_from_"+intype+"_to_"+outtype) and callable(getattr(upcean.convert, "print_convert_barcode_from_"+intype+"_to_"+outtype))):
        return getattr(upcean.convert, "print_convert_barcode_from_"+intype+"_to_"+outtype)(upc)
    if(not hasattr(upcean.convert, "print_convert_barcode_from_"+intype+"_to_"+outtype) or not callable(getattr(upcean.convert, "print_convert_barcode_from_"+intype+"_to_"+outtype))):
        return False
    return False
