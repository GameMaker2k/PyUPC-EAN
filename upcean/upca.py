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

    $FileInfo: validate.py - Last Update: 02/28/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

import cairo, re, upcean.precairo, upcean.validate;
import upcean.ean2, upcean.ean5;
from upcean.precairo import *;
from upcean.validate import *;
from upcean.ean2 import *;
from upcean.ean5 import *;


def create_upca(upc,outfile="./upc.png",resize=1,hidecd=False):
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
		preg_match("/^(\d{11})/", upc, pre_matches); 
		upc = pre_matches[1]+validate_upca(pre_matches[1],True);
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
	upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, 113 + addonsize, 62);
	upc_img = cairo.Context (upc_preimg);
	upc_img.set_antialias(cairo.ANTIALIAS_NONE);
	upc_img.rectangle(0, 0, 113 + addonsize, 62);
	upc_img.set_source_rgb(256, 256, 256);
	upc_img.fill();
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
		if(NumZero!=0): 
			LineSize = 47;
		if(NumZero==0): 
			LineSize = 53;
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
	NumZero = 0; 
	LineStart = 59;
	while (NumZero < len(RightDigit)):
		if(NumZero!=5): 
			LineSize = 47;
		if(NumZero==5): 
			LineSize = 53;
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
				drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, [0, 0, 0]);
			if(right_text_color[InnerUPCNum]==0):
				drawColorLine(upc_img, LineStart, 10, LineStart, LineSize, [256, 256, 256]);
			LineStart += 1;
			InnerUPCNum += 1;
		NumZero += 1;
	drawColorLine(upc_img, 101, 10, 101, 53, [0, 0, 0]);
	drawColorLine(upc_img, 102, 10, 102, 53, [256, 256, 256]);
	drawColorLine(upc_img, 103, 10, 103, 53, [0, 0, 0]);
	drawColorLine(upc_img, 104, 10, 104, 47, [256, 256, 256]);
	drawColorLine(upc_img, 105, 10, 105, 47, [256, 256, 256]);
	drawColorLine(upc_img, 106, 10, 106, 47, [256, 256, 256]);
	drawColorLine(upc_img, 107, 10, 107, 47, [256, 256, 256]);
	drawColorLine(upc_img, 108, 10, 108, 47, [256, 256, 256]);
	drawColorLine(upc_img, 109, 10, 109, 47, [256, 256, 256]);
	drawColorLine(upc_img, 110, 10, 110, 47, [256, 256, 256]);
	drawColorLine(upc_img, 111, 10, 111, 47, [256, 256, 256]);
	drawColorLine(upc_img, 112, 10, 112, 47, [256, 256, 256]);
	if(supplement!=None and len(supplement)==2): 
		create_ean2(supplement,113,upc_img);
	if(supplement!=None and len(supplement)==5): 
		create_ean5(supplement,113,upc_img);
	upc_preimg.write_to_png(outfile);
	return True;
