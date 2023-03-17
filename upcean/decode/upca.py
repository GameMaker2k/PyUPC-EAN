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

    $FileInfo: upca.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.barcodes.getsfname;
from PIL import Image, UnidentifiedImageError;

def decode_upca_barcode(infile="./upca.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
    upc_img = Image.frombytes("RGB", (((113 * barwidth) + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());
  except AttributeError:
   try:
    upc_img = Image.open(infile);
   except UnidentifiedImageError:
    prefile = open(infile, "rb");
    upc_img = Image.frombytes("RGB, (((113 * barwidth) + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
    profile.close();
 barsize = barwidth * int(resize);
 starty = int(upc_img.size[1] / 2);
 left_barcode_dict = { '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3", '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", '0110111': "8", '0001011': "9" };
 right_barcode_dict = { '1110010': "0", '1100110': "1", '1101100': "2", '1000010': "3", '1011100': "4", '1001110': "5", '1010000': "6", '1000100': "7", '1001000': "8", '1110100': "9" };
 startx = 12;
 nexpix = 12 * (barwidth * int(resize));
 endx = 101;
 listcount = 0;
 pre_upc_whole = [];
 while(startx < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<7):
   if(startx==54):
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
 while(listcount<countlist):
  if(listcount<6):
   barcode_list.append(left_barcode_dict.get(pre_upc_whole[listcount], "0"));
  if(listcount>5):
   barcode_list.append(right_barcode_dict.get(pre_upc_whole[listcount], "0"));
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;
