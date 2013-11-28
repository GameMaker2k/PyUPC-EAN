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

    $FileInfo: codabar.py - Last Update: 11/27/2013 Ver. 2.5.4 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import cairo, re, sys, types, upcean.precairo;
from upcean.precairo import *;

def create_codabar(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
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
 upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
 upc_img.fill();
 if(hidetext==False):
  NumTxtZero = 0; 
  LineTxtStart = 20;
  while (NumTxtZero < len(upc_print)):
   drawColorText(upc_img, 10, LineTxtStart, (barheight[1] + 3) + textxy[1], upc_matches[NumTxtZero], barcolor[1]);
   LineTxtStart += 11;
   NumTxtZero += 1;
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 if(pre_upc_matches[0]=="A" or pre_upc_matches[0]=="T"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[0]);
  drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[2]);
  drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[2]);
  drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="B" or pre_upc_matches[0]=="N"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
  drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[0]);
  drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[2]);
  drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[0]);
  drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="C" or pre_upc_matches[0]=="*"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[2]);
  drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[0]);
  drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[2]);
  drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[0]);
  drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
 if(pre_upc_matches[0]=="D" or pre_upc_matches[0]=="E"):
  drawColorLine(upc_img, 0, 4, 0, LineSize, barcolor[2]);
  drawColorLine(upc_img, 1, 4, 1, LineSize, barcolor[2]);
  drawColorLine(upc_img, 2, 4, 2, LineSize, barcolor[2]);
  drawColorLine(upc_img, 3, 4, 3, LineSize, barcolor[2]);
  drawColorLine(upc_img, 4, 4, 4, LineSize, barcolor[2]);
  drawColorLine(upc_img, 5, 4, 5, LineSize, barcolor[2]);
  drawColorLine(upc_img, 6, 4, 6, LineSize, barcolor[2]);
  drawColorLine(upc_img, 7, 4, 7, LineSize, barcolor[2]);
  drawColorLine(upc_img, 8, 4, 8, LineSize, barcolor[2]);
  drawColorLine(upc_img, 9, 4, 9, LineSize, barcolor[0]);
  drawColorLine(upc_img, 10, 4, 10, LineSize, barcolor[2]);
  drawColorLine(upc_img, 11, 4, 11, LineSize, barcolor[0]);
  drawColorLine(upc_img, 12, 4, 12, LineSize, barcolor[2]);
  drawColorLine(upc_img, 13, 4, 13, LineSize, barcolor[2]);
  drawColorLine(upc_img, 14, 4, 14, LineSize, barcolor[0]);
  drawColorLine(upc_img, 15, 4, 15, LineSize, barcolor[0]);
  drawColorLine(upc_img, 16, 4, 16, LineSize, barcolor[2]);
  drawColorLine(upc_img, 17, 4, 17, LineSize, barcolor[2]);
  drawColorLine(upc_img, 18, 4, 18, LineSize, barcolor[0]);
  drawColorLine(upc_img, 19, 4, 19, LineSize, barcolor[2]);
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
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barcolor[2]);
  LineStart += 1;
  NumZero += 1; 
 if(pre_upc_matches[2]=="A" or pre_upc_matches[2]=="T"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="B" or pre_upc_matches[2]=="N"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="C" or pre_upc_matches[2]=="*"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
 if(pre_upc_matches[2]=="D" or pre_upc_matches[2]=="E"):
  drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, LineSize, barcolor[0]);
  drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, LineSize, barcolor[2]);
  drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, LineSize, barcolor[2]);
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
   try:
    new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_codabar(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_codabar(upc,None,resize,hideinfo,barheight,textxy,barcolor);
