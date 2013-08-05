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

    $FileInfo: ean13.py - Last Update: 08/05/2013 Ver. 2.4.3 RC 2 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, types, upcean.prepil, upcean.validate, upcean.convert, upcean.getsfname;
import upcean.ean2, upcean.ean5;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;
from upcean.validate import *;
from upcean.convert import *;
from upcean.getsfname import *;
from upcean.ean2 import *;
from upcean.ean5 import *;

def create_ean13(upc,outfile="./ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==8): 
  upc = convert_upce_to_ean13(upc);
 if(len(upc)==12): 
  upc = convert_upca_to_ean13(upc);
 if(len(upc)==12 and validate_upca(upc)==True): 
  upc = "0"+upc;
 if(len(upc)==12 and validate_upca(upc)==False): 
  upc = upc+str(validate_ean13(upc,true));
 if(len(upc)>13 or len(upc)<13): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(validate_ean13(upc)==False): 
  pre_matches = re.findall("^(\d{12})", upc); 
  upc = pre_matches[0]+str(validate_ean13(pre_matches[0],True));
 upc_matches = re.findall("(\d{1})(\d{6})(\d{6})", upc);
 if(len(upc_matches)<=0): 
  return False;
 upc_matches = upc_matches[0];
 PrefixDigit = upc_matches[0];
 LeftDigit = list(upc_matches[1]);
 RightDigit = list(upc_matches[2]);
 addonsize = 0;
 if(supplement!=None and len(supplement)==2): 
  addonsize = 29;
 if(supplement!=None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = Image.new("RGB", (115 + addonsize, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (115 + addonsize, barheight[1] + 9)], fill=barcolor[2]);
 drawColorLine(upc_img, 0, 10, 0, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 2, 10, 2, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 4, 10, 4, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 5, 10, 5, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 6, 10, 6, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 7, 10, 7, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 8, 10, 8, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 9, 10, 9, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 10, 10, 10, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 11, 10, 11, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 12, 10, 12, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 13, 10, 13, barheight[1], barcolor[0]);
 NumZero = 0; 
 LineStart = 14;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
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
  if(int(upc_matches[0])==1):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==2):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==3):
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==4):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==5):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==6):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==7):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==5): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==8):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==3): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[0])==9):
   if(NumZero==1): 
    left_barcolor = left_barcolor_g;
   if(NumZero==2): 
    left_barcolor = left_barcolor_g;
   if(NumZero==4): 
    left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 56, 10, 56, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 57, 10, 57, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 58, 10, 58, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 59, 10, 59, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 60, 10, 60, barheight[1], barcolor[2]);
 NumZero = 0; 
 LineStart = 61;
 while (NumZero < len(RightDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  right_barcolor = [0, 0, 0, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==0): 
   right_barcolor = [1, 1, 1, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==1): 
   right_barcolor = [1, 1, 0, 0, 1, 1, 0];
  if(int(RightDigit[NumZero])==2): 
   right_barcolor = [1, 1, 0, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==3): 
   right_barcolor = [1, 0, 0, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==4): 
   right_barcolor = [1, 0, 1, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==5): 
   right_barcolor = [1, 0, 0, 1, 1, 1, 0];
  if(int(RightDigit[NumZero])==6): 
   right_barcolor = [1, 0, 1, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==7): 
   right_barcolor = [1, 0, 0, 0, 1, 0, 0];
  if(int(RightDigit[NumZero])==8): 
   right_barcolor = [1, 0, 0, 1, 0, 0, 0];
  if(int(RightDigit[NumZero])==9): 
   right_barcolor = [1, 1, 1, 0, 1, 0, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(right_barcolor)):
   if(right_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(right_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 103, 10, 103, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 104, 10, 104, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 105, 10, 105, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 106, 10, 106, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 107, 10, 107, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 108, 10, 108, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 109, 10, 109, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 110, 10, 110, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 111, 10, 111, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 112, 10, 112, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 113, 10, 113, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 114, 10, 114, barheight[0], barcolor[2]);
 new_upc_img = upc_preimg.resize(((115 + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(hidetext==False):
  if(hidesn!=None and hidesn!=True):
   drawColorText(upc_img, 10 * int(resize), 2 + (2 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), upc_matches[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 17 + (20 * (int(resize) - 1)) - (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 23 + (25 * (int(resize) - 1)) - (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 29 + (30 * (int(resize) - 1)) - (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 35 + (35 * (int(resize) - 1)) + (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 41 + (40 * (int(resize) - 1)) + (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[4], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 47 + (45 * (int(resize) - 1)) + (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[1])[5], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 63 + (65 * (int(resize) - 1)) - (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 69 + (70 * (int(resize) - 1)) - (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 75 + (75 * (int(resize) - 1)) - (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 81 + (80 * (int(resize) - 1)) + (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 87 + (85 * (int(resize) - 1)) + (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[4], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 93 + (90 * (int(resize) - 1)) + (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)), list(upc_matches[2])[5], barcolor[1]);
 del(upc_img);
 if(supplement!=None and len(supplement)==2): 
  upc_sup_img = draw_ean2_supplement(supplement,resize,hideinfo,barheight,barcolor);
  if(upc_sup_img!=False):
   new_upc_img.paste(upc_sup_img,(115 * int(resize),0));
   del(upc_sup_img);
 if(supplement!=None and len(supplement)==5): 
  upc_sup_img = draw_ean5_supplement(supplement,resize,hideinfo,barheight,barcolor);
  if(upc_sup_img!=False):
   new_upc_img.paste(upc_sup_img,(115 * int(resize),0));
   del(upc_sup_img);
 oldoutfile = get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return new_upc_img;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   try:
    new_upc_img.save(sys.stdout, outfileext);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
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

def draw_ean13(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13(upc,None,resize,hideinfo,barheight,barcolor);

def create_ean13_from_list(upc,outfile,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return create_ean13(upc,outfile,resize,hideinfo,barheight,barcolor);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return create_ean13(upc,outfile,resize,hideinfo,barheight,barcolor);
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
   if(isinstance(barcolor[0][0], tuple) or isinstance(barcolor[0][0], list)):
    barcolor_val = barcolor[NumLoop];
   if(isinstance(barcolor[0][0], int)):
    barcolor_val = barcolor;
   retlist.append(create_ean13(upc[NumLoop],outfile[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return retlist;

def draw_ean13_from_list(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(sys.version[0]=="2"):
  if(isinstance(upc, str) or isinstance(upc, unicode)):
   return draw_ean13(upc,resize,hideinfo,barheight);
 if(sys.version[0]=="3"):
  if(isinstance(upc, str)):
   return draw_ean13(upc,resize,hideinfo,barheight);
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
   if(isinstance(barcolor[0][0], tuple) or isinstance(barcolor[0][0], list)):
    barcolor_val = barcolor[NumLoop];
   if(isinstance(barcolor[0][0], int)):
    barcolor_val = barcolor;
   drawlist.append(draw_ean13(upc[NumLoop],resize_val,hideinfo_val,barheight_val,barcolor_val));
   NumLoop = NumLoop + 1;
 return drawlist;
