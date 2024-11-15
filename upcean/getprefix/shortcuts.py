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
import upcean.getprefix.getprefix

'''
// Shortcut Codes by Kazuki Przyborowski
// getprefix
'''


def get_barcode_info(bctype, upc, infotype=None):
    if(infotype is None):
        if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_info") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_info"))):
            return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_info")(upc)
        if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_info") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_info"))):
            return False
    if(infotype is not None):
        if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_"+infotype) and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_"+infotype))):
            return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_"+infotype)(upc)
        if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_"+infotype) or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_"+infotype))):
            return False
    return False


def get_barcode_packagecode(bctype, upc):
    if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_packagecode") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_packagecode"))):
        return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_packagecode")(upc)
    if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_packagecode") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_packagecode"))):
        return False
    return False


def get_barcode_numbersystem(bctype, upc):
    if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_numbersystem") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_numbersystem"))):
        return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_numbersystem")(upc)
    if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_numbersystem") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_numbersystem"))):
        return False
    return False


def get_barcode_manufacturer(bctype, upc):
    if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_manufacturer") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_manufacturer"))):
        return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_manufacturer")(upc)
    if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_manufacturer") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_manufacturer"))):
        return False
    return False


def get_barcode_product(bctype, upc):
    if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_product") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_product"))):
        return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_product")(upc)
    if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_product") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_product"))):
        return False
    return False


def get_barcode_checkdigit(bctype, upc):
    if(hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_checkdigit") and callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_checkdigit"))):
        return getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_checkdigit")(upc)
    if(not hasattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_checkdigit") or not callable(getattr(upcean.getprefix.getprefix, "get_"+bctype+"_barcode_checkdigit"))):
        return False
    return False
