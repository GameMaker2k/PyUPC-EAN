'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: validate.py - Last Update: 12/3/2019 Ver. 2.7.19 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re;

'''
// Digital Root
// Source: http://en.wikipedia.org/wiki/Digital_root
'''
def get_digital_root(number):
 number = str(number);
 while(len(str(number))>1):
  subnum = list(str(number));
  PreCount = 0;
  number = 0;
  while (PreCount<=len(subnum)-1):
   number += int(subnum[PreCount]);
   PreCount += 1;
 return int(number);

'''
// Luhn Algorithm ( Luhn Formula )
// http://en.wikipedia.org/wiki/Luhn_algorithm#Implementation_of_standard_Mod_10
'''
def validate_luhn_checksum(upc, upclen, return_check=False):
 upc = str(upc);
 upclen = int(upclen);
 upclendwn = upclen - 1;
 if(len(upc)>upclen):
  fix_matches = re.findall("^(\d{"+str(upclen)+"})", upc);
  upc = fix_matches[0];
 if(len(upc)>upclen or len(upc)<upclendwn):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_count1 = 0;
 upc_len1 = len(upc_matches1);
 if(len(upc)==upclen and upclen%2==1):
  upc_len1 = len(upc_matches1) - 1;
 OddSum = 0;
 while(upc_count1<upc_len1):
  OddSum = OddSum + upc_matches1[upc_count1];
  upc_count1 = upc_count1 + 1;
 upc_matches2 = upc_matches[1:][::2];
 upc_count2 = 0;
 upc_len2 = len(upc_matches2);
 if(len(upc)==upclen and upclen%2==0):
  upc_len2 = len(upc_matches2) - 1;
 EvenSum = 0;
 while(upc_count2<upc_len2):
  EvenSum = EvenSum + get_digital_root(upc_matches2[upc_count2] * 2);
  upc_count2 = upc_count2 + 1;
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==upclen):
  if(CheckSum!=upc_matches[-1]):
   return False;
  if(CheckSum==upc_matches[-1]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==upclendwn):
  return str(CheckSum);
def get_luhn_checksum(upc, upclen):
 upc = str(upc);
 upclen = int(upclen);
 upclendwn = upclen - 1;
 return validate_luhn_checksum(upc,upclen,True);
def fix_luhn_checksum(upc, upclen):
 upc = str(upc);
 upclen = int(upclen);
 upclendwn = upclen - 1;
 if(len(upc)>upclendwn):
  fix_matches = re.findall("^(\d{"+str(upclendwn)+"})", upc); 
  upc = fix_matches[0];
 return upc+str(get_luhn_checksum(upc,upclen));

def validate_upca_checksum(upc, return_check=False): 
 upc = str(upc);
 if(len(upc)>12):
  fix_matches = re.findall("^(\d{12})", upc);
  upc = fix_matches[0];
 if(len(upc)>12 or len(upc)<11):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 OddSum = (upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3] + upc_matches1[4] + upc_matches1[5]) * 3;
 EvenSum = upc_matches2[0] + upc_matches2[1] + upc_matches2[2] + upc_matches2[3] + upc_matches2[4];
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==12):
  if(CheckSum!=upc_matches2[5]):
   return False;
  if(CheckSum==upc_matches2[5]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==11):
  return str(CheckSum);
def get_upca_checksum(upc):
 upc = str(upc);
 return validate_upca_checksum(upc,True);
def fix_upca_checksum(upc):
 upc = str(upc);
 if(len(upc)>11):
  fix_matches = re.findall("^(\d{11})", upc); 
  upc = fix_matches[0];
 return upc+str(get_upca_checksum(upc));

