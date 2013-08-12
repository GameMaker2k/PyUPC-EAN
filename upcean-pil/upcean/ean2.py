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

    $FileInfo: ean2.py - Last Update: 08/12/2013 Ver. 2.4.4 RC 2 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, types, upcean.prepil, upcean.getsfname;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;
from upcean.getsfname import *;

def create_ean2_supplement(upc,outfile="./ean2_supplement.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc)>2 or len(upc)<2): 
  return False;
 upc_matches = re.findall("(\d{2})", upc);
 if(len(upc_matches)<=0): 
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
 if(pil_is_pillow==True and pil_vercheck>=210):
  pil_addon_fix = int(resize) * 2;
 CheckSum = int(upc_matches[0]) % 4;
 LeftDigit = list(upc_matches[0]);
 upc_preimg = Image.new("RGB", (29, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (29, barheight[1] + 9)], fill=barcolor[2]);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 10, 0, LineSize, barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, LineSize, barcolor[0]);
 drawColorLine(upc_img, 2, 10, 2, LineSize, barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, LineSize, barcolor[0]);
 drawColorLine(upc_img, 4, 10, 4, LineSize, barcolor[0]);
 NumZero = 0; 
 LineStart = 5;
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
  if(CheckSum==0 and NumZero==0): 
   left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==1): 
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==0): 
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==1): 
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==0): 
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==1): 
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==0): 
   left_barcolor = left_barcolor_g;
  if(CheckSum==3 and NumZero==1): 
   left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero == 0):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   LineStart += 1;
  NumZero += 1;
 new_upc_img = upc_preimg.resize((29 * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(hidetext==False):
  drawColorText(upc_img, 10 * int(resize), 5 + (6 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, LeftDigit[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 13 + (13 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, LeftDigit[1], barcolor[1]);
 del(upc_img);
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

def draw_ean2_supplement(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean2_supplement(upc,None,resize,hideinfo,barheight,barcolor);

def create_ean2(upc,outfile="./ean2.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_preimg = Image.new("RGB", ((29 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize)));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), ((29 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize))], fill=barcolor[2]);
 upc_sup_img = draw_ean2_supplement(upc,resize,hideinfo,barheight,barcolor);
 if(upc_sup_img is None or isinstance(upc_sup_img, bool)):
  return False;
 upc_preimg.paste(upc_sup_img,(8 * int(resize),0));
 del(upc_sup_img);
 del(upc_img);
 oldoutfile = get_save_filename(outfile);
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  return upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout, outfileext);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout.buffer, outfileext);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  upc_preimg.save(outfile, outfileext);
 return True;

def draw_ean2(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean2(upc,None,resize,hideinfo,barheight,barcolor);
