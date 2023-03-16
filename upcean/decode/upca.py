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

from PIL import Image;

def decode_upca_barcode(infile="./upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=1,barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
 upc_img = Image.open(infile);
 barsize = barwidth * int(resize);
 starty = int(upc_img.size[1] / 2);
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
  if(listcount<7):
   if(pre_upc_whole[listcount]=="0001101"):
    barcode_list.append("0");
   if(pre_upc_whole[listcount]=="0011001"):
    barcode_list.append("1");
   if(pre_upc_whole[listcount]=="0010011"):
    barcode_list.append("2");
   if(pre_upc_whole[listcount]=="0111101"):
    barcode_list.append("3");
   if(pre_upc_whole[listcount]=="0100011"):
    barcode_list.append("4");
   if(pre_upc_whole[listcount]=="0110001"):
    barcode_list.append("5");
   if(pre_upc_whole[listcount]=="0101111"):
    barcode_list.append("6");
   if(pre_upc_whole[listcount]=="0111011"):
    barcode_list.append("7");
   if(pre_upc_whole[listcount]=="0110111"):
    barcode_list.append("8");
   if(pre_upc_whole[listcount]=="0001011"):
    barcode_list.append("9");
  if(listcount>6):
   if(pre_upc_whole[listcount]=="1110010"):
    barcode_list.append("0");
   if(pre_upc_whole[listcount]=="1100110"):
    barcode_list.append("1");
   if(pre_upc_whole[listcount]=="1101100"):
    barcode_list.append("2");
   if(pre_upc_whole[listcount]=="1000010"):
    barcode_list.append("3");
   if(pre_upc_whole[listcount]=="1011100"):
    barcode_list.append("4");
   if(pre_upc_whole[listcount]=="1001110"):
    barcode_list.append("5");
   if(pre_upc_whole[listcount]=="1010000"):
    barcode_list.append("6");
   if(pre_upc_whole[listcount]=="1000100"):
    barcode_list.append("7");
   if(pre_upc_whole[listcount]=="1001000"):
    barcode_list.append("8");
   if(pre_upc_whole[listcount]=="1110100"):
    barcode_list.append("9");
  listcount += 1;
  upc = "".join(barcode_list);
 return upc;
