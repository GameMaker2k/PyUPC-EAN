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

    $FileInfo: __init__.py - Last Update: 03/25/2014 Ver. 2.5.9 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, re;
__version_info__ = (2, 5, 9, "RC 1");
if(__version_info__[3]!=None):
 __version__ = "{major}.{minor}.{build} {release}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2], release=__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = "{major}.{minor}.{build}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2]);
def version_info():
 global __version_info__;
 if(__version_info__[3]!=None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": __version_info__[3]};
 if(__version_info__[3]==None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": None};
__version_date_info__ = (2014, 03, 25, "RC 1");
def version_date():
 global __version_info__;
 if(__version_date_info__[3]!=None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": __version_date_info__[3]};
 if(__version_date_info__[3]==None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": None};
__version_date__ = "{year}.{month}.{day}".format(year=__version_date_info__[0], month=__version_date_info__[1], day=__version_date_info__[2]);
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

def exec_function(function, *argument):
 if(hasattr(upcean, function) and callable(getattr(upcean, function))):
  return getattr(upcean, function)(*argument);
 if(not hasattr(upcean, function) or not callable(getattr(upcean, function))):
  return False;
def run_function(function, *argument):
 if(hasattr(upcean, function) and callable(getattr(upcean, function))):
  return getattr(upcean, function)(*argument);
 if(not hasattr(upcean, function) or not callable(getattr(upcean, function))):
  return False;

'''
// Barcode Support List
'''
bctype_dict={"EAN2": "ean2", "UPCS2": "ean2", "EAN5": "ean5", "UPCS5": "ean5", "UPCA": "upca", "UPCE": "upce", "EAN13": "ean13","EAN8": "ean8","STF": "stf", "ITF": "itf", "ITF14": "itf14", "CODE11": "code11", "CODE39": "code39", "CODE93": "code93", "CODABAR": "codabar", "MSI": "msi"};
bctype_dict_alt={"ean2": "EAN2", "ean5": "EAN5", "upca": "UPCA", "upce": "UPCE", "ean13": "EAN13","ean8": "EAN8","stf": "STF", "itf": "ITF", "itf14": "ITF14", "code11": "CODE11", "code39": "CODE39", "code93": "CODE93", "codabar": "CODABAR", "msi": "MSI"};
bctype_list=["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi"];
bctype_tuple=("ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi");
bctype_name={"ean2": "EAN-2", "ean5": "EAN-5", "upca": "UPC-A", "upce": "UPC-E", "ean13": "EAN-13", "ean8": "EAN-8", "stf": "STF", "itf": "ITF", "itf14": "ITF-14", "code11": "Code 11", "code39": "Code 39", "code93": "Code 93", "codabar": "Codabar", "msi": "MSI"};
def supported_barcodes(return_type="dict"):
 if(return_type=="dict"):
  return {"EAN2": "ean2", "UPCS2": "ean2", "EAN5": "ean5", "UPCS5": "ean5", "UPCA": "upca", "UPCE": "upce", "EAN13": "ean13","EAN8": "ean8","STF": "stf", "ITF": "itf", "ITF14": "itf14", "CODE11": "code11", "CODE39": "code39", "CODE93": "code93", "CODABAR": "codabar", "MSI": "msi"};
 if(return_type=="list"):
  return ["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi"];
 if(return_type=="tuple"):
  return ("ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi");
 return False;
def barcode_support(return_type="dict"):
 return supported_barcodes(return_type);
def get_barcode_name(barcode_type="upca"):
 bctype_name={"ean2": "EAN-2", "ean5": "EAN-5", "upca": "UPC-A", "upce": "UPC-E", "ean13": "EAN-13", "ean8": "EAN-8", "stf": "STF", "itf": "ITF", "itf14": "ITF-14", "code11": "Code 11", "code39": "Code 39", "code93": "Code 93", "codabar": "Codabar", "msi": "MSI"};
 return bctype_name[barcode_type];

'''
// Object-oriented classes and functions by Kazuki Przyborowski
'''
class barcode:
 __version_info__ = (version_info()["major"], version_info()["minor"], version_info()["build"], version_info()["release"]);
 if(version_info()["release"]!=None):
  __version__ = "{major}.{minor}.{build} {release}".format(major=version_info()["major"], minor=version_info()["minor"], build=version_info()["build"], release=version_info()["release"]);
 if(version_info()["release"]==None):
  __version__ = "{major}.{minor}.{build}".format(major=version_info()["major"], minor=version_info()["minor"], build=version_info()["build"]);
 __version_date_info__ = (version_date()["year"], version_date()["month"], version_date()["day"]);
 __version_date__ = "{year}.{month}.{day}".format(year=version_date()["year"], month=version_date()["month"], day=version_date()["day"]);
 '''
 // Barcode Types
 '''
 EAN2="ean2";
 UPCS2="ean2";
 EAN5="ean5";
 UPCS5="ean5";
 UPCA="upca";
 UPCE="upce";
 EAN13="ean13"
 EAN8="ean8"
 STF="stf";
 ITF="itf";
 ITF14="itf14";
 CODE11="code11";
 CODE39="code39";
 CODE93="code93";
 CODABAR="codabar";
 MSI="msi";
 bctype_dict={"EAN2": "ean2", "UPCS2": "ean2", "EAN5": "ean5", "UPCS5": "ean5", "UPCA": "upca", "UPCE": "upce", "EAN13": "ean13","EAN8": "ean8","STF": "stf", "ITF": "itf", "ITF14": "itf14", "CODE11": "code11", "CODE39": "code39", "CODE93": "code93", "CODABAR": "codabar", "MSI": "msi"};
 bctype_dict_alt={"ean2": "EAN2", "ean5": "EAN5", "upca": "UPCA", "upce": "UPCE", "ean13": "EAN13","ean8": "EAN8","stf": "STF", "itf": "ITF", "itf14": "ITF14", "code11": "CODE11", "code39": "CODE39", "code93": "CODE93", "codabar": "CODABAR", "msi": "MSI"};
 bctype_list=["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi"];
 bctype_tuple=["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf14", "code11", "code39", "code93", "codabar", "msi"];
 bctype_name={"ean2": "EAN-2", "ean5": "EAN-5", "upca": "UPC-A", "upce": "UPC-E", "ean13": "EAN-13", "ean8": "EAN-8", "stf": "STF", "itf": "ITF", "itf14": "ITF-14", "code11": "Code 11", "code39": "Code 39", "code93": "Code 93", "codabar": "Codabar", "msi": "MSI"};
 def __init__(self):
  self.type = "any";
  self.filename = "./barcode.png";
  self.size = 1;
  self.hidesn = False;
  self.hidecd = False;
  self.hidetext = False;
  self.textxy = (1, 1, 1);
  self.barheight = (48, 54);
  self.barcolor = (0, 0, 0);
  self.textcolor = (0, 0, 0);
  self.bgcolor = (255, 255, 255);
  self.return_check = False;
  self.return_type = "dict";
  self.barcode_type = "upca";
 def version_info(self):
  return version_info();
 def version_date(self):
  return version_date();
 def exec_function(self, function, *argument):
  if(hasattr(upcean, function) and callable(getattr(upcean, function))):
   return getattr(upcean, function)(*argument);
  if(not hasattr(upcean, function) or not callable(getattr(upcean, function))):
   return False;
 def run_function(self, function, *argument):
  if(hasattr(upcean, function) and callable(getattr(upcean, function))):
   return getattr(upcean, function)(*argument);
  if(not hasattr(upcean, function) or not callable(getattr(upcean, function))):
   return False;
 def supported_barcodes(self):
  return barcode_support(self.return_type);
 def barcode_support(self):
  return barcode_support(self.return_type);
 def get_barcode_name(self):
  return barcode_support(self.barcode_type);
 def create(self):
  return getattr(upcean, "create_"+self.type+"_barcode")(self.code, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def draw(self):
  return getattr(upcean, "draw_"+self.type+"_barcode")(self.code, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def create_barcode(self):
  return create_barcode(self.type, self.code, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def draw_barcode(self):
  return draw_barcode(self.type, self.code, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def create_from_barcode(self):
  return getattr(upcean, "create_"+self.type+"_barcode_from_"+self.outtype)(self.code, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def draw_from_barcode(self):
  return getattr(upcean, "draw_"+self.type+"_barcode_from_"+self.outtype)(self.code, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def create_vw_barcode(self):
  if(self.type=="upca"):
   return create_vw_barcode_upca(self.code, self.price, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "create_vw_barcode_to_"+self.type) and callable(getattr(upcean, "create_vw_barcode_to_"+self.type))):
    return getattr(upcean, "create_vw_barcode_to_"+self.type)(self.code, self.price, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "create_vw_barcode_to_"+self.type) or not callable(getattr(upcean, "create_vw_barcode_to_"+self.type))):
    return False;
 def draw_vw_barcode(self):
  if(self.type=="upca"):
   return drawvw_upca(self.code, self.price, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "draw_vw_barcode_to_"+self.type) and callable(getattr(upcean, "draw_vw_barcode_to_"+self.type))):
    return getattr(upcean, "draw_vw_barcode_to_"+self.type)(self.code, self.price, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "draw_vw_barcode_to_"+self.type) or not callable(getattr(upcean, "draw_vw_barcode_to_"+self.type))):
    return False;
 def create_goodwill_barcode(self):
  if(self.type=="upca"):
   return create_goodwill_barcode_upca(self.code, self.price, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "create_goodwill_barcode_to_"+self.type) and callable(getattr(upcean, "create_goodwill_barcode_to_"+self.type))):
    return getattr(upcean, "create_goodwill_barcode_to_"+self.type)(self.code, self.price, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "create_goodwill_barcode_to_"+self.type) or not callable(getattr(upcean, "create_goodwill_barcode_to_"+self.type))):
    return False;
 def draw_goodwill_barcode(self):
  if(self.type=="upca"):
   return draw_goodwill_barcode_upca(self.code, self.price, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "draw_goodwill_barcode_to_"+self.type) and callable(getattr(upcean, "draw_goodwill_barcode_to_"+self.type))):
    return getattr(upcean, "draw_goodwill_barcode_to_"+self.type)(self.code, self.price, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "draw_goodwill_barcode_to_"+self.type) or not callable(getattr(upcean, "draw_goodwill_barcode_to_"+self.type))):
    return False;
 def create_coupon_barcode(self):
  if(self.type=="upca"):
   return create_coupon_barcode_upca(self.numbersystem, self.manufacturer, self.family, self.value, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "create_coupon_barcode_to_"+self.type) and callable(getattr(upcean, "create_coupon_barcode_to_"+self.type))):
    return getattr(upcean, "create_coupon_barcode_to_"+self.type)(self.numbersystem, self.manufacturer, self.family, self.value, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "create_coupon_barcode_to_"+self.type) or not callable(getattr(upcean, "create_coupon_barcode_to_"+self.type))):
    return False;
 def draw_coupon_barcode(self):
  if(self.type=="upca"):
   return draw_coupon_barcode_upca(self.numbersystem, self.manufacturer, self.family, self.value, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
  if(not self.type=="upca" and (self.type=="ean13" or self.type=="itf14")):
   if(hasattr(upcean, "draw_coupon_barcode_to_"+self.type) and callable(getattr(upcean, "draw_coupon_barcode_to_"+self.type))):
    return getattr(upcean, "draw_coupon_barcode_to_"+self.type)(self.numbersystem, self.manufacturer, self.family, self.value, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
   if(not hasattr(upcean, "draw_coupon_barcode_to_"+self.type) or not callable(getattr(upcean, "draw_coupon_barcode_to_"+self.type))):
    return False;
 def validate_checksum(self):
  return getattr(upcean, "validate_"+self.type+"_checksum")(self.code, self.return_check);
 def validate_luhn_checksum(self):
  return validate_luhn_checksum(self.code, self.codelen, self.return_check);
 def get_checksum(self):
  return getattr(upcean, "get_"+self.type+"_checksum")(self.code);
 def get_info(self):
  return getattr(upcean, "get_"+self.type+"_info")(self.code);
 def get_packagecode(self):
  return getattr(upcean, "get_"+self.type+"_packagecode")(self.code);
 def get_numbersystem(self):
  return getattr(upcean, "get_"+self.type+"_numbersystem")(self.code);
 def get_manufacturer(self):
  return getattr(upcean, "get_"+self.type+"_manufacturer")(self.code);
 def get_product(self):
  return getattr(upcean, "get_"+self.type+"_product")(self.code);
 def get_checkdigit(self):
  return getattr(upcean, "get_"+self.type+"_checkdigit")(self.code);
 def get_luhn_checksum(self):
  return get_luhn_checksum(self.code, self.codelen);
 def fix_checksum(self):
  return getattr(upcean, "fix_"+self.type+"_checksum")(self.code);
 def fix_luhn_checksum(self):
  return fix_luhn_checksum(self.code, self.codelen);
 def convert(self):
  return getattr(upcean, "convert_"+self.type+"_to_"+self.outtype)(self.code);
 def print(self):
  return getattr(upcean, "print_"+self.type)(self.code);
 def print_convert(self):
  return getattr(upcean, "print_convert_"+self.type+"_to_"+self.outtype)(self.code);
 def make_vw(self):
  if(self.type=="upca"):
   return make_vw_upca(self.code, self.price);
  if(self.type!="upca"):
   return getattr(upcean, "make_vw_to_"+self.type)(self.code, self.price);
 def make_goodwill(self):
  if(self.type=="upca"):
   return make_goodwill_upca(self.code, self.price);
  if(self.type!="upca"):
   return getattr(upcean, "make_goodwill_to_"+self.type)(self.code, self.price);
 def make_coupon(self):
  if(self.type=="upca"):
   return make_coupon_upca(self.numbersystem, self.manufacturer, self.family, self.value);
  if(self.type!="upca"):
   return getattr(upcean, "make_coupon_to_"+self.type)(self.numbersystem, self.manufacturer, self.family, self.value);
 def get_upca_info_from_upce(self):
  return get_upca_info_from_upce(self.code);
 def get_upce_as_upca_info(self):
  return get_upca_info_from_upce(self.code);
 def get_gs1_prefix(self):
  return get_gs1_prefix(self.code);
 def get_isbn_identifier(self):
  return get_isbn_identifier(self.code);
 def get_upca_ns(self):
  return get_upca_ns(self.code);
 def get_itf14_type(self):
  return get_itf14_type(self.code);
 def get_vw_info(self):
  return get_upca_vw_info(self.code);
 def get_vw_numbersystem(self):
  return get_upca_vw_numbersystem(self.code);
 def get_vw_code(self):
  return get_upca_vw_code(self.code);
 def get_vw_price(self):
  return get_upca_vw_price(self.code);
 def get_vw_pricecs(self):
  return get_upca_vw_pricecs(self.code);
 def get_vw_checkdigit(self):
  return get_upca_vw_checkdigit(self.code);
 def get_goodwill_info(self):
  return get_upca_goodwill_info(self.code);
 def get_goodwill_numbersystem(self):
  return get_upca_goodwill_numbersystem(self.code);
 def get_goodwill_code(self):
  return get_upca_goodwill_code(self.code);
 def get_goodwill_price(self):
  return get_upca_goodwill_price(self.code);
 def get_goodwill_checkdigit(self):
  return get_upca_goodwill_checkdigit(self.code);
 def get_coupon_info(self):
  return get_upca_coupon_info(self.code);
 def get_coupon_numbersystem(self):
  return get_upca_coupon_numbersystem(self.code);
 def get_coupon_manufacturer(self):
  return get_upca_coupon_manufacturer(self.code);
 def get_coupon_family(self):
  return get_upca_coupon_family(self.code);
 def get_coupon_value(self):
  return get_upca_coupon_value(self.code);
 def get_coupon_checkdigit(self):
  return get_upca_coupon_checkdigit(self.code);
 def get_coupon_value_code(self):
  return get_upca_coupon_value_code(self.code);
 def get_bcn_mii_prefix(self):
  return get_bcn_mii_prefix(self.code);
 def get_bcn_info(self):
  return get_bcn_info(self.code);
 def get_bcn_mii(self):
  return get_bcn_mii(self.code);
 def get_bcn_iin(self):
  return get_bcn_iin(self.code);
 def get_bcn_account(self):
  return get_bcn_account(self.code);
 def get_bcn_checkdigit(self):
  return get_bcn_checkdigit(self.code);
 def get_ups_info(self):
  return get_ups_info(self.code);
 def get_ups_accountnumber(self):
  return get_ups_accountnumber(self.code);
 def get_ups_servicetype(self):
  return get_ups_servicetype(self.code);
 def get_ups_servicetype_info(self):
  return get_ups_servicetype_info(self.code);
 def get_ups_invoicenumber(self):
  return get_ups_invoicenumber(self.code);
 def get_ups_packagenumber(self):
  return get_ups_packagenumber(self.code);
 def get_ups_checkdigit(self):
  return get_ups_checkdigit(self.code);
 def get_new_imei_info(self):
  return get_new_imei_info(self.code);
 def get_new_imei_tac(self):
  return get_new_imei_tac(self.code);
 def get_new_imei_serialnumber(self):
  return get_new_imei_serialnumber(self.code);
 def get_new_imei_checkdigit(self):
  return get_new_imei_checkdigit(self.code);
 def get_old_imei_info(self):
  return get_old_imei_info(self.code);
 def get_old_imei_tac(self):
  return get_old_imei_tac(self.code);
 def get_old_imei_fac(self):
  return get_old_imei_fac(self.code);
 def get_old_imei_serialnumber(self):
  return get_old_imei_serialnumber(self.code);
 def get_old_imei_checkdigit(self):
  return get_old_imei_checkdigit(self.code);
 def get_new_imeisv_info(self):
  return get_new_imeisv_info(self.code);
 def get_new_imeisv_tac(self):
  return get_new_imeisv_tac(self.code);
 def get_new_imeisv_serialnumber(self):
  return get_new_imeisv_serialnumber(self.code);
 def get_new_imeisv_checkdigit(self):
  return get_new_imeisv_checkdigit(self.code);
 def get_old_imeisv_info(self):
  return get_old_imeisv_info(self.code);
 def get_old_imeisv_tac(self):
  return get_old_imeisv_tac(self.code);
 def get_old_imeisv_fac(self):
  return get_old_imeisv_fac(self.code);
 def get_old_imeisv_serialnumber(self):
  return get_old_imeisv_serialnumber(self.code);
 def get_old_imeisv_checkdigit(self):
  return get_old_imeisv_checkdigit(self.code);
 def get_save_filename(self):
  return get_save_filename(self.filename);
