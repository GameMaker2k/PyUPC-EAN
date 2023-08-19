# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2023 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: precairo.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import os, re, cairo, upcean.fonts;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

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

'''
http://stevehanov.ca/blog/index.php?id=28
'''
def snapCoords( ctx, x, y ):
 (xd, yd) = ctx.user_to_device(x, y);
 return ( round(x) + 0.5, round(y) + 0.5 );

def drawLine( ctx, x1, y1, x2, y2 ):
 point1 = snapCoords( ctx, x1, y1 );
 point2 = snapCoords( ctx, x2, y2 );
 ctx.move_to( point1[0], point1[1] );
 ctx.line_to( point2[0], point2[1] );
 ctx.set_line_width( 1.0 );
 ctx.stroke();
 return True;

def drawRectangle( ctx, x1, y1, x2, y2 ):
 point1 = snapCoords( ctx, x1, y1 );
 point2 = snapCoords( ctx, x2, y2 );
 ctx.move_to( point1[0], point1[1] );
 ctx.rectangle( point1[0], point1[1], point2[0], point2[1] )
 ctx.set_line_width( 1.0 );
 ctx.stroke();
 return True;

def drawColorRectangle( ctx, x1, y1, x2, y2, color ):
 ctx.set_source_rgb(color[0], color[1], color[2]);
 drawRectangle(ctx, x1, y1, x2, y2);
 ctx.close_path();
 return True;

def drawColorLine( ctx, x1, y1, x2, y2, width, color ):
 ctx.set_source_rgb(color[0], color[1], color[2]);
 if(width < 1):
  width = 1;
 width -= 1;
 if(width < 1):
  drawLine(ctx, x1, y1, x2, y2);
 else:
  drawRectangle(ctx, x1, y1, x2 + width, y2);
 ctx.close_path();
 return True;

def drawText( ctx, size, x, y, text, ftype = "ocrb"  ):
 text = str(text);
 point1 = snapCoords( ctx, x, y );
 ctx.select_font_face( "Monospace" );
 ctx.set_font_size( size );
 fo = cairo.FontOptions();
 fo.set_antialias(cairo.ANTIALIAS_DEFAULT);
 fo.set_hint_style(cairo.HINT_STYLE_FULL);
 fo.set_hint_metrics(cairo.HINT_METRICS_ON);
 ctx.set_font_options(fo);
 ctx.move_to( point1[0], point1[1] );
 ctx.show_text( text );
 ctx.stroke();
 return True;

def drawColorText( ctx, size, x, y, text, color, ftype = "ocrb"  ):
 text = str(text);
 ctx.set_source_rgb(color[0], color[1], color[2]);
 drawText(ctx, size, x, y, text, ftype);
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
  elif(outfileext=="SVG"):
   outfileext = "SVG";
  elif(outfileext=="PDF"):
   outfileext = "PDF";
  elif(outfileext=="PS"):
   outfileext = "PS";
  elif(outfileext=="EPS"):
   outfileext = "EPS";
  else:
   outfileext = "PNG";
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
