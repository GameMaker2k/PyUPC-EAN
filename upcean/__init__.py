#!/usr/bin/python

from __future__ import division;
import sys, re, upcean.validate, upcean.convert, upcean.getprefix;
import upcean.upca, upcean.upce, upcean.ean13, upcean.ean8, upcean.itf, upcean.itf14, upcean.code39, upcean.code93;
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
from upcean.itf import *;
from upcean.itf14 import *;
from upcean.code39 import *;
from upcean.code93 import *;
'''
from upcean.cuecat import *;
'''

'''
Shortcut Codes by Kazuki Przyborowski
'''
def validate_barcode(upc,return_check=False):
	if(len(upc)==8): 
		return validate_upce(upc,return_check);
	if(len(upc)==12): 
		return validate_upca(upc,return_check);
	if(len(upc)==13): 
		return validate_ean13(upc,return_check);
	if(len(upc)==14): 
		return validate_itf14(upc,return_check);
	return False;
def fix_barcode_checksum(upc):
	if(len(upc)==7): 
		return upc+validate_upce(upc,true);
	if(len(upc)==11): 
		return upc+validate_upca(upc,true);
	if(len(upc)==12): 
		return upc+validate_ean13(upc,true);
	if(len(upc)==13): 
		return upc+validate_itf14(upc,true);
	return False;
def create_barcode(upc,outfile="./barcode.png",resize=1,hidecd=False):
	if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
		resize = 1;
	if(len(upc)==7 or len(upc)==8):
		return create_upce(upc,outfile,resize,hidecd);
	if(len(upc)==11 or len(upc)==12):
		return create_upca(upc,outfile,resize,hidecd);
	if(len(upc)==13): 
		return create_ean13(upc,outfile,resize,hidecd);
	if(len(upc)==14): 
		return create_itf14(upc,outfile,resize,hidecd);
	return False;

