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

    FileInfo: ean5.py - Last Update: 04/02/2013 Ver. 2.3.5 RC 1 - Author: cooldude2k 
'''

import re, os, sys, types, upcean.prepil;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;

def create_ean5(upc,outfile="./ean5.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 if(len(upc)>5 or len(upc)<5): 
  return False;
 upc_matches = re.findall("(\d{5})", upc);
 if(len(upc_matches)<=0): 
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 LeftDigit = list(upc_matches[0]);
 CheckSum = (int(LeftDigit[0]) * 3) + (int(LeftDigit[1]) * 9) + (int(LeftDigit[2]) * 3) + (int(LeftDigit[3]) * 9) + (int(LeftDigit[4]) * 3);
 CheckSum = CheckSum % 10;
 upc_preimg = Image.new("RGB", (56, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (56, barheight[1] + 9)], fill=(256, 256, 256));
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  drawColorText(upc_img, 10, 7, barheight[0], LeftDigit[0], text_color);
  drawColorText(upc_img, 10, 16, barheight[0], LeftDigit[1], text_color);
  drawColorText(upc_img, 10, 24, barheight[0], LeftDigit[2], text_color);
  drawColorText(upc_img, 10, 32, barheight[0], LeftDigit[3], text_color);
  drawColorText(upc_img, 10, 40, barheight[0], LeftDigit[4], text_color);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 10, 0, LineSize, alt_text_color);
 drawColorLine(upc_img, 1, 10, 1, LineSize, text_color);
 drawColorLine(upc_img, 2, 10, 2, LineSize, alt_text_color);
 drawColorLine(upc_img, 3, 10, 3, LineSize, text_color);
 drawColorLine(upc_img, 4, 10, 4, LineSize, text_color);
 NumZero = 0; 
 LineStart = 5;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_text_color_l = [0, 0, 0, 0, 0, 0, 0]; 
  left_text_color_g = [1, 1, 1, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==0): 
   left_text_color_l = [0, 0, 0, 1, 1, 0, 1]; 
   left_text_color_g = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_text_color_l = [0, 0, 1, 1, 0, 0, 1]; 
   left_text_color_g = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_text_color_l = [0, 0, 1, 0, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_text_color_l = [0, 1, 1, 1, 1, 0, 1]; 
   left_text_color_g = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_text_color_l = [0, 1, 0, 0, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_text_color_l = [0, 1, 1, 0, 0, 0, 1]; 
   left_text_color_g = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_text_color_l = [0, 1, 0, 1, 1, 1, 1]; 
   left_text_color_g = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_text_color_l = [0, 1, 1, 1, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_text_color_l = [0, 1, 1, 0, 1, 1, 1]; 
   left_text_color_g = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9): 
   left_text_color_l = [0, 0, 0, 1, 0, 1, 1]; 
   left_text_color_g = [0, 0, 1, 0, 1, 1, 1];
  left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==0 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==0 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==0 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==1 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==1 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==1 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==2 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==2 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==0):
   left_text_color = left_text_color_g;
  if(CheckSum==3 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==3 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==4 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==4 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==4 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==5 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==5 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==5 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==6 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==6 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==7 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==7 and NumZero==3):
   left_text_color = left_text_color_g;
  if(CheckSum==7 and NumZero==4):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==1):
   left_text_color = left_text_color_g;
  if(CheckSum==8 and NumZero==2):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==8 and NumZero==4):
   left_text_color = left_text_color_g;
  if(CheckSum==9 and NumZero==0):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==1):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==2):
   left_text_color = left_text_color_g;
  if(CheckSum==9 and NumZero==3):
   left_text_color = left_text_color_l;
  if(CheckSum==9 and NumZero==4):
   left_text_color = left_text_color_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero < 4):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   LineStart += 1;
  NumZero += 1;
 new_upc_img = upc_preimg.resize((56 * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
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

def draw_ean5(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_ean5(upc,None,resize,hideinfo,barheight);