def validate_ean13_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc);
  upc = fix_matches[0];
 if(len(upc)>13 or len(upc)<12):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 EvenSum = (upc_matches2[0] + upc_matches2[1] + upc_matches2[2] + upc_matches2[3] + upc_matches2[4] + upc_matches2[5]) * 3;
 OddSum = upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3] + upc_matches1[4] + upc_matches1[5];
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==13):
  if(CheckSum!=upc_matches1[6]):
   return False;
  if(CheckSum==upc_matches1[6]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==12):
  return str(CheckSum);
def get_ean13_checksum(upc):
 upc = str(upc);
 return validate_ean13_checksum(upc,True);
def fix_ean13_checksum(upc):
 upc = str(upc);
 if(len(upc)>12):
  fix_matches = re.findall("^(\d{12})", upc); 
  upc = fix_matches[0];
 return upc+str(get_ean13_checksum(upc));

def validate_itf14_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>14):
  fix_matches = re.findall("^(\d{14})", upc); 
  upc = fix_matches[0];
 if(len(upc)>14 or len(upc)<13):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 EvenSum = upc_matches2[0] + upc_matches2[1] + upc_matches2[2] + upc_matches2[3] + upc_matches2[4] + upc_matches2[5];
 OddSum = (upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3] + upc_matches1[4] + upc_matches1[5] + upc_matches1[6]) * 3;
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==14):
  if(CheckSum!=upc_matches2[6]):
   return False;
  if(CheckSum==upc_matches2[6]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==13):
  return str(CheckSum);
def get_itf14_checksum(upc):
 upc = str(upc);
 return validate_itf14_checksum(upc,True);
def fix_itf14_checksum(upc):
 upc = str(upc);
 if(len(upc)>13):
  fix_matches = re.findall("^(\d{13})", upc); 
  upc = fix_matches[0];
 return upc+str(get_itf14_checksum(upc));

def validate_ean8_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc); 
  upc = fix_matches[0];
 if(len(upc)>8 or len(upc)<7):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 EvenSum = (upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3]) * 3;
 OddSum = upc_matches2[0] + upc_matches2[1] + upc_matches2[2];
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==8):
  if(CheckSum!=upc_matches2[3]):
   return False;
  if(CheckSum==upc_matches2[3]): 
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==7):
  return str(CheckSum);
def get_ean8_checksum(upc):
 upc = str(upc);
 return validate_ean8_checksum(upc,True);
def fix_ean8_checksum(upc):
 upc = str(upc);
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(get_ean8_checksum(upc));

def validate_upce_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>8):
  fix_matches = re.findall("/^(\d{8})/", upc); 
  upc = fix_matches[0];
 if(len(upc)>8 or len(upc)<7):
  return False;
 if(not re.findall("^(0|1)", upc)):
  return False;
 CheckDigit = None;
 if(len(upc)==8 and re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc)):
  upc_matches = re.findall("^(\d{7})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upc_matches = [int(x) for x in upc_matches];
  CheckDigit = upc_matches[1];
 if(re.findall("^(\d{1})(\d{5})([0-3])", upc)):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upc_matches = [int(x) for x in upc_matches];
  if(int(upc_matches[6])==0):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[3] + upc_matches[5]) * 3;
   EvenSum = upc_matches[1] + upc_matches[4];
  if(int(upc_matches[6])==1):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[3] + upc_matches[5]) * 3;
   EvenSum = upc_matches[1] + 1 + upc_matches[4];
  if(int(upc_matches[6])==2):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[3] + upc_matches[5]) * 3;
   EvenSum = upc_matches[1] + 2 + upc_matches[4];
  if(int(upc_matches[6])==3):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[5]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[4];
 if(re.findall("^(\d{1})(\d{5})([4-9])", upc)):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upc_matches = [int(x) for x in upc_matches];
  if(int(upc_matches[6])==4):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[5]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3];
  if(int(upc_matches[6])==5):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[6]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[5];
  if(int(upc_matches[6])==6):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[6]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[5];
  if(int(upc_matches[6])==7):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[6]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[5];
  if(int(upc_matches[6])==8):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[6]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[5];
  if(int(upc_matches[6])==9):
   OddSum = (upc_matches[0] + upc_matches[2] + upc_matches[4] + upc_matches[6]) * 3;
   EvenSum = upc_matches[1] + upc_matches[3] + upc_matches[5];
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==8):
  if(CheckSum!=CheckDigit):
   return False;
  if(CheckSum==CheckDigit):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==7):
  return str(CheckSum);
