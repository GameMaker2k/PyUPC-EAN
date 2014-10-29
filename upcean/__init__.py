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

    $FileInfo: __init__.py - Last Update: 10/29/2014 Ver. 2.7.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import sys, re, imp;

__author__ = "Kazuki Przyborowski";
__copyright__ = "Copyright 2011-2014, Game Maker 2k";
__credits__ = ["Kazuki Przyborowski", "Game Maker 2k"];
__license__ = "Revised BSD License";
__maintainer__ = "Kazuki Przyborowski";
__email__ = "kazuki.przyborowski@gmail.com";
__status__ = "Production";
__project__ = "PyUPC-EAN";
__project_url__ = "https://pypi.python.org/pypi/PyUPC-EAN";
__version_info__ = (2, 7, 0, "RC 1");
__revision__ = __version_info__[3];
if(__version_info__[3]!=None):
 __version__ = "{major}.{minor}.{build} {release}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2], release=__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = "{major}.{minor}.{build}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2]);
__version_alt__ = "{major}.{minor}.{build}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2]);
def version_info():
 global __version_info__;
 if(__version_info__[3]!=None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": __version_info__[3]};
 if(__version_info__[3]==None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": None};
__version_date_info__ = (2014, 10, 21, "RC 1");
def version_date():
 global __version_info__;
 if(__version_date_info__[3]!=None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": __version_date_info__[3]};
 if(__version_date_info__[3]==None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": None};
__version_date__ = "{year}.{month}.{day}".format(year=__version_date_info__[0], month=__version_date_info__[1], day=__version_date_info__[2]);
__version_date_alt__ = "{year}.{month}.{day} {release}".format(year=__version_date_info__[0], month=__version_date_info__[1], day=__version_date_info__[2], release=__version_date_info__[2]);

# PIL Support Check
pilsupport = True;
try:
 imp.find_module('PIL')
 pilsupport = True;
except ImportError:
 try:
  imp.find_module('Image')
  pilsupport = True;
 except ImportError:
  pilsupport = False;

import upcean.validate, upcean.convert, upcean.getprefix, upcean.getsfname;
import upcean.fonts, upcean.xml;
if(pilsupport==True):
 import upcean.barcodes.ean2, upcean.barcodes.ean5, upcean.barcodes.upca, upcean.barcodes.upce, upcean.barcodes.ean13, upcean.barcodes.ean8, upcean.barcodes.itf, upcean.barcodes.itf14;
 import upcean.barcodes.code11, upcean.barcodes.code39, upcean.barcodes.code93, upcean.barcodes.codabar, upcean.barcodes.msi;
 from upcean.barcodes import *;
 ''' // Import extra stuff '''
 from upcean.fonts import *;
''' // Code for validating UPC/EAN by Kazuki Przyborowski '''
from upcean.validate import *;
''' // Code for converting UPC/EAN by Kazuki Przyborowski '''
from upcean.convert import *;
''' // Code for getting GS1 Prefix EAN-8/EAN-13/ITF-14 by Kazuki Przyborowski '''
from upcean.getprefix import *;
''' // Code for getting save file name and type by Kazuki Przyborowski '''
from upcean.getsfname import *;
''' // Import extra stuff '''
from upcean.xml import *;

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
  self.type = "upca";
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
 def create_barcode(self):
  return create_barcode(self.type, self.code, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def draw_barcode(self):
  return draw_barcode(self.type, self.code, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def create_from_barcode(self):
  return getattr(upcean, "create_"+self.type+"_barcode_from_"+self.outtype)(self.code, self.filename, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def draw_from_barcode(self):
  return getattr(upcean, "draw_"+self.type+"_barcode_from_"+self.outtype)(self.code, self.size, (self.hidesn, self.hidecd, self.hidetext), self.barheight, self.textxy, (self.barcolor, self.textcolor, self.bgcolor));
 def create_from_xml(self):
  return create_barcode_from_xml_file(self.xmlfile, False);
 def draw_from_xml(self):
  return draw_barcode_from_xml_file(self.xmlfile);
 def create_from_xml_string(self):
  return create_barcode_from_xml_string(self.xmlfile, False);
 def draw_from_xml_string(self):
  return draw_barcode_from_xml_string(self.xmlfile);
 def create_from_json(self):
  return create_barcode_from_json_file(self.jsonfile, False);
 def draw_from_json(self):
  return draw_barcode_from_json_file(self.jsonfile);
 def create_from_json_string(self):
  return create_barcode_from_json_string(self.jsonfile, False);
 def draw_from_json_string(self):
  return draw_barcode_from_json_string(self.jsonfile);
 def create_from_qs(self):
  return create_barcode_from_qs_file(self.jsonfile, False);
 def draw_from_qs(self):
  return draw_barcode_from_qs_file(self.jsonfile);
 def validate_checksum(self):
  return getattr(upcean, "validate_"+self.type+"_checksum")(self.code, self.return_check);
 def validate_luhn_checksum(self):
  return validate_luhn_checksum(self.code, self.codelen, self.return_check);
 def get_checksum(self):
  return getattr(upcean, "get_"+self.type+"_checksum")(self.code);
 def get_barcode_info(self):
  return getattr(upcean, "get_"+self.type+"_barcode_info")(self.code);
 def get_luhn_checksum(self):
  return get_luhn_checksum(self.code, self.codelen);
 def get_digital_root(self):
  return get_digital_root(self.number);
 def fix_checksum(self):
  return getattr(upcean, "fix_"+self.type+"_checksum")(self.code);
 def fix_luhn_checksum(self):
  return fix_luhn_checksum(self.code, self.codelen);
 def convert(self):
  return getattr(upcean, "convert_barcode_from_"+self.type+"_to_"+self.outtype)(self.code);
 def print_convert(self):
  return getattr(upcean, "print_convert_barcode_from_"+self.type+"_to_"+self.outtype)(self.code);
 def convert_barcode(self):
  return convert_barcode(self.type, self.outtype, self.code);
 def print_convert_barcode(self):
  return print_convert_barcode(self.type, self.outtype, self.code);
 def make_barcode(self):
  return make_barcode(self.type, self.numbersystem, self.manufacturer, self.product);
 def make_vw(self):
  return getattr(upcean, "make_vw_to_"+self.type+"_barcode")(self.code, self.price);
 def make_vw_barcode(self):
  return getattr(upcean, "make_vw_to_"+self.type+"_barcode")(self.code, self.price);
 def make_goodwill(self):
  return getattr(upcean, "make_goodwill_to_"+self.type+"_barcode")(self.code, self.price);
 def make_goodwill_barcode(self):
  return getattr(upcean, "make_goodwill_to_"+self.type+"_barcode")(self.code, self.price);
 def make_coupon(self):
  return getattr(upcean, "make_coupon_to_"+self.type+"_barcode")(self.numbersystem, self.manufacturer, self.family, self.value);
 def make_coupon_barcode(self):
  return getattr(upcean, "make_coupon_to_"+self.type+"_barcode")(self.numbersystem, self.manufacturer, self.family, self.value);
 def get_upca_info_from_upce(self):
  return get_upca_info_from_upce(self.code);
 def get_upce_as_upca_info(self):
  return get_upca_info_from_upce(self.code);
 def get_gs1_prefix(self):
  return get_gs1_prefix(self.code);
 def get_isbn_identifier(self):
  return get_isbn_identifier(self.code);
 def get_upca_barcode_ns(self):
  return get_upca_barcode_ns(self.code);
 def get_itf14_barcode_type(self):
  return get_itf14_barcode_type(self.code);
 def get_vw_info_barcode(self):
  return get_upca_vw_barcode_info(self.code);
 def get_goodwill_info_barcode(self):
  return get_upca_goodwill_barcode_info(self.code);
 def get_coupon_info_barcode(self):
  return get_upca_coupon_barcode_info(self.code);
 def get_bcn_info(self):
  return get_bcn_info(self.code);
 def get_ups_barcode_info(self):
  return get_ups_barcode_info(self.code);
 def get_new_imei_barcode_info(self):
  return get_new_imei_barcode_info(self.code);
 def get_old_imei_barcode_info(self):
  return get_old_imei_barcode_info(self.code);
 def get_new_imeisv_barcode_info(self):
  return get_new_imeisv_barcode_info(self.code);
 def get_old_imeisv_barcode_info(self):
  return get_old_imeisv_barcode_info(self.code);
 def get_save_filename(self):
  return get_save_filename(self.filename);
