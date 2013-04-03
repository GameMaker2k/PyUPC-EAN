#!/usr/bin/python

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

    $FileInfo: __init__.py - Last Update: 04/02/2013 Ver. 2.3.5 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
version_info = (2, 3, 5, "RC 1");
if(version_info[3]!=None):
 __version__ = str(version_info[0])+"."+str(version_info[1])+"."+str(version_info[2])+" "+str(version_info[3]);
if(version_info[3]==None):
 __version__ = str(version_info[0])+"."+str(version_info[1])+"."+str(version_info[2]);
import sys, re, upcean.validate, upcean.convert, upcean.getprefix;
import upcean.upca, upcean.upce, upcean.ean13, upcean.ean8, upcean.itf, upcean.itf14, upcean.code11, upcean.code39, upcean.code93;
'''
import upcean.cuecat;
'''
from sys import argv;
from upcean.validate import *;
from upcean.convert import *;
from upcean.getprefix import *;
from upcean.upca import *;
from upcean.upce import *;
from upcean.ean13 import *;
from upcean.ean8 import *;
from upcean.stf import *;
from upcean.itf import *;
from upcean.itf14 import *;
from upcean.code11 import *;
from upcean.code39 import *;
from upcean.code93 import *;
'''
from upcean.cuecat import *;
'''

'''
Shortcut Codes by Kazuki Przyborowski
'''
def create_barcode(upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
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
    return create_upce(upc,outfile,resize,hideinfo,barheight);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   if(re.findall("^([0-1])", upc)):
    return create_upce(upc+" "+supplement,outfile,resize,hideinfo,barheight);
   if(re.findall("^([2-9])", upc)):
    return create_ean8(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 if(len(upc)==11 or len(upc)==12):
  if(supplement==None):
   return create_upca(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_upca(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 if(len(upc)==13): 
  if(supplement==None):
   return create_ean13(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_ean13(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 if(len(upc)==14): 
  if(supplement==None):
   return create_itf14(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_itf14(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 return False;
def draw_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_barcode(upc,None,resize,hideinfo,barheight);

def create_upc(upc,outfile="./upc.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
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
   return create_upce(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_upce(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 if(len(upc)==11 or len(upc)==12):
  if(supplement==None):
   return create_upca(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_upca(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 return False;
def draw_upc(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_upc(upc,None,resize,hideinfo,barheight);

def create_ean(upc,outfile="./ean.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
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
   return create_ean8(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_ean8(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 if(len(upc)==12 or len(upc)==13): 
  if(supplement==None):
   return create_ean13(upc,outfile,resize,hideinfo,barheight);
  if(supplement!=None):
   return create_ean13(upc+" "+supplement,outfile,resize,hideinfo,barheight);
 return False;
def draw_ean(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ean(upc,None,resize,hideinfo,barheight);

def create_issn13_from_issn8(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ean13(convert_issn8_to_issn13(upc),outfile,resize,hideinfo,barheight);
def draw_issn13_from_issn8(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_issn13_from_issn8(upc,None,resize,hideinfo,barheight);
def create_issn13(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_issn13_from_issn8(upc,outfile,resize,hideinfo,barheight);
def draw_issn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_issn13(upc,None,resize,hideinfo,barheight);

def create_isbn13_from_isbn10(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ean13(convert_isbn10_to_isbn13(upc),outfile,resize,hideinfo,barheight);
def draw_isbn13_from_isbn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_isbn13_from_isbn10(upc,None,resize,hideinfo,barheight);
def create_isbn13(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_isbn13_from_isbn10(upc,outfile,resize,hideinfo,barheight);
def draw_isbn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_isbn13(upc,None,resize,hideinfo,barheight);

def create_ismn13_from_ismn10(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ean13(convert_ismn10_to_ismn13(upc),outfile,resize,hideinfo,barheight);
def draw_ismn13_from_ismn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ismn13_from_ismn10(upc,None,resize,hideinfo,barheight);
def create_ismn13(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ismn13_from_ismn10(upc,outfile,resize,hideinfo,barheight);
def draw_ismn13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ismn13(upc,None,resize,hideinfo,barheight);

def create_vw_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_upca(make_vw_upca(code, price),outfile,resize,hideinfo,barheight);
def draw_vw_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_vw_upca(make_vw_upca(code, price),None,resize,hideinfo,barheight);
def create_vw_to_ean13(code,price,outfile="./vw-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ean13(make_vw_to_ean13(code, price),outfile,resize,hideinfo,barheight);
def draw_vw_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_vw_to_ean13(make_vw_upca(code, price),None,resize,hideinfo,barheight);
def create_vw_to_itf14(code,price,outfile="./vw-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_itf14(make_vw_to_itf14(code, price),outfile,resize,hideinfo,barheight);
def draw_vw_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_vw_to_itf14(make_vw_upca(code, price),None,resize,hideinfo,barheight);


def create_coupon_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_upca(make_coupon_upca(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight);
def draw_vw_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_vw_upca(make_coupon_upca(numbersystem, manufacturer, family, value),None,resize,hideinfo,barheight);
def create_coupon_to_ean13(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_ean13(make_coupon_to_ean13(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight);
def draw_vw_to_ean13(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_vw_to_ean13(make_coupon_to_ean13(numbersystem, manufacturer, family, value),None,resize,hideinfo,barheight);
def create_coupon_to_itf14(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 return create_itf14(make_coupon_to_itf14(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight);
def draw_vw_to_itf14(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_vw_to_itf14(make_coupon_to_itf14(numbersystem, manufacturer, family, value),None,resize,hideinfo,barheight);
