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

    $FileInfo: support.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import imp, platform;
from upcean.versioninfo import getcuryear, __author__, __copyright__, __credits__, __copyright_year__, __license__, __license_string__, __maintainer__, __email__, __status__, __project__, __project_url__, __version_info__, __build_time__, __build_time_utc__, __build_python_info__, __build_python_is_set__, get_build_python_info, __revision__, __version__, __version_alt__, version_info, __version_date_info__, __version_date__, __version_date_alt__, version_date;

''' // Barcode Support List '''
bctype_dict={'EAN2': "ean2", 'UPCS2': "ean2", 'EAN5': "ean5", 'UPCS5': "ean5", 'UPCA': "upca", 'UPCE': "upce", 'EAN13': "ean13",'EAN8': "ean8",'STF': "stf", 'ITF': "itf", 'ITF6': "itf6", 'ITF14': "itf14", 'CODE11': "code11", 'CODE39': "code39", 'CODE93': "code93", 'CODE128': "code128", 'CODE128Alt': "code128alt", 'CODE128Dec': "code128dec", 'CODABAR': "codabar", 'MSI': "msi", "GOODWILL": "goodwill"};
bctype_dict_alt={'ean2': "EAN2", 'ean5': "EAN5", 'upca': "UPCA", 'upce': "UPCE", 'ean13': "EAN13",'ean8': "EAN8",'stf': "STF", 'itf': "ITF", 'itf6': "ITF6", 'itf14': "ITF14", 'code11': "CODE11", 'code39': "CODE39", 'code93': "CODE93", 'code128': "CODE128", 'code128alt': "CODE128Alt", 'code128dec': "CODE128Dec", 'codabar': "CODABAR", 'msi': "MSI", "goodwill": "GOODWILL"};
bctype_list=["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dec", "codabar", "msi"];
PROVIDED_BARCODES=bctype_list;
bctype_tuple=("ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dect", "codabar", "msi");
bctype_name={'ean2': "EAN-2", 'ean5': "EAN-5", 'upca': "UPC-A", 'upce': "UPC-E", 'ean13': "EAN-13", 'ean8': "EAN-8", 'stf': "STF", 'itf': "ITF", 'itf6': "ITF-6", 'itf14': "ITF-14", "code11": "Code 11", "code39": "Code 39", "code93": "Code 93", "code128": "Code 128", "code128alt": "Code 128 Alt", "code128dec": "Code 128 Dec", 'codabar': "Codabar", 'msi': "MSI", "goodwill": "GOODWILL"};
def supported_barcodes(return_type="dict"):
 if(return_type=="dict"):
  return {'EAN2': "ean2", 'UPCS2': "ean2", 'EAN5': "ean5", 'UPCS5': "ean5", 'UPCA': "upca", 'UPCE': "upce", 'EAN13': "ean13",'EAN8': "ean8",'STF': "stf", 'ITF': "itf", 'ITF6': "itf6", 'ITF14': "itf14", 'CODE11': "code11", 'CODE39': "code39", 'CODE93': "code93", 'CODE128': "code128", 'CODE128Alt': "code128alt", 'CODE128Dec': "code128dec", 'CODABAR': "codabar", 'MSI': "msi", "GOODWILL": "goodwill"};
 if(return_type=="list"):
  return ["ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dec", "codabar", "msi", "goodwill"];
 if(return_type=="tuple"):
  return ("ean2", "ean2", "ean5", "ean5", "upca", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dec", "codabar", "msi", "goodwill");
 return False;
def barcode_support(return_type="dict"):
 return supported_barcodes(return_type);
def get_barcode_name(barcode_type="upca"):
 bctype_name={'ean2': "EAN-2", 'ean5': "EAN-5", 'upca': "UPC-A", 'upce': "UPC-E", 'ean13': "EAN-13", 'ean8': "EAN-8", 'stf': "STF", 'itf': "ITF", 'itf6': "ITF-6", 'itf14': "ITF-14", "code11": "Code 11", "code39": "Code 39", "code93": "Code 93", "code128": "Code 128", "code128alt": "Code 128 Alt", "code128dec": "Code 128 dec", 'codabar': "Codabar", 'msi': "MSI", "goodwill": "GOODWILL"};
 return bctype_name.get(barcode_type, False);

def check_for_cairo():
 # PIL Support Check
 cairosupport = True;
 try:
  imp.find_module('cairo');
  cairosupport = True;
 except ImportError:
  cairosupport = False
 return cairosupport;

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
   try:
    from PIL import Image, ImageDraw, ImageFont;
    pilsupport = True;
   except ImportError:
    pilsupport = False;
   return pilsupport;
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
   try:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except AttributeError:
    pil_is_pillow = False;
   except NameError:
    pil_is_pillow = False;
  except NameError:
   try:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except AttributeError:
    pil_is_pillow = False;
   except NameError:
    pil_is_pillow = False;
 return pil_is_pillow;

def check_pil_is_pillow():
 pilsupport = False;
 if(check_for_pil()):
  pilsupport = True;
 pil_is_pillow = False;
 if(pilsupport is True and check_for_pillow() is True):
  pil_is_pillow = True;
 if(pilsupport is False or (pilsupport is True and check_for_pillow() is False)):
  pil_is_pillow = False;
 return pil_is_pillow;

def check_if_pil_is_pillow():
 pil_is_pillow = check_pil_is_pillow();
 return pil_is_pillow;

def check_for_pil_only():
 pilsupport = False;
 if(check_for_pil()):
  pilsupport = True;
 pil_is_not_pillow = False;
 if((pilsupport is True and check_for_pillow() is True) or pilsupport is False):
  pil_is_not_pillow = False;
 if(pilsupport is True and check_for_pillow() is False):
  pil_is_not_pillow = True;
 return pil_is_pillow;

def check_only_for_pil():
 pil_is_not_pillow = check_pil_is_pillow();
 return pil_is_not_pillow;

def check_pil_is_not_pillow():
 pil_is_not_pillow = check_pil_is_pillow();
 return pil_is_not_pillow;

def check_if_pil_is_not_pillow():
 pil_is_not_pillow = check_pil_is_pillow();
 return pil_is_not_pillow;

def get_pil_version(infotype=None):
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
  try:
   pil_ver = Image.VERSION;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
  except AttributeError:
   pil_ver = None;
  except NameError:
   pil_ver = None;
  if(pillow_ver is None and pil_ver is not None):
   pil_info = {'pil_ver': pil_ver, 'pil_is_pillow': pil_is_pillow};
   return pil_info.get(infotype, pil_info);
  if(pillow_ver is not None and pil_ver is not None):
   pil_info = {'pil_ver': pil_ver, 'pillow_ver': pillow_ver, 'pil_is_pillow': pil_is_pillow};
   return pil_info.get(infotype, pil_info);
  if(pillow_ver is not None and pil_ver is None):
   pil_info = {'pillow_ver': pillow_ver, 'pil_is_pillow': pil_is_pillow};
   return pil_info.get(infotype, pil_info);

def get_pillow_version(infotype=None):
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
   try:
    pillow_ver = Image.__version__;
    pil_is_pillow = True;
   except AttributeError:
    pillow_ver = None;
    pil_is_pillow = False;
   except NameError:
    pillow_ver = None;
    pil_is_pillow = False;
  except NameError:
   try:
    pillow_ver = Image.__version__;
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
   pillow_info = {'pillow_ver': pillow_ver, 'pil_is_pillow': pil_is_pillow};
   return pillow_info.get(infotype, pillow_info);

def get_cairo_version(infotype=None):
 cairosupport = check_for_cairo();
 if(not cairosupport):
  return cairosupport;
 if(cairosupport):
  import cairo;
  cairo_ver = cairo.version;
  cairo_info = {'cairo_ver': cairo_ver};
  return cairo_info.get(infotype, cairo_info);

linuxdist = None;
try:
 linuxdist = platform.linux_distribution();
except AttributeError:
 linuxdist = None;

python_info = {'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(), 'system': platform.system(), 'uname': platform.uname(), 'architecture': platform.architecture(), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()};
if(not __build_python_is_set__):
 __build_python_info__ = python_info;
def get_python_info(infotype=None):
 global python_info;
 python_info = python_info;
 if(infotype is None):
  return python_info;
 if(infotype is not None):
  return python_info.get(infotype, python_info);

pilsupport = check_for_pil();
cairosupport = check_for_cairo();
