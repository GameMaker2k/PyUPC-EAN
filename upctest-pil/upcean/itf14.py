#!/usr/bin/python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: itf14.py - Last Update: 04/02/2013 Ver. 2.3.5 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
import Image, ImageDraw, ImageFont, re, os, sys, types, upcean.prepil;
import upcean.ean2, upcean.ean5;
from upcean.prepil import *;

def create_itf14(upc,outfile="./itf14.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc) % 2):
  return False;
 if(len(upc) < 6):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_matches = re.findall("([0-9]{2})", upc);
 upc_size_add = len(upc_matches) * 18;
 if(len(upc_matches)<=0):
  return False;
 upc_preimg = Image.new("RGB", (44 + upc_size_add, barheight[0] + 15));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (44 + upc_size_add, barheight[0] + 15)], fill=(256, 256, 256));
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  NumTxtZero = 0; 
  LineTxtStart = 23;
  while (NumTxtZero < len(upc_matches)):
   ArrayDigit = list(upc_matches[NumTxtZero]);
   drawColorText(upc_img, 10, LineTxtStart, barheight[0] + 3, ArrayDigit[0], text_color);
   LineTxtStart += 9;
   drawColorText(upc_img, 10, LineTxtStart, barheight[0] + 3, ArrayDigit[1], text_color);
   LineTxtStart += 9;
   NumTxtZero += 1;
 drawColorLine(upc_img, 4, 4, 4, barheight[0], alt_text_color);
 drawColorLine(upc_img, 5, 4, 5, barheight[0], alt_text_color);
 drawColorLine(upc_img, 6, 4, 6, barheight[0], alt_text_color);
 drawColorLine(upc_img, 7, 4, 7, barheight[0], alt_text_color);
 drawColorLine(upc_img, 8, 4, 8, barheight[0], alt_text_color);
 drawColorLine(upc_img, 9, 4, 9, barheight[0], alt_text_color);
 drawColorLine(upc_img, 10, 4, 10, barheight[0], alt_text_color);
 drawColorLine(upc_img, 11, 4, 11, barheight[0], alt_text_color);
 drawColorLine(upc_img, 12, 4, 12, barheight[0], alt_text_color);
 drawColorLine(upc_img, 13, 4, 13, barheight[0], alt_text_color);
 drawColorLine(upc_img, 14, 4, 14, barheight[0], alt_text_color);
 drawColorLine(upc_img, 15, 4, 15, barheight[0], alt_text_color);
 drawColorLine(upc_img, 16, 4, 16, barheight[0], alt_text_color);
 drawColorLine(upc_img, 17, 4, 17, barheight[0], text_color);
 drawColorLine(upc_img, 18, 4, 18, barheight[0], alt_text_color);
 drawColorLine(upc_img, 19, 4, 19, barheight[0], text_color);
 drawColorLine(upc_img, 20, 4, 20, barheight[0], alt_text_color);
 NumZero = 0; 
 LineStart = 21; 
 LineSize = barheight[0];
 while (NumZero < len(upc_matches)):
  ArrayDigit = list(upc_matches[NumZero]);
  left_text_color = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[0])==0):
   left_text_color = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[0])==1):
   left_text_color = [1, 0, 0, 0, 1];
  if(int(ArrayDigit[0])==2):
   left_text_color = [0, 1, 0, 0, 1];
  if(int(ArrayDigit[0])==3):
   left_text_color = [1, 1, 0, 0, 0];
  if(int(ArrayDigit[0])==4):
   left_text_color = [0, 0, 1, 0, 1];
  if(int(ArrayDigit[0])==5):
   left_text_color = [1, 0, 1, 0, 0];
  if(int(ArrayDigit[0])==6):
   left_text_color = [0, 1, 1, 0, 0];
  if(int(ArrayDigit[0])==7):
   left_text_color = [0, 0, 0, 1, 1];
  if(int(ArrayDigit[0])==8):
   left_text_color = [1, 0, 0, 1, 0];
  if(int(ArrayDigit[0])==9):
   left_text_color = [0, 1, 0, 1, 0];
  right_text_color = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[1])==0):
   right_text_color = [0, 0, 1, 1, 0];
  if(int(ArrayDigit[1])==1):
   right_text_color = [1, 0, 0, 0, 1];
  if(int(ArrayDigit[1])==2):
   right_text_color = [0, 1, 0, 0, 1];
  if(int(ArrayDigit[1])==3):
   right_text_color = [1, 1, 0, 0, 0];
  if(int(ArrayDigit[1])==4):
   right_text_color = [0, 0, 1, 0, 1];
  if(int(ArrayDigit[1])==5):
   right_text_color = [1, 0, 1, 0, 0];
  if(int(ArrayDigit[1])==6):
   right_text_color = [0, 1, 1, 0, 0];
  if(int(ArrayDigit[1])==7):
   right_text_color = [0, 0, 0, 1, 1];
  if(int(ArrayDigit[1])==8):
   right_text_color = [1, 0, 0, 1, 0];
  if(int(ArrayDigit[1])==9):
   right_text_color = [0, 1, 0, 1, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, text_color); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, text_color); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, text_color); 
    LineStart += 1;
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, text_color); 
    LineStart += 1;
   if(right_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color); 
    LineStart += 1; 
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color); 
    LineStart += 1;
   if(right_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, alt_text_color);
    LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, barheight[0], text_color);
 drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, barheight[0], text_color);
 drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, barheight[0], text_color);
 drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, barheight[0], text_color);
 drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 40 + upc_size_add, 4, 40 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 41 + upc_size_add, 4, 41 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 42 + upc_size_add, 4, 42 + upc_size_add, barheight[0], alt_text_color);
 drawColorLine(upc_img, 43 + upc_size_add, 4, 43 + upc_size_add, barheight[0], alt_text_color);
 drawColorRectangleAlt(upc_img, 0, 0, 43 + upc_size_add, (barheight[0] + 15) - 11, text_color);
 drawColorRectangleAlt(upc_img, 1, 1, 42 + upc_size_add, (barheight[0] + 15) - 12, text_color);
 drawColorRectangleAlt(upc_img, 2, 2, 41 + upc_size_add, (barheight[0] + 15) - 13, text_color);
 drawColorRectangleAlt(upc_img, 3, 3, 40 + upc_size_add, (barheight[0] + 15) - 14, text_color);
 new_upc_img = upc_preimg.resize(((44 + upc_size_add) * int(resize), (barheight[0] + 15) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 if(type(outfile)==types.StringType):
  oldoutfile = outfile[:];
 if(type(outfile)==types.TupleType):
  oldoutfile = tuple(outfile[:]);
 if(type(outfile)==types.ListType):
  oldoutfile = list(outfile[:]);
 if(type(outfile)==types.NoneType or type(outfile)==types.BooleanType):
  oldoutfile = None;
 if(type(oldoutfile)==types.StringType):
  if(outfile!="-" and outfile!="" and outfile!=" "):
   if(len(re.findall("^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))>0):
    outfileext = re.findall("^\.([A-Za-z]+)", os.path.splitext(outfile)[1])[0].upper();
   if(len(re.findall("^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))==0 and len(re.findall("(.*)\:([a-zA-Z]+)", oldoutfile))>0):
    tmpoutfile = re.findall("(.*)\:([a-zA-Z]+)", oldoutfile);
    del(outfile);
    outfile = tmpoutfile[0][0];
    outfileext = tmpoutfile[0][1].upper();
   if(len(re.findall("^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))==0 and len(re.findall("(.*)\:([a-zA-Z]+)", oldoutfile))==0):
    outfileext = "PNG";
  if(outfileext=="DIB"):
   outfileext = "BMP";
  if(outfileext=="PS"):
   outfileext = "EPS";
  if(outfileext=="JPG" or outfileext=="JPE" or outfileext=="JFIF" or outfileext=="JFI"):
   outfileext = "JPEG";
  if(outfileext=="PBM" or outfileext=="PGM"):
   outfileext = "PPM";
  if(outfileext=="TIF"):
   outfileext = "TIFF";
  if(outfileext!="BMP" and outfileext!="EPS" and outfileext!="GIF" and outfileext!="IM" and outfileext!="JPEG" and outfileext!="PCX" and outfileext!="PDF" and outfileext!="PNG" and outfileext!="PPM" and outfileext!="TIFF" and outfileext!="XPM"):
   outfileext = "PNG";
 if(type(oldoutfile)==types.TupleType or type(oldoutfile)==types.ListType):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(type(outfile)==types.NoneType or type(outfile)==types.BooleanType):
  return new_upc_img;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   new_upc_img.save(sys.stdout, outfileext);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   new_upc_img.save(sys.stdout.buffer, outfileext);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  new_upc_img.save(outfile, outfileext);
 return True;

def draw_itf14(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_itf14(upc,None,resize,hideinfo,barheight);
