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

    $FileInfo: __init__.py - Last Update: 04/01/2013 Ver. 2.3.0 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
version_info = (2, 3, 0, "RC 1");
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
def validate_barcode(upc,return_check=False):
 upc = str(upc);
 if(len(upc)==8): 
  if(re.findall("^([0-1])", upc)):
   return validate_upce(upc,return_check);
  if(re.findall("^([2-9])", upc)):
   return validate_ean8(upc,return_check);
 if(len(upc)==12): 
  return validate_upca(upc,return_check);
 if(len(upc)==13): 
  return validate_ean13(upc,return_check);
 if(len(upc)==14): 
  return validate_itf14(upc,return_check);
 return False;
def fix_barcode_checksum(upc):
 upc = str(upc);
 if(len(upc)==7): 
  if(re.findall("^([0-1])", upc)):
   return upc+str(validate_upce(upc,True));
  if(re.findall("^([2-9])", upc)):
   return upc+str(validate_ean8(upc,True));
 if(len(upc)==11): 
  return upc+str(validate_upca(upc,True));
 if(len(upc)==12): 
  return upc+str(validate_ean13(upc,True));
 if(len(upc)==13): 
  return upc+str(validate_itf14(upc,True));
 return False;
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
def validate_upc(upc,return_check=False):
 upc = str(upc);
 if(len(upc)==8): 
  return validate_upce(upc,return_check);
 if(len(upc)==12): 
  return validate_upca(upc,return_check);
 return False;
def fix_upc_checksum(upc):
 upc = str(upc);
 if(len(upc)==7): 
  return upc+str(validate_upce(upc,True));
 if(len(upc)==11): 
  return upc+str(validate_upca(upc,True));
 return False;
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
def validate_ean(upc,return_check=False):
 upc = str(upc);
 if(len(upc)==8): 
  return validate_ean8(upc,return_check);
 if(len(upc)==13): 
  return validate_ean13(upc,return_check);
 return False;
def fix_ean_checksum(upc):
 upc = str(upc);
 if(len(upc)==7): 
  return upc+str(validate_ean8(upc,True));
 if(len(upc)==12): 
  return upc+str(validate_ean13(upc,True));
 return False;
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
