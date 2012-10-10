#!/usr/bin/python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2012 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2012 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2012 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: validate.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

import sys, re;

def validate_upca(upc,return_check=False): 
 if(len(upc)>12):
  fix_matches = re.findall("^(\d{12})", upc);
  upc = fix_matches[0];
 if(len(upc)>12 or len(upc)<11):
  return False;
 if(len(upc)==11):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==12):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches=upc_matches[0];
 OddSum = eval(upc_matches[0]+"+"+upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]+"+"+upc_matches[8]+"+"+upc_matches[10]) * 3;
 EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]+"+"+upc_matches[7]+"+"+upc_matches[9]);
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(return_check==False and len(upc)==12):
  if(CheckSum!=int(upc_matches[11])):
   return False;
  if(CheckSum==int(upc_matches[11])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==11):
  return CheckSum;
def fix_upca_checksum(upc):
 if(len(upc)>11):
  fix_matches = re.findall("^(\d{11})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_upca(upc,True));

def validate_ean13(upc,return_check=False):
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc);
  upc = fix_matches[0];
 if(len(upc)>13 or len(upc)<12):
  return False;
 if(len(upc)==12):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==13):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches=upc_matches[0];
 EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]+"+"+upc_matches[7]+"+"+upc_matches[9]+"+"+upc_matches[11]) * 3;
 OddSum = eval(upc_matches[0]+"+"+upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]+"+"+upc_matches[8]+"+"+upc_matches[10]);
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(return_check==False and len(upc)==13):
  if(CheckSum!=int(upc_matches[12])):
   return False;
  if(CheckSum==int(upc_matches[12])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==12):
  return CheckSum;
def fix_ean13_checksum(upc):
 if(len(upc)>12):
  fix_matches = re.findall("^(\d{12})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_ean13(upc,True));

def validate_itf14(upc,return_check=False):
 if(len(upc)>14):
  fix_matches = re.findall("^(\d{14})", upc); 
  upc = fix_matches[0];
 if(len(upc)>14 or len(upc)<13):
  return False;
 if(len(upc)==13):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==14):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches=upc_matches[0];
 EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]+"+"+upc_matches[7]+"+"+upc_matches[9]+"+"+upc_matches[11]);
 OddSum = eval(upc_matches[0]+"+"+upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]+"+"+upc_matches[8]+"+"+upc_matches[10]+"+"+upc_matches[12]) * 3;
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(return_check==False and len(upc)==14):
  if(CheckSum!=int(upc_matches[13])):
   return False;
  if(CheckSum==int(upc_matches[13])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==13):
  return CheckSum;
def fix_itf14_checksum(upc):
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_itf14(upc,True));

def validate_ean8(upc,return_check=False):
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc); 
  upc = fix_matches[0];
 if(len(upc)>8 or len(upc)<7):
  return False;
 if(len(upc)==7):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==8):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches=upc_matches[0];
 EvenSum = eval(upc_matches[0]+"+"+upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
 OddSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(return_check==False and len(upc)==8):
  if(CheckSum!=int(upc_matches[7])):
   return False;
  if(CheckSum==int(upc_matches[7])): 
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==7):
  return CheckSum;
def fix_ean8_checksum(upc):
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_ean8(upc,True));

