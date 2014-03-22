'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 03/21/2014 Ver. 2.5.6 RC 6 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, re;

import upcean.validate, upcean.convert, upcean.getprefix, upcean.getsfname;
import upcean.barcodes.ean2, upcean.barcodes.ean5, upcean.barcodes.upca, upcean.barcodes.upce, upcean.barcodes.ean13, upcean.barcodes.ean8, upcean.barcodes.itf, upcean.barcodes.itf14;
import upcean.barcodes.code11, upcean.barcodes.code39, upcean.barcodes.code93, upcean.barcodes.codabar, upcean.barcodes.msi;
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
def create_barcode(upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==7 or len(upc)==8):
  if(supplement==None):
   if(re.findall("^([0-1])", upc)):
    return create_upce(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   if(re.findall("^([0-1])", upc)):
    return create_upce(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==2):
  return create_ean2(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==5):
  return create_ean5(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==11 or len(upc)==12):
  if(supplement==None):
   return create_upca(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_upca(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==13): 
  if(supplement==None):
   return create_ean13(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_ean13(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==14): 
  if(supplement==None):
   return create_itf14(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_itf14(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 return False;
def draw_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_any(upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==7 or len(upc)==8):
  if(supplement==None):
   if(re.findall("^([0-1])", upc)):
    return create_upce(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   if(re.findall("^([0-1])", upc)):
    return create_upce(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==2):
  return create_ean2(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==5):
  return create_ean5(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==11 or len(upc)==12):
  if(supplement==None):
   return create_upca(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_upca(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==13): 
  if(supplement==None):
   return create_ean13(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_ean13(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==14): 
  if(supplement==None):
   return create_itf14(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_itf14(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 return False;
def draw_any(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_upc(upc,outfile="./upc.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==7 or len(upc)==8):
  if(supplement==None):
   return create_upce(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_upce(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==11 or len(upc)==12):
  if(supplement==None):
   return create_upca(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_upca(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==13 or len(upc)==14): 
  if(len(upc)==13): 
    upc = "0"+upc;
  if(supplement==None):
   return create_itf14(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_itf14(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 return False;
def draw_upc(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upc(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_ean(upc,outfile="./ean.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==2):
  return create_ean2(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==5):
  return create_ean5(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(len(upc)==7 or len(upc)==8):
  if(supplement==None):
   return create_ean8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_ean8(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==12 or len(upc)==13): 
  if(supplement==None):
   return create_ean13(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_ean13(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 if(len(upc)==14): 
  if(supplement==None):
   return create_itf14(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
  if(supplement!=None):
   return create_itf14(upc+" "+supplement,outfile,resize,hideinfo,barheight,barcolor);
 return False;
def draw_ean(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_issn13_from_issn8(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(convert_issn8_to_issn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13_from_issn8(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_from_issn8(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_issn13(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_from_issn8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_isbn13_from_isbn10(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(convert_isbn10_to_isbn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13_from_isbn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_from_isbn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_isbn13(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_from_isbn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_ismn13_from_ismn10(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(convert_ismn10_to_ismn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13_from_ismn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_from_ismn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_ismn13(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_from_ismn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_vw_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca(make_vw_upca(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_to_ean13(code,price,outfile="./vw-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(make_vw_to_ean13(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_to_itf14(code,price,outfile="./vw-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14(make_vw_to_itf14(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_goodwill_upca(code,price,outfile="./goodwill-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca(make_goodwill_upca(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_to_ean13(code,price,outfile="./goodwill-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(make_goodwill_to_ean13(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_to_itf14(code,price,outfile="./goodwill-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14(make_goodwill_to_itf14(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_coupon_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca(make_coupon_upca(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_upca(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_to_ean13(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(make_coupon_to_ean13(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_to_ean13(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_to_ean13(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_to_itf14(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14(make_coupon_to_itf14(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_to_itf14(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_to_itf14(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);