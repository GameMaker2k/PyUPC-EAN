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

    $FileInfo: barcode.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.support, upcean.getprefix.getprefix;

''' // Code for making EAN-2 supplement by Kazuki Przyborowski '''
from upcean.encode.ean2 import *;
''' // Code for making EAN-5 supplement by Kazuki Przyborowski '''
from upcean.encode.ean5 import *;
''' // Code for making UPC-A by Kazuki Przyborowski '''
from upcean.encode.upca import *;
import upcean.encode.upca as gtin12;
import upcean.encode.upca as ucc12;
''' // Code for making Goodwill Barcodes by Kazuki Przyborowski '''
from upcean.encode.goodwill import *;
''' // Code for making UPC-E by Kazuki Przyborowski '''
from upcean.encode.upce import *;
''' // Code for making EAN-13 by Kazuki Przyborowski '''
from upcean.encode.ean13 import *;
import upcean.encode.ean13 as gtin13;
import upcean.encode.ean13 as ucc13;
''' // Code for making EAN-8 by Kazuki Przyborowski '''
from upcean.encode.ean8 import *;
import upcean.encode.ean8 as gtin8;
import upcean.encode.ean8 as ucc8;
''' // Code for making Standard 2 of 5 by Kazuki Przyborowski '''
from upcean.encode.stf import *;
import upcean.encode.stf as code25;
''' // Code for making Interleaved 2 of 5 by Kazuki Przyborowski '''
from upcean.encode.itf import *;
''' // Code for making ITF-14 by Kazuki Przyborowski '''
from upcean.encode.itf14 import *;
import upcean.encode.itf14 as itf6;
''' // Code for making Code 11 by Kazuki Przyborowski '''
from upcean.encode.code11 import *;
''' // Code for making Code 39 by Kazuki Przyborowski '''
from upcean.encode.code39 import *;
''' // Code for making Code 93 by Kazuki Przyborowski '''
from upcean.encode.code93 import *;
''' // Code for making Code 128 by Kazuki Przyborowski '''
from upcean.encode.code128 import *;
''' // Code for making Codabar by Kazuki Przyborowski '''
from upcean.encode.codabar import *;
''' // Code for making Plessey by Kazuki Przyborowski '''
from upcean.encode.plessey import *;
''' // Code for making Modified Plessey by Kazuki Przyborowski '''
from upcean.encode.msi import *;

def validate_create_upca_barcode(upc,outfile="./upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 return create_upca_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_upca_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_upca_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_upca_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_upca_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_goodwill_barcode(upc,outfile="./goodwill.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 if(not upcean.getprefix.getprefix.get_goodwill_upca_barcode_info(upc)):
  return False;
 return create_goodwill_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_goodwill_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_goodwill_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_goodwill_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_goodwill_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_upce_barcode(upc,outfile="./upce.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not upcean.validate.validate_upce_checksum(upc)):
  return False;
 return create_upce_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_upce_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_upce_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_upce_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_upce_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_ean13_barcode(upc,outfile="./ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 return create_ean13_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_ean13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_ean13_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_ean13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_ean13_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_ean8_barcode(upc,outfile="./ean8.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not upcean.validate.validate_upce_checksum(upc)):
  return False;
 return create_upce_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_ean8_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_ean8_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_ean8_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_ean8_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_itf_barcode(upc,outfile="./itf.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>14 or len(upc)<14):
  return False;
 if(not upcean.validate.validate_itf14_checksum(upc)):
  return False;
 return create_itf_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_itf_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_itf_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_itf6_barcode(upc,outfile="./itf6.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>6 or len(upc)<6):
  return False;
 if(not upcean.validate.validate_itf6_checksum(upc)):
  return False;
 return create_itf6_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_itf6_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf6_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_itf6_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf6_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def validate_create_itf14_barcode(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>14 or len(upc)<14):
  return False;
 if(not upcean.validate.validate_itf14_checksum(upc)):
  return False;
 return create_itf14_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_draw_itf14_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf14_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def validate_encode_itf14_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return validate_create_itf14_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_upca_barcode(upc,outfile="./upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>12 or len(upc)<11):
  return False;
 upc = upcean.validate.fix_upca_checksum(upc);
 return create_upca_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_upca_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_upca_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_upca_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_upca_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_goodwill_barcode(upc,outfile="./goodwill.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>12 or len(upc)<11):
  return False;
 upc = upcean.validate.fix_upca_checksum(upc);
 if(not upcean.getprefix.getprefix.get_goodwill_upca_barcode_info(upc)):
  return False;
 return create_goodwill_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_goodwill_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_goodwill_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_goodwill_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_goodwill_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_upce_barcode(upc,outfile="./upce.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>8 or len(upc)<7):
  return False;
 upc = upcean.validate.fix_upce_checksum(upc);
 return create_upce_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_upce_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_upce_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_upce_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_upce_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_ean13_barcode(upc,outfile="./ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>13 or len(upc)<12):
  return False;
 upc = upcean.validate.fix_ean13_checksum(upc);
 return create_ean13_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_ean13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_ean13_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_ean13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_ean13_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_ean8_barcode(upc,outfile="./ean8.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>8 or len(upc)<7):
  return False;
 upc = upcean.validate.fix_ean8_checksum(upc);
 return create_upce_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_ean8_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_ean8_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_ean8_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_ean8_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_itf_barcode(upc,outfile="./itf.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>14 or len(upc)<13):
  return False;
 upc = upcean.validate.fix_itf14_checksum(upc);
 return create_itf_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_itf_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_itf_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_itf6_barcode(upc,outfile="./itf6.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>6 or len(upc)<5):
  return False;
 upc = upcean.validate.fix_itf6_checksum(upc);
 return create_itf6_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_itf6_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf6_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_itf6_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf6_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def fix_create_itf14_barcode(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 if(len(upc)>14 or len(upc)<13):
  return False;
 upc = upcean.validate.fix_itf14_checksum(upc);
 return create_itf14_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_draw_itf14_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf14_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
def fix_encode_itf14_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return fix_create_itf14_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
