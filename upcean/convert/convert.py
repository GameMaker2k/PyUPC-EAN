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

    $FileInfo: convert.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.validate;

def make_upca_barcode(numbersystem, manufacturer, product):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 product = str(product);
 if(len(numbersystem)<1 or len(manufacturer)<5 or len(product)<5):
  return False;
 if(len(numbersystem)>1):
  fix_matches = re.findall("^(\d{1})", numbersystem);
  numbersystem = fix_matches[0];
 if(len(manufacturer)>5):
  fix_matches = re.findall("^(\d{5})", manufacturer);
  manufacturer = fix_matches[0];
 if(len(product)>5):
  fix_matches = re.findall("^(\d{5})", product);
  product = fix_matches[0];
 upc = numbersystem+manufacturer+product;
 upc = upc+str(upcean.validate.validate_upca_checksum(upc, True));
 return upc;

def make_ean13_barcode(numbersystem, manufacturer, product):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 product = str(product);
 if(len(numbersystem)<2 or len(manufacturer)<5 or len(product)<5):
  return False;
 if(len(numbersystem)>2):
  fix_matches = re.findall("^(\d{2})", numbersystem);
  numbersystem = fix_matches[0];
 if(len(manufacturer)>5):
  fix_matches = re.findall("^(\d{5})", manufacturer);
  manufacturer = fix_matches[0];
 if(len(product)>5):
  fix_matches = re.findall("^(\d{5})", product);
  product = fix_matches[0];
 upc = numbersystem+manufacturer+product;
 upc = upc+str(upcean.validate.validate_ean13_checksum(upc, True));
 return upc;

def make_itf14_barcode(numbersystem, manufacturer, product):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 product = str(product);
 if(len(numbersystem)<3 or len(manufacturer)<5 or len(product)<5):
  return False;
 if(len(numbersystem)>3):
  fix_matches = re.findall("^(\d{3})", numbersystem);
  numbersystem = fix_matches[0];
 if(len(manufacturer)>5):
  fix_matches = re.findall("^(\d{5})", manufacturer);
  manufacturer = fix_matches[0];
 if(len(product)>5):
  fix_matches = re.findall("^(\d{5})", product);
  product = fix_matches[0];
 upc = numbersystem+manufacturer+product;
 upc = upc+str(upcean.validate.validate_itf14_checksum(upc, True));
 return upc;

def make_ean8_barcode(numbersystem, manufacturer, product):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 product = str(product);
 if(len(numbersystem)<1 or len(manufacturer)<3 or len(product)<3):
  return False;
 if(len(numbersystem)>1):
  fix_matches = re.findall("^(\d{1})", numbersystem);
  numbersystem = fix_matches[0];
 if(len(manufacturer)>3):
  fix_matches = re.findall("^(\d{3})", manufacturer);
  manufacturer = fix_matches[0];
 if(len(product)>3):
  fix_matches = re.findall("^(\d{3})", product);
  product = fix_matches[0];
 upc = numbersystem+manufacturer+product;
 upc = upc+str(upcean.validate.validate_ean8_checksum(upc, True));
 return upc;

def make_upce_barcode(numbersystem, manufacturer, product):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 product = str(product);
 if(len(numbersystem)<1 or len(manufacturer)<3 or len(product)<3):
  return False;
 if(len(numbersystem)>1):
  fix_matches = re.findall("^(\d{1})", numbersystem);
  numbersystem = fix_matches[0];
 if(len(manufacturer)>3):
  fix_matches = re.findall("^(\d{3})", manufacturer);
  manufacturer = fix_matches[0];
 if(len(product)>3):
  fix_matches = re.findall("^(\d{3})", product);
  product = fix_matches[0];
 upc = numbersystem+manufacturer+product;
 upc = upc+str(upcean.validate.validate_upce_checksum(upc, True));
 return upc;

