'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: codabar.py - Last Update: 12/3/2019 Ver. 2.7.18 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, types, upcean.barcodes.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;

def create_codabar_barcode(upc,outfile="./codabar.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 upc = upc.upper();
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) < 1): 
  return False;
 if(not re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 try:
  pil_ver = Image.PILLOW_VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  pil_is_pillow = True;
 except AttributeError:
  pil_ver = Image.VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  pil_is_pillow = False;
 except NameError:
  pil_ver = Image.VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  pil_is_pillow = False;
 pil_addon_fix = 0;
 pil_prevercheck = [str(x) for x in pil_ver];
 pil_vercheck = int(pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2]);
 if(pil_is_pillow and pil_vercheck>=210 and pil_vercheck<220):
  pil_addon_fix = int(resize) * 2;
 pre_upc_matches = upc_matches = re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc);
 pre_upc_matches = pre_upc_matches[0];
 upc_matches = list(pre_upc_matches[1]);
 bcsize9 = len(re.findall("([0-9\-\$])", "".join(upc_matches)));
 bcsize10 = len(re.findall("([\:\/\.])", "".join(upc_matches)));
 bcsize12 = len(re.findall("([\+])", "".join(upc_matches)));
 upc_size_add = (bcsize9 * 9) + (bcsize10 * 10) + (bcsize12 * 12) + len(upc_matches) - 1;
 upc_preimg = Image.new("RGB", (40 + upc_size_add, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (40 + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 if(pre_upc_matches[0]=="A" or pre_upc_matches[0]=="T"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="B" or pre_upc_matches[0]=="N"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="C" or pre_upc_matches[0]=="*"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="D" or pre_upc_matches[0]=="E"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 NumZero = 0; 
 LineStart = 20; 
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 0, 1, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 1, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="-"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="$"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]==":"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="/"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="."):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="+"):
   left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
  LineStart += 1;
  NumZero += 1; 
 if(pre_upc_matches[2]=="A" or pre_upc_matches[2]=="T"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="B" or pre_upc_matches[2]=="N"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="C" or pre_upc_matches[2]=="*"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="D" or pre_upc_matches[2]=="E"):
  upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  upcean.barcodes.prepil.drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 new_upc_img = upc_preimg.resize(((40 + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 20;
  while (NumTxtZero < len(upc_matches)):
   upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), LineTxtStart + (16 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_matches[NumTxtZero], barcolor[0]);
   LineTxtStart += 11 * int(resize);
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

def draw_codabar_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_codabar_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);
