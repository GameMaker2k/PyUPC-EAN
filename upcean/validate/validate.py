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

    $FileInfo: validate.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
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
 #if(len(upc)==upclen and upclen%2==1):
 # upc_len1 = len(upc_matches1) - 1;
 OddSum = 0;
 while(upc_count1<upc_len1):
  OddSum = OddSum + upc_matches1[upc_count1];
  upc_count1 = upc_count1 + 1;
 upc_matches2 = upc_matches[1:][::2];
 upc_count2 = 0;
 upc_len2 = len(upc_matches2);
 #if(len(upc)==upclen and upclen%2==0):
 # upc_len2 = len(upc_matches2) - 1;
 EvenSum = 0;
 while(upc_count2<upc_len2):
  EvenSum = EvenSum + upc_matches2[upc_count2];
  upc_count2 = upc_count2 + 1;
 AllSum = OddSum + (EvenSum * 3);
 if(upclen % 2)==0:
  AllSum = OddSum + (EvenSum * 3);
 else:
  AllSum = (OddSum * 3) + EvenSum;
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
 return validate_luhn_checksum(upc,upclen,True);
def fix_luhn_checksum(upc, upclen):
 upc = str(upc);
 upclen = int(upclen);
 if(len(upc)>upclen):
  fix_matches = re.findall("^(\d{"+str(upclen)+"})", upc);
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

def validate_itf6_checksum(upc, return_check=False):
 upc = str(upc);
 if(len(upc)>6):
  fix_matches = re.findall("^(\d{6})", upc);
  upc = fix_matches[0];
 if(len(upc)>6 or len(upc)<5):
  return False;
 upc_matches = list(upc);
 upc_matches = [int(x) for x in upc_matches];
 CheckSum = 10 - ( ( 3 * upc_matches[0] + upc_matches[1] + 3 * upc_matches[2] + upc_matches[3] + 3 * upc_matches[4] ) % 10 );
 if(not return_check and len(upc)==6):
  if(CheckSum!=upc_matches[5]):
   return False;
  if(CheckSum==upc_matches[5]):
   return True;
 if(return_check):
  return str(CheckSum);
 if(len(upc)==5):
  return str(CheckSum);
def get_itf6_checksum(upc):
 upc = str(upc);
 return validate_itf6_checksum(upc,True);
def fix_itf6_checksum(upc):
 upc = str(upc);
 if(len(upc)>5):
  fix_matches = re.findall("^(\d{5})", upc);
  upc = fix_matches[0];
 return upc+str(get_itf6_checksum(upc));

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

def get_itf_checksum(upc):
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
 EvenSum = 0;
 EvenNum = 0;
 EvenNumX = len(upc_matches2);
 while(EvenNum < EvenNumX):
  EvenSum += upc_matches2[EvenNum];
  EvenNum += 1;
 OddSum = 0;
 OddNum = 0;
 OddNumX = len(upc_matches1);
 while(OddNum < OddNumX):
  OddSum += (upc_matches1[EvenNum] * 3);
  OddNum += 1;
 AllSum = OddSum + EvenSum;
 CheckSum = AllSum % 10;
 if(CheckSum>0):
  CheckSum = 10 - CheckSum;
 return str(CheckSum);

