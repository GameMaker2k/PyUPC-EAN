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

    $FileInfo: prepil.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
from PIL import Image, ImageDraw, ImageFont;
import os, re, upcean.fonts;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

try:
 basestring;
except NameError:
 basestring = str;

fontpathocra = upcean.fonts.fontpathocra;
fontpathocraalt = upcean.fonts.fontpathocraalt;
fontpathocrb = upcean.fonts.fontpathocrb;
fontpathocrbalt = upcean.fonts.fontpathocrbalt;
fontpath = upcean.fonts.fontpath;

''' // Source: http://stevehanov.ca/blog/index.php?id=28 '''
def snapCoords( ctx, x, y ):
 (xd, yd) = ctx.user_to_device(x, y);
 return ( round(x) + 0.5, round(y) + 0.5 );

def drawColorRectangle( ctx, x1, y1, x2, y2, color ):
 ctx.rectangle([(x1, y1), (x2, y2)], fill=color);
 return True;

def drawColorLine( ctx, x1, y1, x2, y2, width, color ):
 if(width < 1):
  width = 1;
 width -= 1;
 if(width < 1):
  ctx.line((x1, y1, x2, y2), fill=color);
 else:
  ctx.rectangle([(x1, y1), (x2 + width, y2)], fill=color);
 return True;

def drawColorText( ctx, size, x, y, text, color, ftype = "ocrb" ):
 font = ImageFont.truetype(fontpathocra, size);
 if(ftype=="ocra"):
  try:
   font = ImageFont.truetype(fontpathocra, size);
  except OSError:
   font = ImageFont.truetype(fontpathocraalt, size);
 if(ftype=="ocrb"):
  try:
   font = ImageFont.truetype(fontpathocrb, size);
  except OSError:
   font = ImageFont.truetype(fontpathocrbalt, size);
 text = str(text);
 ctx.text((x, y), text, font=font, fill=color);
 del(font);
 return True;

def drawColorRectangleAlt( ctx, x1, y1, x2, y2, color ):
 ctx.rectangle([(x1, y1), (x2, y2)], outline=color);
 return True;

def get_save_filename(outfile):
 oldoutfile = None;
 if(isinstance(outfile, basestring)):
  oldoutfile = outfile[:];
 elif(isinstance(outfile, tuple)):
  oldoutfile = tuple(outfile[:]);
 elif(isinstance(outfile, list)):
  oldoutfile = list(outfile[:]);
 elif(outfile is None or isinstance(outfile, bool)):
  oldoutfile = None;
 else:
  return False;
 if(isinstance(oldoutfile, basestring)):
  if(outfile!="-" and outfile!="" and outfile!=" "):
   if(len(re.findall(r"^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))>0):
    outfileext = re.findall(r"^\.([A-Za-z]+)", os.path.splitext(outfile)[1])[0].upper();
   if(len(re.findall(r"^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))==0 and len(re.findall(r"(.*)\:([a-zA-Z]+)", oldoutfile))>0):
    tmpoutfile = re.findall(r"(.*)\:([a-zA-Z]+)", oldoutfile);
    del(outfile);
    outfile = tmpoutfile[0][0];
    outfileext = tmpoutfile[0][1].upper();
   if(len(re.findall(r"^\.([A-Za-z]+)$", os.path.splitext(oldoutfile)[1]))==0 and len(re.findall(r"(.*)\:([a-zA-Z]+)", oldoutfile))==0):
    outfileext = "PNG";
  if(outfileext=="BYTES"):
   outfileext = "BYTES";
  else:
   outfileext = Image.registered_extensions().get("."+outfileext.lower(), "PNG");
  return (outfile, outfileext.upper());
 elif(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
  del(outfile);
  outfile = oldoutfile[0];
  outfileext = oldoutfile[1];
  return (outfile, outfileext.upper());
 elif(outfile is None or isinstance(outfile, bool) or isinstance(outfile, file)):
  return outfile;
 else:
  return False;