def get_upce_checksum(upc):
 upc = str(upc);
 return validate_upce_checksum(upc,True);
def fix_upce_checksum(upc):
 upc = str(upc);
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(get_upce_checksum(upc));

def validate_ean2_checksum(upc, return_check=False): 
 upc = str(upc);
 if(len(upc)>3):
  fix_matches = re.findall("^(\d{3})", upc);
  upc = fix_matches[0];
 if(len(upc)>3 or len(upc)<2):
  return False;
 if(len(upc)==2):
  upc_matches = re.findall("^(\d{2})", upc);
  upc_matches = [int(x) for x in upc_matches];
 if(len(upc)==3):
  upc_matches = re.findall("^(\d{2})(\d{1})", upc);
  upc_matches = upc_matches[0];
  upc_matches = [int(x) for x in upc_matches];
 if(len(upc_matches)<=0): 
  return False;
 CheckSum = upc_matches[0] % 4;
 if(not return_check and len(upc)==3):
  if(CheckSum!=upc_matches[1]):
   return False;
  if(CheckSum==upc_matches[1]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==2):
  return str(CheckSum);
def get_ean2_checksum(upc):
 upc = str(upc);
 return validate_ean2_checksum(upc,True);
def fix_ean2_checksum(upc):
 upc = str(upc);
 if(len(upc)>2):
  fix_matches = re.findall("^(\d{2})", upc); 
  upc = fix_matches[0];
 return upc+str(get_ean2_checksum(upc));

def validate_ean5_checksum(upc, return_check=False): 
 upc = str(upc);
 if(len(upc)>6):
  fix_matches = re.findall("^(\d{6})", upc);
  upc = fix_matches[0];
 if(len(upc)>6 or len(upc)<5):
  return False;
 if(len(upc)==5):
  upc_matches = re.findall("^(\d{5})", upc);
 if(len(upc)==6):
  upc_matches = re.findall("^(\d{5})(\d{1})", upc);
  upc_matches = upc_matches[0];
 if(len(upc_matches)<=0): 
  return False;
 LeftDigit = list(upc_matches[0]);
 LeftDigit = [int(x) for x in LeftDigit];
 CheckSum = (LeftDigit[0] * 3) + (LeftDigit[1] * 9) + (LeftDigit[2] * 3) + (LeftDigit[3] * 9) + (LeftDigit[4] * 3);
 CheckSum = CheckSum % 10;
 upc_matches = [int(x) for x in upc_matches];
 if(not return_check and len(upc)==6):
  if(CheckSum!=upc_matches[1]):
   return False;
  if(CheckSum==upc_matches[1]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==5):
  return str(CheckSum);
def get_ean5_checksum(upc):
 upc = str(upc);
 return validate_ean5_checksum(upc,True);
def fix_ean5_checksum(upc):
 upc = str(upc);
 if(len(upc)>5):
  fix_matches = re.findall("^(\d{5})", upc); 
  upc = fix_matches[0];
 return upc+str(get_ean5_checksum(upc));

