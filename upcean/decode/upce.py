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

    $FileInfo: upce.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.barcodes.getsfname;
from PIL import Image, UnidentifiedImageError;

def decode_upce_barcode(infile="./upce.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
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
    '''upc_img = Image.frombytes("RGB", (((69 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
  except AttributeError:
   try:
    upc_img = Image.open(infile);
   except UnidentifiedImageError:
    return False;
    '''prefile = open(infile, "rb");
    upc_img = Image.frombytes("RGB", (((69 * barwidth) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
    prefile.close();'''
 barsize = barwidth * int(resize);
 starty = int(upc_img.size[1] / 2);
 fist_number_dict = { 'EEEOOO': "0", 'EEOEOO': "0", 'EEOOEO': "0", 'EEOOOE': "0", 'EOEEOO': "0", 'EOOEEO': "0", 'EOOOEE': "0", 'EOEOEO': "0", 'EOEOOE': "0", 'EOOEOE': "0", 'OOOEEE': "1", 'OOEOEE': "1", 'OOEEOE': "1", 'OOEEEO': "1", 'OEOOEE': "1", 'OEEOOE': "1", 'OEEEOO': "1", 'OEOEOE': "1", 'OEOEEO': "1", 'OEEOEO': "9" };
 last_number_dict = { 'EEEOOO': "0", 'EEOEOO': "1", 'EEOOEO': "2", 'EEOOOE': "3", 'EOEEOO': "4", 'EOOEEO': "5", 'EOOOEE': "6", 'EOEOEO': "7", 'EOEOOE': "8", 'EOOEOE': "9", 'OOOEEE': "0", 'OOEOEE': "1", 'OOEEOE': "2", 'OOEEEO': "3", 'OEOOEE': "4", 'OEEOOE': "5", 'OEEEOO': "6", 'OEOEOE': "7", 'OEOEEO': "8", 'OEEOEO': "9" };
 left_barcode_o_dict = { '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3", '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", '0110111': "8", '0001011': "9" };
 left_barcode_e_dict = { '0100111': "0", '0110011': "1", '0011011': "2", '0100001': "3", '0011101': "4", '0111001': "5", '0000101': "6", '0010001': "7", '0001001': "8", '0010111': "9" };
 startx = 12;
 nexpix = 12 * (barwidth * int(resize));
 endx = 53;
 listcount = 0;
 pre_upc_whole = [];
 while(startx < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<7):
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
 parity_pattern_list = [];
 while(listcount<countlist):
  if(left_barcode_o_dict.get(pre_upc_whole[listcount], None) is not None):
   parity_pattern_list.append("O");
   barcode_list.append(left_barcode_o_dict.get(pre_upc_whole[listcount], "0"));
  if(left_barcode_e_dict.get(pre_upc_whole[listcount], None) is not None):
   parity_pattern_list.append("E");
   barcode_list.append(left_barcode_e_dict.get(pre_upc_whole[listcount], "0"));
  listcount += 1;
 get_parity_pattern = "".join(parity_pattern_list);
 barcode_list.insert(0, fist_number_dict.get(get_parity_pattern, "0"));
 barcode_list.append(last_number_dict.get(get_parity_pattern, "0"));
 upc = "".join(barcode_list);
 return upc;
