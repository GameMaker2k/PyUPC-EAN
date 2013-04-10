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

    $FileInfo: ean2.py - Last Update: 04/10/2013 Ver. 2.3.7 RC 1 - Author: cooldude2k $
'''

import cairo, re, sys, types, upcean.precairo;
from upcean.precairo import *;

def create_ean2(upc,outfile="./ean2.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc)>2 or len(upc)<2): 
  return False;
 upc_matches = re.findall("(\d{2})", upc);
 if(len(upc_matches)<=0): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 CheckSum = int(upc_matches[0]) % 4;
 LeftDigit = list(upc_matches[0]);
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 83, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 83, barheight[1] + 8);
 upc_img.set_source_rgb(256, 256, 256);
 upc_img.fill();
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  drawColorText(upc_img, 10, 3, barheight[1] + 2, LeftDigit[0], text_color);
  drawColorText(upc_img, 10, 11, barheight[1] + 2, LeftDigit[1], text_color);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 10, 0, LineSize, alt_text_color);
 drawColorLine(upc_img, 1, 10, 1, LineSize, text_color);
 drawColorLine(upc_img, 2, 10, 2, LineSize, alt_text_color);
 drawColorLine(upc_img, 3, 10, 3, LineSize, text_color);
 drawColorLine(upc_img, 4, 10, 4, LineSize, text_color);
 NumZero = 0; 
 LineStart = 5;
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
   left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==1): 
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==0): 
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==1): 
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==0): 
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==1): 
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==0): 
   left_text_color = left_text_color_g;
  if(CheckSum==3 and NumZero==1): 
   left_text_color = left_text_color_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero == 0):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   LineStart += 1;
  NumZero += 1;
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 83 * int(resize), (barheight[1] + 8) * int(resize));
 new_upc_img = cairo.Context(new_upc_preimg);
 new_upc_img.set_source(upc_imgpat);
 new_upc_img.paint();
 del(upc_preimg);
 if(outfile is None or isinstance(outfile, bool)):
  return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   new_upc_preimg.write_to_png(sys.stdout);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   new_upc_preimg.write_to_png(sys.stdout.buffer);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  new_upc_preimg.write_to_png(outfile);
 return True;

def draw_ean2(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ean2(upc,None,resize,hideinfo,barheight);
