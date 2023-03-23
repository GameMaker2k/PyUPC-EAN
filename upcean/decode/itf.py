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

    $FileInfo: ean8.py - Last Update: 3/23/2023 Ver. 2.8.6 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.barcodes.getsfname, upcean.support;
from PIL import Image, UnidentifiedImageError;

pilsupport = upcean.support.check_for_pil();
cairosupport = upcean.support.check_for_cairo();
from upcean.barcodes.predraw import *;
if(cairosupport):
 import cairo;

def decode_itf_barcode(infile="./itf.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(isinstance(infile, Image.Image)):
  upc_img = infile.convert('RGB');
 elif(cairosupport and isinstance(infile, cairo.ImageSurface)):
  #upc_img = Image.frombuffer("RGB", (infile.get_width(), infile.get_height()), infile.get_data().tobytes(), "raw", "BGR", 0, 1).convert('RGB');
  #upc_img = Image.frombytes("RGB", (infile.get_width(), infile.get_height()), infile.get_data().tobytes()).convert('RGB');
  return False;
 else:
  try:
   infile.seek(0);
   try:
    upc_img = Image.open(infile).convert('RGB');
   except UnidentifiedImageError:
    return False;
    '''upc_img = Image.frombytes("RGB", (((115 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
  except AttributeError:
   try:
    upc_img = Image.open(infile).convert('RGB');
   except UnidentifiedImageError:
    return False;
    '''prefile = open(infile, "rb");
    upc_img = Image.frombytes("RGB", (((115 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
    prefile.close();'''
 barsize = barwidth * int(resize);
 starty = int(upc_img.size[1] / 2) + shiftxy[1];
 pixlist = (upc_img.getpixel((0, starty)), upc_img.getpixel((1, starty)), upc_img.getpixel((2, starty)), upc_img.getpixel((3, starty)));
 if(pixlist[0]==barcolor[0] and pixlist[0]==barcolor[1] and pixlist[0]==barcolor[2] and pixlist[0]==barcolor[3]):
  drawColorRectangleAlt(upc_img, 0, 0, ((44 * barwidth) + upc_size_add) - 1, ((barheight[0] + 15) - 11), barcolor[2]);
  drawColorRectangleAlt(upc_img, 1, 1, ((44 * barwidth) + upc_size_add) - 2, ((barheight[0] + 15) - 12), barcolor[2]);
  drawColorRectangleAlt(upc_img, 2, 2, ((44 * barwidth) + upc_size_add) - 3, ((barheight[0] + 15) - 13), barcolor[2]);
  drawColorRectangleAlt(upc_img, 3, 3, ((44 * barwidth) + upc_size_add) - 4, ((barheight[0] + 15) - 14), barcolor[2]);
 fist_number_dict = { 'LLLLLL': "0", 'LLGLGG': "1", 'LLGGLG': "2", 'LLGGGL': "3", 'LGLLGG': "4", 'LGGLLG': "5", 'LGGGLL': "6", 'LGLGLG': "7", 'LGLGGL': "8", 'LGGLGL': "9" };
 left_barcode_dict = { '00110': "0", '10001': "1", '01001': "2", '11000': "3", '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9" };
 right_barcode_dict = { '00110': "0", '10001': "1", '01001': "2", '11000': "3", '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9" };
 barcodepresize = ((39 * barwidth) ) * int(resize);
 barcodesize = int( ( (upc_img.size[0]) - barcodepresize ) / 18 );
 startx = 17;
 if(shiftxy[0] is None):
  prestartx = 0;
  startx = 0;
  gotvalue = False;
  barcodesize = 0;
  while(prestartx<upc_img.size[0]):
   inprestartx = prestartx;
   substartx = prestartx + (4 * (barwidth * int(resize)));
   curpixelist=[];
   if(upc_img.getpixel((inprestartx, starty))==barcolor[0]):
    if(inprestartx+(4 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    curpixelist.append(upc_img.getpixel((inprestartx, starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(1 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(2 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(3 * (barwidth * int(resize))), starty)));
    if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[2] and curpixelist[2]==barcolor[0] and curpixelist[3]==barcolor[2])):
     preinprestartx = inprestartx + (4 * (barwidth * int(resize)));
     precurpixelist = [];
     while(preinprestartx<upc_img.size[0]):
      precurpixelist = [];
      if((preinprestartx+(9 * (barwidth * int(resize))) > upc_img.size[0])):
       return False;
      precurpixelist.append(upc_img.getpixel((preinprestartx, starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(1 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(2 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(3 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(4 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(5 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(6 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(7 * (barwidth * int(resize))), starty)));
      precurpixelist.append(upc_img.getpixel((preinprestartx+(8 * (barwidth * int(resize))), starty)));
      preinprestartx += (9 * (barwidth * int(resize)));
      barcodesize += 1;
      if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[0] and precurpixelist[3]==barcolor[2] and precurpixelist[4]==barcolor[0] and precurpixelist[5]==barcolor[2] and precurpixelist[6]==barcolor[2] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
       break;
     barcodesize = int((barcodesize) / 2);
     inprestartx += (4 + (barcodesize * 18)) * (barwidth * int(resize));
     curpixelist.append(upc_img.getpixel((inprestartx, starty)));
     curpixelist.append(upc_img.getpixel((inprestartx+(1 * (barwidth * int(resize))), starty)));
     curpixelist.append(upc_img.getpixel((inprestartx+(2 * (barwidth * int(resize))), starty)));
     curpixelist.append(upc_img.getpixel((inprestartx+(3 * (barwidth * int(resize))), starty)));
     curpixelist.append(upc_img.getpixel((inprestartx+(4 * (barwidth * int(resize))), starty)));
     if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[2] and curpixelist[2]==barcolor[0] and curpixelist[3]==barcolor[2]) and (curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[0] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2] and curpixelist[8]==barcolor[0])):
      startx = substartx;
      break;
   prestartx += 1;
  shiftxy = (0, shiftxy[1]);
 else:
  startx = ((17 * (barwidth * int(resize)))  + shiftxy[0]);
  preinprestartx = startx;
  precurpixelist = [];
  barcodesize = 0;
  while(preinprestartx<upc_img.size[0]):
   precurpixelist = [];
   if((preinprestartx+(8 * (barwidth * int(resize))) > upc_img.size[0])):
    return False;   
   precurpixelist.append(upc_img.getpixel((preinprestartx, starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(1 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(2 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(3 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(4 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(5 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(6 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(7 * (barwidth * int(resize))), starty)));
   precurpixelist.append(upc_img.getpixel((preinprestartx+(8 * (barwidth * int(resize))), starty)));
   preinprestartx += (9 * (barwidth * int(resize)));
   barcodesize += 1;
   if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[0] and precurpixelist[3]==barcolor[2] and precurpixelist[4]==barcolor[0] and precurpixelist[5]==barcolor[2] and precurpixelist[6]==barcolor[2] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
    break;
  barcodesize = int((barcodesize) / 2);
 endx = int(startx + ( (barcodesize * 18 ) * (barwidth * int(resize)) ));
 listcount = 0;
 pre_upc_whole_left = [];
 pre_upc_whole_right = [];
 pre_upc_list_left = [];
 pre_upc_list_right = [];
 skiptwo = False;
 prestartx = startx;
 while(startx < endx):
  listcount = 0;
  curpixel = upc_img.getpixel((startx, starty));
  if(curpixel==barcolor[0]):
   nexpixel = upc_img.getpixel((startx + (1 * (barwidth * int(resize))), starty));
   if(nexpixel==barcolor[0] and startx<(endx - (2* (barwidth * int(resize))))):
    pre_upc_list_left.append("1");
    skiptwo = True;
   else:
    pre_upc_list_left.append("0");
    skiptwo = False;
  if(curpixel==barcolor[2]):
   nexpixel = upc_img.getpixel((startx + (1 * (barwidth * int(resize))), starty));
   if(nexpixel==barcolor[2] and startx<(endx - (2* (barwidth * int(resize))))):
    pre_upc_list_right.append("1");
    skiptwo = True;
   else:
    pre_upc_list_right.append("0");
    skiptwo = False;
  if(skiptwo):
   startx += 3 * (barwidth * int(resize));
  else:
   startx += 1 * (barwidth * int(resize));
 pre_upc_whole_left = "".join(pre_upc_list_left);
 pre_upc_whole_right = "".join(pre_upc_list_right);
 upc_img.close();
 pre_upc_whole_left_re = re.findall("([0-9]{5})", pre_upc_whole_left);
 pre_upc_whole_right_re = re.findall("([0-9]{5})", pre_upc_whole_right);
 countlist = barcodesize;
 listcount = 0;
 barcode_list = [];
 fist_number_list = [];
 while(listcount<countlist):
  left_barcode_value = left_barcode_dict.get(pre_upc_whole_left_re[listcount], False);
  if(not left_barcode_value):
   return False;
  barcode_list.append(left_barcode_value);
  right_barcode_value = right_barcode_dict.get(pre_upc_whole_right_re[listcount], False);
  if(not right_barcode_value):
   return False;
  barcode_list.append(right_barcode_value);
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;
