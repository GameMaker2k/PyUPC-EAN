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

    $FileInfo: code39.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, sys, upcean.encode.getsfname, upcean.support;
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
if(pilsupport):
 import upcean.encode.prepil;
if(cairosupport):
 import upcean.encode.precairo;

def create_code39_barcode(upc,outfile="./code39.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 upc = str(upc);
 hidesn = hideinfo[0];
 hidecd = hideinfo[1];
 hidetext = hideinfo[2];
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
 if(outfile is None):
  if(imageoutlib=="cairosvg"):
   oldoutfile = None;
   outfile = None;
   outfileext = "SVG";
  else:
   oldoutfile = None;
   outfile = None;
   outfileext = None;
 else:
  oldoutfile = upcean.encode.getsfname.get_save_filename(outfile, imageoutlib);
  if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
   del(outfile);
   outfile = oldoutfile[0];
   outfileext = oldoutfile[1];
   if(cairosupport and imageoutlib=="cairo" and outfileext=="SVG"):
    imageoutlib = "cairosvg";
   if(cairosupport and imageoutlib=="cairosvg" and outfileext!="SVG"):
    imageoutlib = "cairo";
 if(len(upc) < 1):
  return False;
 if(not re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
  return False;
 if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
  resize = 1;
 if(pilsupport and imageoutlib=="pillow"):
  try:
   pil_ver = Image.PILLOW_VERSION;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
   pil_is_pillow = True;
  except AttributeError:
   try:
    pil_ver = Image.VERSION;
    pil_is_pillow = False;
   except AttributeError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except NameError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
  except NameError:
   try:
    pil_ver = Image.VERSION;
    pil_is_pillow = False;
   except AttributeError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   except NameError:
    pil_ver = Image.__version__;
    pil_is_pillow = True;
   pil_ver = pil_ver.split(".");
   pil_ver = [int(x) for x in pil_ver];
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
  pil_prevercheck = [str(x) for x in pil_ver];
  pil_vercheck = int(pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2]);
  if(pil_is_pillow and pil_vercheck>=210 and pil_vercheck<220):
   pil_addon_fix = int(resize) * 2;
   cairo_addon_fix = 0;
 elif(pilsupport and imageoutlib=="pillow"):
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
 elif(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  pil_addon_fix = 0;
  cairo_addon_fix = (8 * (int(resize) ) );
 else:
  pil_addon_fix = 0;
  cairo_addon_fix = 0;
 upc = upc.upper();
 upc_matches = list(upc);
 upc_size_add = ((len(upc_matches) * 15) + (len(upc_matches) + 1)) * barwidth[0];
 if(len(upc_matches)<=0):
  return False;
 if(pilsupport and imageoutlib=="pillow"):
  upc_preimg = Image.new("RGB", ((50 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1])));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((50 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]))], fill=barcolor[2]);
 if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  if(outfileext=="SVG"):
   upc_preimg = cairo.SVGSurface(None, (50 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  elif(outfileext=="PDF"):
   upc_preimg = cairo.PDFSurface(None, (50 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
  elif(outfileext=="PS" or outfileext=="EPS"):
   upc_preimg = cairo.PSSurface(None, (50 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
   if(outfileext=="EPS"):
    upc_preimg.set_eps(True);
   else:
    upc_preimg.set_eps(False);
  else:
   upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (50 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (50 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0];
 LineStart = 0;
 BarNum = 0;
 start_bc_num_end = len(start_barcode);
 while(BarNum < start_bc_num_end):
  if(start_barcode[BarNum]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
  if(start_barcode[BarNum]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
  LineStart += barwidth[0];
  BarNum += 1;
 NumZero = 0;
 while (NumZero < len(upc_matches)):
  left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="0"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="1"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="2"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="3"):
   left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="4"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="5"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="6"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="7"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="8"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="9"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="A"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="B"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="C"):
   left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="D"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="E"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="F"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="G"):
   left_barcolor = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="H"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="I"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="J"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="K"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="L"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="M"):
   left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="N"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="O"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="P"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="Q"):
   left_barcolor = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="R"):
   left_barcolor = [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="S"):
   left_barcolor = [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="T"):
   left_barcolor = [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="U"):
   left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="V"):
   left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="W"):
   left_barcolor = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="X"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="Y"):
   left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="Z"):
   left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="-"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1];
  if(upc_matches[NumZero]=="."):
   left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]==" "):
   left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1];
  if(upc_matches[NumZero]=="$"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1];
  if(upc_matches[NumZero]=="/"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="+"):
   left_barcolor = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
  if(upc_matches[NumZero]=="%"):
   left_barcolor = [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1];
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
    LineStart += barwidth[0];
    BarNum += 1;
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
    LineStart += barwidth[0];
    BarNum += 1;
   InnerUPCNum += 1;
  drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
  LineStart += barwidth[0];
  BarNum += 1;
  NumZero += 1;
 end_barcode = [0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0];
 end_bc_num = 0;
 end_bc_num_end = len(end_barcode);
 while(end_bc_num < end_bc_num_end):
  if(end_barcode[end_bc_num]==1):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
  if(end_barcode[end_bc_num]==0):
   drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
  end_bc_num += 1;
  LineStart += barwidth[0];
  BarNum += 1;
 if(pilsupport and imageoutlib=="pillow"):
  new_upc_img = upc_preimg.resize((((50 * barwidth[0]) + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize)), Image.NEAREST); # use nearest neighbour
  del(upc_img);
  del(upc_preimg);
  upc_img = ImageDraw.Draw(new_upc_img);
 if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  upc_imgpat = cairo.SurfacePattern(upc_preimg);
  scaler = cairo.Matrix();
  scaler.scale(1/int(resize),1/int(resize));
  upc_imgpat.set_matrix(scaler);
  upc_imgpat.set_filter(cairo.FILTER_NEAREST);
  if(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS"):
   if(outfile is None):
    imgoutfile = None;
   else:
    if(sys.version[0]=="2"):
     imgoutfile = StringIO();
    if(sys.version[0]>="3"):
     imgoutfile = BytesIO();
   if(outfileext=="SVG"):
    new_upc_preimg = cairo.SVGSurface(imgoutfile, ((50 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PDF"):
    new_upc_preimg = cairo.PDFSurface(imgoutfile, ((50 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PS" or outfileext=="EPS"):
    new_upc_preimg = cairo.PSSurface(imgoutfile, ((50 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
    if(outfileext=="EPS"):
     new_upc_preimg.set_eps(True);
    else:
     new_upc_preimg.set_eps(False);
   else:
    new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((50 * barwidth[0]) + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize));
  else:
   new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, ((50 * barwidth[0]) + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize));
  new_upc_img = cairo.Context(new_upc_preimg);
  new_upc_img.set_source(upc_imgpat);
  new_upc_img.paint();
  upc_img = new_upc_img;
 if(not hidetext):
  drawColorText(upc_img, 10 * int(resize * barwidth[1]), (14 * int(resize)) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), "*", barcolor[1], "ocrb", imageoutlib);
  NumTxtZero = 0;
  LineTxtStart = 30 * int(resize);
  while (NumTxtZero < len(upc_matches)):
   drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (int(resize) - 1)) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_matches[NumTxtZero], barcolor[1], "ocrb", imageoutlib);
   LineTxtStart += 16 * int(resize);
   NumTxtZero += 1;
 if(not hidetext):
  drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (int(resize) - 1)) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), "*", barcolor[1], "ocrb", imageoutlib);
 del(upc_img);
 exargdict = {};
 if(oldoutfile is None or isinstance(oldoutfile, bool)):
  if(pilsupport and imageoutlib=="pillow"):
   return new_upc_img;
  if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
   return new_upc_preimg;
 if(sys.version[0]=="2"):
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   stdoutfile = StringIO();
   if(outfileext=="WEBP"):
    exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
   elif(outfileext=="JPEG"):
    exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
   elif(outfileext=="PNG"):
    exargdict.update( { 'optimize': True, 'compress_level': 9 } );
   else:
    exargdict = {};
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_img.tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XBM"):
      stdoutfile.write(new_upc_img.convert(mode="1").tobitmap());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XPM"):
      new_upc_img.convert(mode="P").save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_img.save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
    if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_preimg.get_data().tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
      new_upc_preimg.flush();
      new_upc_preimg.finish();
      imgoutfile.seek(0);
      svgouttext = imgoutfile.read();
      stdoutfile.write(svgouttext);
      imgoutfile.close();
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_preimg.write_to_png(stdoutfile);
      stdoutfile.seek(0);
      return stdoutfile;
   except:
    return False;
 if(sys.version[0]>="3"):
  stdoutfile = BytesIO();
  if(outfile=="-" or outfile=="" or outfile==" " or outfile is None):
   if(outfileext=="WEBP"):
    exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
   elif(outfileext=="JPEG"):
    exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
   elif(outfileext=="PNG"):
    exargdict.update( { 'optimize': True, 'compress_level': 9 } );
   else:
    exargdict = {};
   try:
    if(pilsupport and imageoutlib=="pillow"):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_img.tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XBM"):
      stdoutfile.write(new_upc_img.convert(mode='1').tobitmap());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="XPM"):
      new_upc_img.convert(mode="P").save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_img.save(stdoutfile, outfileext, **exargdict);
      stdoutfile.seek(0);
      return stdoutfile;
    if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
     if(outfileext=="BYTES"):
      stdoutfile.write(new_upc_preimg.get_data().tobytes());
      stdoutfile.seek(0);
      return stdoutfile;
     elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
      new_upc_preimg.flush();
      new_upc_preimg.finish();
      imgoutfile.seek(0);
      svgouttext = imgoutfile.read();
      stdoutfile.write(svgouttext);
      imgoutfile.close();
      stdoutfile.seek(0);
      return stdoutfile;
     else:
      new_upc_preimg.write_to_png(stdoutfile);
      stdoutfile.seek(0);
      return stdoutfile;
   except:
    return False;
 if(outfile!="-" and outfile!="" and outfile!=" "):
  if(outfileext=="WEBP"):
   exargdict.update( { 'lossless': True, 'quality': 100, 'method': 6 } );
  elif(outfileext=="JPEG"):
   exargdict.update( { 'quality': 95, 'optimize': True, 'progressive': True } );
  elif(outfileext=="PNG"):
   exargdict.update( { 'optimize': True, 'compress_level': 9 } );
  else:
   exargdict = {};
  try:
   if(pilsupport and imageoutlib=="pillow"):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_img.tobytes());
    elif(outfileext=="XBM"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_preimg.get_data().tobytes());
    elif(outfileext=="XPM"):
     new_upc_img.convert(mode="P").save(outfile, outfileext, **exargdict);
    else:
     new_upc_img.save(outfile, outfileext, **exargdict);
   if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
    if(outfileext=="BYTES"):
     with open(outfile, 'wb+') as f:
      f.write(new_upc_preimg.get_data().tobytes());
     return True;
    elif(outfileext=="SVG" or outfileext=="PDF" or outfileext=="PS" or outfileext=="EPS" or imageoutlib=="cairosvg"):
     new_upc_preimg.flush();
     new_upc_preimg.finish();
     imgoutfile.seek(0);
     svgouttext = imgoutfile.read();
     with open(outfile, 'wb+') as f:
      f.write(svgouttext);
     return True;
    else:
     new_upc_preimg.write_to_png(outfile);
     return True;
  except:
   return False;
 return True;

def draw_code39_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code39_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code39_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code39_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
