'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: code128.py - Last Update: 12/3/2019 Ver. 2.7.19 RC 1 - Author: cooldude2k $
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

def create_code128_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9]+)", upc)):
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
 upc = upc.lower();
 upc_matches = re.findall("[0-9a-f]{2}", upc);
 upc_print = list(upc_matches);
 upc_size_add = len(upc_matches) * 20;
 if(pilsupport):
  upc_preimg = Image.new("RGB", (34 + upc_size_add, barheight[1] + 9));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), (34 + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
 if(cairosupport):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 34 + upc_size_add, barheight[1] + 8);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, 34 + upc_size_add, barheight[1] + 8);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
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
 drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[2]);
 drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
 drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[2]);
 drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
 drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
 NumZero = 0; 
 LineStart = 14; 
 cur_set = 0;
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="00"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="01"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="02"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="03"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="04"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="05"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="06"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="07"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="08"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="09"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0a"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="0b"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="0c"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="0d"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="0e"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="0f"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="10"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="11"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="12"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="13"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="14"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="15"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="16"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="17"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="18"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="19"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="1a"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="1b"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="1c"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="1d"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="1e"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="1f"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="20"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="21"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="22"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="23"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="24"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="25"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="26"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="27"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="28"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="29"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="2a"):
   left_barcolor =  [1, 0, 1, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="2b"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="2c"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="2d"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="2e"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="2f"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="30"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="31"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="32"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="33"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="34"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="35"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="36"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="37"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="38"):
   left_barcolor =  [1, 1, 1, 0, 0, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="39"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="3a"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="3b"):
   left_barcolor =  [1, 1, 1, 0, 0, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="3c"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="3d"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="3e"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="3f"):
   left_barcolor =  [1, 0, 1, 0, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="40"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="41"):
   left_barcolor =  [1, 0, 0, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="42"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="43"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="44"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="45"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="46"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="47"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="48"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="49"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="4a"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="4b"):
   left_barcolor =  [1, 1, 0, 0, 0, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="4c"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="4d"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="4e"):
   left_barcolor =  [1, 1, 0, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="4f"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="50"):
   left_barcolor =  [1, 0, 1, 0, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="51"):
   left_barcolor =  [1, 0, 0, 1, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="52"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 1, 1, 1, 1];
  if(upc_matches[NumZero]=="53"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="54"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="55"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="56"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="57"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="58"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="59"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 1, 1, 1, 1];
  if(upc_matches[NumZero]=="5a"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="5b"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="5c"):
   left_barcolor =  [1, 0, 1, 0, 1, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="5d"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 1, 1, 1, 1];
  if(upc_matches[NumZero]=="5e"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 1, 1, 1, 1];
  if(upc_matches[NumZero]=="5f"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="60"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="61"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="62"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 0, 0, 1];
   old_cur_set = cur_set;
   if(cur_set==0):
    cur_set = 1;
   if(cur_set==1):
    cur_set = 0;
   cur_set = old_cur_set;
  if(upc_matches[NumZero]=="63"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 1, 1, 1, 1];
   if(cur_set==0 or cur_set==1):
    cur_set = 2;
  if(upc_matches[NumZero]=="64"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1];
   if(cur_set==0 or cur_set==2):
    cur_set = 1;
  if(upc_matches[NumZero]=="65"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 1, 1, 1, 1];
   if(cur_set==1 or cur_set==2):
    cur_set = 0;
  if(upc_matches[NumZero]=="66"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="67"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 0, 1, 0];
   cur_set = 0;
  if(upc_matches[NumZero]=="68"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 1, 0, 0, 0];
   cur_set = 1;
  if(upc_matches[NumZero]=="69"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 1, 1, 1, 0];
   cur_set = 2;
  if(upc_matches[NumZero]=="6a"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="6b"):
   left_barcolor =  [1, 1, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="6c"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
 drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
 new_upc_img = upc_preimg.resize(((34 + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 16;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10 * int(resize), LineTxtStart + (16 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1]);
   LineTxtStart += 12 * int(resize);
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

def draw_code128_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_code128_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);
