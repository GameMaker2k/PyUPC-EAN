# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: upce.py - Last Update: 2/19/2023 Ver. 2.7.23 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, types, upcean.getsfname, upcean.support;
import upcean.barcodes.ean2, upcean.barcodes.ean5;
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

def create_upce_barcode(upc,outfile="./upce.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(barwidth < 1): 
  barwidth = 1;
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
 if(not re.findall("^(0|1)", upc)):
  return False;
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
 if(supplement is not None and len(supplement)==2): 
  addonsize = 29;
 if(supplement is not None and len(supplement)==5): 
  addonsize = 56;
 if(pilsupport):
  upc_preimg = Image.new("RGB", ((69 * barwidth) + addonsize, barheight[1] + 9));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((69 * barwidth) + addonsize, barheight[1] + 9)], fill=barcolor[2]);
 if(cairosupport):
  upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (69 * barwidth) + addonsize, barheight[1] + 8);
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (69 * barwidth) + addonsize, barheight[1] + 8);
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 upc_array['code'].append( [0, 0, 0, 0, 0, 0, 0, 0, 0] );
 upc_array['code'].append( [1, 0, 1] );
 start_barcolor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1];
 LineStart = 0;
 BarNum = 0;
 start_bc_num_end = len(start_barcolor);
 LineSize = barheight[1];
 while(LineStart < start_bc_num_end):
  if(LineStart<9):
   LineSize = barheight[0];
  else:
   LineSize = barheight[1];
  if(hidetext):
   LineSize = barheight[1];
  if(start_barcolor[BarNum]==1):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
  if(start_barcolor[BarNum]==0):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
  LineStart += barwidth;
  BarNum += 1;
 NumZero = 0; 
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext):
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
  upc_array['code'].append( left_barcolor );
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
   LineStart += barwidth;
   BarNum += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 upc_array['code'].append( [0, 1, 0, 1, 0, 1] );
 upc_array['code'].append( [0, 0, 0, 0, 0, 0, 0, 0, 0] );
 end_barcolor = [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_bc_num_end = len(end_barcolor);
 LineSize = barheight[1];
 while(end_bc_num < end_bc_num_end):
  if(end_bc_num<7):
   LineSize = barheight[1];
  else:
   LineSize = barheight[0];
  if(hidetext):
   LineSize = barheight[1];
  if(end_barcolor[end_bc_num]==1):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[0]);
  if(end_barcolor[end_bc_num]==0):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barwidth, barcolor[2]);
  end_bc_num += 1;
  LineStart += barwidth;
  BarNum += 1;
 new_upc_img = upc_preimg.resize((((69 * barwidth) + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST);
 del(upc_img);
 del(upc_preimg);
 upc_img = ImageDraw.Draw(new_upc_img);
 if(not hidetext):
  if(hidesn is not None and not hidesn):
   drawColorText(upc_img, 10 * int(resize), 1 + (2 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[0] * int(resize)), upc_matches[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 15 + (18 * (int(resize) - 1)) - (5 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[0], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 21 + (23 * (int(resize) - 1)) - (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[1], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 27 + (28 * (int(resize) - 1)) - (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[2], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 33 + (33 * (int(resize) - 1)) + (1 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[3], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 39 + (38 * (int(resize) - 1)) + (3 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[4], barcolor[1]);
  drawColorText(upc_img, 10 * int(resize), 45 + (43 * (int(resize) - 1)) + (5 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), list(upc_matches[1])[5], barcolor[1]);  
  if(hidecd is not None and not hidecd):
   drawColorText(upc_img, 10 * int(resize), 61 + (61 * (int(resize) - 1)), (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[2] * int(resize)), upc_matches[2], barcolor[1]);
 del(upc_img);
 if(pilsupport):
  if(supplement is not None and len(supplement)==2): 
   upc_sup_img = upcean.barcodes.ean2.draw_ean2_barcode_supplement(supplement,resize,hideinfo,barheight,barwidth,textxy,barcolor);
   if(upc_sup_img):
    new_upc_img.paste(upc_sup_img,((69 * barwidth) * int(resize),0));
    del(upc_sup_img);
  if(supplement is not None and len(supplement)==5): 
   upc_sup_img = upcean.barcodes.ean5.draw_ean5_barcode_supplement(supplement,resize,hideinfo,barheight,barwidth,textxy,barcolor);
   if(upc_sup_img):
    new_upc_img.paste(upc_sup_img,((69 * barwidth) * int(resize),0));
    del(upc_sup_img);
 if(cairosupport):
  if(supplement!=None and len(supplement)==2):
   upc_sup_img = draw_ean2_supplement(supplement,1,hideinfo,barheight,barwidth,barcolor);
   upc_img.set_source_surface(upc_sup_img, (69 * barwidth), 0);
   upc_img.paint();
   del(upc_sup_img);
 if(supplement!=None and len(supplement)==5):
   upc_sup_img = draw_ean5_supplement(supplement,1,hideinfo,barheight,barwidth,barcolor);
   upc_img.set_source_surface(upc_sup_img, (69 * barwidth), 0);
   upc_img.paint();
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

def draw_upce_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upce_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor);