def convert_barcode_from_upce_to_upca(upc):
 upc = str(upc);
 if(len(upc)==7):
  upc = upc+str(upcean.validate.validate_upce_checksum(upc,True));
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not re.findall("^(0|1)", upc)):
  return False;
 if(not upcean.validate.validate_upce_checksum(upc)):
  return False;
 if(re.findall("(0|1)(\d{5})([0-3])(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches = upc_matches[0];
  if(int(upc_matches[6])==0):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6]+"0000"+upc_matches[3]+upc_matches[4]+upc_matches[5]+upc_matches[7];
  if(int(upc_matches[6])==1):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6]+"0000"+upc_matches[3]+upc_matches[4]+upc_matches[5]+upc_matches[7];
  if(int(upc_matches[6])==2):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6]+"0000"+upc_matches[3]+upc_matches[4]+upc_matches[5]+upc_matches[7];
  if(int(upc_matches[6])==3):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+"00000"+upc_matches[4]+upc_matches[5]+upc_matches[7];
 if(re.findall("(0|1)(\d{5})([4-9])(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches = upc_matches[0];
  if(int(upc_matches[6])==4):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+"00000"+upc_matches[5]+upc_matches[7];
  if(int(upc_matches[6])==5):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+upc_matches[5]+"0000"+upc_matches[6]+upc_matches[7];
  if(int(upc_matches[6])==6):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+upc_matches[5]+"0000"+upc_matches[6]+upc_matches[7];
  if(int(upc_matches[6])==7):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+upc_matches[5]+"0000"+upc_matches[6]+upc_matches[7];
  if(int(upc_matches[6])==8):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+upc_matches[5]+"0000"+upc_matches[6]+upc_matches[7];
  if(int(upc_matches[6])==9):
   upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3]+upc_matches[4]+upc_matches[5]+"0000"+upc_matches[6]+upc_matches[7];
 return upce;

def convert_barcode_from_upca_to_ean13(upc):
 upc = str(upc);
 if(len(upc)==11):
  upc = upc+str(upcean.validate.validate_upca_checksum(upc,True));
 if(len(upc)>13 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 if(len(upc)==12):
  ean13 = "0"+upc;
 if(len(upc)==13):
  ean13 = upc;
 return ean13;
def convert_barcode_from_ean13_to_itf14(upc):
 upc = str(upc);
 if(len(upc)==11):
  upc = upc+str(upcean.validate.validate_upca_checksum(upc,True));
 if(len(upc)==12):
  upc = "0"+upc;
 if(len(upc)>14 or len(upc)<13):
  return False;
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(len(upc)==13):
  itf14 = "0"+upc;
 if(len(upc)==14):
  itf14 = upc;
 return itf14;

def convert_barcode_from_upce_to_ean13(upc):
 upc = str(upc);
 return convert_barcode_from_upca_to_ean13(convert_barcode_from_upce_to_upca(upc));

def convert_barcode_from_upce_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upce_to_ean13(upc));

def convert_barcode_from_upca_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upca_to_ean13(upc));

def convert_barcode_from_ean13_to_upca(upc):
 upc = str(upc);
 if(len(upc)==12):
  upc = "0"+upc;
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(not re.findall("^0(\d{12})", upc)):
  return False;
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upca = upc_matches[0];
 return upca;

def convert_barcode_from_itf14_to_ean13(upc):
 upc = str(upc);
 if(len(upc)==13):
  upc = "0"+upc;
 if(len(upc)>14 or len(upc)<14):
  return False;
 if(not upcean.validate.validate_itf14_checksum(upc)):
  return False;
 if(not re.findall("^(\d{1})(\d{12})(\d{1})", upc)):
  return False;
 if(re.findall("^(\d{1})(\d{12})(\d{1})", upc)):
  upc_matches = re.findall("^(\d{1})(\d{12})(\d{1})", upc);
  upc_matches = upc_matches[0];
  ean13 = upc_matches[1]+str(upcean.validate.validate_ean13_checksum(upc_matches[1], True));
 return ean13;

