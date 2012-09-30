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

    $FileInfo: upce.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

from __future__ import division;
import cairo, re, upcean.precairo, upcean.validate;
import upcean.ean2, upcean.ean5;
from upcean.precairo import *;
from upcean.validate import *;
from upcean.ean2 import *;
from upcean.ean5 import *;


def create_upce(upc,outfile="./upce.png",resize=1,hidecd=False):
	upc_pieces = None; supplement = None;
	if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc)):
		upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", upc);
		upc_pieces = upc_pieces[0];
		upc = upc_pieces[0]; supplement = upc_pieces[2];
	if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc)):
		upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", upc);
		upc_pieces = upc_pieces[0];
		upc = upc_pieces[0]; supplement = upc_pieces[2];
	if(len(upc)==12):
		upc = convert_upca_to_upce(upc);
	if(len(upc)==13):
		upc = convert_ean13_to_upce(upc);
	if(len(upc)==7):
		upc = upc+validate_upce(upc,True);
	if(len(upc)>8 or len(upc)<8):
		return False;
	if(not re.findall("^([0-9]*[\.]?[0-9])", str(resize)) or int(resize) < 1):
		resize = 1;
	if(not re.findall("^0", upc)):
		return False;
	if(validate_upce(upc)==False):
		pre_matches = re.findall("^(\d{7})", upc); 
		upc = pre_matches[1]+validate_upce(pre_matches[1],True);
	upc_matches = re.findall("(\d{1})(\d{6})(\d{1})", upc);
	upc_matches = upc_matches[0];
	if(len(upc_matches)<=0):
		return False;
	if(int(upc_matches[0])>1):
		return False;
	PrefixDigit = upc_matches[0];
	LeftDigit = list(upc_matches[1]);
	CheckDigit = upc_matches[2];
	addonsize = 0;
	if(supplement!=None and len(supplement)==2): 
		addonsize = 29;
	if(supplement!=None and len(supplement)==5): 
		addonsize = 56;
	upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 69 + addonsize, 62);
	upc_img = cairo.Context (upc_preimg);
	upc_img.set_antialias(cairo.ANTIALIAS_NONE);
	upc_img.rectangle(0, 0, 69 + addonsize, 62);
	upc_img.set_source_rgb(256, 256, 256);
	upc_img.fill();
	drawColorText(upc_img, 11, 0, 57, upc_matches[0], [0, 0, 0]);
	drawColorText(upc_img, 11, 11, 57, upc_matches[1], [0, 0, 0]);
	if(hidecd!=None and hidecd!=True):
		drawColorText(upc_img, 11, 59, 57, upc_matches[2], [0, 0, 0]);
	drawColorLine(upc_img, 0, 10, 0, 47, [256, 256, 256]);
	drawColorLine(upc_img, 1, 10, 1, 47, [256, 256, 256]);
	drawColorLine(upc_img, 2, 10, 2, 47, [256, 256, 256]);
	drawColorLine(upc_img, 3, 10, 3, 47, [256, 256, 256]);
	drawColorLine(upc_img, 4, 10, 4, 47, [256, 256, 256]);
	drawColorLine(upc_img, 5, 10, 5, 47, [256, 256, 256]);
	drawColorLine(upc_img, 6, 10, 6, 47, [256, 256, 256]);
	drawColorLine(upc_img, 7, 10, 7, 47, [256, 256, 256]);
	drawColorLine(upc_img, 8, 10, 8, 47, [256, 256, 256]);
	drawColorLine(upc_img, 9, 10, 9, 53, [0, 0, 0]);
	drawColorLine(upc_img, 10, 10, 10, 53, [256, 256, 256]);
	drawColorLine(upc_img, 11, 10, 11, 53, [0, 0, 0]);
	NumZero = 0; 
	LineStart = 12;
	while (NumZero < len(LeftDigit)):
		LineSize = 47;
		left_text_color = [0, 0, 0, 0, 0, 0, 0];
		left_text_color_odd = [0, 0, 0, 0, 0, 0, 0];
		left_text_color_even = [0, 0, 0, 0, 0, 0, 0];
		if(int(LeftDigit[NumZero])==0): 
			left_text_color_odd = [0, 0, 0, 1, 1, 0, 1]; 
			left_text_color_even = [0, 1, 0, 0, 1, 1, 1];
		if(int(LeftDigit[NumZero])==1): 
			left_text_color_odd = [0, 0, 1, 1, 0, 0, 1]; 
			left_text_color_even = [0, 1, 1, 0, 0, 1, 1];
		if(int(LeftDigit[NumZero])==2): 
			left_text_color_odd = [0, 0, 1, 0, 0, 1, 1]; 
			left_text_color_even = [0, 0, 1, 1, 0, 1, 1];
		if(int(LeftDigit[NumZero])==3): 
			left_text_color_odd = [0, 1, 1, 1, 1, 0, 1]; 
			left_text_color_even = [0, 1, 0, 0, 0, 0, 1];
		if(int(LeftDigit[NumZero])==4): 
			left_text_color_odd = [0, 1, 0, 0, 0, 1, 1]; 
			left_text_color_even = [0, 0, 1, 1, 1, 0, 1];
		if(int(LeftDigit[NumZero])==5): 
			left_text_color_odd = [0, 1, 1, 0, 0, 0, 1]; 
			left_text_color_even = [0, 1, 1, 1, 0, 0, 1];
		if(int(LeftDigit[NumZero])==6): 
			left_text_color_odd = [0, 1, 0, 1, 1, 1, 1]; 
			left_text_color_even = [0, 0, 0, 0, 1, 0, 1];
		if(int(LeftDigit[NumZero])==7): 
			left_text_color_odd = [0, 1, 1, 1, 0, 1, 1]; 
			left_text_color_even = [0, 0, 1, 0, 0, 0, 1];
		if(int(LeftDigit[NumZero])==8): 
			left_text_color_odd = [0, 1, 1, 0, 1, 1, 1]; 
			left_text_color_even = [0, 0, 0, 1, 0, 0, 1];
		if(int(LeftDigit[NumZero])==9):
			left_text_color_odd = [0, 0, 0, 1, 0, 1, 1];
			left_text_color_even = [0, 0, 1, 0, 1, 1, 1];
		left_text_color = left_text_color_odd;
		if(int(upc_matches[2])==0 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==1 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==2 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==3 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==4 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==5 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==6 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==7 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==8 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==9 and int(upc_matches[0])==0):
			if(NumZero==0): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==0 and int(upc_matches[0])==1):
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==1 and int(upc_matches[0])==1):
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==2 and int(upc_matches[0])==1):
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==3 and int(upc_matches[0])==1):
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==4 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==5 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==6 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==7 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==5): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==8 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==3): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		if(int(upc_matches[2])==9 and int(upc_matches[0])==1):
			if(NumZero==1): 
				left_text_color = left_text_color_even;
			if(NumZero==2): 
				left_text_color = left_text_color_even;
			if(NumZero==4): 
				left_text_color = left_text_color_even;
		InnerUPCNum = 0;
		while (InnerUPCNum < len(left_text_color)):
			if(left_text_color[InnerUPCNum]==1):
				drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, [0, 0, 0]);
			if(left_text_color[InnerUPCNum]==0):
				drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, [256, 256, 256]);
			LineStart += 1;
			InnerUPCNum += 1;
		NumZero += 1;
	drawColorLine(upc_img, 54, 10, 54, 53, [256, 256, 256]);
	drawColorLine(upc_img, 55, 10, 55, 53, [0, 0, 0]);
	drawColorLine(upc_img, 56, 10, 56, 53, [256, 256, 256]);
	drawColorLine(upc_img, 57, 10, 57, 53, [0, 0, 0]);
	drawColorLine(upc_img, 58, 10, 58, 53, [256, 256, 256]);
	drawColorLine(upc_img, 59, 10, 59, 53, [0, 0, 0]);
	drawColorLine(upc_img, 60, 10, 60, 47, [256, 256, 256]);
	drawColorLine(upc_img, 61, 10, 61, 47, [256, 256, 256]);
	drawColorLine(upc_img, 62, 10, 62, 47, [256, 256, 256]);
	drawColorLine(upc_img, 63, 10, 63, 47, [256, 256, 256]);
	drawColorLine(upc_img, 64, 10, 64, 47, [256, 256, 256]);
	drawColorLine(upc_img, 65, 10, 65, 47, [256, 256, 256]);
	drawColorLine(upc_img, 66, 10, 66, 47, [256, 256, 256]);
	drawColorLine(upc_img, 67, 10, 67, 47, [256, 256, 256]);
	drawColorLine(upc_img, 68, 10, 68, 47, [256, 256, 256]);
	if(supplement!=None and len(supplement)==2):
		create_ean2(supplement,69,upc_img);
	if(supplement!=None and len(supplement)==5):
		create_ean5(supplement,69,upc_img);
	upc_imgpat = cairo.SurfacePattern(upc_preimg);
	scaler = cairo.Matrix();
	scaler.scale(1/int(resize),1/int(resize));
	upc_imgpat.set_matrix(scaler);
	upc_imgpat.set_filter(cairo.FILTER_BEST);
	new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (69 + addonsize) * int(resize), 62 * int(resize));
	new_upc_img = cairo.Context(new_upc_preimg);
	new_upc_img.set_source(upc_imgpat);
	new_upc_img.paint();
	del(upc_preimg);
	new_upc_preimg.write_to_png(outfile);
	return True;
