'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: support.py - Last Update: 11/20/2014 Ver. 2.7.7 RC 3 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import imp;

''' // Barcode Support List '''
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

def check_for_pil():
 # PIL Support Check
 pilsupport = True;
 try:
  imp.find_module('PIL');
  pilsupport = True;
 except ImportError:
  try:
   imp.find_module('Image');
   pilsupport = True;
  except ImportError:
   pilsupport = False;
 return pilsupport;

def check_for_pillow():
 pilsupport = check_for_pil();
 if(not pilsupport):
  return pilsupport;
 if(pilsupport):
  from PIL import Image;
  try:
   pil_ver = Image.PILLOW_VERSION;
   pil_is_pillow = True;
  except AttributeError:
   pil_is_pillow = False;
  except NameError:
   pil_is_pillow = False;
 return pil_is_pillow;

def get_pil_version():
 pilsupport = check_for_pil();
 if(not pilsupport):
  return pilsupport;
 if(pilsupport):
  from PIL import Image;
  try:
   pillow_ver = Image.PILLOW_VERSION;
   pillow_ver = pillow_ver.split(".");
   pillow_ver = [int(x) for x in pillow_ver];
   pil_is_pillow = True;
  except AttributeError:
   pillow_ver = None;
   pil_is_pillow = False;
  except NameError:
   pillow_ver = None;
   pil_is_pillow = False;
  pil_ver = Image.VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  if(pillow_ver is None):
   return {'pil_ver': pil_ver, 'pil_is_pillow': pil_is_pillow};
  if(pillow_ver is not None):
   return {'pil_ver': pil_ver, 'pillow_ver': pillow_ver, 'pil_is_pillow': pil_is_pillow};

def get_pillow_version():
 pilsupport = check_for_pil();
 if(not pilsupport):
  return pilsupport;
 if(pilsupport):
  from PIL import Image;
  try:
   pillow_ver = Image.PILLOW_VERSION;
   pillow_ver = pillow_ver.split(".");
   pillow_ver = [int(x) for x in pillow_ver];
   pil_is_pillow = True;
  except AttributeError:
   pillow_ver = None;
   pil_is_pillow = False;
  except NameError:
   pillow_ver = None;
   pil_is_pillow = False;
  if(pillow_ver is None):
   return False;
  if(pillow_ver is not None):
   return {'pillow_ver': pillow_ver, 'pil_is_pillow': pil_is_pillow};
