'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: ean8.py - Last Update: 12/3/2019 Ver. 2.7.18 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, sys, types, upcean.barcodes.prepil, upcean.getsfname;
import upcean.barcodes.ean2, upcean.barcodes.ean5;
from PIL import Image, ImageDraw, ImageFont;

def create_ean8_barcode(upc,outfile="./ean8.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 upc_pieces = None; 
 supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; 
  supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)>8 or len(upc)<8):
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
 upc_matches = re.findall("(\d{4})(\d{4})", upc);
 upc_matches = upc_matches[0];
 if(len(upc_matches)<=0):
  return False;
 LeftDigit = list(upc_matches[0]);
 upc_matches_new = re.findall("(\d{2})(\d{2})", upc_matches[0]);
 upc_matches_new= upc_matches_new[0];
 LeftLeftDigit = upc_matches_new[0];
 LeftRightDigit = upc_matches_new[1];
 RightDigit = list(upc_matches[1]);
 upc_matches_new = re.findall("(\d{2})(\d{2})", upc_matches[1]);
 upc_matches_new= upc_matches_new[0];
 RightLeftDigit = upc_matches_new[0];
 RightRightDigit = upc_matches_new[1];
 addonsize = 0;
 if(supplement is not None and len(supplement)==2): 
  addonsize = 29;
 if(supplement is not None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = Image.new("RGB", (83 + addonsize, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (83 + addonsize, barheight[1] + 9)], fill=barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 0, 10, 0, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 1, 10, 1, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 2, 10, 2, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 3, 10, 3, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 4, 10, 4, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 5, 10, 5, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 6, 10, 6, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 7, 10, 7, barheight[1], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 8, 10, 8, barheight[1], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 9, 10, 9, barheight[1], barcolor[0]);
 NumZero = 0; 
 LineStart = 10;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext):
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
  if(int(upc_matches[1])==1):
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==4):
    left_barcolor = left_barcolor_g;
   if(NumZero==5):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==2):
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==3):
    left_barcolor = left_barcolor_g;
   if(NumZero==5):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==3):
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==3):
    left_barcolor = left_barcolor_g;
   if(NumZero==4):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==4):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==4):
    left_barcolor = left_barcolor_g;
   if(NumZero==5):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==5):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==5):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==6):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==3):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==7):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==3):
    left_barcolor = left_barcolor_g;
   if(NumZero==5):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==8):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==3):
    left_barcolor = left_barcolor_g;
   if(NumZero==4):
    left_barcolor = left_barcolor_g;
  if(int(upc_matches[1])==9):
   if(NumZero==1):
    left_barcolor = left_barcolor_g;
   if(NumZero==2):
    left_barcolor = left_barcolor_g;
   if(NumZero==4):
    left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 upcean.barcodes.prepil.drawColorLine(upc_img, 38, 10, 38, barheight[1], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 39, 10, 39, barheight[1], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 40, 10, 40, barheight[1], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 41, 10, 41, barheight[1], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 42, 10, 42, barheight[1], barcolor[2]);
 NumZero = 0; LineStart = 43;
 while (NumZero < len(RightDigit)):
  LineSize = barheight[0];
  if(hidetext):
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
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(right_barcolor[InnerUPCNum]==0):
    upcean.barcodes.prepil.drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 upcean.barcodes.prepil.drawColorLine(upc_img, 71, 10, 71, barheight[1], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 72, 10, 72, barheight[1], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 73, 10, 73, barheight[1], barcolor[0]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 74, 10, 74, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 75, 10, 75, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 76, 10, 76, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 77, 10, 77, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 78, 10, 78, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 79, 10, 79, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 80, 10, 80, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 81, 10, 81, barheight[0], barcolor[2]);
 upcean.barcodes.prepil.drawColorLine(upc_img, 82, 10, 82, barheight[0], barcolor[2]);
 new_upc_img = upc_preimg.resize(((83 + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 11 + (14 * (int(resize) - 1)) - (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(LeftLeftDigit)[0], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 17 + (19 * (int(resize) - 1)) - (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(LeftLeftDigit)[1], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 24 + (24 * (int(resize) - 1)) + (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(LeftRightDigit)[0], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 30 + (29 * (int(resize) - 1)) + (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(LeftRightDigit)[1], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 43 + (46 * (int(resize) - 1)) - (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(RightLeftDigit)[0], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 49 + (51 * (int(resize) - 1)) - (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(RightLeftDigit)[1], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 56 + (56 * (int(resize) - 1)) + (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(RightRightDigit)[0], barcolor[1]);
  upcean.barcodes.prepil.drawColorText(upc_img, 10 * int(resize), 62 + (61 * (int(resize) - 1)) + (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(RightRightDigit)[1], barcolor[1]);
 del(upc_img);
 if(supplement is not None and len(supplement)==2): 
  upc_sup_img = upcean.barcodes.ean2.draw_ean2_barcode_supplement(supplement,resize,hideinfo,barheight,textxy,barcolor);
  if(upc_sup_img):
   new_upc_img.paste(upc_sup_img,(83 * int(resize),0));
   del(upc_sup_img);
 if(supplement is not None and len(supplement)==5): 
  upc_sup_img = upcean.barcodes.ean5.draw_ean5_barcode_supplement(supplement,resize,hideinfo,barheight,textxy,barcolor);
  if(upc_sup_img):
   new_upc_img.paste(upc_sup_img,(83 * int(resize),0));
   del(upc_sup_img);
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

def draw_ean8_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean8_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);
