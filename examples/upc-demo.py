#!/usr/bin/env python
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

    $FileInfo: upc-ui.py - Last Update: 2/18/2023 Ver. 2.7.22 RC 1  - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import os, sys, platform, re, upcean, pygame, random;
from PIL import Image, ImageDraw, ImageFont;
import PIL;

def rot_center(image, rect, angle):
 """rotate an image while keeping its center"""
 rot_image = pygame.transform.rotate(image, angle)
 rot_rect = rot_image.get_rect(center=rect.center)
 return rot_image,rot_rect
numbarcodes = 12;
barcodesize = 1;
pygame.init();
'''
pyicon = pygame.image.load("/mnt/utmp/pyupc-ean-demo/old_icon.png");
pygame.display.set_icon(pyicon);
'''
DisPlayRes = pygame.display.Info();
size = width, height = DisPlayRes.current_w, DisPlayRes.current_h;
screen = pygame.display.set_mode(size);
screen_rect=screen.get_rect();
pygame.display.set_caption("PyUPC-EAN Demo - "+upcean. __version__);
pygame.display.toggle_fullscreen();
'''
pybgimg = pygame.image.load("/usr/share/wallpapers/Sky.jpg");
pybgimg = pygame.transform.scale(pybgimg, (width, height));
'''
barcodeobj={};
barcodedrw={};
barcodeimg={};
position={};
dirx={};
diry={};
randbarcode={};
randsubbarcode={};
randchck={};
count=0;
maxnum=numbarcodes;
print("Python Version: "+platform.python_version());
pygamesdlver=pygame.get_sdl_version();
pygamesdlstr=str(pygamesdlver[0])+"."+str(pygamesdlver[1])+"."+str(pygamesdlver[2]);
del(pygamesdlver);
print("SDL Version: "+pygamesdlstr);
del(pygamesdlstr);
pygamever=pygame.version.vernum;
pygamestr=str(pygamever[0])+"."+str(pygamever[1])+"."+str(pygamever[2]);
del(pygamever);
print("PyGame Version: "+pygamestr);
del(pygamestr);
try:
 print("PIL Version: "+Image.VERSION);
except AttributeError:
 pass;
except NameError:
 pass;
try:
 print("Pillow Version: "+Image.PILLOW_VERSION);
except AttributeError:
 try:
  print("Pillow Version: "+PIL.__version__);
 except AttributeError:
  pass;
 except NameError:
  pass;
except NameError:
 try:
  print("Pillow Version: "+PIL.__version__);
 except AttributeError:
  pass;
 except NameError:
  pass;
