#!/usr/bin/python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2012 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2012 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2012 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: prepil.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

import Image, ImageDraw, ImageFont;

'''
http://stevehanov.ca/blog/index.php?id=28
'''
def snapCoords( ctx, x, y ):
 (xd, yd) = ctx.user_to_device(x, y);
 return ( round(x) + 0.5, round(y) + 0.5 );

def drawColorLine( ctx, x1, y1, x2, y2, color ):
 ctx.line((x1, y1, x2, y2), fill=color);

def drawColorRectangle( ctx, x1, y1, x2, y2, color ):
 ctx.rectangle([(x1, y1), (x2, y2)], fill=color);

def drawColorText( ctx, size, x, y, text, color ):
 font = ImageFont.load("./upcean/ISO8859-1.pil");
 text = str(text);
 ctx.text((x, y), text, font=font, fill=color);
 del(font);

def drawColorRectangleAlt( ctx, x1, y1, x2, y2, color ):
 ctx.rectangle([(x1, y1), (x2, y2)], outline=color);
    
