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
import upcean.encode.barcode, upcean.xml.files, upcean.support;

''' // Shortcut Codes by Kazuki Przyborowski '''
def create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.encode.barcode, "create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "create_"+bctype+"_barcode"))):
  return getattr(upcean.encode.barcode, "create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
 if(not hasattr(upcean.encode.barcode, "create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "create_"+bctype+"_barcode"))):
  return False;
 return False;
def draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def encode_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="goodwill" or bctype=="upce" or bctype=="ean13" or bctype=="ean8" or bctype=="itf" or bctype=="itf6" or bctype=="itf14"):
  if(hasattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode"))):
   return getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
  if(not hasattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "validate_create_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="goodwill" and bctype!="upce" and bctype!="ean13" and bctype!="ean8" and bctype!="itf" and bctype!="itf6" and bctype!="itf14"):
  return create_barcode(bctype,upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="goodwill" or bctype=="upce" or bctype=="ean13" or bctype=="ean8" or bctype=="itf" or bctype=="itf6" or bctype=="itf14"):
  if(hasattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode") and callable(getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode"))):
   return getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
  if(not hasattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode") or not callable(getattr(upcean.encode.barcode, "fix_create_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="goodwill" and bctype!="upce" and bctype!="ean13" and bctype!="ean8" and bctype!="itf" and bctype!="itf6" and bctype!="itf14"):
  return create_barcode(bctype,upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_barcode(bctype,upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
