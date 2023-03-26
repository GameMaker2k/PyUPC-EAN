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

    $FileInfo: shortcuts.py - Last Update: 3/26/2023 Ver. 2.8.10 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.validate.validate, upcean.support;

'''
// Shortcut Codes by Kazuki Przyborowski
// validate
'''
def validate_checksum(bctype, upc, return_check=False):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.validate.validate, "validate_"+bctype+"_checksum") and callable(getattr(upcean.validate.validate, "validate_"+bctype+"_checksum"))):
  return getattr(upcean.validate.validate, "validate_"+bctype+"_checksum")(upc,return_check);
 if(not hasattr(upcean.validate.validate, "validate_"+bctype+"_checksum") or not callable(getattr(upcean.validate.validate, "validate_"+bctype+"_checksum"))):
  return False;
 return False;
def get_checksum(bctype, upc):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.validate.validate, "get_"+bctype+"_checksum") and callable(getattr(upcean.validate.validate, "get_"+bctype+"_checksum"))):
  return getattr(upcean.validate.validate, "get_"+bctype+"_checksum")(upc);
 if(not hasattr(upcean.validate.validate, "get_"+bctype+"_checksum") or not callable(getattr(upcean.validate.validate, "get_"+bctype+"_checksum"))):
  return False;
 return False;
def fix_checksum(bctype, upc):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.validate.validate, "fix_"+bctype+"_checksum") and callable(getattr(upcean.validate.validate, "fix_"+bctype+"_checksum"))):
  return getattr(upcean.validate.validate, "fix_"+bctype+"_checksum")(upc);
 if(not hasattr(upcean.validate.validate, "fix_"+bctype+"_checksum") or not callable(getattr(upcean.validate.validate, "fix_"+bctype+"_checksum"))):
  return False;
 return False;