def convert_barcode_from_upca_to_upce(upc):
 upc = str(upc);
 if(len(upc)==11):
  upc = upc+str(upcean.validate.validate_upca_checksum(upc,True));
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 if(not re.findall("(0|1)(\d{11})", upc)):
  return False;
 upce = None;
 if(re.findall("(0|1)(\d{2})00000(\d{3})(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})00000(\d{3})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"0";
  upce = upce+upc_matches[3];
  return upce;
 if(re.findall("(0|1)(\d{2})10000(\d{3})(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})10000(\d{3})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"1";
  upce = upce+upc_matches[3];
  return upce;
 if(re.findall("(0|1)(\d{2})20000(\d{3})(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})20000(\d{3})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"2";
  upce = upce+upc_matches[3];
  return upce;
 if(re.findall("(0|1)(\d{3})00000(\d{2})(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{3})00000(\d{2})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"3";
  upce = upce+upc_matches[3];
  return upce;
 if(re.findall("(0|1)(\d{4})00000(\d{1})(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{4})00000(\d{1})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"4";
  upce = upce+upc_matches[3];
  return upce;
 if(re.findall("(0|1)(\d{5})00005(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})00005(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+"5";
  upce = upce+upc_matches[2];
  return upce;
 if(re.findall("(0|1)(\d{5})00006(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})00006(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+"6";
  upce = upce+upc_matches[2];
  return upce;
 if(re.findall("(0|1)(\d{5})00007(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})00007(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+"7";
  upce = upce+upc_matches[2];
  return upce;
 if(re.findall("(0|1)(\d{5})00008(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})00008(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+"8";
  upce = upce+upc_matches[2];
  return upce;
 if(re.findall("(0|1)(\d{5})00009(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})00009(\d{1})", upc);
  upc_matches = upc_matches[0];
  upce = upc_matches[0]+upc_matches[1]+"9";
  upce = upce+upc_matches[2];
  return upce;
 if(upce is None):
  return False;
 return upce;

def convert_barcode_from_ean13_to_upce(upc):
 upc = str(upc);
 return convert_barcode_from_upca_to_upce(convert_barcode_from_ean13_to_upca(upc));

def convert_barcode_from_itf14_to_upca(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_upca(convert_barcode_from_itf14_to_ean13(upc));

def convert_barcode_from_itf14_to_upce(upc):
 upc = str(upc);
 return convert_barcode_from_upca_to_upce(convert_barcode_from_itf14_to_upca(upc));

'''
// Changing a EAN-8 code to UPC-A and EAN-13 based on whats used at:
// Source: http://www.upcdatabase.com/
'''
def convert_barcode_from_ean8_to_upca(upc):
 upc = str(upc);
 if(len(upc)==7):
  upc = upc+str(upcean.validate.validate_ean8_checksum(upc,True));
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not upcean.validate.validate_ean8_checksum(upc)):
  return False;
 upca = "0000"+upc;
 return upca;

def convert_barcode_from_ean8_to_ean13(upc):
 upc = str(upc);
 return convert_barcode_from_upca_to_ean13(convert_barcode_from_ean8_to_upca(upc));

def convert_barcode_from_ean8_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_ean8_to_ean13(upc));

def convert_barcode_from_upca_to_ean8(upc):
 upc = str(upc);
 if(len(upc)==11):
  upc = upc+str(upcean.validate.validate_upca_checksum(upc,True));
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 if(not re.findall("^0000(\d{8})", upc)):
  return False;
 if(re.findall("^0000(\d{8})", upc)):
  upc_matches = re.findall("^0000(\d{8})", upc);
  ean8 = upc_matches[0];
 return ean8;

def convert_barcode_from_ean13_to_ean8(upc):
 upc = str(upc);
 return convert_barcode_from_upca_to_ean8(convert_barcode_from_ean13_to_upca(upc));

def convert_barcode_from_itf14_to_ean8(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_ean8(convert_barcode_from_itf14_to_ean13(upc));

'''
// ISSN (International Standard Serial Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Serial_Number
'''
def convert_barcode_from_issn8_to_issn13(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 upc = upc.replace("X", "");
 if(not upcean.validate.validate_issn8_checksum(upc)):
  return False;
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc);
  upc = fix_matches[0];
 issn13 = "977"+upc+"00"+str(upcean.validate.validate_ean13_checksum("977"+upc+"00",True));
 return issn13;
def convert_barcode_from_issn13_to_issn8(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 upc = upc.replace("X", "");
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(not re.findall("/^977(\d{7})/", upc)):
  return False;
 if(re.findall("^977(\d{7})", upc)):
  upc_matches = re.findall("^977(\d{7})", upc);
  issn8 = upc_matches[1]+upcean.validate.validate_issn8_checksum(upc_matches[1],True);
 return issn8;
def convert_barcode_from_issn8_to_ean13(upc):
 upc = str(upc);
 return convert_barcode_from_issn8_to_issn13(upc);
def convert_barcode_from_ean13_to_issn8(upc):
 upc = str(upc);
 return convert_barcode_from_issn13_to_issn8(upc);
def convert_barcode_from_issn8_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_issn8_to_issn13(upc));
def convert_barcode_from_itf14_to_issn8(upc):
 upc = str(upc);
 return convert_barcode_from_itf14_to_ean13(convert_barcode_from_issn13_to_issn8(upc));
def print_issn8_barcode(upc):
 upc = str(upc);
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc);
  upc = fix_matches[1];
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not re.findall("^(\d{4})(\d{4})", upc)):
  return False;
 issn_matches = re.findall("^(\d{4})(\d{4})", upc);
 issn_matches = issn_matches[0];
 issn8 = issn_matches[0]+"-"+issn_matches[1];
 return issn8;
def print_issn13_barcode(upc):
 upc = str(upc);
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc);
  upc = fix_matches[1];
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not re.findall("^(\d{3})(\d{4})(\d{4})(\d{2})", upc)):
  return False;
 issn_matches = re.findall("^(\d{3})(\d{4})(\d{4})(\d{2})", upc);
 issn_matches = issn_matches[0];
 issn13 = issn_matches[0]+"-"+issn_matches[1]+"-"+issn_matches[2]+"-"+issn_matches[3];
 return issn13;
def print_convert_barcode_from_issn8_to_issn13(upc):
 upc = str(upc);
 issn13 = print_issn13_barcode(convert_barcode_from_issn8_to_issn13(upc));
 return issn13;
def print_convert_barcode_from_issn13_to_issn8(upc):
 upc = str(upc);
 issn8 = print_issn8_barcode(convert_barcode_from_issn13_to_issn8(upc));
 return issn8;

'''
// ISBN (International Standard Book Number)
// Source: http://en.wikipedia.org/wiki/ISBN
'''
def convert_barcode_from_isbn10_to_isbn13(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(not upcean.validate.validate_isbn10_checksum(upc)):
  return False;
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc);
  upc = fix_matches[0];
  isbn13 = "978"+upc+str(upcean.validate.validate_ean13_checksum("978"+upc,True));
 return isbn13;
def convert_barcode_from_isbn13_to_isbn10(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(not re.findall("^978(\d{9})", upc)):
  return False;
 if(re.findall("^978(\d{9})", upc)):
  upc_matches = re.findall("^978(\d{9})", upc);
  isbn10 = upc_matches[0]+str(upcean.validate.validate_isbn10_checksum(upc_matches[0],True));
 return isbn10;
def convert_barcode_from_isbn10_to_ean13(upc):
 upc = str(upc);
 return convert_barcode_from_isbn10_to_isbn13(upc);
def convert_barcode_from_ean13_to_isbn10(upc):
 upc = str(upc);
 return convert_barcode_from_isbn13_to_isbn10(upc);
def convert_barcode_from_isbn10_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_isbn10_to_isbn13(upc));
def convert_barcode_from_itf14_to_isbn10(upc):
 upc = str(upc);
 return convert_barcode_from_itf14_to_ean13(convert_barcode_from_isbn13_to_isbn10(upc));
def print_isbn10_barcode(upc):
 upc = str(upc);
 if(len(upc)>10):
  fix_matches = re.findall("^(\d{9})(\d{1}|X{1})", upc);
  fix_matches = fix_matches[0]
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>10 or len(upc)<10):
  return False;
 if(not re.findall("^(\d{1})(\d{3})(\d{5})(\d{1}|X{1})", upc)):
  return False;
 isbn_matches = re.findall("^(\d{1})(\d{3})(\d{5})(\d{1}|X{1})", upc);
 isbn_matches = isbn_matches[0];
 isbn10 = isbn_matches[0]+"-"+isbn_matches[1]+"-"+isbn_matches[2]+"-"+isbn_matches[3];
 return isbn10;
def print_isbn13_barcode(upc):
 upc = str(upc);
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc);
  upc = fix_matches[1];
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not re.findall("^(\d{3})(\d{1})(\d{3})(\d{5})(\d{1})", upc)):
  return False;
 isbn_matches = re.findall("^(\d{3})(\d{1})(\d{3})(\d{5})(\d{1})", upc);
 isbn_matches = isbn_matches[0];
 isbn13 = isbn_matches[0]+"-"+isbn_matches[1]+"-"+isbn_matches[2]+"-"+isbn_matches[3]+"-"+isbn_matches[4];
 return isbn13;
def print_convert_barcode_from_isbn10_to_isbn13(upc):
 upc = str(upc);
 isbn13 = print_isbn13_barcode(convert_barcode_from_isbn10_to_isbn13(upc));
 return isbn13;
def print_convert_barcode_from_isbn13_to_isbn10(upc):
 upc = str(upc);
 isbn10 = print_isbn10_barcode(convert_barcode_from_isbn13_to_isbn10(upc));
 return isbn10;

'''
// ISMN (International Standard Music Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Music_Number
// Source: http://www.ismn-international.org/whatis.html
// Source: http://www.ismn-international.org/manual_1998/chapter2.html
'''
def convert_barcode_from_ismn10_to_ismn13(upc):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(not upcean.validate.validate_ismn10_checksum(upc)):
  return False;
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc);
  upc = fix_matches[0];
 ismn13 = "9790"+upc+str(upcean.validate.validate_ean13_checksum("9790"+upc,True));
 return ismn13;
def convert_barcode_from_ismn13_to_ismn10(upc):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(not re.findall("^9790(\d{8})", upc)):
  return False;
 if(re.findall("^9790(\d{8})", upc)):
  upc_matches = re.findall("^9790(\d{8})", upc);
  ismn10 = upc_matches[0]+str(upcean.validate.validate_ismn10_checksum(upc_matches[0],True));
 return ismn10;
def convert_barcode_from_ismn10_to_ean13(upc):
 upc = str(upc);
 return convert_barcode_from_ismn10_to_ismn13(upc);
def convert_barcode_from_ean13_to_ismn10(upc):
 upc = str(upc);
 return convert_barcode_from_ismn13_to_ismn10(upc);
def convert_barcode_from_ismn10_to_itf14(upc):
 upc = str(upc);
 return convert_barcode_from_ean13_to_itf14(convert_barcode_from_ismn10_to_ismn13(upc));
def convert_barcode_from_itf14_to_ismn10(upc):
 upc = str(upc);
 return convert_barcode_from_itf14_to_ean13(convert_barcode_from_ismn13_to_ismn10(upc));
def print_ismn10_barcode(upc):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc);
  upc = fix_matches[0];
 if(len(upc)>9 or len(upc)<9):
  return False;
 if(not re.findall("^(\d{4})(\d{4})(\d{1})", upc)):
  return False;
 ismn_matches = re.findall("^(\d{4})(\d{4})(\d{1})", upc);
 ismn_matches = ismn_matches[0];
 ismn10 = "M-"+ismn_matches[0]+"-"+ismn_matches[1]+"-"+ismn_matches[2];
 return ismn10;
def print_ismn13_barcode(upc):
 upc = str(upc);
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc);
  upc = fix_matches[0];
 if(len(upc)>13 or len(upc)<13):
  return False;
 if(not re.findall("^(\d{3})(\d{1})(\d{4})(\d{4})(\d{1})", upc)):
  return False;
 ismn_matches = re.findall("^(\d{3})(\d{1})(\d{4})(\d{4})(\d{1})", upc);
 ismn_matches = ismn_matches[0];
 ismn13 = ismn_matches[0]+"-"+ismn_matches[1]+"-"+ismn_matches[2]+"-"+ismn_matches[3]+"-"+ismn_matches[4];
 return ismn13;
def print_convert_barcode_from_ismn10_to_ismn13(upc):
 upc = str(upc);
 ismn13 = print_ismn13_barcode(convert_barcode_from_ismn10_to_ismn13(upc));
 return ismn13;
def print_convert_barcode_from_ismn13_to_ismn10(upc):
 upc = str(upc);
 ismn10 = print_ismn10_barcode(convert_barcode_from_ismn13_to_ismn10(upc));
 return ismn10;

'''
// Get variable weight price checksum for UPC-A
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
// Source: http://barcodes.gs1us.org/GS1%20US%20BarCodes%20and%20eCom%20-%20The%20Global%20Language%20of%20Business.htm
'''
def make_upca_vw_to_upca_barcode(code, price):
 code = str(code);
 price = str(price);
 if(len(code)>5):
  if(re.findall("^(\d{5})", code)):
   code_matches = re.findall("^(\d{5})", code);
   code = code_matches[0];
 if(len(price)>4):
  if(re.findall("^(\d{4})", price)):
   price_matches = re.findall("^(\d{4})", price);
   price = price_matches[0];
 pricecs = str(upcean.validate.get_vw_price_checksum(price));
 vwupc = "2"+code+pricecs+price.zfill(4);
 vwupc = vwupc+str(upcean.validate.validate_upca_checksum(vwupc, True));
 return vwupc;
def make_vw_to_upca_barcode(code, price):
 return make_upca_vw_to_upca_barcode(code, price);
def make_upca_vw_to_ean13_barcode(code, price):
 code = str(code);
 price = str(price);
 vwean13 = convert_barcode_from_upca_to_ean13(make_upca_vw_to_upca_barcode(code, price));
 return vwean13;
def make_vw_to_ean13_barcode(code, price):
 return make_upca_vw_to_ean13_barcode(code, price);
def make_upca_vw_to_itf14_barcode(code, price):
 code = str(code);
 price = str(price);
 vwitf14 = convert_barcode_from_upca_to_itf14(make_upca_vw_to_upca_barcode(code, price));
 return vwitf14;
def make_vw_to_itf14_barcode(code, price):
 return make_upca_vw_to_itf14_barcode(code, price);

'''
// Get variable weight price checksum for EAN-13
// Source: https://softmatic.com/barcode-ean-13.html#ean-country
'''
def make_ean13_vw_to_ean13_barcode(numbersystem, code, price):
 code = str(code);
 price = str(price);
 numbersystem = str(numbersystem);
 if(len(numbersystem)>1):
  if(re.findall("^(\d{1})", numbersystem)):
   ns_matches = re.findall("^(\d{1})", numbersystem);
   numbersystem = ns_matches[0];
 if(len(code)>5):
  if(re.findall("^(\d{5})", code)):
   code_matches = re.findall("^(\d{5})", code);
   code = code_matches[0];
 if(len(price)>5):
  if(re.findall("^(\d{5})", price)):
   price_matches = re.findall("^(\d{5})", price);
   price = price_matches[0];
 vwupc = "2"+numbersystem+code+price.zfill(5);
 vwupc = vwupc+str(upcean.validate.validate_ean13_checksum(vwupc, True));
 return vwupc;
def make_ean13_vw_to_itf14_barcode(numbersystem, code, price):
 code = str(code);
 price = str(price);
 vwitf14 = convert_barcode_from_upca_to_itf14(make_ean13_vw_to_upca_barcode(numbersystem, code, price));
 return vwitf14;

def make_goodwill_to_upca_barcode(code, price):
 code = str(code);
 price = str(price);
 if(len(code)>5):
  if(re.findall("^(\d{5})", code)):
   code_matches = re.findall("^(\d{5})", code);
   code = code_matches[0];
 if(len(price)>5):
  if(re.findall("^(\d{5})", price)):
   price_matches = re.findall("^(\d{5})", price);
   price = price_matches[0];
 vwupc = "4"+code+price.zfill(5);
 vwupc = vwupc+str(upcean.validate.validate_upca_checksum(vwupc, True));
 return vwupc;
def make_goodwill_to_ean13_barcode(code, price):
 code = str(code);
 price = str(price);
 vwean13 = convert_barcode_from_upca_to_ean13(make_goodwill_to_upca_barcode(code, price));
 return vwean13;
def make_goodwill_to_itf14_barcode(code, price):
 code = str(code);
 price = str(price);
 vwitf14 = convert_barcode_from_upca_to_itf14(make_goodwill_to_upca_barcode(code, price));
 return vwitf14;

def make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 family = str(family);
 value = str(value);
 if(int(numbersystem)!=5 and int(numbersystem)!=9):
  numbersystem = "5";
 if(len(manufacturer)>5):
  fix_matches = re.findall("^(\d{5})", manufacturer);
  upc = fix_matches[0];
 if(len(family)>3):
  fix_matches = re.findall("^(\d{3})", family);
  upc = fix_matches[0];
 if(len(value)>2):
  fix_matches = re.findall("^(\d{2})", value);
  upc = fix_matches[0];
 couponupca = numbersystem+manufacturer+family+value;
 couponupca = couponupca+str(upcean.validate.validate_upca_checksum(couponupca, True));
 return couponupca;
def make_coupon_to_ean13_barcode(numbersystem, manufacturer, family, value):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 family = str(family);
 value = str(value);
 couponean13 = convert_barcode_from_upca_to_ean13(make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value));
 return couponean13;
def make_coupon_to_itf14_barcode(numbersystem, manufacturer, family, value):
 numbersystem = str(numbersystem);
 manufacturer = str(manufacturer);
 family = str(family);
 value = str(value);
 couponitf14 = convert_barcode_from_upca_to_itf14(make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value));
 return couponitf14;

'''
// NDC (National Drug Codes)
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''
def make_ndc_to_upca_barcode(labeler, product, package):
 labeler = str(labeler);
 product = str(product);
 package = str(package);
 if(len(labeler)>4):
  if(re.findall("^(\d{4})", labeler)):
   labeler_matches = re.findall("^(\d{4})", labeler);
   labeler = labeler_matches[0];
 if(len(product)>4):
  if(re.findall("^(\d{4})", product)):
   product_matches = re.findall("^(\d{4})", product);
   product = product_matches[0];
 if(len(package)>2):
  if(re.findall("^(\d{2})", package)):
   package_matches = re.findall("^(\d{2})", package);
   package = package_matches[0];
 ndcupc = "3"+labeler+product+package;
 ndcupc = ndcupc+str(upcean.validate.validate_upca_checksum(ndcupc, True));
 return ndcupc;
def make_ndc_to_ean13_barcode(labeler, product, package):
 labeler = str(labeler);
 product = str(product);
 package = str(package);
 ndcean13 = convert_barcode_from_upca_to_ean13(make_ndc_to_upca_barcode(labeler, product, package));
 return ndcean13;
def make_ndc_to_itf14_barcode(labeler, product, package):
 labeler = str(labeler);
 product = str(product);
 package = str(package);
 ndcitf14 = convert_barcode_from_upca_to_itf14(make_ndc_to_upca_barcode(labeler, product, package));
 return ndcitf14;

def convert_barcode_from_ndc_to_upca(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 if(len(upc)>10):
  fix_matches = re.findall("^(\d{10})", upc);
  upc = fix_matches[0];
 ndcupca = "3"+upc+str(upcean.validate.validate_upca_checksum("3"+upc,True));
 return ndcupca;
def convert_barcode_from_upca_to_ndc(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 if(not upcean.validate.validate_upca_checksum(upc)):
  return False;
 if(not re.findall("^3(\d{10})", upc)):
  return False;
 if(re.findall("^3(\d{10})", upc)):
  upc_matches = re.findall("^3(\d{10})", upc);
  ndc = upc_matches[0];
 return ndc;
def convert_barcode_from_ndc_to_ean13(upc):
 upc = str(upc);
 ndcean13 = convert_barcode_from_upca_to_ean13(convert_barcode_from_ndc_to_upca(upc));
 return ndcean13;
def convert_barcode_from_ndc_to_itf14(upc):
 upc = str(upc);
 ndcitf14 = convert_barcode_from_upca_to_itf14(convert_barcode_from_ndc_to_upca(upc));
 return ndcitf14;
def print_ndc_barcode(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 if(len(upc)>10):
  fix_matches = re.findall("^(\d{10})", upc);
  upc = fix_matches[0];
 if(len(upc)>10 or len(upc)<10):
  return False;
 if(not re.findall("^(\d{4})(\d{4})(\d{2})", upc)):
  return False;
 ndc_matches = re.findall("^(\d{4})(\d{4})(\d{2})", upc);
 ndc_matches = ndc_matches[0];
 ndc = ndc_matches[0]+"-"+ndc_matches[1]+"-"+ndc_matches[2];
 return ndc;
def print_convert_barcode_from_upca_to_ndc(upc):
 upc = str(upc);
 ndc = print_ndc_barcode(convert_barcode_from_upca_to_ndc(upc));
 return ndc;