'''
// Get USPS Checkdigit by MACY8167
// Source: http://www.mrexcel.com/forum/excel-questions/530675-usps-mod-10-check-digit.html
'''
def validate_usps_checksum(upc, return_check=False): 
 upc = str(upc);
 if(len(upc)>22):
  fix_matches = re.findall("^(\d{22})", upc);
  upc = fix_matches[0];
 if(len(upc)>22 or len(upc)<21):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 OddSum = (upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3] + upc_matches1[4] + upc_matches1[5] + upc_matches1[6] + upc_matches1[7] + upc_matches1[8] + upc_matches1[9] + upc_matches1[10]) * 3;
 EvenSum = upc_matches2[0] + upc_matches2[1] + upc_matches2[2] + upc_matches2[3] + upc_matches2[4] + upc_matches2[5] + upc_matches2[6] + upc_matches2[7] + upc_matches2[8] + upc_matches2[9];
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==22):
  if(CheckSum!=upc_matches2[10]):
   return False;
  if(CheckSum==upc_matches2[10]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==21):
  return str(CheckSum);
def get_usps_checksum(upc):
 upc = str(upc);
 return validate_usps_checksum(upc,True);
def fix_usps_checksum(upc):
 upc = str(upc);
 if(len(upc)>21):
  fix_matches = re.findall("^(\d{21})", upc); 
  upc = fix_matches[0];
 return upc+str(get_usps_checksum(upc));

'''
// Get UPS Checkdigit and Info by stebo0728 and HolidayBows
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit?msg=2961884#xx2961884xx
'''
def validate_ups_checksum(upc, return_check=False): 
 upc = str(upc).upper();
 if(not re.findall("^1Z", upc)):
  return False;
 if(re.findall("^1Z", upc)):
  fix_matches = re.findall("^1Z(\w*)", upc);
  upc = fix_matches[0];
 if(len(upc)>16):
  fix_matches = re.findall("^(\w{16})", upc);
  upc = fix_matches[0];
 if(len(upc)>16 or len(upc)<15):
  return False;
 if(len(upc)>16):
  fix_matches = re.findall("^(\w{16})", upc);
  upc = fix_matches[0];
 if(len(upc)>16 or len(upc)<15):
  return False;
 upc_matches = list(upc);
 upc_matches1 = upc_matches[0:][::2];
 upc_count1 = 0;
 OddSum = 0;
 while(upc_count1<8):
  if(upc_matches1[upc_count1].isdigit()):
   OddSum = OddSum + int(upc_matches1[upc_count1]);
  if(not upc_matches1[upc_count1].isdigit()):
   OddSum = OddSum + ((ord(upc_matches1[upc_count1]) - 63) % 10);
  upc_count1 = upc_count1 + 1;
 upc_matches2 = upc_matches[1:][::2];
 upc_count2 = 0;
 EvenSum = 0;
 while(upc_count2<7):
  if(upc_matches2[upc_count2].isdigit()):
   EvenSum = EvenSum + (int(upc_matches2[upc_count2]) * 2);
  if(not upc_matches2[upc_count2].isdigit()):
   EvenSum = EvenSum + (((ord(upc_matches2[upc_count2]) - 63) % 10) * 2);
  upc_count2 = upc_count2 + 1;
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 if(not return_check and len(upc)==16):
  if(CheckSum!=int(upc_matches2[7])):
   return False;
  if(CheckSum==int(upc_matches2[7])):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==15):
  return str(CheckSum);
def get_ups_checksum(upc):
 upc = str(upc);
 print(upc);
 return validate_ups_checksum(upc,True);
def fix_ups_checksum(upc):
 upc = str(upc);
 if(len(upc)>17):
  fix_matches = re.findall("^(\w{17})", upc); 
  upc = fix_matches[0];
 return upc+str(get_ups_checksum(upc));

