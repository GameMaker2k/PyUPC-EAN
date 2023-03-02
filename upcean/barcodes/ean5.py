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

    FileInfo: ean5.py - Last Update: 2/19/2023 Ver. 2.7.23 RC 1 - Author: cooldude2k 
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, types, upcean.getsfname, upcean.support;
pilsupport = upcean.support.check_for_pil();
if(pilsupport):
 cairosupport = False;
else:
 cairosupport = upcean.support.check_for_cairo();
if(pilsupport):
 from upcean.barcodes.prepil import *;
 from PIL import Image, ImageDraw, ImageFont;
if(cairosupport):
 from upcean.precairo import *;
 import cairo;

def create_ean5_barcode_supplement(upc,outfile="./ean5_supplement.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(barwidth < 1): 
  barwidth = 1;
 if(len(upc)>5 or len(upc)<5): 
  return False;
 upc_matches = re.findall("(\d{5})", upc);
 if(len(upc_matches)<=0): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 try:
  pil_ver = Image.PILLOW_VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  pil_is_pillow = True;
 except AttributeError:
  try:
   pil_ver = Image.VERSION;
   pil_is_pillow = False;
  except AttributeError:
   pil_ver = Image.__version__;
   pil_is_pillow = True;
  except NameError:
   pil_ver = Image.__version__;
   pil_is_pillow = True;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
 except NameError:
  try:
   pil_ver = Image.VERSION;
   pil_is_pillow = False;
  except AttributeError:
   pil_ver = Image.__version__;
   pil_is_pillow = True;
  except NameError:
   pil_ver = Image.__version__;
   pil_is_pillow = True;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
 pil_addon_fix = 0;
 pil_prevercheck = [str(x) for x in pil_ver];
 pil_vercheck = int(pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2]);
 if(pil_is_pillow and pil_vercheck>=210 and pil_vercheck<220):
  pil_addon_fix = int(resize) * 2;
 LeftDigit = list(upc_matches[0]);
 CheckSum = (int(LeftDigit[0]) * 3) + (int(LeftDigit[1]) * 9) + (int(LeftDigit[2]) * 3) + (int(LeftDigit[3]) * 9) + (int(LeftDigit[4]) * 3);
 CheckSum = CheckSum % 10;
 if(pilsupport):
  upc_preimg = Image.new("RGB", ((56 * barwidth), barheight[1] + 9));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((56 * barwidth), barheight[1] + 9)], fill=barcolor[2]);
 if(cairosupport):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 83, barheight[1] + 8);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, 83, barheight[1] + 8);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 upc_array['code'].append( [0, 1, 0, 1, 1] );
 start_barcolor = [0, 1, 0, 1, 1];
 LineStart = 0;
 BarNum = 0;
 start_bc_num_end = len(start_barcolor);
 while(BarNum < start_bc_num_end):
  if(start_barcolor[BarNum]==1):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
  if(start_barcolor[BarNum]==0):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
  LineStart += barwidth;
  BarNum += 1;
 NumZero = 0; 
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext):
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
  upc_array['code'].append( left_barcolor );
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
   LineStart += barwidth;
   BarNum += 1;
   InnerUPCNum += 1;
  if(NumZero < 4):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
   LineStart += barwidth;
   BarNum += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
   LineStart += barwidth;
   BarNum += 1;
  NumZero += 1;
 new_upc_img = upc_preimg.resize(((56 * barwidth) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  drawColorText(upc_img, 10 * int(resize), (7 + (7 * (int(resize) - 1))) * barwidth, (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), LeftDigit[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), (16 + (15 * (int(resize) - 1))) * barwidth, (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), LeftDigit[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), (24 + (24 * (int(resize) - 1))) * barwidth, (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), LeftDigit[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), (32 + (32 * (int(resize) - 1))) * barwidth, (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), LeftDigit[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), (40 + (40 * (int(resize) - 1))) * barwidth, (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), LeftDigit[4], barcolor[1]);
 del(upc_img);
 oldoutfile = upcean.getsfname.get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return new_upc_img;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   try:
    new_upc_img.save(sys.stdout, outfileext);
   except:
    return False;
 if(sys.version[0]>="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
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

def draw_ean5_barcode_supplement(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5_barcode_supplement(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor);

def create_ean5_barcode(upc,outfile="./ean5.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_preimg = Image.new("RGB", (((56 * barwidth) * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize)));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (((56 * barwidth) * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize))], fill=barcolor[2]);
 upc_sup_img = create_ean5_barcode_supplement(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor);
 if(upc_sup_img is None or isinstance(upc_sup_img, bool)):
  return False;
 upc_preimg.paste(upc_sup_img,(8 * int(resize),0));
 del(upc_sup_img);
 del(upc_img);
 oldoutfile = upcean.getsfname.get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return new_upc_img;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   try:
    if(pilsupport):
     new_upc_img.save(sys.stdout, outfileext);
    if(cairosupport):
     new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]>="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   try:
    if(pilsupport):
     new_upc_img.save(sys.stdout.buffer, outfileext);
    if(cairosupport):
     new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   if(pilsupport):
    new_upc_img.save(outfile, outfileext);
   if(cairosupport):
    new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_ean5_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor);
