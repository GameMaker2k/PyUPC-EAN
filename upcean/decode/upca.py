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

    $FileInfo: upca.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.encode.getsfname, upcean.support;
try:
 from PIL import Image, UnidentifiedImageError;
 hasuie = True;
except ImportError:
 from PIL import Image;
 hasuie = False;
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
pillowsupport = upcean.support.check_for_pillow();
cairosupport = upcean.support.check_for_cairo();
from upcean.encode.predraw import *;
if(cairosupport):
 import cairo;

def decode_upca_barcode(infile="./upca.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 if(not re.findall(r"^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
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
   if(hasuie):
    try:
     upc_img = Image.open(infile).convert('RGB');
    except UnidentifiedImageError:
     return False;
     '''upc_img = Image.frombytes("RGB", (((113 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
   else:
    try:
     upc_img = Image.open(infile).convert('RGB');
    except IOError:
     return False;
     '''upc_img = Image.frombytes("RGB", (((113 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), infile.read());'''
  except AttributeError:
   if(hasuie):
    try:
     upc_img = Image.open(infile).convert('RGB');
    except UnidentifiedImageError:
     return False;
     '''prefile = open(infile, "rb");
     upc_img = Image.frombytes("RGB", (((113 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
     prefile.close();'''
   else:
    try:
     upc_img = Image.open(infile).convert('RGB');
    except IOError:
     return False;
     '''prefile = open(infile, "rb");
     upc_img = Image.frombytes("RGB", (((113 * barwidth[0]) ) * int(resize), (barheight[1] + 9) * int(resize)), prefile.read());
     prefile.close();'''
 barsize = barwidth[0] * int(resize);
 starty = (int(upc_img.size[1] / 2) - ((barwidth[1] - 1) * 6) ) + shiftxy[1];
 left_barcode_dict = { '0001101': "0", '0011001': "1", '0010011': "2", '0111101': "3", '0100011': "4", '0110001': "5", '0101111': "6", '0111011': "7", '0110111': "8", '0001011': "9" };
 right_barcode_dict = { '1110010': "0", '1100110': "1", '1101100': "2", '1000010': "3", '1011100': "4", '1001110': "5", '1010000': "6", '1000100': "7", '1001000': "8", '1110100': "9" };
 startx = 12;
 if(shiftcheck):
  prestartx = shiftxy[0];
  startx = shiftxy[0];
  gotvalue = False;
  while(prestartx<upc_img.size[0]):
   inprestartx = prestartx;
   substartx = prestartx + (3 * (barwidth[0] * int(resize)));
   curpixelist=[];
   if(upc_img.getpixel((inprestartx, starty))==barcolor[0]):
    if(inprestartx+(2 * (barwidth[0] * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 3;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    inprestartx += (3 + 42) * (barwidth[0] * int(resize));
    jumpcode = inprestartx;
    if(inprestartx+(4 * (barwidth[0] * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 5;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    inprestartx += (5 + 42) * (barwidth[0] * int(resize));
    if(inprestartx+(2 * (barwidth[0] * int(resize))) > upc_img.size[0]):
     return False;
    icount = 0;
    imaxc = 3;
    while(icount < imaxc):
     curpixelist.append(upc_img.getpixel((inprestartx+(icount * (barwidth[0] * int(resize))), starty)));
     icount += 1;
    if((curpixelist[0]==barcolor[0] and curpixelist[1]==barcolor[2] and curpixelist[2]==barcolor[0]) and (curpixelist[3]==barcolor[2] and curpixelist[4]==barcolor[0] and curpixelist[5]==barcolor[2] and curpixelist[6]==barcolor[0] and curpixelist[7]==barcolor[2]) and (curpixelist[8]==barcolor[0] and curpixelist[9]==barcolor[2] and curpixelist[10]==barcolor[0])):
     startx = substartx;
     break;
   prestartx += 1;
  shiftxy = (0, shiftxy[1]);
 else:
  startx = ((12 * (barwidth[0] * int(resize)))  + shiftxy[0]);
  jumpcode = ((54 * (barwidth[0] * int(resize))) + shiftxy[0]);
 endx = (42 + 42) * (barwidth[0] * int(resize));
 if(locatebarcode):
  prestartx = startx - (3 * (barwidth[0] * int(resize)));
  jumpcodeend = jumpcode + (4 * (barwidth[0] * int(resize)));
  endx = startx + ((42 + 4 + 42) * (barwidth[0] * int(resize)));
  postendx = endx + (3 * (barwidth[0] * int(resize)));
  countyup = starty;
  while(countyup >= 0):
   curonepixel = upc_img.getpixel((prestartx, countyup));
   curtwopixel = upc_img.getpixel((prestartx + (1 * (barwidth[0] * int(resize))), countyup));
   if(curonepixel==barcolor[2] or curtwopixel==barcolor[0]):
    break;
   countyup += 1;
  countyup -= 1;
  countydown = starty;
  while(countydown <= upc_img.size[1]):
   curonepixel = upc_img.getpixel((prestartx, countydown));
   curtwopixel = upc_img.getpixel((prestartx + (1 * (barwidth[0] * int(resize))), countydown));
   if(curonepixel==barcolor[2] or curtwopixel==barcolor[0]):
    break;
   countydown -= 1;
  countydown -= 1;
  return ("upca", prestartx, startx, jumpcode, jumpcodeend, endx, countyup, round(countyup / 2), round(countydown * 2), countydown, countyup, 12);
 startxalt = 0;
 listcount = 0;
 pre_upc_whole = [];
 while(startxalt < endx):
  listcount = 0;
  pre_upc_list = [];
  while(listcount<7):
   if(startx==jumpcode):
    startx += 5 * (barwidth[0] * int(resize));
   curpixel = upc_img.getpixel((startx, starty));
   if(curpixel==barcolor[0]):
    incount = 0;
    inbarwidth = barwidth[0] - 1;
    while(incount<=inbarwidth):
     incurpixel = upc_img.getpixel((startx + incount, starty));
     if(incurpixel!=barcolor[0]):
      return False;
     incount += 1;
    pre_upc_list.append("1");
   if(curpixel==barcolor[2]):
    incount = 0;
    inbarwidth = barwidth[0] - 1;
    while(incount<=inbarwidth):
     incurpixel = upc_img.getpixel((startx + incount, starty));
     if(incurpixel!=barcolor[2]):
      return False;
     incount += 1;
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
  if(listcount<6):
   leftbarcodevalue = left_barcode_dict.get(pre_upc_whole[listcount], False);
   if(not leftbarcodevalue):
    return False;
   barcode_list.append(leftbarcodevalue);
  if(listcount>5):
   rightbarcodevalue = right_barcode_dict.get(pre_upc_whole[listcount], False);
   if(not rightbarcodevalue):
    return False;
   barcode_list.append(rightbarcodevalue);
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;

def get_upca_barcode_location(infile="./upca.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_upca_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);

def decode_ean12_barcode(infile="./ean12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_upca_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def decode_gtin12_barcode(infile="./gtin12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_upca_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def get_ean12_barcode_location(infile="./ean12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_ean12_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);

def get_gtin12_barcode_location(infile="./gtin12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_gtin12_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);

def decode_ucc12_barcode(infile="./ucc12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),locatebarcode=False,imageoutlib="pillow"):
 return decode_upca_barcode(infile,resize,barheight,barwidth,barcolor,locatebarcode,imageoutlib);

def get_ucc12_barcode_location(infile="./ucc12.png",resize=1,barheight=(48, 54),barwidth=(1, 1),shiftcheck=False,shiftxy=(0, 0),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return decode_ucc12_barcode(infile,resize,barheight,barwidth,shiftcheck,shiftxy,barcolor,True,imageoutlib);