def validate_upce(upc,return_check=False):
 if(len(upc)>8):
  fix_matches = re.findall("/^(\d{8})/", upc); 
  upc = fix_matches[0];
 if(len(upc)>8 or len(upc)<7):
  return False;
 if(not re.findall("^0", upc)):
  return False;
 CheckDigit = None;
 if(len(upc)==8 and re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc)):
  upc_matches = re.findall("^(\d{7})(\d{1})", upc);
  upc_matches=upc_matches[0];
  CheckDigit = upc_matches[1];
 if(re.findall("^(\d{1})(\d{5})([0-3])", upc)):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches=upc_matches[0];
  if(int(upc_matches[6])==0):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[3]+"+"+upc_matches[5]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[4]);
  if(int(upc_matches[6])==1):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[3]+"+"+upc_matches[5]) * 3;
   EvenSum = eval(upc_matches[1]+"+1+"+upc_matches[4]);
  if(int(upc_matches[6])==2):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[3]+"+"+upc_matches[5]) * 3;
   EvenSum = eval(upc_matches[1]+"+2+"+upc_matches[4]);
  if(int(upc_matches[6])==3):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
 if(re.findall("^(\d{1})(\d{5})([4-9])", upc)):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches=upc_matches[0];
  if(int(upc_matches[6])==4):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[5]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]);
  if(int(upc_matches[6])==5):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
  if(int(upc_matches[6])==6):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
  if(int(upc_matches[6])==7):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
  if(int(upc_matches[6])==8):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
  if(int(upc_matches[6])==9):
   OddSum = eval(upc_matches[2]+"+"+upc_matches[4]+"+"+upc_matches[6]) * 3;
   EvenSum = eval(upc_matches[1]+"+"+upc_matches[3]+"+"+upc_matches[5]);
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(return_check==False and len(upc)==8):
  if(CheckSum!=int(CheckDigit)):
   return False;
  if(CheckSum==int(CheckDigit)):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==7):
  return CheckSum;
def fix_upce_checksum(upc):
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_upce(upc,True));

'''
ISSN (International Standard Serial Number)
http://en.wikipedia.org/wiki/International_Standard_Serial_Number
'''
def validate_issn8(upc,return_check=False):
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc); 
  upc = fix_matches[0].fix_matches[1];
 if(len(upc)>8 or len(upc)<7):
  return False;
 if(len(upc)==7):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==8):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches = upc_matches[0];
 AllSum = eval(upc_matches[0]+"*8") + eval(upc_matches[1]+"*7") + eval(upc_matches[2]+"*6") + eval(upc_matches[3]+"*5") + eval(upc_matches[4]+"*4") + eval(upc_matches[5]+"*3") + eval(upc_matches[6]+"*2");
 CheckSum = AllSum % 11;
 if(CheckSum>0):
  CheckSum = 11 - CheckSum;
 if(return_check==False and len(upc)==8):
  if(CheckSum!=int(upc_matches[7])):
   return False;
  if(CheckSum==int(upc_matches[7])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==7):
  return CheckSum;
def fix_issn8_checksum(upc):
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(validate_issn8(upc,True));
def validate_issn13(upc,return_check=False):
 if(not re.findall("^977(\d{9})", upc)):
  return False;
 if(re.findall("^977(\d{9})", upc)):
  return validate_ean13(upc,return_check);
def fix_issn13_checksum(upc):
 if(not re.findall("^977(\d{9})", upc)):
  return False;
 if(re.findall("^977(\d{9})", upc)):
  return fix_ean13_checksum(upc);

'''
ISBN (International Standard Book Number)
http://en.wikipedia.org/wiki/ISBN
'''
def validate_isbn10(upc,return_check=False):
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>10):
  fix_matches = re.findall("^(\d{9})(\d{1}|X{1})", upc); 
  upc = fix_matches[0].fix_matches[1];
 if(len(upc)>10 or len(upc)<9):
  return False;
 if(len(upc)==9):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==10):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1}|X{1})", upc);
 upc_matches = upc_matches[0];
 AllSum = eval(upc_matches[0]+"*10") + eval(upc_matches[1]+"*9") + eval(upc_matches[2]+"*8") + eval(upc_matches[3]+"*7") + eval(upc_matches[4]+"*6") + eval(upc_matches[5]+"*5") + eval(upc_matches[6]+"*4") + eval(upc_matches[7]+"*3") + eval(upc_matches[8]+"*2");
 CheckSum = 0;
 while((AllSum + (CheckSum * 1)) % 11):
  CheckSum += 1;
 if(CheckSum==10):
  CheckSum = "X";
 if(return_check==False and len(upc)==10):
  if(str(CheckSum)!=upc_matches[9]):
   return False;
  if(str(CheckSum)==upc_matches[9]):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==9):
  return CheckSum;
def fix_isbn10_checksum(upc):
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc);
  upc = fix_matches[1];
 return upc+str(validate_isbn10(upc,True));
def validate_isbn13(upc,return_check=False):
 if(not re.findall("^978(\d{9})", upc)):
  return False;
 if(re.findall("^978(\d{9})", upc)):
  return validate_ean13(upc,return_check);
