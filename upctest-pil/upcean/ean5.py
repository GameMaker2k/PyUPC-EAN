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

    FileInfo: ean5.py - Last Update: 08/03/2013 Ver. 2.4.3 RC 1 - Author: cooldude2k 
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, types, upcean.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;
from upcean.getsfname import *;

def create_ean5_supplement(upc,outfile="./ean5_supplement.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc)>5 or len(upc)<5): 
  return False;
 upc_matches = re.findall("(\d{5})", upc);
 if(len(upc_matches)<=0): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 LeftDigit = list(upc_matches[0]);
 CheckSum = (int(LeftDigit[0]) * 3) + (int(LeftDigit[1]) * 9) + (int(LeftDigit[2]) * 3) + (int(LeftDigit[3]) * 9) + (int(LeftDigit[4]) * 3);
 CheckSum = CheckSum % 10;
 upc_preimg = Image.new("RGB", (56, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (56, barheight[1] + 9)], fill=barcolor[2]);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 10, 0, LineSize, barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, LineSize, barcolor[0]);
 drawColorLine(upc_img, 2, 10, 2, LineSize, barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, LineSize, barcolor[0]);
 drawColorLine(upc_img, 4, 10, 4, LineSize, barcolor[0]);
 NumZero = 0; 
 LineStart = 5;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_barcolor_l = [0, 0, 0, 0, 0, 0, 0]; 
  left_barcolor_g = [1, 1, 1, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==0): 
   left_barcolor_l = [0, 0, 0, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_barcolor_l = [0, 0, 1, 1, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_barcolor_l = [0, 0, 1, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_barcolor_l = [0, 1, 1, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_barcolor_l = [0, 1, 0, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_barcolor_l = [0, 1, 1, 0, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_barcolor_l = [0, 1, 0, 1, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_barcolor_l = [0, 1, 1, 1, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_barcolor_l = [0, 1, 1, 0, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9): 
   left_barcolor_l = [0, 0, 0, 1, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 0, 1, 1, 1];
  left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==0 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==0 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==1 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==1 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==3 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==4 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==4 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==5 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==5 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==6 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==7 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==7 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==8 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==9 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==9 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==4):
   left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero < 4):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   LineStart += 1;
  NumZero += 1;
 new_upc_img = upc_preimg.resize((56 * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(hidetext==False):
  drawColorText(upc_img, 10 * int(resize), 7 + (7 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), LeftDigit[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 16 + (15 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), LeftDigit[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 24 + (24 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), LeftDigit[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 32 + (32 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), LeftDigit[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 40 + (40 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), LeftDigit[4], barcolor[1]);
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
   new_upc_img.save(sys.stdout, outfileext);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   new_upc_img.save(sys.stdout.buffer, outfileext);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  new_upc_img.save(outfile, outfileext);
 return True;

def draw_ean5_supplement(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5_supplement(upc,None,resize,hideinfo,barheight,barcolor);

def create_ean5(upc,outfile="./ean5.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_preimg = Image.new("RGB", ((56 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize)));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), ((56 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize))], fill=barcolor[2]);
 upc_sup_img = draw_ean5_supplement(upc,resize,hideinfo,barheight,barcolor);
 if(upc_sup_img is None or isinstance(upc_sup_img, bool)):
  return False;
 upc_preimg.paste(upc_sup_img,(8 * int(resize),0));
 del(upc_sup_img);
 del(upc_img);
 oldoutfile = get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout, outfileext);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout.buffer, outfileext);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  upc_preimg.save(outfile, outfileext);
 return True;

def draw_ean5(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5(upc,None,resize,hideinfo,barheight,barcolor);

def create_ean5_from_list(upc,outfile,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return create_ean5(upc,outfile,resize,hideinfo,barheight,barcolor);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return create_ean5(upc,outfile,resize,hideinfo,barheight,barcolor);
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
   retlist.append(create_ean5(upc[NumLoop],outfile[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return retlist;

def draw_ean5_from_list(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return draw_ean5(upc,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return draw_ean5(upc,resize,hideinfo,barheight);
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
   drawlist.append(draw_ean5(upc[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return drawlist;
