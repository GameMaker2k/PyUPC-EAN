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

    FileInfo: ean5.py - Last Update: 08/12/2013 Ver. 2.4.4 RC 2 - Author: cooldude2k 
'''

from __future__ import division, absolute_import, print_function;
import cairo, re, sys, types, upcean.precairo;
from upcean.precairo import *;

def create_ean5_supplement(upc,outfile="./ean5_supplement.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
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
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 83, barheight[1] + 8);
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, 83, barheight[1] + 8);
 upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
 upc_img.fill();
 if(hidetext==False):
  drawColorText(upc_img, 10, 5, barheight[1] + 2, LeftDigit[0], barcolor[1]);
  drawColorText(upc_img, 10, 14, barheight[1] + 2, LeftDigit[1], barcolor[1]);
  drawColorText(upc_img, 10, 22, barheight[1] + 2, LeftDigit[2], barcolor[1]);
  drawColorText(upc_img, 10, 30, barheight[1] + 2, LeftDigit[3], barcolor[1]);
  drawColorText(upc_img, 10, 38, barheight[1] + 2, LeftDigit[4], barcolor[1]);
 LineSize = barheight[0];
 if(hidetext==True):
  LineSize = barheight[1];
 drawColorLine(upc_img, 0, 10, 0, LineSize, barcolor[2]);
 drawColorLine(upc_img, 1, 10, 1, LineSize, barcolor[0]);
 drawColorLine(upc_img, 2, 10, 2, LineSize, barcolor[2]);
 drawColorLine(upc_img, 3, 10, 3, LineSize, barcolor[0]);
 drawColorLine(upc_img, 4, 10, 4, LineSize, barcolor[0]);
 NumZero = 0; 
 LineStart = 5;
 while (NumZero < len(LeftDigit)):
  LineSize = barheight[0];
  if(hidetext==True):
   LineSize = barheight[1];
  left_barcolor_l = [0, 0, 0, 0, 0, 0, 0]; 
  left_barcolor_g = [1, 1, 1, 1, 1, 1, 1];
  if(int(LeftDigit[NumZero])==0): 
   left_barcolor_l = [0, 0, 0, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 1, 1, 1];
  if(int(LeftDigit[NumZero])==1): 
   left_barcolor_l = [0, 0, 1, 1, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 0, 0, 1, 1];
  if(int(LeftDigit[NumZero])==2): 
   left_barcolor_l = [0, 0, 1, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 0, 1, 1];
  if(int(LeftDigit[NumZero])==3): 
   left_barcolor_l = [0, 1, 1, 1, 1, 0, 1]; 
   left_barcolor_g = [0, 1, 0, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==4): 
   left_barcolor_l = [0, 1, 0, 0, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 1, 1, 0, 1];
  if(int(LeftDigit[NumZero])==5): 
   left_barcolor_l = [0, 1, 1, 0, 0, 0, 1]; 
   left_barcolor_g = [0, 1, 1, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==6): 
   left_barcolor_l = [0, 1, 0, 1, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 0, 1, 0, 1];
  if(int(LeftDigit[NumZero])==7): 
   left_barcolor_l = [0, 1, 1, 1, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 0, 0, 0, 1];
  if(int(LeftDigit[NumZero])==8): 
   left_barcolor_l = [0, 1, 1, 0, 1, 1, 1]; 
   left_barcolor_g = [0, 0, 0, 1, 0, 0, 1];
  if(int(LeftDigit[NumZero])==9): 
   left_barcolor_l = [0, 0, 0, 1, 0, 1, 1]; 
   left_barcolor_g = [0, 0, 1, 0, 1, 1, 1];
  left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==0 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==0 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==0 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==1 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==1 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==1 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==2 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==2 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==0):
   left_barcolor = left_barcolor_g;
  if(CheckSum==3 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==3 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==4 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==4 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==4 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==5 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==5 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==5 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==6 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==6 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==7 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==7 and NumZero==3):
   left_barcolor = left_barcolor_g;
  if(CheckSum==7 and NumZero==4):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==1):
   left_barcolor = left_barcolor_g;
  if(CheckSum==8 and NumZero==2):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==8 and NumZero==4):
   left_barcolor = left_barcolor_g;
  if(CheckSum==9 and NumZero==0):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==1):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==2):
   left_barcolor = left_barcolor_g;
  if(CheckSum==9 and NumZero==3):
   left_barcolor = left_barcolor_l;
  if(CheckSum==9 and NumZero==4):
   left_barcolor = left_barcolor_g;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   InnerUPCNum += 1;
  if(NumZero < 4):
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[2]);
   LineStart += 1;
   drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, barcolor[0]);
   LineStart += 1;
  NumZero += 1;
 upc_imgpat = cairo.SurfacePattern(upc_preimg);
 scaler = cairo.Matrix();
 scaler.scale(1/int(resize),1/int(resize));
 upc_imgpat.set_matrix(scaler);
 upc_imgpat.set_filter(cairo.FILTER_NEAREST);
 new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 83 * int(resize), (barheight[1] + 8) * int(resize));
 new_upc_img = cairo.Context(new_upc_preimg);
 new_upc_img.set_source(upc_imgpat);
 new_upc_img.paint();
 del(upc_preimg);
 if(outfile is None or isinstance(outfile, bool)):
  return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout);
   except:
    return False;
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" "):
   try:
    new_upc_preimg.write_to_png(sys.stdout.buffer);
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  try:
   new_upc_preimg.write_to_png(outfile);
  except:
   return False;
 return True;

def draw_ean5_supplement(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5_supplement(upc,None,resize,hideinfo,barheight,barcolor);

def create_ean5(upc,outfile="./ean5.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (56 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize));
 upc_img = cairo.Context (upc_preimg);
 upc_img.set_antialias(cairo.ANTIALIAS_NONE);
 upc_img.rectangle(0, 0, (56 * int(resize)) + (8 * int(resize)), (barheight[1] + 9) * int(resize));
 upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
 upc_img.fill();
 upc_sup_img = draw_ean5_supplement(upc,resize,hideinfo,barheight,barcolor);
 if(upc_sup_img is None or isinstance(upc_sup_img, bool)):
  return False;
 upc_img.set_source_surface(upc_sup_img, 8 * int(resize), 0);
 upc_img.paint();
 del(upc_sup_img);
 del(upc_img);
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
  return upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout, outfileext);
 if(sys.version[0]=="3"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile==None):
   upc_preimg.save(sys.stdout.buffer, outfileext);
 if(outfile!="-" and outfile!="" and outfile!=" "):
  upc_preimg.save(outfile, outfileext);
 return True;

def draw_ean5(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean5(upc,None,resize,hideinfo,barheight,barcolor); 