def get_stf_checksum(upc):
 CheckSum = get_itf_checksum(upc);
 return str(CheckSum);

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
  UPC_Sum += (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
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
  UPC_Sum += (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1;
  UPC_Weight += 1;
 CheckSum = str(CheckSum)+str(Code11Array[UPC_Sum % 11]);
 return str(CheckSum);

'''
// Code 39
// Source: http://www.barcodeisland.com/code39.phtml
// Source: http://en.wikipedia.org/wiki/Code_39
'''
def get_code39_checksum_mod10(upc):
 if(len(upc) < 1):
  return False;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 upc = upc.upper();
 upc_matches = list(upc);
 if(len(upc_matches)<=0):
  return False;
 Code39Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%"};
 Code39Values = dict(zip(Code39Array.values(),Code39Array));
 upc_print = list(upc_matches);
 UPC_Count = 0;
 UPC_Sum = 0;
 while (UPC_Count < len(upc_matches)):
  UPC_Sum += Code39Values[str(upc_matches[UPC_Count])];
  UPC_Count += 1;
 CheckSum = str(Code39Array[UPC_Sum % 10]);
 return str(CheckSum);

def get_code39_checksum_mod43(upc):
 if(len(upc) < 1):
  return False;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 upc = upc.upper();
 upc_matches = list(upc);
 if(len(upc_matches)<=0):
  return False;
 Code39Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I", 19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R", 28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z", 36: "-", 37: ".", 38: " ", 39: "$", 40: "/", 41: "+", 42: "%"};
 Code39Values = dict(zip(Code39Array.values(),Code39Array));
 upc_print = list(upc_matches);
 UPC_Count = 0;
 UPC_Sum = 0;
 while (UPC_Count < len(upc_matches)):
  UPC_Sum += Code39Values[str(upc_matches[UPC_Count])];
  UPC_Count += 1;
 CheckSum = str(Code39Array[UPC_Sum % 43]);
 return str(CheckSum);

def get_code39_checksum(upc, getmod="43"):
 getmod = str(getmod);
 if(getmod!="10" and getmod!="43"):
  getmod = "43";
 if(getmod=="10"):
  return get_code39_checksum_mod10(upc);
 if(getmod=="43"):
  return get_code39_checksum_mod43(upc);
 return False;

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
  UPC_Sum += (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
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
  UPC_Sum += (UPC_Weight * Code93Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1;
  UPC_Weight += 1;
 CheckSum = str(CheckSum)+str(Code93Array[UPC_Sum % 47]);
 return str(CheckSum);

'''
// Code 128
// Source: http://www.barcodeisland.com/code128.phtml
// Source: http://en.wikipedia.org/wiki/Code_128
'''
def get_code128_checksum(upc):
 if(len(upc) % 2):
  return False;
 if(len(upc) < 6):
  return False;
 if(not re.findall("([0-9a-f]+)", upc)):
  return False;
 upc = upc.lower();
 if(not re.findall("[0-9a-f]{2}", upc)):
  return False;
 upc_matches = re.findall("[0-9a-f]{2}", upc);
 upc_to_dec = list([int(x, 16) for x in upc_matches]);
 icount = 1;
 icountadd = 1;
 checksum = 0;
 if(upc_to_dec[0]>102 and upc_to_dec[0]<106):
  checksum = checksum + upc_to_dec[0];
  icount = 1;
 else:
  checksum = 0;
  icount = 0;
 upc_less_count = len(upc_to_dec) - 1;
 while(icount < len(upc_to_dec)):
  if(icount==upc_less_count and (upc_to_dec[icount]>105 and upc_to_dec[icount]<108)):
   checksum = checksum;
  else:
   checksum = checksum + (upc_to_dec[icount] * icountadd);
  icount = icount + 1;
  icountadd = icountadd + 1;
 checksum = str(format(checksum % 103, 'x')).zfill(2);
 return checksum;

def convert_ascii_code128_to_hex_code128(upc):
 upc = str(upc);
 if(len(upc) < 4):
  return False;
 hextoascii = { '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Î" };
 asciitohex = { ' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Î': "6c" };
 barcodeout = "";
 for upcpart in upc:
  barcodeout = barcodeout + asciitohex.get(upcpart, '');
 return barcodeout;

def convert_hex_code128_to_ascii_code128(upc):
 upc = str(upc);
 if(len(upc) < 8):
  return False;
 hextoascii = { '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Î" };
 asciitohex = { ' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Î': "6c" };
 barcodeout = "";
 for upcpart in upc:
  barcodeout = barcodeout + hextoascii.get(upcpart, '');
 return barcodeout;

def convert_text_to_hex_code128(upc):
 hextocharsetone = { ' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '\x00': "40", '\x01': "41", '\x02': "42", '\x03': "43", '\x04': "44", '\x05': "45", '\x06': "46", '\x07': "47", '\x08': "48", '\x09': "49", '\x0a': "4a", '\x0b': "4b", '\x0c': "4c", '\x0d': "4d", '\x0e': "4e", '\x0f': "4f", '\x10': "50", '\x11': "51", '\x12': "52", '\x13': "53", '\x14': "54", '\x15': "55", '\x16': "56", '\x17': "57", '\x18': "58", '\x19': "59", '\x1a': "5a", '\x1b': "5b", '\x1c': "5c", '\x1d': "5d", '\x1e': "5e", '\x1f': "5f" };
 hextocharsettwo = { ' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", '\x7f': "5f" };
 hextocharsetthree = { '00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '10': "0a", '11': "0b", '12': "0c", '13': "0d", '14': "0e", '15': "0f", '16': "10", '17': "11", '18': "12", '19': "13", '20': "14", '21': "15", '22': "16", '23': "17", '24': "18", '25': "19", '26': "1a", '27': "1b", '28': "1c", '29': "1d", '30': "1e", '31': "1f", '32': "20", '33': "21", '34': "22", '35': "23", '36': "24", '37': "25", '38': "26", '39': "27", '40': "28", '41': "29", '42': "2a", '43': "2b", '44': "2c", '45': "2d", '46': "2e", '47': "2f", '48': "30", '49': "31", '50': "32", '51': "33", '52': "34", '53': "35", '54': "36", '55': "37", '56': "38", '57': "39", '58': "3a", '59': "3b", '60': "3c", '61': "3d", '62': "3e", '63': "3f", '64': "40", '65': "41", '66': "42", '67': "43", '68': "44", '69': "45", '70': "46", '71': "47", '72': "48", '73': "49", '74': "4a", '75': "4b", '76': "4c", '77': "4d", '78': "4e", '79': "4f", '80': "50", '81': "51", '82': "52", '83': "53", '84': "54", '85': "55", '86': "56", '87': "57", '88': "58", '89': "59", '90': "5a", '91': "5b", '92': "5c", '93': "5d", '94': "5e", '95': "5f", '96': "60", '97': "61", '98': "62", '99': "63", ' ': "64", ' ': "65", ' ': "66", ' ': "67", ' ': "68", ' ': "69", ' ': "6a", ' ': "6b", ' ': "6c" };
 hextocharsetfour = { '32': "00", '194': "00", '207': "00", '212': "00", '252': "00", '33': "01", '34': "02", '35': "03", '36': "04", '37': "05", '38': "06", '39': "07", '40': "08", '41': "09", '42': "0a", '43': "0b", '44': "0c", '45': "0d", '46': "0e", '47': "0f", '48': "10", '49': "11", '50': "12", '51': "13", '52': "14", '53': "15", '54': "16", '55': "17", '56': "18", '57': "19", '58': "1a", '59': "1b", '60': "1c", '61': "1d", '62': "1e", '63': "1f", '64': "20", '65': "21", '66': "22", '67': "23", '68': "24", '69': "25", '70': "26", '71': "27", '72': "28", '73': "29", '74': "2a", '75': "2b", '76': "2c", '77': "2d", '78': "2e", '79': "2f", '80': "30", '81': "31", '82': "32", '83': "33", '84': "34", '85': "35", '86': "36", '87': "37", '88': "38", '89': "39", '90': "3a", '91': "3b", '92': "3c", '93': "3d", '94': "3e", '95': "3f", '96': "40", '97': "41", '98': "42", '99': "43", '100': "44", '101': "45", '102': "46", '103': "47", '104': "48", '105': "49", '106': "4a", '107': "4b", '108': "4c", '109': "4d", '110': "4e", '111': "4f", '112': "50", '113': "51", '114': "52", '115': "53", '116': "54", '117': "55", '118': "56", '119': "57", '120': "58", '121': "59", '122': "5a", '123': "5b", '124': "5c", '125': "5d", '126': "5e", '195': "5f", '200': "5f", '240': "5f", '196': "60", '201': "60", '241': "60", '197': "61", '202': "61", '242': "61", '198': "62", '203': "62", '243': "62", '199': "63", '204': "63", '244': "63", '200': "64", '205': "64", '245': "64", '201': "65", '206': "65", '246': "65", '202': "66", '207': "66", '247': "66", '203': "67", '208': "67", '248': "67", '204': "68", '209': "68", '249': "68", '205': "69", '210': "69", '250': "69", '127': "6a", '128': "6b", '129': "6c" };
 hextoascii = { '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Î" };
 asciitohex = { 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Î': "6c" };
 textlen = len(upc);
 textc = 0;
 incharset = None;
 shiftcharset = None;
 textlist = [];
 while(textc < textlen):
  skipcheck = False;
  if(asciitohex.get(upc[textc], False)):
   if((upc[textc]=="Ä" and (incharset==1 or incharset==2 or incharset is None)) or (upc[textc]=="Å" and (incharset==1 or incharset==2 or incharset is None)) or (upc[textc]=="È" and (incharset==2 or incharset is None)) or (upc[textc]=="É" and (incharset==1 or incharset is None)) or upc[textc]=="Ê"):
    if(textc==0):
     textlist.append("67");
     incharset = 2;
    textlist.append(asciitohex.get(upc[textc], False));
  elif((incharset==1 and upc[textc]==" ") or (incharset==2 and upc[textc]==" ")):
   textlist.append(hextocharsetone.get(upc[textc], False));
  elif((upc[textc].isnumeric() and ((textc+1) < textlen) and upc[textc+1].isnumeric()) and not skipcheck):
   if(hextocharsetthree.get(upc[textc]+upc[textc+1], False)):
    if(incharset==3):
     textlist.append(hextocharsetthree.get(upc[textc]+upc[textc+1], False));
    else:
     if(textc==0):
      textlist.append("69");
     else:
      textlist.append("63");
     textlist.append(hextocharsetthree.get(upc[textc]+upc[textc+1], False));
    incharset = 3;
    skipcheck = True;
    textc += 1;
  elif(hextocharsettwo.get(upc[textc], False) and not (incharset==1 and shiftcharset is None and hextocharsetone.get(upc[textc], False)) and not skipcheck):
   if(incharset==2):
    textlist.append(hextocharsettwo.get(upc[textc], False));
   else:
    if(textc==0):
     textlist.append("68");
    else:
     if(((textc+1) < textlen) and hextocharsettwo.get(upc[textc+1], False) or incharset==3):
      textlist.append("64");
     else:
      textlist.append("62");
      shiftcharset = True;
    textlist.append(hextocharsettwo.get(upc[textc], False));
   skipcheck = True;
   if(shiftcharset is None):
    incharset = 2;
   else:
    shiftcharset = None;
  elif(hextocharsetone.get(upc[textc], False) and not skipcheck):
   if(incharset==1):
    textlist.append(hextocharsetone.get(upc[textc], False));
   else:
    if(textc==0):
     textlist.append("67");
    else:
     if(((textc+1) < textlen) and hextocharsetone.get(upc[textc+1], False) or incharset==3):
      textlist.append("65");
     else:
      textlist.append("62");
      shiftcharset = True;
    textlist.append(hextocharsetone.get(upc[textc], False));
   skipcheck = True;
   if(shiftcharset is None):
    incharset = 1;
   else:
    shiftcharset = None;
  textc += 1;
 if(not any(textlist)):
  return False;
 return str(''.join(textlist));

def convert_text_to_hex_code128_manual(upc):
 hextocharsetone = { ' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '\x00': "40", '\x01': "41", '\x02': "42", '\x03': "43", '\x04': "44", '\x05': "45", '\x06': "46", '\x07': "47", '\x08': "48", '\x09': "49", '\x0a': "4a", '\x0b': "4b", '\x0c': "4c", '\x0d': "4d", '\x0e': "4e", '\x0f': "4f", '\x10': "50", '\x11': "51", '\x12': "52", '\x13': "53", '\x14': "54", '\x15': "55", '\x16': "56", '\x17': "57", '\x18': "58", '\x19': "59", '\x1a': "5a", '\x1b': "5b", '\x1c': "5c", '\x1d': "5d", '\x1e': "5e", '\x1f': "5f" };
 hextocharsettwo = { ' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", '\x7f': "5f" };
 hextocharsetthree = { '00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '10': "0a", '11': "0b", '12': "0c", '13': "0d", '14': "0e", '15': "0f", '16': "10", '17': "11", '18': "12", '19': "13", '20': "14", '21': "15", '22': "16", '23': "17", '24': "18", '25': "19", '26': "1a", '27': "1b", '28': "1c", '29': "1d", '30': "1e", '31': "1f", '32': "20", '33': "21", '34': "22", '35': "23", '36': "24", '37': "25", '38': "26", '39': "27", '40': "28", '41': "29", '42': "2a", '43': "2b", '44': "2c", '45': "2d", '46': "2e", '47': "2f", '48': "30", '49': "31", '50': "32", '51': "33", '52': "34", '53': "35", '54': "36", '55': "37", '56': "38", '57': "39", '58': "3a", '59': "3b", '60': "3c", '61': "3d", '62': "3e", '63': "3f", '64': "40", '65': "41", '66': "42", '67': "43", '68': "44", '69': "45", '70': "46", '71': "47", '72': "48", '73': "49", '74': "4a", '75': "4b", '76': "4c", '77': "4d", '78': "4e", '79': "4f", '80': "50", '81': "51", '82': "52", '83': "53", '84': "54", '85': "55", '86': "56", '87': "57", '88': "58", '89': "59", '90': "5a", '91': "5b", '92': "5c", '93': "5d", '94': "5e", '95': "5f", '96': "60", '97': "61", '98': "62", '99': "63" };
 hextocharsetfour = { '32': "00", '194': "00", '207': "00", '212': "00", '252': "00", '33': "01", '34': "02", '35': "03", '36': "04", '37': "05", '38': "06", '39': "07", '40': "08", '41': "09", '42': "0a", '43': "0b", '44': "0c", '45': "0d", '46': "0e", '47': "0f", '48': "10", '49': "11", '50': "12", '51': "13", '52': "14", '53': "15", '54': "16", '55': "17", '56': "18", '57': "19", '58': "1a", '59': "1b", '60': "1c", '61': "1d", '62': "1e", '63': "1f", '64': "20", '65': "21", '66': "22", '67': "23", '68': "24", '69': "25", '70': "26", '71': "27", '72': "28", '73': "29", '74': "2a", '75': "2b", '76': "2c", '77': "2d", '78': "2e", '79': "2f", '80': "30", '81': "31", '82': "32", '83': "33", '84': "34", '85': "35", '86': "36", '87': "37", '88': "38", '89': "39", '90': "3a", '91': "3b", '92': "3c", '93': "3d", '94': "3e", '95': "3f", '96': "40", '97': "41", '98': "42", '99': "43", '100': "44", '101': "45", '102': "46", '103': "47", '104': "48", '105': "49", '106': "4a", '107': "4b", '108': "4c", '109': "4d", '110': "4e", '111': "4f", '112': "50", '113': "51", '114': "52", '115': "53", '116': "54", '117': "55", '118': "56", '119': "57", '120': "58", '121': "59", '122': "5a", '123': "5b", '124': "5c", '125': "5d", '126': "5e", '195': "5f", '200': "5f", '240': "5f", '196': "60", '201': "60", '241': "60", '197': "61", '202': "61", '242': "61", '198': "62", '203': "62", '243': "62", '199': "63", '204': "63", '244': "63", '200': "64", '205': "64", '245': "64", '201': "65", '206': "65", '246': "65", '202': "66", '207': "66", '247': "66", '203': "67", '208': "67", '248': "67", '204': "68", '209': "68", '249': "68", '205': "69", '210': "69", '250': "69", '127': "6a", '128': "6b", '129': "6c" };
 hextoascii = { '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Î" };
 asciitohex = { 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Î': "6c" };
 textlen = len(upc);
 textc = 0;
 incharset = None;
 shiftcharset = None;
 textlist = [];
 while(textc < textlen):
  skipcheck = False;
  if(asciitohex.get(upc[textc], False)):
   if(upc[textc]=="Ë" and textc==0):
    incharset = 1;
   elif(upc[textc]=="Ì" and textc==0):
    incharset = 2;
   elif(upc[textc]=="Í" and textc==0):
    incharset = 3;
   elif(upc[textc]=="Æ"):
    if(incharset==1):
     shiftcharset = 2;
    elif(incharset==2):
     shiftcharset = 1;
   elif(upc[textc]=="Ç" and (incharset==1 or incharset==2)):
    incharset = 3;
   elif(upc[textc]=="È" and (incharset==1 or incharset==3)):
    incharset = 2;
   elif(upc[textc]=="É" and (incharset==2 or incharset==3)):
    incharset = 1;
   textlist.append(asciitohex.get(upc[textc], False));
  elif(incharset==3):
   textlist.append(hextocharsetthree.get(upc[textc]+upc[textc+1], False));
   skipcheck = True;
   textc += 1;
  elif((incharset==2 and shiftcharset is None) or (shiftcharset==2 and incharset==1)):
   textlist.append(hextocharsettwo.get(upc[textc], False));
   if(shiftcharset==2 and incharset==1):
    shiftcharset = None;
   skipcheck = True;
  elif((incharset==1 and shiftcharset is None) or (shiftcharset==1 and incharset==2)):
   textlist.append(hextocharsetone.get(upc[textc], False));
   if(shiftcharset==1 and incharset==2):
    shiftcharset = None;
   skipcheck = True;
  textc += 1;
 if(not any(textlist)):
  return False;
 return str(''.join(textlist));

def convert_text_to_hex_code128_with_checksum(upc):
 code128out = convert_text_to_hex_code128(upc);
 if(not code128out):
  return False;
 return code128out + "6d" + get_code128_checksum(code128out)+"6c";

def convert_text_to_hex_code128_manual_with_checksum(upc):
 code128out = convert_text_to_hex_code128_manual(upc);
 if(not code128out):
  return False;
 return code128out + "6d" + get_code128_checksum(code128out)+"6c";

def get_code128alt_checksum(upc):
 upc = str(upc);
 if(len(upc) < 4):
  return False;
 upc = convert_ascii_code128_to_hex_code128(upc);
 return get_code128_checksum(upc);

def get_code128dec_checksum(upc):
 upc = str(upc);
 if(len(upc) < 12):
  return False;
 if(not re.findall("[0-9]{3}", upc)):
  return False;
 upc_matches = re.findall("[0-9]{3}", upc);
 il = len(upc_matches);
 i = 0;
 upcout = "";
 while(i < il):
  dectohex = format(int(upc_matches[i]), 'x');
  dectohexzero = str(dectohex).zfill(2);
  if(len(dectohexzero)>2):
   return False;
  upcout = upcout+str(dectohexzero);
  i = i + 1;
 upc = upcout;
 return get_code128_checksum(upc);

'''
// MSI (Modified Plessey)
// Source: http://www.barcodeisland.com/msi.phtml
// Source: http://en.wikipedia.org/wiki/MSI_Barcode
'''
def get_msi_checksum_mod10(upc):
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
  UPC_Sum += upc_matches1[PreCount];
  PreCount += 1;
 PreCount = 0;
 while (PreCount<=len(upc_matches2)-1):
  UPC_Sum += upc_matches2[PreCount];
  PreCount += 1;
 CheckSum = 10 - (UPC_Sum % 10);
 return str(CheckSum);

def get_msi_checksum_mod11(upc, modtype="ibm"):
 if(modtype=="ibm"):
  countup = (2, 3, 4, 5, 6, 7);
 elif(modtype=="ncr"):
  countup = (2, 3, 4, 5, 6, 7, 8, 9);
 else:
  countup = (2, 3, 4, 5, 6, 7);
 upc_reverse = list(upc);
 upc_reverse.reverse();
 startcount = 0;
 seccount = countup[0];
 endcount = len(upc_reverse);
 UPC_Sum = 0;
 while(startcount<endcount):
  if(seccount>countup[-1]):
   seccount = countup[0];
  UPC_Sum += int(upc_reverse[startcount]) * seccount;
  seccount += 1;
  startcount += 1;
 CheckSum = ((11 - (UPC_Sum % 11)) % 11) % 11;
 return str(CheckSum);
 
def get_msi_checksum_mod1010(upc):
 CheckSum = get_msi_checksum_mod10(get_msi_checksum_mod10(upc));
 return str(CheckSum);

def get_msi_checksum_mod1110(upc, modtype="ibm"):
 CheckSum = get_msi_checksum_mod10(get_msi_checksum_mod11(upc, modtype));
 return str(CheckSum);

def get_msi_checksum(upc, getmod="10", modtype="ibm"):
 getmod = str(getmod);
 if(getmod!="10" and getmod!="11" and getmod!="1010" and getmod!="1110"):
  getmod = "10";
 if(getmod=="10"):
  return get_msi_checksum_mod10(upc);
 if(getmod=="11"):
  return get_msi_checksum_mod11(upc, modtype);
 if(getmod=="1010"):
  return get_msi_checksum_mod1010(upc);
 if(getmod=="1110"):
  return get_msi_checksum_mod1110(upc, modtype);
 return False;

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
 if(not re.findall("^(97[8-9])(\d{9})", upc)):
  return False;
 if(re.findall("^(97[8-9])(\d{9})", upc)):
  return validate_ean13_checksum(upc,return_check);
def get_isbn13_checksum(upc):
 upc = str(upc);
 return validate_isbn13_checksum(upc,True);
def fix_isbn13_checksum(upc):
 upc = str(upc);
 if(not re.findall("^(97[8-9])(\d{9})", upc)):
  return False;
 if(re.findall("^(97[8-9])(\d{9})", upc)):
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