'''
// Get FEDEX Checkdigit by jbf777-ga
// Source: http://answers.google.com/answers/threadview/id/207899.html
'''
def validate_fedex_checksum(upc, return_check=False): 
 upc = str(upc);
 if(len(upc)>12):
  fix_matches = re.findall("^(\d{12})", upc);
  upc = fix_matches[0];
 if(len(upc)>12 or len(upc)<11):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 OddSum = (upc_matches1[0] * 3) + (upc_matches1[1] * 7) + (upc_matches1[2] * 1) + (upc_matches1[3] * 3) + (upc_matches1[4] * 7) + (upc_matches1[5] * 1);
 EvenSum = (upc_matches2[0] * 1) + (upc_matches2[1] * 3) + (upc_matches2[2] * 7) + (upc_matches2[3] * 1) + (upc_matches2[4] * 3);
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 11;
 if(not return_check and len(upc)==12):
  if(CheckSum!=upc_matches2[5]):
   return False;
  if(CheckSum==upc_matches2[5]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==11):
  return str(CheckSum);
def get_fedex_checksum(upc):
 upc = str(upc);
 return validate_fedex_checksum(upc,True);
def fix_fedex_checksum(upc):
 upc = str(upc);
 if(len(upc)>11):
  fix_matches = re.findall("^(\d{11})", upc); 
  upc = fix_matches[0];
 return upc+str(get_fedex_checksum(upc));

'''
// IMEI (International Mobile Station Equipment Identity)
// Source: http://en.wikipedia.org/wiki/IMEI#Check_digit_computation
'''
def validate_imei_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>15):
  fix_matches = re.findall("^(\d{15})", upc);
  upc = fix_matches[0];
 if(len(upc)>15 or len(upc)<14):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 UPC_Sum = upc_matches1[0] + get_digital_root(upc_matches2[0] * 2) + upc_matches1[1] + get_digital_root(upc_matches2[1] * 2) + upc_matches1[2] + get_digital_root(upc_matches2[2] * 2) + upc_matches1[3] + get_digital_root(upc_matches2[3] * 2) + upc_matches1[4] + get_digital_root(upc_matches2[4] * 2) + upc_matches1[5] + get_digital_root(upc_matches2[5] * 2) + upc_matches1[6] + get_digital_root(upc_matches2[6] * 2);
 PreCheckSum = 0;
 while((UPC_Sum + PreCheckSum) % 10 != 0):
  PreCheckSum += 1;
 CheckSum = PreCheckSum;
 if(not return_check and len(upc)==15):
  if(CheckSum!=upc_matches1[7]):
   return False;
  if(CheckSum==upc_matches1[7]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==14):
  return str(CheckSum);
def get_imei_checksum(upc):
 upc = str(upc);
 return validate_imei_checksum(upc,True);
def fix_imei_checksum(upc):
 upc = str(upc);
 if(len(upc)>14):
  fix_matches = re.findall("^(\d{14})", upc); 
  upc = fix_matches[0];
 return upc+str(get_imei_checksum(upc));

'''
// Bank Card Numbers
// Source: http://tywkiwdbi.blogspot.com/2012/06/checksum-number-on-credit-card.html
// Source: http://en.wikipedia.org/wiki/Luhn_algorithm#Implementation_of_standard_Mod_10
'''
def validate_bcn_checksum(upc, return_check=False):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>16):
  fix_matches = re.findall("^(\d{16})", upc);
  upc = fix_matches[0];
 if(len(upc)>16 or len(upc)<15):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 upc_matches1 = upc_matches[0:][::2];
 upc_matches2 = upc_matches[1:][::2];
 UPC_Sum = upc_matches2[0] + get_digital_root(upc_matches1[0] * 2) + upc_matches2[1] + get_digital_root(upc_matches1[1] * 2) + upc_matches2[2] + get_digital_root(upc_matches1[2] * 2) + upc_matches2[3] + get_digital_root(upc_matches1[3] * 2) + upc_matches2[4] + get_digital_root(upc_matches1[4] * 2) + upc_matches2[5] + get_digital_root(upc_matches1[5] * 2) + upc_matches2[6] + get_digital_root(upc_matches1[6] * 2) + get_digital_root(upc_matches1[7] * 2);
 PreCheckSum = 0;
 while((UPC_Sum + PreCheckSum) % 10 != 0):
  PreCheckSum += 1;
 CheckSum = PreCheckSum;
 if(not return_check and len(upc)==16):
  if(CheckSum!=upc_matches2[7]):
   return False;
  if(CheckSum==upc_matches2[7]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==15):
  return str(CheckSum);
