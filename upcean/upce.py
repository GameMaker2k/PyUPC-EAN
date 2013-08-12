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

    $FileInfo: upce.py - Last Update: 08/12/2013 Ver. 2.4.4 RC 2 - Author: cooldude2k $
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

def create_upce(upc,outfile="./upce.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
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
 if(len(upc)==12):
  upc = convert_upca_to_upce(upc);
 if(len(upc)==13):
  upc = convert_ean13_to_upce(upc);
 if(len(upc)==7):
  upc = upc+validate_upce(upc,True);
 if(len(upc)>8 or len(upc)<8):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 try:
  pil_ver = Image.PILLOW_VERSION;
  pil_ver = pil_ver.split(".");
  pil_ver = [int(x) for x in pil_ver];
  pil_is_pillow = True;
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
 if(not re.findall("^(0|1)", upc)):
  return False;
 if(validate_upce(upc)==False):
  pre_matches = re.findall("^(\d{7})", upc); 
  upc = pre_matches[0]+str(validate_upce(pre_matches[0],True));
 upc_matches = re.findall("(\d{1})(\d{6})(\d{1})", upc);
 upc_matches = upc_matches[0];
 if(len(upc_matches)<=0):
  return False;
 if(int(upc_matches[0])>1):
  return False;
 PrefixDigit = upc_matches[0];
 LeftDigit = list(upc_matches[1]);
 CheckDigit = upc_matches[2];
 addonsize = 0;
 if(supplement!=None and len(supplement)==2): 
  addonsize = 29;
 if(supplement!=None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = Image.new("RGB", (69 + addonsize, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (69 + addonsize, barheight[1] + 9)], fill=barcolor[2]);
 drawColorLine(upc_img, 0, 10, 0, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 2, 10, 2, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 4, 10, 4, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 5, 10, 5, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 6, 10, 6, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 7, 10, 7, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 8, 10, 8, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 9, 10, 9, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 10, 10, 10, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 11, 10, 11, barheight[1], barcolor[0]);
 NumZero = 0; 
 LineStart = 12;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_barcolor = [0, 0, 0, 0, 0, 0, 0];
  left_barcolor_odd = [0, 0, 0, 0, 0, 0, 0];
  left_barcolor_even = [0, 0, 0, 0, 0, 0, 0];
  if(int(LeftDigit[NumZero])==0): 
   left_barcolor_odd = [0, 0, 0, 1, 1, 0, 1]; 
   left_barcolor_even = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_barcolor_odd = [0, 0, 1, 1, 0, 0, 1]; 
   left_barcolor_even = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_barcolor_odd = [0, 0, 1, 0, 0, 1, 1]; 
   left_barcolor_even = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_barcolor_odd = [0, 1, 1, 1, 1, 0, 1]; 
   left_barcolor_even = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_barcolor_odd = [0, 1, 0, 0, 0, 1, 1]; 
   left_barcolor_even = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_barcolor_odd = [0, 1, 1, 0, 0, 0, 1]; 
   left_barcolor_even = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_barcolor_odd = [0, 1, 0, 1, 1, 1, 1]; 
   left_barcolor_even = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_barcolor_odd = [0, 1, 1, 1, 0, 1, 1]; 
   left_barcolor_even = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_barcolor_odd = [0, 1, 1, 0, 1, 1, 1]; 
   left_barcolor_even = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9):
   left_barcolor_odd = [0, 0, 0, 1, 0, 1, 1];
   left_barcolor_even = [0, 0, 1, 0, 1, 1, 1];
  left_barcolor = left_barcolor_odd;
  if(int(upc_matches[2])==0 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==1 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==2 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==3 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==4 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==5 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==6 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==7 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==8 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==9 and int(upc_matches[0])==0):
   if(NumZero==0): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==0 and int(upc_matches[0])==1):
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==1 and int(upc_matches[0])==1):
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==2 and int(upc_matches[0])==1):
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==3 and int(upc_matches[0])==1):
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==4 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==5 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==6 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==7 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==5): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==8 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==3): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  if(int(upc_matches[2])==9 and int(upc_matches[0])==1):
   if(NumZero==1): 
    left_barcolor = left_barcolor_even;
   if(NumZero==2): 
    left_barcolor = left_barcolor_even;
   if(NumZero==4): 
    left_barcolor = left_barcolor_even;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 54, 10, 54, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 55, 10, 55, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 56, 10, 56, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 57, 10, 57, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 58, 10, 58, barheight[1], barcolor[2]);
 drawColorLine(upc_img, 59, 10, 59, barheight[1], barcolor[0]);
 drawColorLine(upc_img, 60, 10, 60, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 61, 10, 61, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 62, 10, 62, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 63, 10, 63, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 64, 10, 64, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 65, 10, 65, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 66, 10, 66, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 67, 10, 67, barheight[0], barcolor[2]);
 drawColorLine(upc_img, 68, 10, 68, barheight[0], barcolor[2]);
 new_upc_img = upc_preimg.resize(((69 + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(hidetext==False):
  if(hidesn!=None and hidesn!=True):
   drawColorText(upc_img, 10 * int(resize), 1 + (2 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, upc_matches[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 15 + (18 * (int(resize) - 1)) - (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 21 + (23 * (int(resize) - 1)) - (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 27 + (28 * (int(resize) - 1)) - (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 33 + (33 * (int(resize) - 1)) + (1 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 39 + (38 * (int(resize) - 1)) + (3 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[4], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 45 + (43 * (int(resize) - 1)) + (5 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, list(upc_matches[1])[5], barcolor[1]);  
  if(hidecd!=None and hidecd!=True):
   drawColorText(upc_img, 10 * int(resize), 61 + (61 * (int(resize) - 1)), barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix, upc_matches[2], barcolor[1]);
 del(upc_img);
 if(supplement!=None and len(supplement)==2): 
  upc_sup_img = draw_ean2_supplement(supplement,resize,hideinfo,barheight,barcolor);
  if(upc_sup_img!=False):
   new_upc_img.paste(upc_sup_img,(69 * int(resize),0));
   del(upc_sup_img);
 if(supplement!=None and len(supplement)==5): 
  upc_sup_img = draw_ean5_supplement(supplement,resize,hideinfo,barheight,barcolor);
  if(upc_sup_img!=False):
   new_upc_img.paste(upc_sup_img,(69 * int(resize),0));
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

def draw_upce(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upce(upc,None,resize,hideinfo,barheight,barcolor);