print("PyUPC-EAN Version: "+upcean.__version__);
while(count < maxnum):
 barcodeobj[count] = upcean.oopfuncs.barcode();
 randbarcode[count] = random.randint(1, 9);
 if(randbarcode[count]==1):
  barcodeobj[count].type = "upca";
  barcodeobj[count].code = str(random.randint(0, 99999999999)).zfill(11);
 if(randbarcode[count]==2):
  barcodeobj[count].type = "upce";
  barcodeobj[count].code = str(random.randint(0, 1999999)).zfill(7);
 if(randbarcode[count]==3):
  barcodeobj[count].type = "ean13";
  barcodeobj[count].code = str(random.randint(0, 999999999999)).zfill(12);
 if(randbarcode[count]==4):
  barcodeobj[count].type = "ean8";
  barcodeobj[count].code = str(random.randint(0, 9999999)).zfill(7);
 if(randbarcode[count]==5):
  barcodeobj[count].type = "itf14";
  barcodeobj[count].code = str(random.randint(0, 9999999999999)).zfill(13);
 if(randbarcode[count]==6):
  randsubbarcode[count] = random.randint(1, 3);
  barcodeobj[count].type = "upce";
  if(randsubbarcode[count]==1):
   barcodeobj[count].outtype = "upca";
  if(randsubbarcode[count]==2):
   barcodeobj[count].outtype = "ean13";
  if(randsubbarcode[count]==3):
   barcodeobj[count].outtype = "itf14";
  barcodeobj[count].code = str(random.randint(0, 1999999)).zfill(7);
 if(randbarcode[count]==7):
  randsubbarcode[count] = random.randint(1, 2);
  barcodeobj[count].type = "upca";
  if(randsubbarcode[count]==1):
   barcodeobj[count].outtype = "ean13";
  if(randsubbarcode[count]==2):
   barcodeobj[count].outtype = "itf14";
  barcodeobj[count].code = str(random.randint(0, 99999999999)).zfill(11);
 if(randbarcode[count]==8):
  barcodeobj[count].type = "ean13";
  barcodeobj[count].outtype = "itf14";
  barcodeobj[count].code = str(random.randint(0, 999999999999)).zfill(12);
 if(randbarcode[count]==9):
  randsubbarcode[count] = random.randint(1, 3);
  barcodeobj[count].type = "ean8";
  if(randsubbarcode[count]==1):
   barcodeobj[count].outtype = "upca";
  if(randsubbarcode[count]==2):
   barcodeobj[count].outtype = "ean13";
  if(randsubbarcode[count]==3):
   barcodeobj[count].outtype = "itf14";
  barcodeobj[count].code = str(random.randint(0, 9999999)).zfill(7);
 barcodeobj[count].code = barcodeobj[count].fix_checksum();
 if(randbarcode[count]==6 or randbarcode[count]==7 or randbarcode[count]==8 or randbarcode[count]==9):
  barcodeobj[count].code = barcodeobj[count].convert_barcode();
  barcodeobj[count].type = barcodeobj[count].outtype;
 barcodeobj[count].size = barcodesize;
 barcodedrw[count] = barcodeobj[count].validate_draw_barcode().convert("RGBA").rotate(random.randint(0, 360), Image.BICUBIC, True);
 barcodeimg[count] = pygame.image.fromstring(barcodedrw[count].tobytes(), barcodedrw[count].size, barcodedrw[count].mode);
 position[count] = barcodeimg[count].get_rect();
 position[count].move_ip([1, 1]);
 position[count] = position[count].move(random.randint(0, 800), random.randint(0, height));
 dirx[count] = random.randint(-2, 2);
 diry[count] = random.randint(-2, 2);
 if(dirx[count]==0 and diry[count]==0):
  randchck[count] = random.randint(1, 4);
  if(randchck[count]==1):
   dirx[count] = random.randint(1, 2);
   diry[count] = random.randint(1, 2);
  if(randchck[count]==2):
   dirx[count] = random.randint(-2, -1);
   diry[count] = random.randint(-2, -1);
  if(randchck[count]==3):
   dirx[count] = random.randint(1, 2);
   diry[count] = random.randint(-2, -1);
  if(randchck[count]==4):
   dirx[count] = random.randint(-2, -1);
   diry[count] = random.randint(1, 2);
 print("Generating Barcode "+str(count + 1)+"\nType: "+barcodeobj[count].type+"\nRand: "+str(randbarcode[count])+"\nCode: "+barcodeobj[count].code+"\nPosition: X:"+str(position[count].center[0])+",Y:"+str(position[count].center[0]));
 count = count + 1;