def get_bcn_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 return validate_bcn_checksum(upc,True);
def fix_bcn_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>15):
  fix_matches = re.findall("^(\d{15})", upc); 
  upc = fix_matches[0];
 return upc+str(get_bcn_checksum(upc));

'''
// Code 11
// Source: http://www.barcodeisland.com/code11.phtml
// Source: http://en.wikipedia.org/wiki/Code_11
'''
def get_code11_checksum(upc):
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9\-]+)", upc)):
  return False;
 upc = upc.upper();
 upc_matches = list(upc);
 if(len(upc_matches)<=0):
  return False;
 Code11Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "-"};
 Code11Values = dict(zip(Code11Array.values(),Code11Array));
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 upc_print = list(upc_matches);
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>10):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 CheckSum = str(Code11Array[UPC_Sum % 11]);
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>9):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 CheckSum = str(CheckSum)+str(Code11Array[UPC_Sum % 11]);
 return str(CheckSum);

'''
// Code 93
// Source: http://www.barcodeisland.com/code93.phtml
// Source: http://en.wikipedia.org/wiki/Code_93
'''
def get_code93_checksum(upc):
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 upc = upc.upper();
 upc_matches = list(upc);
 if(len(upc_matches)<=0):
  return False;
 Code93Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%", 43: "($)", 44: "(%)", 45: "(/)", 46: "(+)"};
 Code93Values = dict(zip(Code93Array.values(),Code93Array));
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 upc_print = list(upc_matches);
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>20):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 CheckSum = str(Code93Array[UPC_Sum % 47]);
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>15):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 CheckSum = str(CheckSum)+str(Code93Array[UPC_Sum % 47]);
 return str(CheckSum);

'''
// MSI (Modified Plessey)
// Source: http://www.barcodeisland.com/msi.phtml
// Source: http://en.wikipedia.org/wiki/MSI_Barcode
'''
def get_msi_checksum(upc):
 upc = str(upc);
 upc = upc.upper();
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 if(len(upc) % 2==0):
  upc_matches1 = "".join([str(i) for i in upc_matches[1:][::2]]);
  upc_matches1 = list(str(int(upc_matches1) * 2));
  upc_matches1 = [int(x) for x in upc_matches1];
  upc_matches2 = upc_matches[0:][::2];
 else:
  upc_matches1 = "".join([str(i) for i in upc_matches[0:][::2]]);
  upc_matches1 = list(str(int(upc_matches1) * 2));
  upc_matches1 = [int(x) for x in upc_matches1];
  upc_matches2 = upc_matches[1:][::2];
 PreCount = 0;
 UPC_Sum = 0;
 while (PreCount<=len(upc_matches1)-1):
  UPC_Sum = UPC_Sum + upc_matches1[PreCount];
  PreCount += 1;
 PreCount = 0;
 while (PreCount<=len(upc_matches2)-1):
  UPC_Sum = UPC_Sum + upc_matches2[PreCount];
  PreCount += 1;
 CheckSum = 10 - (UPC_Sum % 10);
 return str(CheckSum);

'''
// ISSN (International Standard Serial Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Serial_Number
'''
def validate_issn8_checksum(upc, return_check=False):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>8):
  fix_matches = re.findall("^(\d{8})", upc); 
  fix_matches = fix_matches[0];
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>8 or len(upc)<7):
  return False;
 if(len(upc)==7):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==8):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches = upc_matches[0];
 upc_matches = [int(x) for x in upc_matches];
 AllSum = (upc_matches[0] * 8) + (upc_matches[1] * 7) + (upc_matches[2] * 6) + (upc_matches[3] * 5) + (upc_matches[4] * 4) + (upc_matches[5] * 3) + (upc_matches[6] * 2);
 CheckSum = AllSum % 11;
 if(CheckSum>0):
  CheckSum = 11 - CheckSum;
 if(not return_check and len(upc)==8):
  if(CheckSum!=upc_matches[7]):
   return False;
  if(CheckSum==upc_matches[7]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==7):
  return str(CheckSum);
