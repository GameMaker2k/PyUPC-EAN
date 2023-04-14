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

    $FileInfo: shortcuts.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.oopfuncs.oopfuncs, upcean.support;

'''
// Shortcut Codes by Kazuki Przyborowski
// oopfuncs
'''

def barcode_encode(type=None, code=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.encode(type, code);

def encode_barcode(type=None, code=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.encode(type, code);

def barcode_class(type=None, code=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.barcode(type, code);

def class_barcode(type=None, code=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.barcode(type, code);

def barcode_decode(type=None, filename=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.decode(type, filename);

def decode_barcode(type=None, code=None):
 if(type not in upcean.support.supported_barcodes("tuple")):
  return False;
 return upcean.oopfuncs.oopfuncs.decode(type, filename);
