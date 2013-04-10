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

    $FileInfo: upca.py - Last Update: 04/10/2013 Ver. 2.3.7 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
import re, os, sys, types, upcean.prepil, upcean.validate, upcean.convert;
import upcean.ean2, upcean.ean5;
from PIL import Image, ImageDraw, ImageFont;
from upcean.prepil import *;
from upcean.validate import *;
from upcean.convert import *;
from upcean.ean2 import *;
from upcean.ean5 import *;

def create_upca(upc,outfile="./upca.png",resize=1,hideinfo=(False, False, False),barheight=(47, 53)):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
 upc_pieces = None; supplement = None;
 if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
  upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
  upc_pieces = upc_pieces[0];
  upc = upc_pieces[0]; supplement = upc_pieces[2];
 if(len(upc)==8):
  upc = convert_upce_to_upca(upc);
 if(len(upc)==13):
  upc = convert_ean13_to_upca(upc);
 if(len(upc)==11):
  upc = upc+validate_upca(upc,True);
 if(len(upc)>12 or len(upc)<12):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(validate_upca(upc)==False):
  pre_matches = re.findall("^(\d{11})", upc); 
  upc = pre_matches[0]+str(validate_upca(pre_matches[0],True));
 upc_matches = re.findall("(\d{1})(\d{5})(\d{5})(\d{1})", upc);
 if(len(upc_matches)<=0):
  return False;
 upc_matches = upc_matches[0];
 PrefixDigit = upc_matches[0];
 LeftDigit = list(str(upc_matches[0])+str(upc_matches[1]));
 RightDigit = list(str(upc_matches[2])+str(upc_matches[3]));
 CheckDigit = upc_matches[3];
 addonsize = 0;
 if(supplement!=None and len(supplement)==2): 
  addonsize = 29;
 if(supplement!=None and len(supplement)==5): 
  addonsize = 56;
 upc_preimg = Image.new("RGB", (113 + addonsize, barheight[1] + 9));
 upc_img = ImageDraw.Draw(upc_preimg);
 upc_img.rectangle([(0, 0), (113 + addonsize, barheight[1] + 9)], fill=(256, 256, 256));
 text_color = (0, 0, 0);
 alt_text_color = (256, 256, 256);
 if(hidetext==False):
  if(hidesn!=None and hidesn!=True):
   drawColorText(upc_img, 10, 2, barheight[0], upc_matches[0], text_color);
  drawColorText(upc_img, 10, 22, barheight[0], upc_matches[1], text_color);
  drawColorText(upc_img, 10, 61, barheight[0], upc_matches[2], text_color);
  if(hidecd!=None and hidecd!=True):
   drawColorText(upc_img, 10, 106, barheight[0], upc_matches[3], text_color);
 drawColorLine(upc_img, 0, 10, 0, barheight[0], alt_text_color);
 drawColorLine(upc_img, 1, 10, 1, barheight[0], alt_text_color);
 drawColorLine(upc_img, 2, 10, 2, barheight[0], alt_text_color);
 drawColorLine(upc_img, 3, 10, 3, barheight[0], alt_text_color);
 drawColorLine(upc_img, 4, 10, 4, barheight[0], alt_text_color);
 drawColorLine(upc_img, 5, 10, 5, barheight[0], alt_text_color);
 drawColorLine(upc_img, 6, 10, 6, barheight[0], alt_text_color);
 drawColorLine(upc_img, 7, 10, 7, barheight[0], alt_text_color);
 drawColorLine(upc_img, 8, 10, 8, barheight[0], alt_text_color);
 drawColorLine(upc_img, 9, 10, 9, barheight[1], text_color);
 drawColorLine(upc_img, 10, 10, 10, barheight[1], alt_text_color);
 drawColorLine(upc_img, 11, 10, 11, barheight[1], text_color);
 NumZero = 0; 
 LineStart = 12;
 while (NumZero < len(LeftDigit)):
  if(NumZero!=0): 
   LineSize = barheight[0];
  if(NumZero==0): 
   LineSize = barheight[1];
  if(hidetext==True):
   LineSize = barheight[1];
  left_text_color = [0, 0, 0, 0, 0, 0, 0];
  if(int(LeftDigit[NumZero])==0): 
   left_text_color = [0, 0, 0, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_text_color = [0, 0, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_text_color = [0, 0, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_text_color = [0, 1, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_text_color = [0, 1, 0, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_text_color = [0, 1, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_text_color = [0, 1, 0, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_text_color = [0, 1, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_text_color = [0, 1, 1, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==9):
   left_text_color = [0, 0, 0, 1, 0, 1, 1];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_text_color)):
   if(left_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(left_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 54, 10, 54, barheight[1], alt_text_color);
 drawColorLine(upc_img, 55, 10, 55, barheight[1], text_color);
 drawColorLine(upc_img, 56, 10, 56, barheight[1], alt_text_color);
 drawColorLine(upc_img, 57, 10, 57, barheight[1], text_color);
 drawColorLine(upc_img, 58, 10, 58, barheight[1], alt_text_color);
 NumZero = 0; 
 LineStart = 59;
 while (NumZero < len(RightDigit)):
  if(NumZero!=5): 
   LineSize = barheight[0];
  if(NumZero==5): 
   LineSize = barheight[1];
  if(hidetext==True):
   LineSize = barheight[1];
  right_text_color = [0, 0, 0, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==0): 
   right_text_color = [1, 1, 1, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==1): 
   right_text_color = [1, 1, 0, 0, 1, 1, 0];
  if(int(RightDigit[NumZero])==2): 
   right_text_color = [1, 1, 0, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==3): 
   right_text_color = [1, 0, 0, 0, 0, 1, 0];
  if(int(RightDigit[NumZero])==4): 
   right_text_color = [1, 0, 1, 1, 1, 0, 0];
  if(int(RightDigit[NumZero])==5): 
   right_text_color = [1, 0, 0, 1, 1, 1, 0];
  if(int(RightDigit[NumZero])==6): 
   right_text_color = [1, 0, 1, 0, 0, 0, 0];
  if(int(RightDigit[NumZero])==7): 
   right_text_color = [1, 0, 0, 0, 1, 0, 0];
  if(int(RightDigit[NumZero])==8): 
   right_text_color = [1, 0, 0, 1, 0, 0, 0];
  if(int(RightDigit[NumZero])==9):
   right_text_color = [1, 1, 1, 0, 1, 0, 0];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(right_text_color)):
   if(right_text_color[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, text_color);
   if(right_text_color[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, alt_text_color);
   LineStart += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 drawColorLine(upc_img, 101, 10, 101, barheight[1], text_color);
 drawColorLine(upc_img, 102, 10, 102, barheight[1], alt_text_color);
 drawColorLine(upc_img, 103, 10, 103, barheight[1], text_color);
 drawColorLine(upc_img, 104, 10, 104, barheight[0], alt_text_color);
 drawColorLine(upc_img, 105, 10, 105, barheight[0], alt_text_color);
 drawColorLine(upc_img, 106, 10, 106, barheight[0], alt_text_color);
 drawColorLine(upc_img, 107, 10, 107, barheight[0], alt_text_color);
 drawColorLine(upc_img, 108, 10, 108, barheight[0], alt_text_color);
 drawColorLine(upc_img, 109, 10, 109, barheight[0], alt_text_color);
 drawColorLine(upc_img, 110, 10, 110, barheight[0], alt_text_color);
 drawColorLine(upc_img, 111, 10, 111, barheight[0], alt_text_color);
 drawColorLine(upc_img, 112, 10, 112, barheight[0], alt_text_color);
 if(supplement!=None and len(supplement)==2): 
  upc_sup_img = create_ean2(supplement,None,1,hideinfo,barheight);
  if(upc_sup_img!=False):
   upc_preimg.paste(upc_sup_img,(113,0));
   del(upc_sup_img);
 if(supplement!=None and len(supplement)==5): 
  upc_sup_img = create_ean5(supplement,None,1,hideinfo,barheight);
  if(upc_sup_img!=False):
   upc_preimg.paste(upc_sup_img,(113,0));
   del(upc_sup_img);
 new_upc_img = upc_preimg.resize(((113 + addonsize) * int(resize), (barheight[1] + 9) * int(resize)), Image.NEAREST); # use nearest neighbour
 del(upc_img);
 del(upc_preimg);
 if(sys.version[0]=="2"):
  if(isinstance(outfile, str) or isinstance(outfile, unicode)):
   oldoutfile = outfile[:];
 if(sys.version[0]=="3"):
  if(isinstance(outfile, str)):
   oldoutfile = outfile[:];
 if(isinstance(outfile, tuple)):
  oldoutfile = tuple(outfile[:]);
 if(isinstance(outfile, list)):
  oldoutfile = list(outfile[:]);
 if(outfile is None or isinstance(outfile, bool)):
  oldoutfile = None;
 if(sys.version[0]=="2"):
  if(isinstance(oldoutfile, str) or isinstance(outfile, unicode)):
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
 if(sys.version[0]=="3"):
  if(isinstance(oldoutfile, str)):
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
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
 if(outfile is None or isinstance(outfile, bool)):
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

def draw_upca(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54)):
 return create_upca(upc,None,resize,hideinfo,barheight);
