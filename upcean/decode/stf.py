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

    $FileInfo: stf.py - Last Update: 3/27/2023 Ver. 2.8.13 RC 1 - Author: cooldude2k $
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

def decode_stf_barcode(infile="./stf.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
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
    '''upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
  except AttributeError:
   try:
    upc_img = Image.open(infile).convert('RGB');
   except UnidentifiedImageError:
    return False;
    '''prefile = open(infile, "rb");
    upc_img = Image.frombytes("RGB", (((115 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
    prefile.close();'''
 threewidebar = True;
 barsize = barwidth[0] * int(resize);
 starty = (int(upc_img.size[1] / 2) - ((barwidth[1] - 1) * 9) ) + shiftxy[1];
 if(threewidebar):
  barcode_dict = { '10101110111010': "0", '11101010101110': "1", '10111010101110': "2", '11101110101010': "3", '10101110101110': "4", '11101011101010': "5", '10111011101010': "6", '10101011101110': "7", '11101010111010': "8", '10111010111010': "9" };
 else:
  barcode_dict = { '10101110111010': "0", '11101010101110': "1", '10111010101110': "2", '11101110101010': "3", '10101110101110': "4", '11101011101010': "5", '10111011101010': "6", '10101011101110': "7", '11101010111010': "8", '10111010111010': "9" };
 startx = 17;
 if(shiftcheck):
  prestartx = shiftxy[0];
  startx = shiftxy[0];
  gotvalue = False;
  barcodesize = 0;
  while(prestartx<upc_img.size[0]):
   inprestartx = prestartx;
   substartx = prestartx + (8 * (barwidth[0] * int(resize)));
   curpixelist=[];
   if(upc_img.getpixel((inprestartx, starty))==barcolor[0]):
    if(inprestartx+(8 * (barwidth[0] * int(resize))) > upc_img.size[0]):
     return False;
    if(threewidebar):
     icount = 0;
     imaxc = 8;
     while(icount < imaxc):
      curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
      icount += 1;
     if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[0] and curpixelist[2]==barcolor[2] and curpixelist[3]==barcolor[0] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2])):
      preinprestartx = inprestartx + (8 * (barwidth[0] * int(resize)));
      precurpixelist = [];
      while(preinprestartx<upc_img.size[0]):
       precurpixelist = [];
       if((preinprestartx+(14 * (barwidth[0] * int(resize))) > upc_img.size[0])):
        return False;
       icount = 0;
       imaxc = 14;
       while(icount < imaxc):
        precurpixelist.append(upc_img.getpixel((preinprestartx+(icount * (barwidth[0] * int(resize))), starty)));
        icount += 1;
       preinprestartx += (14 * (barwidth[0] * int(resize)));
       barcodesize += 1;
       if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[2] and precurpixelist[3]==barcolor[0] and precurpixelist[4]==barcolor[2] and precurpixelist[5]==barcolor[0] and precurpixelist[6]==barcolor[0] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
        break;
      barcodesize = barcodesize - 1;
      inprestartx += (8 + (barcodesize * 14)) * (barwidth[0] * int(resize));
      icount = 0;
      imaxc = 7;
      while(icount < imaxc):
       curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
       icount += 1;
      if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[0] and curpixelist[2]==barcolor[2] and curpixelist[3]==barcolor[0] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2]) and (curpixelist[8]==barcolor[0] and curpixelist[9]==barcolor[0] and curpixelist[10]==barcolor[2] and curpixelist[11]==barcolor[0] and curpixelist[12]==barcolor[2] and curpixelist[13]==barcolor[0] and curpixelist[14]==barcolor[0])):
       startx = substartx;
       break;
    else:
     icount = 0;
     imaxc = 8;
     while(icount < imaxc):
      curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
      icount += 1;
     if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[0] and curpixelist[2]==barcolor[2] and curpixelist[3]==barcolor[0] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2])):
      preinprestartx = inprestartx + (8 * (barwidth[0] * int(resize)));
      precurpixelist = [];
      while(preinprestartx<upc_img.size[0]):
       precurpixelist = [];
       if((preinprestartx+(12 * (barwidth[0] * int(resize))) > upc_img.size[0])):
        return False;
       icount = 0;
       imaxc = 12;
       while(icount < imaxc):
        precurpixelist.append(upc_img.getpixel((preinprestartx+(icount * (barwidth[0] * int(resize))), starty)));
        icount += 1;
       preinprestartx += (12 * (barwidth[0] * int(resize)));
       barcodesize += 1;
       if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[2] and precurpixelist[3]==barcolor[0] and precurpixelist[4]==barcolor[2] and precurpixelist[5]==barcolor[0] and precurpixelist[6]==barcolor[0] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
        break;
      barcodesize = barcodesize - 1;
      inprestartx += (8 + (barcodesize * 12)) * (barwidth[0] * int(resize));
      icount = 0;
      imaxc = 7;
      while(icount < imaxc):
       curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
       icount += 1;
      if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[0] and curpixelist[2]==barcolor[2] and curpixelist[3]==barcolor[0] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2]) and (curpixelist[8]==barcolor[0] and curpixelist[9]==barcolor[0] and curpixelist[10]==barcolor[2] and curpixelist[11]==barcolor[0] and curpixelist[12]==barcolor[2] and curpixelist[13]==barcolor[0] and curpixelist[14]==barcolor[0])):
       startx = substartx;
       break;
   prestartx += 1;
  shiftxy = (0, shiftxy[1]);
 else:
  startx = ((21 * (barwidth[0] * int(resize)))  + shiftxy[0]);
  preinprestartx = startx;
  precurpixelist = [];
  barcodesize = 0;
  while(preinprestartx<upc_img.size[0]):
   precurpixelist = [];
   if(threewidebar):
    if((preinprestartx+(14 * (barwidth[0] * int(resize))) > upc_img.size[0])):
     return False;
    icount = 0;
    imaxc = 14;
    while(icount < imaxc):
     precurpixelist.append(upc_img.getpixel((preinprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    preinprestartx += (14 * (barwidth[0] * int(resize)));
    barcodesize += 1;
    if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[2] and precurpixelist[3]==barcolor[0] and precurpixelist[4]==barcolor[2] and precurpixelist[5]==barcolor[0] and precurpixelist[6]==barcolor[0] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
     break;
  startx = ((21 * (barwidth[0] * int(resize)))  + shiftxy[0]);
  preinprestartx = startx;
  precurpixelist = [];
  barcodesize = 0;
  while(preinprestartx<upc_img.size[0]):
   precurpixelist = [];
   if(threewidebar):
    if((preinprestartx+(14 * (barwidth[0] * int(resize))) > upc_img.size[0])):
     return False;
    icount = 0;
    imaxc = 14;
    while(icount < imaxc):
     precurpixelist.append(upc_img.getpixel((preinprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    preinprestartx += (14 * (barwidth[0] * int(resize)));
    barcodesize += 1;
    if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[2] and precurpixelist[3]==barcolor[0] and precurpixelist[4]==barcolor[2] and precurpixelist[5]==barcolor[0] and precurpixelist[6]==barcolor[0] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
     break;
   else:
    if((preinprestartx+(12 * (barwidth[0] * int(resize))) > upc_img.size[0])):
     return False;
    icount = 0;
    imaxc = 12;
    while(icount < imaxc):
     precurpixelist.append(upc_img.getpixel((preinprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    preinprestartx += (12 * (barwidth[0] * int(resize)));
    barcodesize += 1;
    if((precurpixelist[0]==barcolor[0] and precurpixelist[1]==barcolor[0] and precurpixelist[2]==barcolor[2] and precurpixelist[3]==barcolor[0] and precurpixelist[4]==barcolor[2] and precurpixelist[5]==barcolor[0] and precurpixelist[6]==barcolor[0] and precurpixelist[7]==barcolor[2] and precurpixelist[8]==barcolor[2])):
     break;
  barcodesize = barcodesize - 1;
 endx = int(startx + ( (barcodesize * 14 ) * (barwidth[0] * int(resize)) ));
 if(threewidebar):
  if(locatebarcode):
   postendx = endx + (5 * (barwidth[0] * int(resize)));
  endx = int(startx + ( (barcodesize * 14 ) * (barwidth[0] * int(resize)) ));
 else:
  if(locatebarcode):
   postendx = endx + (5 * (barwidth[0] * int(resize)));
  endx = int(startx + ( (barcodesize * 12 ) * (barwidth[0] * int(resize)) ));
 if(locatebarcode):
  prestartx = startx - (4 * (barwidth[0] * int(resize)));
  return ("stf", prestartx, startx, (barcodesize * 2), endx, postendx);
 startxalt = startx;
 listcount = 0;
 pre_upc_whole = [];
 prestartx = startx;
 while(startxalt < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<14):
   curpixel = upc_img.getpixel((startx, starty));
   if(curpixel==barcolor[0]):
    pre_upc_list.append("1");
   if(curpixel==barcolor[2]):
    pre_upc_list.append("0");
   startx += 1 * (barwidth[0] * int(resize));
   startxalt += 1 * (barwidth[0] * int(resize));
   listcount += 1;
  pre_upc_whole.append("".join(pre_upc_list));
 upc_img.close();
 countlist = len(pre_upc_whole);
 listcount = 0;
 barcode_list = [];
 while(listcount<countlist):
  barcode_value = barcode_dict.get(pre_upc_whole[listcount], False);
  if(not barcode_value):
   return False;
  barcode_list.append(barcode_value);
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;

def get_stf_barcode_location(infile="./stf.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_itf14_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);

def decode_code25_barcode(infile="./code25.png",resize=1,barheight=(48, 54),barwidth=(1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_stf_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def get_code25_barcode_location(infile="./code25.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_code25_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);
