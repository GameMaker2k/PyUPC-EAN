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
import upcean.decode.barcode, upcean.support;

''' // Shortcut Codes by Kazuki Przyborowski '''
def decode_barcode(bctype,infile,resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.decode.barcode, "decode_"+bctype+"_barcode") and callable(getattr(upcean.decode.barcode, "decode_"+bctype+"_barcode"))):
  return getattr(upcean.decode.barcode, "decode_"+bctype+"_barcode")(infile,resize,barheight,barwidth,shiftxy,barcolor,imageoutlib);
 if(not hasattr(upcean.decode.barcode, "decode_"+bctype+"_barcode") or not callable(getattr(upcean.decode.barcode, "decode_"+bctype+"_barcode"))):
  return False;
 return False;

def validate_decode_barcode(bctype,infile="./barcode.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="upce" or bctype=="ean13" or bctype=="ean8" or bctype=="itf" or bctype=="itf6" or bctype=="itf14"):
  if(hasattr(upcean.decode.barcode, "validate_decode_"+bctype+"_barcode") and callable(getattr(upcean.decode.barcode, "validate_decode_"+bctype+"_barcode"))):
   return getattr(upcean.decode.barcode, "validate_decode_"+bctype+"_barcode")(infile,resize,barheight,barwidth,shiftxy,barcolor,imageoutlib);
  if(not hasattr(upcean.decode.barcode, "validate_decode_"+bctype+"_barcode") or not callable(getattr(upcean.decode.barcode, "validate_decode_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="upce" and bctype!="ean13" and bctype!="ean8" and bctype!="itf" and bctype!="itf6" and bctype!="itf14"):
  return decode_barcode(bctype,infile,resize,barheight,barwidth,shiftxy,barcolor,imageoutlib);

def fix_decode_barcode(bctype,infile="./barcode.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="upce" or bctype=="ean13" or bctype=="ean8" or bctype=="itf" or bctype=="itf6" or bctype=="itf14"):
  if(hasattr(upcean.decode.barcode, "fix_decode_"+bctype+"_barcode") and callable(getattr(upcean.decode.barcode, "fix_decode_"+bctype+"_barcode"))):
   return getattr(upcean.decode.barcode, "fix_decode_"+bctype+"_barcode")(infile,resize,barheight,barwidth,shiftxy,barcolor,imageoutlib);
  if(not hasattr(upcean.decode.barcode, "fix_decode_"+bctype+"_barcode") or not callable(getattr(upcean.decode.barcode, "fix_decode_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="upce" and bctype!="ean13" and bctype!="ean8" and bctype!="itf" and bctype!="itf6" and bctype!="itf14"):
  return decode_barcode(bctype,infile,resize,barheight,barwidth,shiftxy,barcolor,imageoutlib);
