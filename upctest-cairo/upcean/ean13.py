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

    $FileInfo: ean13.py - Last Update: 04/25/2013 Ver. 2.4.0 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import cairo, re, sys, types, upcean.precairo, upcean.validate, upcean.convert;
import upcean.ean2, upcean.ean5;
from upcean.precairo import *;
from upcean.validate import *;
from upcean.convert import *;
from upcean.ean2 import *;
from upcean.ean5 import *;

def create_ean13(upc,outfile="./ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==8): 
  upc = convert_upce_to_ean13(upc);
 if(len(upc)==12): 
  upc = convert_upca_to_ean13(upc);
 if(len(upc)==12 and validate_upca(upc)==True): 
  upc = "0"+upc;
 if(len(upc)==12 and validate_upca(upc)==False): 
  upc = upc+str(validate_ean13(upc,true));
 if(len(upc)>13 or len(upc)<13): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(validate_ean13(upc)==False): 
  pre_matches = re.findall("^(\d{12})", upc); 
  upc = pre_matches[0]+str(validate_ean13(pre_matches[0],True));
 upc_matches = re.findall("(\d{1})(\d{6})(\d{6})", upc);
 if(len(upc_matches)<=0): 
  return False;
 upc_matches = upc_matches[0];
 PrefixDigit = upc_matches[0];
 LeftDigit = list(upc_matches[1]);
 RightDigit = list(upc_matches[2]);
 addonsize = 0;
 if(supplement!=None and len(supplement)==2): 
  addonsize = 29;
 if(supplement!=None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 115 + addonsize, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 115 + addonsize, barheight[1] + 8);
 upc_img.set_source_rgb(256, 256, 256);
 upc_img.fill();
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  if(hidesn!=None and hidesn!=True):
   drawColorText(upc_img, 10, 2, barheight[1] + 2, upc_matches[0], text_color);
  drawColorText(upc_img, 10, 16, barheight[1] + 2, upc_matches[1], text_color);
  drawColorText(upc_img, 10, 62, barheight[1] + 2, upc_matches[2], text_color);
 drawColorLine(upc_img, 0, 10, 0, barheight[0], alt_text_color);
 drawColorLine(upc_img, 1, 10, 1, barheight[0], alt_text_color);
 drawColorLine(upc_img, 2, 10, 2, barheight[0], alt_text_color);
 drawColorLine(upc_img, 3, 10, 3, barheight[0], alt_text_color);
 drawColorLine(upc_img, 4, 10, 4, barheight[0], alt_text_color);
 drawColorLine(upc_img, 5, 10, 5, barheight[0], alt_text_color);
 drawColorLine(upc_img, 6, 10, 6, barheight[0], alt_text_color);
 drawColorLine(upc_img, 7, 10, 7, barheight[0], alt_text_color);
 drawColorLine(upc_img, 8, 10, 8, barheight[0], alt_text_color);
 drawColorLine(upc_img, 9, 10, 9, barheight[0], alt_text_color);
 drawColorLine(upc_img, 10, 10, 10, barheight[1], alt_text_color);
 drawColorLine(upc_img, 11, 10, 11, barheight[1], text_color);
 drawColorLine(upc_img, 12, 10, 12, barheight[1], alt_text_color);
 drawColorLine(upc_img, 13, 10, 13, barheight[1], text_color);
 NumZero = 0; 
 LineStart = 14;
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
  if(int(upc_matches[0])==1):
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==4): 
    left_text_color = left_text_color_g;
   if(NumZero==5): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==2):
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==3): 
    left_text_color = left_text_color_g;
   if(NumZero==5): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==3):
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==3): 
    left_text_color = left_text_color_g;
   if(NumZero==4): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==4):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==4): 
    left_text_color = left_text_color_g;
   if(NumZero==5): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==5):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==5): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==6):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==3): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==7):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==3): 
    left_text_color = left_text_color_g;
   if(NumZero==5): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==8):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==3): 
    left_text_color = left_text_color_g;
   if(NumZero==4): 
    left_text_color = left_text_color_g;
  if(int(upc_matches[0])==9):
   if(NumZero==1): 
    left_text_color = left_text_color_g;
   if(NumZero==2): 
    left_text_color = left_text_color_g;
   if(NumZero==4): 
    left_text_color = left_text_color_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 56, 10, 56, barheight[1], alt_text_color);
 drawColorLine(upc_img, 57, 10, 57, barheight[1], text_color);
 drawColorLine(upc_img, 58, 10, 58, barheight[1], alt_text_color);
 drawColorLine(upc_img, 59, 10, 59, barheight[1], text_color);
 drawColorLine(upc_img, 60, 10, 60, barheight[1], alt_text_color);
 NumZero = 0; 
 LineStart = 61;
 while (NumZero < len(RightDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  right_text_color = [0, 0, 0, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==0): 
   right_text_color = [1, 1, 1, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==1): 
   right_text_color = [1, 1, 0, 0, 1, 1, 0];
  if(int(RightDigit[NumZero])==2): 
   right_text_color = [1, 1, 0, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==3): 
   right_text_color = [1, 0, 0, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==4): 
   right_text_color = [1, 0, 1, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==5): 
   right_text_color = [1, 0, 0, 1, 1, 1, 0];
  if(int(RightDigit[NumZero])==6): 
   right_text_color = [1, 0, 1, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==7): 
   right_text_color = [1, 0, 0, 0, 1, 0, 0];
  if(int(RightDigit[NumZero])==8): 
   right_text_color = [1, 0, 0, 1, 0, 0, 0];
  if(int(RightDigit[NumZero])==9): 
   right_text_color = [1, 1, 1, 0, 1, 0, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(right_text_color)):
   if(right_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(right_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 103, 10, 103, barheight[1], text_color);
 drawColorLine(upc_img, 104, 10, 104, barheight[1], alt_text_color);
 drawColorLine(upc_img, 105, 10, 105, barheight[1], text_color);
 drawColorLine(upc_img, 106, 10, 106, barheight[0], alt_text_color);
 drawColorLine(upc_img, 107, 10, 107, barheight[0], alt_text_color);
 drawColorLine(upc_img, 108, 10, 108, barheight[0], alt_text_color);
 drawColorLine(upc_img, 109, 10, 109, barheight[0], alt_text_color);
 drawColorLine(upc_img, 110, 10, 110, barheight[0], alt_text_color);
 drawColorLine(upc_img, 111, 10, 111, barheight[0], alt_text_color);
 drawColorLine(upc_img, 112, 10, 112, barheight[0], alt_text_color);
 drawColorLine(upc_img, 113, 10, 113, barheight[0], alt_text_color);
 drawColorLine(upc_img, 114, 10, 114, barheight[0], alt_text_color);
 if(supplement!=None and len(supplement)==2):
  upc_sup_img = draw_ean2_supplement(supplement,1,hideinfo,barheight);
  upc_img.set_source_surface(upc_sup_img, 115, 0);
  upc_img.paint();
  del(upc_sup_img);
 if(supplement!=None and len(supplement)==5):
  upc_sup_img = draw_ean5_supplement(supplement,1,hideinfo,barheight);
  upc_img.set_source_surface(upc_sup_img, 115, 0);
  upc_img.paint();
  del(upc_sup_img);
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (115 + addonsize) * int(resize), (barheight[1] + 8) * int(resize));
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

def draw_ean13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ean13(upc,None,resize,hideinfo,barheight);

def create_ean13_from_list(upc,outfile,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return create_ean13(upc,outfile,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return create_ean13(upc,outfile,resize,hideinfo,barheight);
 if(isinstance(upc, tuple) or isinstance(upc, list)):
  NumLoop = 0;
  retlist = list();
  while (NumLoop < len(upc)):
   if(isinstance(resize, tuple) or isinstance(resize, list)):
    resize_val = resize[NumLoop];
   if(sys.version[0]=="2"):
    if(isinstance(resize, str) or isinstance(resize, unicode) or isinstance(resize, int)):
     resize_val = resize;
   if(sys.version[0]=="3"):
    if(isinstance(resize, str) or isinstance(resize, int)):
     resize_val = resize;
   if(isinstance(hideinfo[0], tuple) or isinstance(hideinfo[0], list)):
    hideinfo_val = hideinfo[NumLoop];
   if(isinstance(hideinfo[0], bool)):
    hideinfo_val = hideinfo;
   if(isinstance(barheight[0], tuple) or isinstance(barheight[0], list)):
    barheight_val = barheight[NumLoop];
   if(isinstance(barheight[0], int)):
    barheight_val = barheight;
   retlist.append(create_ean13(upc[NumLoop],outfile[NumLoop],resize_val,hideinfo_val,barheight_val));
   NumLoop = NumLoop + 1;
 return retlist;

def draw_ean13_from_list(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return draw_ean13(upc,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return draw_ean13(upc,resize,hideinfo,barheight);
 if(isinstance(upc, tuple) or isinstance(upc, list)):
  NumLoop = 0;
  drawlist = list();
  while (NumLoop < len(upc)):
   if(isinstance(resize, tuple) or isinstance(resize, list)):
    resize_val = resize[NumLoop];
   if(sys.version[0]=="2"):
    if(isinstance(resize, str) or isinstance(resize, unicode) or isinstance(resize, int)):
     resize_val = resize;
   if(sys.version[0]=="3"):
    if(isinstance(resize, str) or isinstance(resize, int)):
     resize_val = resize;
   if(isinstance(hideinfo[0], tuple) or isinstance(hideinfo[0], list)):
    hideinfo_val = hideinfo[NumLoop];
   if(isinstance(hideinfo[0], bool)):
    hideinfo_val = hideinfo;
   if(isinstance(barheight[0], tuple) or isinstance(barheight[0], list)):
    barheight_val = barheight[NumLoop];
   if(isinstance(barheight[0], int)):
    barheight_val = barheight;
   drawlist.append(draw_ean13(upc[NumLoop],resize_val,hideinfo_val,barheight_val));
   NumLoop = NumLoop + 1;
 return drawlist;