def get_issn8_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 return validate_issn8_checksum(upc,True);
def fix_issn8_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>7):
  fix_matches = re.findall("^(\d{7})", upc); 
  upc = fix_matches[0];
 return upc+str(get_issn8_checksum(upc));
def validate_issn13_checksum(upc, return_check=False):
 upc = str(upc);
 if(not re.findall("^977(\d{9})", upc)):
  return False;
 if(re.findall("^977(\d{9})", upc)):
  return validate_ean13_checksum(upc,return_check);
def get_issn13_checksum(upc):
 upc = str(upc);
 return validate_issn13_checksum(upc,True);
def fix_issn13_checksum(upc):
 upc = str(upc);
 if(not re.findall("^977(\d{9})", upc)):
  return False;
 if(re.findall("^977(\d{9})", upc)):
  return fix_ean13_checksum(upc);

'''
// ISBN (International Standard Book Number)
// Source: http://en.wikipedia.org/wiki/ISBN
'''
def validate_isbn10_checksum(upc, return_check=False):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>10):
  fix_matches = re.findall("^(\d{9})(\d{1}|X{1})", upc); 
  fix_matches = fix_matches[0];
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>10 or len(upc)<9):
  return False;
 if(len(upc)==9):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==10):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1}|X{1})", upc);
 upc_matches = upc_matches[0];
 upc_matches = [int(x) for x in upc_matches];
 AllSum = (upc_matches[0] * 10) + (upc_matches[1] * 9) + (upc_matches[2] * 8) + (upc_matches[3] * 7) + (upc_matches[4] * 6) + (upc_matches[5] * 5) + (upc_matches[6] * 4) + (upc_matches[7] * 3) + (upc_matches[8] * 2);
 CheckSum = 0;
 while((AllSum + (CheckSum * 1)) % 11):
  CheckSum += 1;
 if(CheckSum==10):
  CheckSum = "X";
 if(not return_check and len(upc)==10):
  if(str(CheckSum)!=upc_matches[9]):
   return False;
  if(str(CheckSum)==upc_matches[9]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==9):
  return str(CheckSum);
def get_isbn10_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 return validate_isbn10_checksum(upc,True);
def fix_isbn10_checksum(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc);
  upc = fix_matches[1];
 return upc+str(get_isbn10_checksum(upc));
def validate_isbn13_checksum(upc, return_check=False):
 upc = str(upc);
 if(not re.findall("^978(\d{9})", upc)):
  return False;
 if(re.findall("^978(\d{9})", upc)):
  return validate_ean13_checksum(upc,return_check);
def get_isbn13_checksum(upc):
 upc = str(upc);
 return validate_isbn13_checksum(upc,True);
def fix_isbn13_checksum(upc):
 upc = str(upc);
 if(not re.findall("^978(\d{9})", upc)):
  return False;
 if(re.findall("^978(\d{9})", upc)):
  return fix_ean13_checksum(upc);

