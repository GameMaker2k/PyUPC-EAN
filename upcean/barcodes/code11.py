'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: code11.py - Last Update: 12/3/2019 Ver. 2.7.18 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, sys, types, upcean.barcodes.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;
from upcean.barcodes.prepil import *;

def create_code11_barcode(upc,outfile="./code11.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) < 1): 
  return False;
 if(not re.findall("([0-9\-]+)", upc)):
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
 upc = upc.upper();
 upc_matches = list(upc);
 if(len(upc_matches)<=0):
  return False;
 Code11Array = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "-"};
 Code11Values = dict(zip(Code11Array.values(),Code11Array));
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 upc_print = list(upc_matches);
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>10):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 upc_matches.append(Code11Array[UPC_Sum % 11]);
 upc_reverse = list(upc_matches);
 upc_reverse.reverse();
 UPC_Count = 0; 
 UPC_Weight = 1; 
 UPC_Sum = 0;
 while (UPC_Count < len(upc_reverse)):
  if(UPC_Weight>9):
   UPC_Weight = 1;
  UPC_Sum = UPC_Sum + (UPC_Weight * Code11Values[str(upc_reverse[UPC_Count])]);
  UPC_Count += 1; 
  UPC_Weight += 1;
 upc_matches.append(Code11Array[UPC_Sum % 11]);
 bcsize6 = len(re.findall("([09\-])", "".join(upc_matches)));
 bcsize7 = len(re.findall("([1-8])", "".join(upc_matches)));
 upc_size_add = (bcsize6 * 6) + (bcsize7 * 7) + len(upc_matches) - 1;
 upc_preimg = Image.new("RGB", (34 + upc_size_add, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (34 + upc_size_add, barheight[1] + 9)], fill=barcolor[2]);
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
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
 NumZero = 0; 
 LineStart = 17; 
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 1, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 1, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 1, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="-"):
   left_barcolor = [1, 0, 1, 1, 0, 1];
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
 upcean.barcodes.prepil.drawColorLine(upc_img, 18 + upc_size_add, 4, 18 + upc_size_add, LineSize, barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 19 + upc_size_add, 4, 19 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 20 + upc_size_add, 4, 20 + upc_size_add, LineSize, barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
 new_upc_img = upc_preimg.resize(((34 + upc_size_add) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 16;
  while (NumTxtZero < len(upc_print)):
   upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), LineTxtStart + (16 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1]);
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

def draw_code11_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_code11_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);
