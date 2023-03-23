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

    $FileInfo: getsfname.py - Last Update: 3/23/2023 Ver. 2.8.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import sys, os, re, upcean.support;
pilsupport = upcean.support.check_for_pil();
cairosupport = upcean.support.check_for_cairo();

def get_save_filename(outfile, imageoutlib="pillow"):
 imageoutlib = imageoutlib.lower();
 if(not pilsupport and imageoutlib=="pillow"):
  imageoutlib = "cairo";
 if(not cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  imageoutlib = "pillow";
 if(not cairosupport and imageoutlib=="cairosvg"):
  imageoutlib = "pillow";
 if(imageoutlib!="pillow" and imageoutlib!="cairo" and imageoutlib!="cairosvg"):
  imageoutlib = "pillow";
 if(not pilsupport and not cairosupport):
  return False;
 if(sys.version[0]=="2"):
  if(isinstance(outfile, str) or isinstance(outfile, unicode)):
   oldoutfile = outfile[:];
 if(sys.version[0]>="3"):
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
   if(imageoutlib=="pillow"):
    if(outfileext=="DIB"):
     outfileext = "BMP";
    if(outfileext=="PS"):
     outfileext = "EPS";
    if(outfileext=="JPG" or outfileext=="JPE" or outfileext=="JFIF" or outfileext=="JFI"):
     outfileext = "JPEG";
    if(outfileext=="JP2" or outfileext=="J2K" or outfileext=="JPX" or outfileext=="JPEG2"):
     outfileext = "JPEG2000";
    if(outfileext=="PBM" or outfileext=="PGM"):
     outfileext = "PPM";
    if(outfileext=="TIF"):
     outfileext = "TIFF";
    if(outfileext=="BYTES"):
     outfileext = "BYTES";
    if(outfileext!="BMP" and outfileext!="DCX" and outfileext!="EPS" and outfileext!="GIF" and outfileext!="IM" and outfileext!="JPEG" and outfileext!="JPEG2000" and outfileext!="MSP" and outfileext!="PCX" and outfileext!="PDF" and outfileext!="PNG" and outfileext!="PPM" and outfileext!="TIFF" and outfileext!="WEBP" and outfileext!="XPM" and outfileext!="BYTES"):
     outfileext = "PNG";
   elif(imageoutlib=="pillow"):
    outfileext = "PNG";
   else:
    if(outfileext=="BYTES"):
     outfileext = "BYTES";
    elif(outfileext=="SVG"):
     outfileext = "SVG";
    else:
     outfileext = "PNG";
   return (outfile, outfileext.upper());   
 if(sys.version[0]>="3"):
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
   if(imageoutlib=="pillow"):
    if(outfileext=="DIB"):
     outfileext = "BMP";
    if(outfileext=="PS"):
     outfileext = "EPS";
    if(outfileext=="JPG" or outfileext=="JPE" or outfileext=="JFIF" or outfileext=="JFI"):
     outfileext = "JPEG";
    if(outfileext=="JP2" or outfileext=="J2K" or outfileext=="JPX" or outfileext=="JPEG2"):
     outfileext = "JPEG2000";
    if(outfileext=="PBM" or outfileext=="PGM"):
     outfileext = "PPM";
    if(outfileext=="TIF"):
     outfileext = "TIFF";
    if(outfileext=="BYTES"):
     outfileext = "BYTES";
    if(outfileext!="BMP" and outfileext!="DCX" and outfileext!="EPS" and outfileext!="GIF" and outfileext!="IM" and outfileext!="JPEG" and outfileext!="JPEG2000" and outfileext!="MSP" and outfileext!="PCX" and outfileext!="PDF" and outfileext!="PNG" and outfileext!="PPM" and outfileext!="TIFF" and outfileext!="WEBP" and outfileext!="XPM" and outfileext!="BYTES"):
     outfileext = "PNG";
   elif(imageoutlib=="pillow"):
    outfileext = "PNG";
   else:
    if(outfileext=="BYTES"):
     outfileext = "BYTES";
    elif(outfileext=="SVG"):
     outfileext = "SVG";
    else:
     outfileext = "PNG";
   return (outfile, outfileext.upper());
 if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
  return (outfile, outfileext.upper());
 if(outfile is None or isinstance(outfile, bool) or isinstance(outfile, file)):
  return outfile;