running = True
while running:
 screen.fill((0, 0, 0));
 '''
 screen.blit(pybgimg,(0,0));
 '''
 count=0;
 while(count < maxnum):
  if((position[count].center[0]<0 or position[count].center[0]>width) or (position[count].center[1]<0 or position[count].center[1]>height)):
   barcodeobj[count] = upcean.oopfuncs.barcode();
   randbarcode[count] = random.randint(1, 9);
   if(randbarcode[count]==1):
    barcodeobj[count].type = "upca";
    barcodeobj[count].code = str(random.randint(0, 99999999999)).zfill(11);
   if(randbarcode[count]==2):
    barcodeobj[count].type = "upce";
    barcodeobj[count].code = str(random.randint(0, 1999999)).zfill(7);
   if(randbarcode[count]==3):
    barcodeobj[count].type = "ean13";
    barcodeobj[count].code = str(random.randint(0, 999999999999)).zfill(12);
   if(randbarcode[count]==4):
    barcodeobj[count].type = "ean8";
    barcodeobj[count].code = str(random.randint(0, 9999999)).zfill(7);
   if(randbarcode[count]==5):
    barcodeobj[count].type = "itf14";
    barcodeobj[count].code = str(random.randint(0, 9999999999999)).zfill(13);
   if(randbarcode[count]==6):
    randsubbarcode[count] = random.randint(1, 3);
    barcodeobj[count].type = "upce";
    if(randsubbarcode[count]==1):
     barcodeobj[count].outtype = "upca";
    if(randsubbarcode[count]==2):
     barcodeobj[count].outtype = "ean13";
    if(randsubbarcode[count]==3):
     barcodeobj[count].outtype = "itf14";
    barcodeobj[count].code = str(random.randint(0, 1999999)).zfill(7);
   if(randbarcode[count]==7):
    randsubbarcode[count] = random.randint(1, 2);
    barcodeobj[count].type = "upca";
    if(randsubbarcode[count]==1):
     barcodeobj[count].outtype = "ean13";
    if(randsubbarcode[count]==2):
     barcodeobj[count].outtype = "itf14";
    barcodeobj[count].code = str(random.randint(0, 99999999999)).zfill(11);
   if(randbarcode[count]==8):
    barcodeobj[count].type = "ean13";
    barcodeobj[count].outtype = "itf14";
    barcodeobj[count].code = str(random.randint(0, 999999999999)).zfill(12);
   if(randbarcode[count]==9):
    randsubbarcode[count] = random.randint(1, 3);
    barcodeobj[count].type = "ean8";
    if(randsubbarcode[count]==1):
     barcodeobj[count].outtype = "upca";
    if(randsubbarcode[count]==2):
     barcodeobj[count].outtype = "ean13";
    if(randsubbarcode[count]==3):
     barcodeobj[count].outtype = "itf14";
    barcodeobj[count].code = str(random.randint(0, 9999999)).zfill(7);
   barcodeobj[count].code = barcodeobj[count].fix_checksum();
   if(randbarcode[count]==6 or randbarcode[count]==7 or randbarcode[count]==8 or randbarcode[count]==9):
    barcodeobj[count].code = barcodeobj[count].convert_barcode();
    barcodeobj[count].type = barcodeobj[count].outtype;
   barcodeobj[count].size = barcodesize;
   barcodedrw[count] = barcodeobj[count].validate_draw_barcode().convert("RGBA").rotate(random.randint(0, 360), Image.BICUBIC, True);
   barcodeimg[count] = pygame.image.fromstring(barcodedrw[count].tobytes(), barcodedrw[count].size, barcodedrw[count].mode);
   position[count] = barcodeimg[count].get_rect();
   position[count].move_ip([1, 1]);
   position[count] = position[count].move(random.randint(0, width), random.randint(0, height));
   dirx[count] = random.randint(-2, 2);
   diry[count] = random.randint(-2, 2);
   if(dirx[count]==0 and diry[count]==0):
    randchck[count] = random.randint(1, 4);
    if(randchck[count]==1):
     dirx[count] = random.randint(1, 2);
     diry[count] = random.randint(1, 2);
    if(randchck[count]==2):
     dirx[count] = random.randint(-2, -1);
     diry[count] = random.randint(-2, -1);
    if(randchck[count]==3):
     dirx[count] = random.randint(1, 2);
     diry[count] = random.randint(-2, -1);
    if(randchck[count]==4):
     dirx[count] = random.randint(-2, -1);
     diry[count] = random.randint(1, 2);
   print("Generating Barcode "+str(count + 1)+"\nType: "+barcodeobj[count].type+"\nRand: "+str(randbarcode[count])+"\nCode: "+barcodeobj[count].code+"\nPosition: X:"+str(position[count].center[0])+",Y:"+str(position[count].center[0]));
  screen.blit(barcodeimg[count],position[count]);
  position[count] = position[count].move(dirx[count], diry[count]);
  count = count + 1;
 pygame.display.flip();
 pygame.time.delay(10);
 for event in pygame.event.get():
  if event.type==pygame.QUIT:
   running = False;
  if event.type==pygame.KEYDOWN:
   if event.key==pygame.K_ESCAPE or event.key==pygame.K_q:
    running = False;