'''
// ISMN (International Standard Music Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Music_Number
// Source: http://www.ismn-international.org/whatis.html
// Source: http://www.ismn-international.org/manual_1998/chapter2.html
'''
def validate_ismn10_checksum(upc, return_check=False):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{8})(\d{1})", upc); 
  fix_matches = fix_matches[0];
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>9 or len(upc)<8):
  return False;
 if(len(upc)==8):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 if(len(upc)==9):
  upc_matches = re.findall("^(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc);
 upc_matches = upc_matches[0];
 upc_matches = [int(x) for x in upc_matches];
 AllSum = (3 * 3) + (upc_matches[0] * 1) + (upc_matches[1] * 3) + (upc_matches[2] * 1) + (upc_matches[3] * 3) + (upc_matches[4] * 1) + (upc_matches[5] * 3) + (upc_matches[6] * 1) + (upc_matches[7] * 3);
 CheckSum = 1;
 while((AllSum + (CheckSum * 1)) % 10):
  CheckSum += 1;
 if(not return_check and len(upc)==9):
  if(CheckSum!=upc_matches[8]):
   return False;
  if(CheckSum==upc_matches[8]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==8):
  return str(CheckSum);
def get_ismn10_checksum(upc):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 return validate_ismn10_checksum(upc,True);
def fix_ismn10_checksum(upc):
 upc = str(upc);
 upc = upc.replace("M", "");
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>9):
  fix_matches = re.findall("^(\d{9})", upc); 
  upc = fix_matches[1];
 return upc+str(get_ismn10_checksum(upc));
def validate_ismn13_checksum(upc, return_check=False):
 upc = str(upc);
 if(not re.findall("^9790(\d{8})", upc)):
  return False;
 if(re.findall("^9790(\d{8})", upc)):
  return validate_ean13_checksum(upc,return_check);
def get_ismn13_checksum(upc):
 upc = str(upc);
 return validate_ismn13_checksum(upc,True);
def fix_ismn13_checksum(upc):
 upc = str(upc);
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
def validate_vw_price_checksum(price, return_check=False):
 price = str(price);
 if(len(price)==1):
  price = "000"+price;
 if(len(price)==2):
  price = "00"+price;
 if(len(price)==3):
  price = "0"+price;
 if(len(price)>5):
  if(re.findall("^(\d{5})", price)):
   price_matches = re.findall("^(\d{5})", price);
   price = price_matches[0];
 price_split = list(price);
 price_split = [int(x) for x in price_split];
 numrep1 = [0, 2, 4, 6, 8, 9, 1, 3, 5, 7];
 numrep2 = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7];
 numrep3 = [0, 5, 9, 4, 8, 3, 7, 2, 6, 1];
 if(len(price)==4):
  price_split[0] = numrep1[price_split[0]];
  price_split[1] = numrep1[price_split[1]];
  price_split[2] = numrep2[price_split[2]];
  price_split[3] = numrep3[price_split[3]];
  price_add = (price_split[0] + price_split[1] + price_split[2] + price_split[3]) * 3;
 if(len(price)==5):
  price_split[1] = numrep1[price_split[1]];
  price_split[2] = numrep1[price_split[2]];
  price_split[3] = numrep2[price_split[3]];
  price_split[4] = numrep3[price_split[4]]; 
  price_add = (price_split[1] + price_split[2] + price_split[3] + price_split[4]) * 3;
 CheckSum = price_add % 10;
 if(not return_check and len(price)==5):
  if(CheckSum!=price_split[0]):
   return False;
  if(CheckSum==price_split[0]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(price)==4):
  return str(CheckSum);
 return str(CheckSum);
def get_vw_price_checksum(price, return_check=False):
 price = str(price);
 if(len(price)==1):
  price = "000"+price;
 if(len(price)==2):
  price = "00"+price;
 if(len(price)==3):
  price = "0"+price;
 return validate_vw_price_checksum(price,True);
def fix_vw_price_checksum(price):
 price = str(price);
 if(len(price)==1):
  price = "000"+price;
 if(len(price)==2):
  price = "00"+price;
 if(len(price)==3):
  price = "0"+price;
 if(len(price)==5):
  fix_matches = re.findall("^(\d{1})(\d{4})", price); 
  fix_matches = fix_matches[0];
  price = fix_matches[1];
 if(len(price)>4):
  fix_matches = re.findall("^(\d{4})", price); 
  price = fix_matches[0];
 return str(get_vw_price_checksum(price,True))+price;
