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

    $FileInfo: msi.py - Last Update: 3/9/2023 Ver. 2.7.26 RC 1 - Author: cooldude2k $
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

def create_msi_barcode(upc,outfile="./msi.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
 if(barwidth < 1): 
  barwidth = 1;
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9]+)", upc)):
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
 upc_print = list(upc_matches);
 if(len(upc) % 2==0):
  PreChck1 = list(str(int("".join(upc_matches[1:][::2])) * 2));
  PreChck2 = upc_matches[0:][::2];
 else:
  PreChck1 = list(str(int("".join(upc_matches[0:][::2])) * 2));
  PreChck2 = upc_matches[1:][::2];
 PreCount = 0;
 UPC_Sum = 0;
 while (PreCount<=len(PreChck1)-1):
  UPC_Sum = UPC_Sum + int(PreChck1[PreCount]);
  PreCount += 1;
 PreCount = 0;
 while (PreCount<=len(PreChck2)-1):
  UPC_Sum = UPC_Sum + int(PreChck2[PreCount]);
  PreCount += 1;
 upc_matches.append(str(10 - (UPC_Sum % 10)));
 upc_size_add = (len(upc_matches) * 12) * barwidth;
 if(pilsupport and imageoutlib=="pillow"):
  upc_preimg = Image.new("RGB", ((34 * barwidth) + upc_size_add, barheight[1] + 9));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((34 * barwidth) + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
 if(cairosupport and imageoutlib=="cairo"):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (34 * barwidth) + upc_size_add, barheight[1] + 8);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (34 * barwidth) + upc_size_add, barheight[1] + 8);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 start_barcolor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0];
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
  left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0];
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
 end_barcolor = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_bc_num_end = len(end_barcolor);
 while(end_bc_num < end_bc_num_end):
  if(end_barcolor[end_bc_num]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[0], imageoutlib);
  if(end_barcolor[end_bc_num]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth, barcolor[2], imageoutlib);
  end_bc_num += 1;
  LineStart += barwidth;
  BarNum += 1;
 if(pilsupport and imageoutlib=="pillow"):
  new_upc_img = upc_preimg.resize((((34 * barwidth) + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
  del(upc_img);
  del(upc_preimg);
  upc_img = ImageDraw.Draw(new_upc_img);
 if(cairosupport and imageoutlib=="cairo"):
  upc_imgpat = cairo.SurfacePattern(upc_preimg);
  scaler = cairo.Matrix();
  scaler.scale(1/int(resize),1/int(resize));
  upc_imgpat.set_matrix(scaler);
  upc_imgpat.set_filter(cairo.FILTER_NEAREST);
  new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((34 * barwidth) + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize));
  new_upc_img = cairo.Context(new_upc_preimg);
  new_upc_img.set_source(upc_imgpat);
  new_upc_img.paint();
  upc_img = new_upc_img;
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 16;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10 * int(resize), (LineTxtStart + (16 * (int(resize) - 1))) * barwidth, cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib);
   LineTxtStart += 12 * int(resize);
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

def draw_msi_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 return create_msi_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
