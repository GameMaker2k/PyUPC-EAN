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

    $FileInfo: ean13.py - Last Update: 3/27/2023 Ver. 2.8.13 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.encode.getsfname, upcean.support;
from PIL import Image, UnidentifiedImageError;
try:
 from io import StringIO, BytesIO;
except ImportError:
 try:
  from cStringIO import StringIO;
  from cStringIO import StringIO as BytesIO;
 except ImportError:
  from StringIO import StringIO;
  from StringIO import StringIO as BytesIO;
pilsupport = upcean.support.check_for_pil();
cairosupport = upcean.support.check_for_cairo();
from upcean.encode.predraw import *;
if(cairosupport):
 import cairo;

def decode_ean13_barcode(infile="./ean13.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(barwidth)) or int(barwidth) < 1):
  barwidth = 1;
 if(isinstance(infile, Image.Image)):
  upc_img = infile.convert('RGB');
 elif(cairosupport and isinstance(infile, cairo.ImageSurface)):
  if(sys.version[0]=="2"):
   stdoutfile = StringIO();
  if(sys.version[0]>="3"):
   stdoutfile = BytesIO();
  infile.write_to_png(stdoutfile);
  stdoutfile.seek(0);
  upc_img = Image.open(stdoutfile).convert('RGB');
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
   substartx = prestartx + (3 * (barwidth * int(resize)));
   curpixelist=[];
   if(upc_img.getpixel((inprestartx, starty))==barcolor[0]):
    if(inprestartx+(2 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 3;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth * int(resize))), starty)));
     icount += 1;
    inprestartx += (3 + 42) * (barwidth * int(resize));
    jumpcode = inprestartx;
    if(inprestartx+(4 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 5;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth * int(resize))), starty)));
     icount += 1;
    inprestartx += (5 + 42) * (barwidth * int(resize));
    if(inprestartx+(2 * (barwidth * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 3;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth * int(resize))), starty)));
     icount += 1;
    if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[2] and curpixelist[2]==barcolor[0]) and (curpixelist[3]==barcolor[2] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2]) and (curpixelist[8]==barcolor[0] and curpixelist[9]==barcolor[2] and curpixelist[10]==barcolor[0])):
     startx = substartx;
     break;
   prestartx += 1;
  shiftxy = (0, shiftxy[1]);
 else:
  startx = ((14 * (barwidth * int(resize))) + shiftxy[0]);
  jumpcode = ((56 * (barwidth * int(resize))) + shiftxy[0]);
 endx = (42 + 42) * (barwidth * int(resize));
 if(locatebarcode):
  prestartx = startx - (3 * (barwidth * int(resize)));
  postendx = endx + (3 * (barwidth * int(resize)));
  return ("ean18", prestartx, startx, 13, endx, postendx); 
 startxalt = 0;
 listcount = 0;
 pre_upc_whole = [];
 prestartx = startx;
 while(startxalt < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<7):
   if(startx==jumpcode):
    startx += 5 * (barwidth * int(resize));
   curpixel = upc_img.getpixel((startx, starty));
   if(curpixel==barcolor[0]):
    pre_upc_list.append("1");
   if(curpixel==barcolor[2]):
    pre_upc_list.append("0");
   startx += 1 * (barwidth * int(resize));
   startxalt += 1 * (barwidth * int(resize));
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

def get_ean13_barcode_location(infile="./ean8.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_ean13_barcode(infile,resize,barheight,barwidth,shiftxy,barcolor,True,imageoutlib);

def decode_gtin13_barcode(infile="./gtin13.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def get_gtin13_barcode_location(infile="./gtin13.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_gtin13_barcode(infile,resize,barheight,barwidth,shiftxy,barcolor,True,imageoutlib);

def decode_ucc13_barcode(infile="./ucc13.png",resize=1,barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_ean13_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def get_ucc13_barcode_location(infile="./ucc13.png",resize=1,barheight=(48, 54),barwidth=1,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_ucc13_barcode(infile,resize,barheight,barwidth,shiftxy,barcolor,True,imageoutlib);
