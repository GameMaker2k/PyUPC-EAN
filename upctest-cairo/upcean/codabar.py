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

    $FileInfo: codabar.py - Last Update: 04/25/2013 Ver. 2.4.0 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, types, upcean.prepil;
import upcean.ean2, upcean.ean5;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;

def create_codabar(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
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
 pre_upc_matches = upc_matches = re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc);
 pre_upc_matches = pre_upc_matches[0];
 upc_matches = list(pre_upc_matches[1]);
 bcsize9 = len(re.findall("([0-9\-\$])", "".join(upc_matches)));
 bcsize10 = len(re.findall("([\:\/\.])", "".join(upc_matches)));
 bcsize12 = len(re.findall("([\+])", "".join(upc_matches)));
 upc_size_add = (bcsize9 * 9) + (bcsize10 * 10) + (bcsize12 * 12) + len(upc_matches) - 1;
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 40 + upc_size_add, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 40 + upc_size_add, barheight[1] + 8);
 upc_img.set_source_rgb(256, 256, 256);
 upc_img.fill();
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  NumTxtZero = 0; 
  LineTxtStart = 20;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10, LineTxtStart, barheight[1] + 3, upc_matches[NumTxtZero], text_color);
   LineTxtStart += 11;
   NumTxtZero += 1;
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 if(pre_upc_matches[0]=="A" or pre_upc_matches[0]=="T"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, alt_text_color);
  drawColorLine(upc_img, 1, 4, 1, LineSize, alt_text_color);
  drawColorLine(upc_img, 2, 4, 2, LineSize, alt_text_color);
  drawColorLine(upc_img, 3, 4, 3, LineSize, alt_text_color);
  drawColorLine(upc_img, 4, 4, 4, LineSize, alt_text_color);
  drawColorLine(upc_img, 5, 4, 5, LineSize, alt_text_color);
  drawColorLine(upc_img, 6, 4, 6, LineSize, alt_text_color);
  drawColorLine(upc_img, 7, 4, 7, LineSize, alt_text_color);
  drawColorLine(upc_img, 8, 4, 8, LineSize, alt_text_color);
  drawColorLine(upc_img, 9, 4, 9, LineSize, text_color);
  drawColorLine(upc_img, 10, 4, 10, LineSize, alt_text_color);
  drawColorLine(upc_img, 11, 4, 11, LineSize, text_color);
  drawColorLine(upc_img, 12, 4, 12, LineSize, text_color);
  drawColorLine(upc_img, 13, 4, 13, LineSize, alt_text_color);
  drawColorLine(upc_img, 14, 4, 14, LineSize, alt_text_color);
  drawColorLine(upc_img, 15, 4, 15, LineSize, text_color);
  drawColorLine(upc_img, 16, 4, 16, LineSize, alt_text_color);
  drawColorLine(upc_img, 17, 4, 17, LineSize, alt_text_color);
  drawColorLine(upc_img, 18, 4, 18, LineSize, text_color);
  drawColorLine(upc_img, 19, 4, 19, LineSize, alt_text_color);
 if(pre_upc_matches[0]=="B" or pre_upc_matches[0]=="N"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, alt_text_color);
  drawColorLine(upc_img, 1, 4, 1, LineSize, alt_text_color);
  drawColorLine(upc_img, 2, 4, 2, LineSize, alt_text_color);
  drawColorLine(upc_img, 3, 4, 3, LineSize, alt_text_color);
  drawColorLine(upc_img, 4, 4, 4, LineSize, alt_text_color);
  drawColorLine(upc_img, 5, 4, 5, LineSize, alt_text_color);
  drawColorLine(upc_img, 6, 4, 6, LineSize, alt_text_color);
  drawColorLine(upc_img, 7, 4, 7, LineSize, alt_text_color);
  drawColorLine(upc_img, 8, 4, 8, LineSize, alt_text_color);
  drawColorLine(upc_img, 9, 4, 9, LineSize, text_color);
  drawColorLine(upc_img, 10, 4, 10, LineSize, alt_text_color);
  drawColorLine(upc_img, 11, 4, 11, LineSize, text_color);
  drawColorLine(upc_img, 12, 4, 12, LineSize, alt_text_color);
  drawColorLine(upc_img, 13, 4, 13, LineSize, alt_text_color);
  drawColorLine(upc_img, 14, 4, 14, LineSize, text_color);
  drawColorLine(upc_img, 15, 4, 15, LineSize, alt_text_color);
  drawColorLine(upc_img, 16, 4, 16, LineSize, alt_text_color);
  drawColorLine(upc_img, 17, 4, 17, LineSize, text_color);
  drawColorLine(upc_img, 18, 4, 18, LineSize, text_color);
  drawColorLine(upc_img, 19, 4, 19, LineSize, alt_text_color);
 if(pre_upc_matches[0]=="C" or pre_upc_matches[0]=="*"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, alt_text_color);
  drawColorLine(upc_img, 1, 4, 1, LineSize, alt_text_color);
  drawColorLine(upc_img, 2, 4, 2, LineSize, alt_text_color);
  drawColorLine(upc_img, 3, 4, 3, LineSize, alt_text_color);
  drawColorLine(upc_img, 4, 4, 4, LineSize, alt_text_color);
  drawColorLine(upc_img, 5, 4, 5, LineSize, alt_text_color);
  drawColorLine(upc_img, 6, 4, 6, LineSize, alt_text_color);
  drawColorLine(upc_img, 7, 4, 7, LineSize, alt_text_color);
  drawColorLine(upc_img, 8, 4, 8, LineSize, alt_text_color);
  drawColorLine(upc_img, 9, 4, 9, LineSize, text_color);
  drawColorLine(upc_img, 10, 4, 10, LineSize, alt_text_color);
  drawColorLine(upc_img, 11, 4, 11, LineSize, alt_text_color);
  drawColorLine(upc_img, 12, 4, 12, LineSize, text_color);
  drawColorLine(upc_img, 13, 4, 13, LineSize, alt_text_color);
  drawColorLine(upc_img, 14, 4, 14, LineSize, alt_text_color);
  drawColorLine(upc_img, 15, 4, 15, LineSize, text_color);
  drawColorLine(upc_img, 16, 4, 16, LineSize, alt_text_color);
  drawColorLine(upc_img, 17, 4, 17, LineSize, text_color);
  drawColorLine(upc_img, 18, 4, 18, LineSize, text_color);
  drawColorLine(upc_img, 19, 4, 19, LineSize, alt_text_color);
 if(pre_upc_matches[0]=="D" or pre_upc_matches[0]=="E"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, alt_text_color);
  drawColorLine(upc_img, 1, 4, 1, LineSize, alt_text_color);
  drawColorLine(upc_img, 2, 4, 2, LineSize, alt_text_color);
  drawColorLine(upc_img, 3, 4, 3, LineSize, alt_text_color);
  drawColorLine(upc_img, 4, 4, 4, LineSize, alt_text_color);
  drawColorLine(upc_img, 5, 4, 5, LineSize, alt_text_color);
  drawColorLine(upc_img, 6, 4, 6, LineSize, alt_text_color);
  drawColorLine(upc_img, 7, 4, 7, LineSize, alt_text_color);
  drawColorLine(upc_img, 8, 4, 8, LineSize, alt_text_color);
  drawColorLine(upc_img, 9, 4, 9, LineSize, text_color);
  drawColorLine(upc_img, 10, 4, 10, LineSize, alt_text_color);
  drawColorLine(upc_img, 11, 4, 11, LineSize, text_color);
  drawColorLine(upc_img, 12, 4, 12, LineSize, alt_text_color);
  drawColorLine(upc_img, 13, 4, 13, LineSize, alt_text_color);
  drawColorLine(upc_img, 14, 4, 14, LineSize, text_color);
  drawColorLine(upc_img, 15, 4, 15, LineSize, text_color);
  drawColorLine(upc_img, 16, 4, 16, LineSize, alt_text_color);
  drawColorLine(upc_img, 17, 4, 17, LineSize, alt_text_color);
  drawColorLine(upc_img, 18, 4, 18, LineSize, text_color);
  drawColorLine(upc_img, 19, 4, 19, LineSize, alt_text_color);
 NumZero = 0; 
 LineStart = 20; 
 while (NumZero < len(upc_matches)):
  left_text_color = [1, 0, 1, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="0"):
   left_text_color = [1, 0, 1, 0, 1, 0, 0, 1, 1];
  if(upc_matches[NumZero]=="1"):
   left_text_color = [1, 0, 1, 0, 1, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="2"):
   left_text_color = [1, 0, 1, 0, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="3"):
   left_text_color = [1, 1, 0, 0, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="4"):
   left_text_color = [1, 0, 1, 1, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="5"):
   left_text_color = [1, 1, 0, 1, 0, 1, 0, 0, 1];
  if(upc_matches[NumZero]=="6"):
   left_text_color = [1, 0, 0, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="7"):
   left_text_color = [1, 0, 0, 1, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="8"):
   left_text_color = [1, 0, 0, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="9"):
   left_text_color = [1, 1, 0, 1, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="-"):
   left_text_color = [1, 0, 1, 0, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="$"):
   left_text_color = [1, 0, 1, 1, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]==":"):
   left_text_color = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="/"):
   left_text_color = [1, 1, 0, 1, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="."):
   left_text_color = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="+"):
   left_text_color = [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color);
  LineStart += 1;
  NumZero += 1; 
 if(pre_upc_matches[2]=="A" or pre_upc_matches[2]=="T"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, alt_text_color);
 if(pre_upc_matches[2]=="B" or pre_upc_matches[2]=="N"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, alt_text_color);
 if(pre_upc_matches[2]=="C" or pre_upc_matches[2]=="*"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, alt_text_color);
 if(pre_upc_matches[2]=="D" or pre_upc_matches[2]=="E"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, text_color);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, alt_text_color);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, alt_text_color);
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (40 + upc_size_add) * int(resize), (barheight[1] + 8) * int(resize));
 new_upc_img = cairo.Context(new_upc_preimg);
 new_upc_img.set_source(upc_imgpat);
 new_upc_img.paint();
 del(upc_preimg);
 if(outfile is None or isinstance(outfile, bool)):
  return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   new_upc_preimg.write_to_png(sys.stdout);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   new_upc_preimg.write_to_png(sys.stdout.buffer);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  new_upc_preimg.write_to_png(outfile);
 return True;

def draw_codabar(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_codabar(upc,None,resize,hideinfo,barheight);

def create_codabar_from_list(upc,outfile,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return create_codabar(upc,outfile,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return create_codabar(upc,outfile,resize,hideinfo,barheight);
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
   retlist.append(create_codabar(upc[NumLoop],outfile[NumLoop],resize_val,hideinfo_val,barheight_val));
   NumLoop = NumLoop + 1;
 return retlist;

def draw_codabar_from_list(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return draw_codabar(upc,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return draw_codabar(upc,resize,hideinfo,barheight);
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
   drawlist.append(draw_codabar(upc[NumLoop],resize_val,hideinfo_val,barheight_val));
   NumLoop = NumLoop + 1;
 return drawlist;
