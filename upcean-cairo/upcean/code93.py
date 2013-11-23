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

    $FileInfo: code93.py - Last Update: 11/23/2013 Ver. 2.5.0 RC 1  - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import cairo, re, sys, types, upcean.precairo;
from upcean.precairo import *;

def create_code93(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
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
 upc_matches.append(Code93Array[UPC_Sum % 47]);
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
 upc_matches.append(Code93Array[UPC_Sum % 47]);
 upc_size_add = (len(upc_matches) * 9);
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 37 + upc_size_add, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 37 + upc_size_add, barheight[1] + 8);
 upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
 upc_img.fill();
 if(hidetext==False):
  NumTxtZero = 0; 
  LineTxtStart = 16;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10, LineTxtStart, barheight[1] + 3, upc_print[NumTxtZero], barcolor[1]);
   LineTxtStart += 9;
   NumTxtZero += 1;
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
 drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
 drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
 drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
 drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
 drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
 drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
 drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
 drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
 drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
 drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
 drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
 drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
 drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[0]);
 drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[0]);
 drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
 drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[0]);
 drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[2]);
 NumZero = 0; 
 LineStart = 18; 
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 0, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="A"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="B"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="C"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="D"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="E"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="F"):
   left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="G"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="H"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="I"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="J"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="K"):
   left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="L"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="M"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="N"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="O"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="P"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Q"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="R"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="S"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="T"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="U"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="V"):
   left_barcolor = [1, 1, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="W"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="X"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Y"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="Z"):
   left_barcolor = [1, 0, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="-"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="."):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="$"):
   left_barcolor = [1, 1, 1, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="/"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="+"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="%"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="($)"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="(%)"):
   left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="(/)"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="(+)"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1; 
 drawColorLine(upc_img, 18 + upc_size_add, 4, 18 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 19 + upc_size_add, 4, 19 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 20 + upc_size_add, 4, 20 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
 drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (37 + upc_size_add) * int(resize), (barheight[1] + 8) * int(resize));
 new_upc_img = cairo.Context(new_upc_preimg);
 new_upc_img.set_source(upc_imgpat);
 new_upc_img.paint();
 del(upc_preimg);
 if(outfile is None or isinstance(outfile, bool)):
  return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_code93(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_code93(upc,None,resize,hideinfo,barheight,barcolor);
