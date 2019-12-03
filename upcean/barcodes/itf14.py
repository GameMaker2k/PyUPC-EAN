'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: itf14.py - Last Update: 12/3/2019 Ver. 2.7.19 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, sys, types, upcean.barcodes.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;

def create_itf14_barcode(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
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
 upc_matches = re.findall("([0-9]{2})", upc);
 upc_size_add = len(upc_matches) * 18;
 if(len(upc_matches)<=0):
  return False;
 upc_preimg = Image.new("RGB", (44 + upc_size_add, barheight[0] + 15));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (44 + upc_size_add, barheight[0] + 15)], fill=barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 4, 4, 4, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 5, 4, 5, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 6, 4, 6, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 7, 4, 7, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 8, 4, 8, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 9, 4, 9, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 10, 4, 10, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 11, 4, 11, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 12, 4, 12, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 13, 4, 13, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 14, 4, 14, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 15, 4, 15, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 16, 4, 16, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 17, 4, 17, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 18, 4, 18, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 19, 4, 19, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 20, 4, 20, barheight[0], barcolor[2]);
 NumZero = 0; 
 LineStart = 21; 
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
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]); 
    LineStart += 1; 
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]); 
    LineStart += 1; 
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]); 
    LineStart += 1;
   if(left_barcolor[InnerUPCNum]==0):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]); 
    LineStart += 1;
   if(right_barcolor[InnerUPCNum]==1):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]); 
    LineStart += 1; 
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]); 
    LineStart += 1; 
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]); 
    LineStart += 1;
   if(right_barcolor[InnerUPCNum]==0):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
    LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 upcean.barcodes.prepil.drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, barheight[0], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 43 + upc_size_add, 4, 43 + upc_size_add, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorRectangleAlt(upc_img, 0, 0, 43 + upc_size_add, (barheight[0] + 15) - 11, barcolor[0]);
 upcean.barcodes.prepil.drawColorRectangleAlt(upc_img, 1, 1, 42 + upc_size_add, (barheight[0] + 15) - 12, barcolor[0]);
 upcean.barcodes.prepil.drawColorRectangleAlt(upc_img, 2, 2, 41 + upc_size_add, (barheight[0] + 15) - 13, barcolor[0]);
 upcean.barcodes.prepil.drawColorRectangleAlt(upc_img, 3, 3, 40 + upc_size_add, (barheight[0] + 15) - 14, barcolor[0]);
 new_upc_img = upc_preimg.resize(((44 + upc_size_add) * int(resize), (barheight[0] + 15) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  NumTxtZero = 0; 
  LineTxtStart = 23;
  while (NumTxtZero < len(upc_matches)):
   ArrayDigit = list(upc_matches[NumTxtZero]);
   upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), LineTxtStart + (24 * (int(resize) - 1)), (barheight[0] + (4 * (int(resize))) + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[0], barcolor[1]);
   LineTxtStart += 9 * int(resize);
   upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), LineTxtStart + (24 * (int(resize) - 1)), (barheight[0] + (4 * (int(resize))) + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[1], barcolor[1]);
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

def draw_itf14_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);
