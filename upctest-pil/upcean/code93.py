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

    $FileInfo: code93.py - Last Update: 08/06/2013 Ver. 2.4.3 RC 3 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, types, upcean.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;
from upcean.getsfname import *;

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
 upc_preimg = Image.new("RGB", (37 + upc_size_add, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (37 + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
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
 new_upc_img = upc_preimg.resize(((37 + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(hidetext==False):
  NumTxtZero = 0; 
  LineTxtStart = 18;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10 * int(resize), LineTxtStart + (19 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), upc_print[NumTxtZero], barcolor[1]);
   LineTxtStart += 9 * int(resize);
   NumTxtZero += 1;
 del(upc_img);
 oldoutfile = get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return new_upc_img;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   try:
    new_upc_img.save(sys.stdout, outfileext);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   try:
    new_upc_img.save(sys.stdout.buffer, outfileext);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   new_upc_img.save(outfile, outfileext);
  except:
   return False;
 return True;

def draw_code93(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_code93(upc,None,resize,hideinfo,barheight,barcolor);

def create_code93_from_list(upc,outfile,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return create_code93(upc,outfile,resize,hideinfo,barheight,barcolor);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return create_code93(upc,outfile,resize,hideinfo,barheight,barcolor);
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
   if(isinstance(barcolor[0][0], tuple) or isinstance(barcolor[0][0], list)):
    barcolor_val = barcolor[NumLoop];
   if(isinstance(barcolor[0][0], int)):
    barcolor_val = barcolor;
   retlist.append(create_code93(upc[NumLoop],outfile[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return retlist;

def draw_code93_from_list(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return draw_code93(upc,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return draw_code93(upc,resize,hideinfo,barheight);
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
   if(isinstance(barcolor[0][0], tuple) or isinstance(barcolor[0][0], list)):
    barcolor_val = barcolor[NumLoop];
   if(isinstance(barcolor[0][0], int)):
    barcolor_val = barcolor;
   drawlist.append(draw_code93(upc[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return drawlist;
