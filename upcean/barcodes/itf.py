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

    $FileInfo: itf.py - Last Update: 2/19/2023 Ver. 2.7.23 RC 1 - Author: cooldude2k $
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

def create_itf_barcode(upc,outfile="./itf.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) % 2):
  return False;
 if(len(upc) < 6):
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
 upc_matches = re.findall("([0-9]{2})", upc);
 upc_size_add = len(upc_matches) * 18;
 if(len(upc_matches)<=0):
  return False;
 if(pilsupport):
  upc_preimg = Image.new("RGB", (39 + upc_size_add, barheight[0] + 15));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), (39 + upc_size_add, barheight[0] + 15)], fill=barcolor[2]);
 if(cairosupport):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 39 + upc_size_add, barheight[0] + 14);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, 39 + upc_size_add, barheight[0] + 14);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 start_barcolor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0];
 start_bc_num = 0;
 start_bc_num_end = len(start_barcolor);
 while(start_bc_num < start_bc_num_end):
  if(start_barcolor[start_bc_num]==1):
   drawColorLine(upc_img, start_bc_num, 4, start_bc_num, LineSize, barwidth, barcolor[0]);
  if(start_barcolor[start_bc_num]==0):
   drawColorLine(upc_img, start_bc_num, 4, start_bc_num, LineSize, barwidth, barcolor[2]);
  start_bc_num = 1 + start_bc_num;
 NumZero = 0; 
 LineStart = 17; 
 LineSize = barheight[0];
 while (NumZero < len(upc_matches)):
  ArrayDigit = list(upc_matches[NumZero]);
  left_barcolor = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[0])==0):
   left_barcolor = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[0])==1):
   left_barcolor = [1, 0, 0, 0, 1];
  if(int(ArrayDigit[0])==2):
   left_barcolor = [0, 1, 0, 0, 1];
  if(int(ArrayDigit[0])==3):
   left_barcolor = [1, 1, 0, 0, 0];
  if(int(ArrayDigit[0])==4):
   left_barcolor = [0, 0, 1, 0, 1];
  if(int(ArrayDigit[0])==5):
   left_barcolor = [1, 0, 1, 0, 0];
  if(int(ArrayDigit[0])==6):
   left_barcolor = [0, 1, 1, 0, 0];
  if(int(ArrayDigit[0])==7):
   left_barcolor = [0, 0, 0, 1, 1];
  if(int(ArrayDigit[0])==8):
   left_barcolor = [1, 0, 0, 1, 0];
  if(int(ArrayDigit[0])==9):
   left_barcolor = [0, 1, 0, 1, 0];
  right_barcolor = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[1])==0):
   right_barcolor = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[1])==1):
   right_barcolor = [1, 0, 0, 0, 1];
  if(int(ArrayDigit[1])==2):
   right_barcolor = [0, 1, 0, 0, 1];
  if(int(ArrayDigit[1])==3):
   right_barcolor = [1, 1, 0, 0, 0];
  if(int(ArrayDigit[1])==4):
   right_barcolor = [0, 0, 1, 0, 1];
  if(int(ArrayDigit[1])==5):
   right_barcolor = [1, 0, 1, 0, 0];
  if(int(ArrayDigit[1])==6):
   right_barcolor = [0, 1, 1, 0, 0];
  if(int(ArrayDigit[1])==7):
   right_barcolor = [0, 0, 0, 1, 1];
  if(int(ArrayDigit[1])==8):
   right_barcolor = [1, 0, 0, 1, 0];
  if(int(ArrayDigit[1])==9):
   right_barcolor = [0, 1, 0, 1, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0]); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0]); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0]); 
    LineStart += 1;
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0]); 
    LineStart += 1;
   if(right_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2]); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2]); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2]); 
    LineStart += 1;
   if(right_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2]);
    LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 end_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_bc_num_end = len(end_barcolor);
 end_bc_line_start = 17;
 while(end_bc_num < end_bc_num_end):
  if(end_barcolor[end_bc_num]==1):
   drawColorLine(upc_img, end_bc_line_start + upc_size_add, 4, end_bc_line_start + upc_size_add, LineSize, barwidth, barcolor[0]);
  if(end_barcolor[end_bc_num]==0):
   drawColorLine(upc_img, end_bc_line_start + upc_size_add, 4, end_bc_line_start + upc_size_add, LineSize, barwidth, barcolor[2]);
  end_bc_num = 1 + end_bc_num;
  end_bc_line_start = 1 + end_bc_line_start;
 new_upc_img = upc_preimg.resize(((39 + upc_size_add) * int(resize), (barheight[0] + 15) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 20;
  while (NumTxtZero < len(upc_matches)):
   ArrayDigit = list(upc_matches[NumTxtZero]);
   drawColorText(upc_img, 10 * int(resize), LineTxtStart + (21 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[0], barcolor[1]);
   LineTxtStart += 9 * int(resize);
   drawColorText(upc_img, 10 * int(resize), LineTxtStart + (21 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[1], barcolor[1]);
   LineTxtStart += 9 * int(resize);
   NumTxtZero += 1;
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

def draw_itf_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor);
