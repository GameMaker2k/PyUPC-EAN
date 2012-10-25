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

    FileInfo: ean5.py - Last Update: 10/04/2012 Ver. 2.0.0 - Author: cooldude2k 
'''

import cairo, re, upcean.precairo;
from upcean.precairo import *;

def create_ean5(upc,offsetadd,imgres,hidetext=False,barheight=(48, 54)):
 upc = str(upc);
 if(len(upc)>5 or len(upc)<5): 
  return False;
 upc_matches = re.findall("(\d{5})", upc);
 if(len(upc_matches)<=0): 
  return False;
 LeftDigit = list(upc_matches[0]);
 CheckSum = (int(LeftDigit[0]) * 3) + (int(LeftDigit[1]) * 9) + (int(LeftDigit[2]) * 3) + (int(LeftDigit[3]) * 9) + (int(LeftDigit[4]) * 3);
 CheckSum = CheckSum % 10;
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  drawColorText(imgres, 10, 5 + offsetadd, barheight[1] + 2, LeftDigit[0], text_color);
  drawColorText(imgres, 10, 14 + offsetadd, barheight[1] + 2, LeftDigit[1], text_color);
  drawColorText(imgres, 10, 22 + offsetadd, barheight[1] + 2, LeftDigit[2], text_color);
  drawColorText(imgres, 10, 30 + offsetadd, barheight[1] + 2, LeftDigit[3], text_color);
  drawColorText(imgres, 10, 38 + offsetadd, barheight[1] + 2, LeftDigit[4], text_color);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(imgres, 0 + offsetadd, 10, 0 + offsetadd, LineSize, alt_text_color);
 drawColorLine(imgres, 1 + offsetadd, 10, 1 + offsetadd, LineSize, text_color);
 drawColorLine(imgres, 2 + offsetadd, 10, 2 + offsetadd, LineSize, alt_text_color);
 drawColorLine(imgres, 3 + offsetadd, 10, 3 + offsetadd, LineSize, text_color);
 drawColorLine(imgres, 4 + offsetadd, 10, 4 + offsetadd, LineSize, text_color);
 NumZero = 0; 
 LineStart = 5 + offsetadd;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_text_color_l = [0, 0, 0, 0, 0, 0, 0]; 
  left_text_color_g = [1, 1, 1, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==0): 
   left_text_color_l = [0, 0, 0, 1, 1, 0, 1]; 
   left_text_color_g = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_text_color_l = [0, 0, 1, 1, 0, 0, 1]; 
   left_text_color_g = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_text_color_l = [0, 0, 1, 0, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_text_color_l = [0, 1, 1, 1, 1, 0, 1]; 
   left_text_color_g = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_text_color_l = [0, 1, 0, 0, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_text_color_l = [0, 1, 1, 0, 0, 0, 1]; 
   left_text_color_g = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_text_color_l = [0, 1, 0, 1, 1, 1, 1]; 
   left_text_color_g = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_text_color_l = [0, 1, 1, 1, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_text_color_l = [0, 1, 1, 0, 1, 1, 1]; 
   left_text_color_g = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9): 
   left_text_color_l = [0, 0, 0, 1, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 0, 1, 1, 1];
  left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==0 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==0 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==1 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==1 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==3 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==4 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==4 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==5 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==5 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==6 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==7 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==7 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==8 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==9 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==9 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==4):
   left_text_color = left_text_color_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(imgres, LineStart, 10, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(imgres, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero < 5):
   drawColorLine(imgres, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   drawColorLine(imgres, LineStart, 10, LineStart, LineSize, text_color);
   LineStart += 1;
  NumZero += 1;
 return True;
