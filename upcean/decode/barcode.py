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

    $FileInfo: barcode.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.support, upcean.getprefix.getprefix;

''' // Code for decoding UPC-A by Kazuki Przyborowski '''
from upcean.decode.upca import *;
''' // Code for decoding UPC-E by Kazuki Przyborowski '''
from upcean.decode.upce import *;
''' // Code for decoding EAN-13 by Kazuki Przyborowski '''
from upcean.decode.ean13 import *;
''' // Code for decoding EAN-8 by Kazuki Przyborowski '''
from upcean.decode.ean8 import *;

def validate_decode_upca_barcode(infile,resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_upca_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 return True;

def validate_decode_upce_barcode(infile,resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_upce_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not upcean.validate.validate_upce_checksum(upc)):
  return False;
 return True;

def validate_decode_ean13_barcode(infile,resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 return True;

def validate_decode_ean13_from_upca_barcode(infile,resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>13 or len(upc)<12): 
  return False;
 if(len(upc)<13):
  if(not upcean.validate.validate_upca_checksum(upc)):
   return False;
  upc = "0"+str(upc);
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 return True;

def fix_decode_upca_barcode(infile,outfile="./upca.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_upca_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>12 or len(upc)<11):
  return False;
 upc = upcean.validate.fix_upca_checksum(upc);
 return upc;

def fix_decode_upce_barcode(infile,outfile="./upca.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_upce_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>8 or len(upc)<7):
  return False;
 upc = upcean.validate.fix_upce_checksum(upc);
 return upc;

def fix_decode_ean13_barcode(infile,outfile="./upca.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>13 or len(upc)<12):
  return False;
 upc = upcean.validate.fix_ean13_checksum(upc);
 return upc;

def fix_decode_ean13_from_upca_barcode(infile,resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>13 or len(upc)<11): 
  return False;
 if(len(upc)<13):
  upc = upcean.validate.fix_upca_checksum(upc);
  upc = "0"+str(upc);
 if(len(upc)>13 or len(upc)<12):
  return False;
 upc = upcean.validate.fix_ean13_checksum(upc);
 return True;

def fix_decode_ean8_barcode(infile,outfile="./upca.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = decode_ean8_barcode(infile,resize,barheight,barwidth,barcolor,imageoutlib);
 if(len(upc)>8 or len(upc)<7):
  return False;
 upc = upcean.validate.fix_ean8_checksum(upc);
 return upc;
