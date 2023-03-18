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

    $FileInfo: itf.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.barcodes.getsfname;
from PIL import Image, UnidentifiedImageError;

def decode_itf14_barcode(infile="./itf14.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(isinstance(infile, Image.Image)):
  upc_img = infile;
 else:
  try:
   infile.seek(0);
   try:
    upc_img = Image.open(infile);
   except UnidentifiedImageError:
    return False;
    '''upc_img = Image.frombytes("RGB", (((115 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
  except AttributeError:
   try:
    upc_img = Image.open(infile);
   except UnidentifiedImageError:
    return False;
    '''prefile = open(infile, "rb");
    upc_img = Image.frombytes("RGB", (((115 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
    prefile.close();'''
 barsize = barwidth * int(resize);
 starty = int(upc_img.size[1] / 2);
 fist_number_dict = { 'LLLLLL': "0", 'LLGLGG': "1", 'LLGGLG': "2", 'LLGGGL': "3", 'LGLLGG': "4", 'LGGLLG': "5", 'LGGGLL': "6", 'LGLGLG': "7", 'LGLGGL': "8", 'LGGLGL': "9" };
 left_barcode_dict = { '00110': "0", '10001': "1", '01001': "2", '11000': "3", '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9" };
 right_barcode_dict = { '00110': "0", '10001': "1", '01001': "2", '11000': "3", '00101': "4", '10100': "5", '01100': "6", '00011': "7", '10010': "8", '01010': "9" };
 barcodepresize = ((44 * barwidth) ) * int(resize);
 barcodesize = ( (upc_img.size[0]) - barcodepresize ) / 18;
 startx = 17;
 nexpix = 17 * (barwidth * int(resize));
 endx = int(17 + ( (barcodesize * 18 ) ));
 listcount = 0;
 pre_upc_whole_left = [];
 pre_upc_whole_right = [];
 pre_upc_list_left = [];
 pre_upc_list_right = [];
 skiptwo = False;
 while(startx < endx):
  listcount = 0;
  curpixel = upc_img.getpixel((nexpix, starty));
  if(curpixel==barcolor[0]):
   nexpixel = upc_img.getpixel((nexpix + 1, starty));
   if(nexpixel==barcolor[0] and startx<(endx-2)):
    pre_upc_list_left.append("1");
    skiptwo = True;
   else:
    pre_upc_list_left.append("0");
    skiptwo = False;
  if(curpixel==barcolor[2]):
   nexpixel = upc_img.getpixel((nexpix + 1, starty));
   if(nexpixel==barcolor[2] and startx<(endx-2)):
    pre_upc_list_right.append("1");
    skiptwo = True;
   else:
    pre_upc_list_right.append("0");
    skiptwo = False;
  if(skiptwo):
   startx += 3;
   nexpix += 3 * (barwidth * int(resize));
  else:
   startx += 1;
   nexpix += 1 * (barwidth * int(resize));
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

def decode_itf6_barcode(infile="./itf14.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 return decode_itf14_barcode(infile,resize,barheight,barwidth,barcolor, imageoutlib);
