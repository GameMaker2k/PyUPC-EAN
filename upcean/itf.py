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

    $FileInfo: itf.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
import cairo, re, upcean.precairo;
import upcean.ean2, upcean.ean5;
from upcean.precairo import *;

def create_itf(upc,outfile="./itf.png",resize=1,hidecd=False):
	if(len(upc) % 2):
		return False;
	if(len(upc) < 6):
		return False;
	if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
		resize = 1;
	upc_matches = list(upc);
	upci = 0;
	new_upc_matches = [];
	while (upci < len(upc_matches) / 2):
		new_upc_matches.append(upc_matches[upci*2]+upc_matches[(upci*2)+1]);
		upci += 1;
	upc_matches = new_upc_matches;
	del(new_upc_matches);
	upc_size_add = len(upc_matches) * 18;
	if(len(upc_matches)<=0):
		return False;
	upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 39 + upc_size_add, 62);
	upc_img = cairo.Context (upc_preimg);
	upc_img.set_antialias(cairo.ANTIALIAS_NONE);
	upc_img.rectangle(0, 0, 39 + upc_size_add, 62);
	upc_img.set_source_rgb(256, 256, 256);
	upc_img.fill();
	text_color = [0, 0, 0];
	alt_text_color = [256, 256, 256];
	NumTxtZero = 0; 
	LineTxtStart = 18;
	while (NumTxtZero < len(upc_matches)):
		ArrayDigit = list(upc_matches[NumTxtZero]);
		drawColorText(upc_img, 10, LineTxtStart, 57, ArrayDigit[0], text_color);
		LineTxtStart += 9;
		drawColorText(upc_img, 10, LineTxtStart, 57, ArrayDigit[1], text_color);
		LineTxtStart += 9;
		NumTxtZero += 1;
	drawColorLine(upc_img, 0, 4, 0, 48, alt_text_color);
	drawColorLine(upc_img, 1, 4, 1, 48, alt_text_color);
	drawColorLine(upc_img, 2, 4, 2, 48, alt_text_color);
	drawColorLine(upc_img, 3, 4, 3, 48, alt_text_color);
	drawColorLine(upc_img, 4, 4, 4, 48, alt_text_color);
	drawColorLine(upc_img, 5, 4, 5, 48, alt_text_color);
	drawColorLine(upc_img, 6, 4, 6, 48, alt_text_color);
	drawColorLine(upc_img, 7, 4, 7, 48, alt_text_color);
	drawColorLine(upc_img, 8, 4, 8, 48, alt_text_color);
	drawColorLine(upc_img, 9, 4, 9, 48, alt_text_color);
	drawColorLine(upc_img, 10, 4, 10, 48, alt_text_color);
	drawColorLine(upc_img, 11, 4, 11, 48, alt_text_color);
	drawColorLine(upc_img, 12, 4, 12, 48, alt_text_color);
	drawColorLine(upc_img, 13, 4, 13, 48, text_color);
	drawColorLine(upc_img, 14, 4, 14, 48, alt_text_color);
	drawColorLine(upc_img, 15, 4, 15, 48, text_color);
	drawColorLine(upc_img, 16, 4, 16, 48, alt_text_color);
	NumZero = 0; 
	LineStart = 17; 
	LineSize = 48;
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
	drawColorLine(upc_img, 17 + upc_size_add, 4, 17 + upc_size_add, 48, text_color);
	drawColorLine(upc_img, 18 + upc_size_add, 4, 18 + upc_size_add, 48, text_color);
	drawColorLine(upc_img, 19 + upc_size_add, 4, 19 + upc_size_add, 48, text_color);
	drawColorLine(upc_img, 20 + upc_size_add, 4, 20 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 21 + upc_size_add, 4, 21 + upc_size_add, 48, text_color);
	drawColorLine(upc_img, 22 + upc_size_add, 4, 22 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 23 + upc_size_add, 4, 23 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 24 + upc_size_add, 4, 24 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 25 + upc_size_add, 4, 25 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 26 + upc_size_add, 4, 26 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 27 + upc_size_add, 4, 27 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 28 + upc_size_add, 4, 28 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 29 + upc_size_add, 4, 29 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 30 + upc_size_add, 4, 30 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 31 + upc_size_add, 4, 31 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 32 + upc_size_add, 4, 32 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 33 + upc_size_add, 4, 33 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 34 + upc_size_add, 4, 34 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 35 + upc_size_add, 4, 35 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 36 + upc_size_add, 4, 36 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 37 + upc_size_add, 4, 37 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 38 + upc_size_add, 4, 38 + upc_size_add, 48, alt_text_color);
	drawColorLine(upc_img, 39 + upc_size_add, 4, 39 + upc_size_add, 48, alt_text_color);
	upc_imgpat = cairo.SurfacePattern(upc_preimg);
	scaler = cairo.Matrix();
	scaler.scale(1/int(resize),1/int(resize));
	upc_imgpat.set_matrix(scaler);
	upc_imgpat.set_filter(cairo.FILTER_BEST);
	new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (39 + upc_size_add) * int(resize), 62 * int(resize));
	new_upc_img = cairo.Context(new_upc_preimg);
	new_upc_img.set_source(upc_imgpat);
	new_upc_img.paint();
	del(upc_preimg);
	new_upc_preimg.write_to_png(outfile);
	return True;
