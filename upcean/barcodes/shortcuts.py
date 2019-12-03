'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: shortcuts.py - Last Update: 12/3/2019 Ver. 2.7.18 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.barcodes.barcode, upcean.barcodes.files, upcean.support;

''' // Shortcut Codes by Kazuki Przyborowski '''
def create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(hasattr(upcean.barcodes.barcode, "create_"+bctype+"_barcode") and callable(getattr(upcean.barcodes.barcode, "create_"+bctype+"_barcode"))):
  return getattr(upcean.barcodes.barcode, "create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(not hasattr(upcean.barcodes.barcode, "create_"+bctype+"_barcode") or not callable(getattr(upcean.barcodes.barcode, "create_"+bctype+"_barcode"))):
  return False;
 return False;
def draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_barcode(bctype,upc,None,resize,hideinfo,barheight,textxy,barcolor);

def validate_create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="upce" or bctype=="ean13" or bctype=="ean" or bctype=="itf" or bctype=="itf"):
  if(hasattr(upcean.barcodes.barcode, "validate_create_"+bctype+"_barcode") and callable(getattr(upcean.barcodes.barcode, "validate_create_"+bctype+"_barcode"))):
   return getattr(upcean.barcodes.barcode, "validate_create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(not hasattr(upcean.barcodes.barcode, "validate_create_"+bctype+"_barcode") or not callable(getattr(upcean.barcodes.barcode, "validate_create_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="upce" and bctype!="ean13" and bctype!="ean" and bctype!="itf" and bctype!="itf"):
  return create_barcode(bctype,upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def validate_draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return validate_create_barcode(bctype,upc,None,resize,hideinfo,barheight,textxy,barcolor);

def fix_create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(bctype not in upcean.support.supported_barcodes("tuple")):
  return False;
 if(bctype=="upca" or bctype=="upce" or bctype=="ean13" or bctype=="ean" or bctype=="itf" or bctype=="itf"):
  if(hasattr(upcean.barcodes.barcode, "fix_create_"+bctype+"_barcode") and callable(getattr(upcean.barcodes.barcode, "fix_create_"+bctype+"_barcode"))):
   return getattr(upcean.barcodes.barcode, "fix_create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(not hasattr(upcean.barcodes.barcode, "fix_create_"+bctype+"_barcode") or not callable(getattr(upcean.barcodes.barcode, "fix_create_"+bctype+"_barcode"))):
   return False;
  return False;
 if(bctype!="upca" and bctype!="upce" and bctype!="ean13" and bctype!="ean" and bctype!="itf" and bctype!="itf"):
  return create_barcode(bctype,upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def fix_draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return fix_create_barcode(bctype,upc,None,resize,hideinfo,barheight,textxy,barcolor);
