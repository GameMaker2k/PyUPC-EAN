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

    $FileInfo: ean8.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.barcodes.getsfname, upcean.support;
from PIL import Image, UnidentifiedImageError;

pilsupport = upcean.support.check_for_pil();
cairosupport = upcean.support.check_for_cairo();
from upcean.barcodes.predraw import *;
if(cairosupport):
 import cairo;

def decode_ean13_barcode(infile="./ean13.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
 fist_number_dict = { 'LLLLLL': "0", 'LLGLGG': "1", 'LLGGLG': "2", 'LLGGGL': "3", 'LGLLGG': "4", 'LGGLLG': "5", 'LGGGLL': "6", 'LGLGLG': "7", 'LGLGGL': "8", 'LGGLGL': "9" };
 left_barcode_l_dict = { '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3", '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", '0110111': "8", '0001011': "9" };
 left_barcode_g_dict = { '0100111': "0", '0110011': "1", '0011011': "2", '0100001': "3", '0011101': "4", '0111001': "5", '0000101': "6", '0010001': "7", '0001001': "8", '0010111': "9" };
 right_barcode_dict = { '1110010': "0", '1100110': "1", '1101100': "2", '1000010': "3", '1011100': "4", '1001110': "5", '1010000': "6", '1000100': "7", '1001000': "8", '1110100': "9" };
 startx = 14;
 jumpcode = 0;
 if(shiftxy[0] is None):
  prestartx = 0;
  startx = 0;
  gotvalue = False;
  while(prestartx<upc_img.size[0]):
   inprestartx = prestartx;
   substartx = 14;
   curpixelist=[];
   if(upc_img.getpixel((inprestartx, starty))==barcolor[0]):
    if(inprestartx+(2 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    curpixelist.append(upc_img.getpixel((inprestartx, starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(1 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(2 * (barwidth * int(resize))), starty)));
    inprestartx += (3 + 42) * (barwidth * int(resize));
    jumpcode = 56;
    if(inprestartx+(4 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    curpixelist.append(upc_img.getpixel((inprestartx, starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(1 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(2 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(3 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(4 * (barwidth * int(resize))), starty)));
    inprestartx += (5 + 42) * (barwidth * int(resize));
    if(inprestartx+(2 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    curpixelist.append(upc_img.getpixel((inprestartx, starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(1 * (barwidth * int(resize))), starty)));
    curpixelist.append(upc_img.getpixel((inprestartx+(2 * (barwidth * int(resize))), starty)));
    if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[2] and curpixelist[2]==barcolor[0]) and (curpixelist[3]==barcolor[2] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2]) and (curpixelist[8]==barcolor[0] and curpixelist[9]==barcolor[2] and curpixelist[10]==barcolor[0])):
     startx = substartx;
     break;
   prestartx += 1;
  shiftxy = (0, 0);
 else:
  startx = (14 + shiftxy[0]);
  jumpcode = (56 + shiftxy[0]);
 nexpix = startx * (barwidth * int(resize));
 endx = (3 + 42 + 5 + 42 + 3);
 listcount = 0;
 pre_upc_whole = [];
 prestartx = startx;
 while(startx < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<7):
   if(startx==jumpcode):
    startx += 5;
    nexpix += 5 * (barwidth * int(resize));
   curpixel = upc_img.getpixel((nexpix, starty));
   if(curpixel==barcolor[0]):
    pre_upc_list.append("1");
   if(curpixel==barcolor[2]):
    pre_upc_list.append("0");
   startx += 1;
   nexpix += 1 * (barwidth * int(resize));
   listcount += 1;
  pre_upc_whole.append("".join(pre_upc_list));
 upc_img.close();
 countlist = len(pre_upc_whole);
 listcount = 0;
 barcode_list = [];
 fist_number_list = [];
 while(listcount<countlist):
  if(listcount<6):
   if(left_barcode_l_dict.get(pre_upc_whole[listcount], None) is not None):
    fist_number_list.append("L");
    barcode_list.append(left_barcode_l_dict.get(pre_upc_whole[listcount], "0"));
   elif(left_barcode_g_dict.get(pre_upc_whole[listcount], None) is not None):
    fist_number_list.append("G");
    barcode_list.append(left_barcode_g_dict.get(pre_upc_whole[listcount], "0"));
   else:
    return False;
  if(listcount==6):
   get_fist_number = "".join(fist_number_list);
   first_num_value = fist_number_dict.get(get_fist_number, False);
   if(not first_num_value):
    return False;
   barcode_list.insert(0, first_num_value);
  if(listcount>5):
   barcode_list.append(right_barcode_dict.get(pre_upc_whole[listcount], "0"));
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;
