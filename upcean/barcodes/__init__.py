'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2014 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 10/12/2014 Ver. 2.6.5 RC 2 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, re, os, xml.etree.cElementTree;

import upcean.validate, upcean.convert, upcean.getprefix, upcean.getsfname;
import upcean.barcodes.ean2, upcean.barcodes.ean5, upcean.barcodes.upca, upcean.barcodes.upce, upcean.barcodes.ean13, upcean.barcodes.ean8, upcean.barcodes.itf, upcean.barcodes.itf14;
import upcean.barcodes.code11, upcean.barcodes.code39, upcean.barcodes.code93, upcean.barcodes.codabar, upcean.barcodes.msi;
from upcean.barcodes import *;
''' // Code for validating UPC/EAN by Kazuki Przyborowski '''
from upcean.validate import *;
''' // Code for converting UPC/EAN by Kazuki Przyborowski '''
from upcean.convert import *;
''' // Code for getting GS1 Prefix EAN-8/EAN-13/ITF-14 by Kazuki Przyborowski '''
from upcean.getprefix import *;
''' // Code for getting save file name and type by Kazuki Przyborowski '''
from upcean.getsfname import *;
''' // Code for making EAN-2 supplement by Kazuki Przyborowski '''
from upcean.barcodes.ean2 import *;
''' // Code for making EAN-5 supplement by Kazuki Przyborowski '''
from upcean.barcodes.ean5 import *;
''' // Code for making UPC-A by Kazuki Przyborowski '''
from upcean.barcodes.upca import *;
''' // Code for making UPC-E by Kazuki Przyborowski '''
from upcean.barcodes.upce import *;
''' // Code for making EAN-13 by Kazuki Przyborowski '''
from upcean.barcodes.ean13 import *;
''' // Code for making EAN-8 by Kazuki Przyborowski '''
from upcean.barcodes.ean8 import *;
''' // Code for making Standard 2 of 5 by Kazuki Przyborowski '''
from upcean.barcodes.stf import *;
''' // Code for making Interleaved 2 of 5 by Kazuki Przyborowski '''
from upcean.barcodes.itf import *;
''' // Code for making ITF-14 by Kazuki Przyborowski '''
from upcean.barcodes.itf14 import *;
''' // Code for making Code 11 by Kazuki Przyborowski '''
from upcean.barcodes.code11 import *;
''' // Code for making Code 39 by Kazuki Przyborowski '''
from upcean.barcodes.code39 import *;
''' // Code for making Code 93 by Kazuki Przyborowski '''
from upcean.barcodes.code93 import *;
''' // Code for making Codabar by Kazuki Przyborowski '''
from upcean.barcodes.codabar import *;
''' // Code for making Modified Plessey by Kazuki Przyborowski '''
from upcean.barcodes.msi import *;

'''
// UPC Resources and Info
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code
// Source: http://en.wikipedia.org/wiki/Global_Trade_Item_Number
// Source: http://en.wikipedia.org/wiki/Barcode
// Source: http://www.ucancode.net/CPP_Library_Control_Tool/Draw-Print-encode-UPCA-barcode-UPCE-barcode-EAN13-barcode-VC-Code.htm
// Source: http://en.wikipedia.org/wiki/International_Article_Number
// Source: http://www.upcdatabase.com/docs/
// Source: http://www.accipiter.org/projects/cat.php
// Source: http://www.accipiter.org/download/kittycode.js
// Source: http://uscan.sourceforge.net/upc.txt
// Source: http://www.adams1.com/upccode.html
// Source: http://www.documentmedia.com/Media/PublicationsArticles/QuietZone.pdf
// Source: http://zxing.org/w/decode.jspx
// Source: http://code.google.com/p/zxing/
// Source: http://www.terryburton.co.uk/barcodewriter/generator/
// Source: http://en.wikipedia.org/wiki/Interleaved_2_of_5
// Source: http://www.gs1au.org/assets/documents/info/user_manuals/barcode_technical_details/ITF_14_Barcode_Structure.pdf
// Source: http://www.barcodeisland.com/
'''

'''
// Shortcut Codes by Kazuki Przyborowski
'''
def create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(hasattr(upcean, "create_"+bctype+"_barcode") and callable(getattr(upcean, "create_"+bctype+"_barcode"))):
  return getattr(upcean, "create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(not hasattr(upcean, "create_"+bctype+"_barcode") or not callable(getattr(upcean, "create_"+bctype+"_barcode"))):
  return False;
 return False;
def draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_barcode(bctype,upc,None,resize,hideinfo,barheight,textxy,barcolor);

'''
// Create barcode from XML file
'''
def create_barcode_from_xml(xmlfile):
 tree = xml.etree.cElementTree.ElementTree(file=xmlfile)
 root = tree.getroot();
 for child in root:
  xmlbarcode = {"bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": child.attrib['file']};
  if('size' in child.attrib):
   xmlbarcode.update({"resize": int(child.attrib['size'])});
  if('hideinfo' in child.attrib):
   hidebcinfo = child.attrib['hideinfo'].split();
   hidebcinfoval = [];
   if(hidebcinfo[0]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[0]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[1]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[1]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[2]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[2]=="1"):
    hidebcinfoval.append(True);
   xmlbarcode.update({"hideinfo": tuple(hidebcinfoval)});
  if('height' in child.attrib):
   xmlbarcode.update({"barheight": tuple(map(int, child.attrib['height'].split()))});
  if('color' in child.attrib):
   colorsplit = child.attrib['color'].split();
   colorsplit1 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0]);
   colorsplit1 = colorsplit1[0];
   colorlist1 = (int(colorsplit1[0], 16), int(colorsplit1[1], 16), int(colorsplit1[2], 16));
   colorsplit2 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1]);
   colorsplit2 = colorsplit2[0];
   colorlist2 = (int(colorsplit2[0], 16), int(colorsplit2[1], 16), int(colorsplit2[2], 16));
   colorsplit3 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2]);
   colorsplit3 = colorsplit3[0];
   colorlist3 = (int(colorsplit3[0], 16), int(colorsplit3[1], 16), int(colorsplit3[2], 16));
   colorlist = (colorlist1, colorlist2, colorlist3);
   xmlbarcode.update({"barcolor": colorlist});
  upcean.create_barcode(**xmlbarcode);

def create_issn13_barcode_from_issn8(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_issn8_to_issn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13_barcode_from_issn8(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode_from_issn8(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_issn13_barcode(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode_from_issn8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_isbn13_barcode_from_isbn10(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_isbn10_to_isbn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13_barcode_from_isbn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode_from_isbn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_isbn13_barcode(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode_from_isbn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_ismn13_barcode_from_ismn10(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_ismn10_to_ismn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13_barcode_from_ismn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode_from_ismn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_ismn13_barcode(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode_from_ismn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_vw_barcode_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_vw_to_upca_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_ean13(code,price,outfile="./vw-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_vw_to_ean13_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_itf14(code,price,outfile="./vw-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_vw_to_itf14_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_goodwill_barcode_upca(code,price,outfile="./goodwill-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_goodwill_to_upca_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_upca(code,price,outfile="./goodwill-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_ean13(code,price,outfile="./goodwill-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_goodwill_to_ean13_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_itf14(code,price,outfile="./goodwill-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_goodwill_to_itf14_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_coupon_barcode_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_coupon_to_ean13_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_coupon_to_itf14_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
