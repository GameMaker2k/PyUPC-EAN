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

    $FileInfo: code93.py - Last Update: 3/9/2023 Ver. 2.7.26 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, types, upcean.barcodes.getsfname, upcean.support;
pilsupport = upcean.support.check_for_pil();
cairosupport = upcean.support.check_for_cairo();
from upcean.barcodes.predraw import *;
if(pilsupport):
 import upcean.barcodes.prepil;
if(cairosupport):
 import upcean.barcodes.precairo;

def create_code93_barcode(upc,outfile="./code93.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 imageoutlib = imageoutlib.lower();
 if(not pilsupport and imageoutlib=="pillow"):
  imageoutlib = "cairo";
 if(not cairosupport and imageoutlib=="cairo"):
  imageoutlib = "pillow";
 if(imageoutlib!="pillow" and imageoutlib!="cairo"):
  imageoutlib = "pillow";
 if(not pilsupport and not cairosupport):
  return False;
 oldoutfile = upcean.barcodes.getsfname.get_save_filename(outfile, imageoutlib);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(len(upc) < 1): 
  return False;
 if(barwidth < 1): 
  barwidth = 1;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(pilsupport and imageoutlib=="pillow"):
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
  cairo_addon_fix = 0;
  pil_prevercheck = [str(x) for x in pil_ver];
  pil_vercheck = int(pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2]);
  if(pil_is_pillow and pil_vercheck>=210 and pil_vercheck<220):
   pil_addon_fix = int(resize) * 2;
   cairo_addon_fix = 0;
 elif(pilsupport and imageoutlib=="pillow"):
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
 elif(pilsupport and imageoutlib=="cairo"):
  pil_addon_fix = 0;
  cairo_addon_fix = (8 * (int(resize) ) );
 else:
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
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
 upc_size_add = (len(upc_matches) * 9) * barwidth;
 if(pilsupport and imageoutlib=="pillow"):
  upc_preimg = Image.new("RGB", ((37 * barwidth) + upc_size_add, barheight[1] + 9));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((37 * barwidth) + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
 if(cairosupport and imageoutlib=="cairo"):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (37 * barwidth) + upc_size_add, barheight[1] + 8);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (37 * barwidth) + upc_size_add, barheight[1] + 8);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 start_barcolor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0];
 LineStart = 0;
 BarNum = 0;
 start_bc_num_end = len(start_barcolor);
 while(BarNum < start_bc_num_end):
  if(start_barcolor[BarNum]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0], imageoutlib);
  if(start_barcolor[BarNum]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2], imageoutlib);
  LineStart += barwidth;
  BarNum += 1;
 NumZero = 0; 
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
  ''' Unused barcodes
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0];
  '''
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0], imageoutlib);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2], imageoutlib);
   LineStart += barwidth;
   BarNum += 1;
   InnerUPCNum += 1;
  NumZero += 1; 
 end_barcolor = [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_b
 while(end_bc_num < end_bc_num_end):
  if(end_barcolor[end_bc_num]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0], imageoutlib);
  if(end_barcolor[end_bc_num]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2], imageoutlib);
  end_bc_num += 1;
  LineStart += barwidth;
  BarNum += 1;
 if(pilsupport and imageoutlib=="pillow"):
  new_upc_img = upc_preimg.resize((((37 * barwidth) + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
  del(upc_img);
  del(upc_preimg);
  upc_img = ImageDraw.Draw(new_upc_img);
 if(cairosupport and imageoutlib=="cairo"):
  upc_imgpat = cairo.SurfacePattern(upc_preimg);
  scaler = cairo.Matrix();
  scaler.scale(1/int(resize),1/int(resize));
  upc_imgpat.set_matrix(scaler);
  upc_imgpat.set_filter(cairo.FILTER_NEAREST);
  new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((37 * barwidth) + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize));
  new_upc_img = cairo.Context(new_upc_preimg);
  new_upc_img.set_source(upc_imgpat);
  new_upc_img.paint();
  upc_img = new_upc_img;
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 18;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10 * int(resize), (LineTxtStart + (19 * (int(resize) - 1))) * barwidth, cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib);
   LineTxtStart += 9 * int(resize);
   NumTxtZero += 1;
 del(upc_img);
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  if(pilsupport and imageoutlib=="pillow"):
   return new_upc_img;
  if(cairosupport and imageoutlib=="cairo"):
   return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      os.write(sys.stdout.fileno(), new_upc_img.tobytes());
     else:
      new_upc_img.save(sys.stdout, outfileext);
    if(cairosupport and imageoutlib=="cairo"):
     if(outfileext=="BYTES"):
      os.write(sys.stdout.fileno(), new_upc_preimg.get_data().tobytes());
     else:
      new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]>="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      os.write(sys.stdout.buffer.fileno(), new_upc_img.tobytes());
     else:
      new_upc_img.save(sys.stdout.buffer, outfileext);
    if(cairosupport and imageoutlib=="cairo"):
     if(outfileext=="BYTES"):
      os.write(sys.stdout.buffer.fileno(), new_upc_preimg.get_data().tobytes());
     else:
      new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   if(pilsupport and imageoutlib=="pillow"):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_img.tobytes());
    else:
     new_upc_img.save(outfile, outfileext);
   if(cairosupport and imageoutlib=="cairo"):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_preimg.get_data().tobytes());
    else:
     new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_code93_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 return create_code93_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