def fix_isbn13_checksum(upc):
 if(not re.findall("^978(\d{9})", upc)):
  return False;
 if(re.findall("^978(\d{9})", upc)):
  return fix_ean13_checksum(upc);

'''
ISMN (International Standard Music Number)
http://en.wikipedia.org/wiki/International_Standard_Music_Number
http://www.ismn-international.org/whatis.html
http://www.ismn-international.org/manual_1998/chapter2.html
'''
def validate_ismn10(upc,return_check=False):
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{8})(\d{1})", upc); 
  upc = fix_matches[0].fix_matches[1];
 if(len(upc)>9 or len(upc)<8):
  return False;
 if(len(upc)==8):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==9):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches = upc_matches[0];
 AllSum = (3 * 3) + eval(upc_matches[0]+"*1") + eval(upc_matches[1]+"*3") + eval(upc_matches[2]+"*1") + eval(upc_matches[3]+"*3") + eval(upc_matches[4]+"*1") + eval(upc_matches[5]+"*3") + eval(upc_matches[6]+"*1") + eval(upc_matches[7]+"*3");
 CheckSum = 1;
 while((AllSum + (CheckSum * 1)) % 10):
  CheckSum += 1;
 if(return_check==False and len(upc)==9):
  if(CheckSum!=int(upc_matches[8])):
   return False;
  if(CheckSum==int(upc_matches[8])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(upc)==8):
  return CheckSum;
def fix_ismn10_checksum(upc):
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc); 
  upc = fix_matches[1];
 return upc+str(validate_ismn10(upc,True));
def validate_ismn13(upc,return_check=False):
 if(not re.findall("^9790(\d{8})", upc)):
  return False;
 if(re.findall("^9790(\d{8})", upc)):
  return validate_ean13(upc,return_check);
def fix_ismn13_checksum(upc):
 if(not re.findall("^9790(\d{8})", upc)):
  return False;
 if(re.findall("^9790(\d{8})", upc)):
  return fix_ean13_checksum(upc);

'''
// Get variable weight price checksum
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
// Source: http://barcodes.gs1us.org/GS1%20US%20BarCodes%20and%20eCom%20-%20The%20Global%20Language%20of%20Business.htm
'''
def get_vw_price_checksum(price,return_check=False):
 if(len(price)==1):
  price = "000".price;
 if(len(price)==2):
  price = "00".price;
 if(len(price)==3):
  price = "0".price;
 if(len(price)>5):
  if(re.findall("^(\d{5})", price)):
   price_matches = re.findall("^(\d{5})", price);
   price = price_matches[0];
 price_split = list(price);
 numrep1 = [0, 2, 4, 6, 8, 9, 1, 3, 5, 7];
 numrep2 = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7];
 numrep3 = [0, 5, 9, 4, 8, 3, 7, 2, 6, 1];
 if(len(price)==4):
  price_split[0] = numrep1[int(price_split[0])];
  price_split[1] = numrep1[int(price_split[1])];
  price_split[2] = numrep2[int(price_split[2])];
  price_split[3] = numrep3[int(price_split[3])];
  price_add = (price_split[0] + price_split[1] + price_split[2] + price_split[3]) * 3;
 if(len(price)==5):
  price_split[1] = numrep1[int(price_split[1])];
  price_split[2] = numrep1[int(price_split[2])];
  price_split[3] = numrep2[int(price_split[3])];
  price_split[4] = numrep3[int(price_split[4])]; 
  price_add = (price_split[1] + price_split[2] + price_split[3] + price_split[4]) * 3;
 CheckSum = price_add % 10;
 if(return_check==False and len(price)==5):
  if(CheckSum!=int(price_split[0])):
   return False;
  if(CheckSum==int(price_split[0])):
   return True;
 if(return_check==True):
  return CheckSum;
 if(len(price)==4):
  return CheckSum;
 return CheckSum;
def fix_vw_price_checksum(price):
 if(len(price)==5):
  fix_matches = re.findall("^(\d{1})(\d{4})", price); 
  fix_matches = fix_matches[0];
  price = fix_matches[1];
 if(len(price)>4):
  fix_matches = re.findall("^(\d{4})", price); 
  price = fix_matches[0];
 return str(get_vw_price_checksum(price,True))+price;
