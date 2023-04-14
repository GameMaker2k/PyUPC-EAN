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

    $FileInfo: code128.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, sys, upcean.encode.getsfname, upcean.support;
from upcean.validate import convert_ascii_code128_to_hex_code128, convert_text_to_hex_code128_with_checksum, convert_text_to_hex_code128_manual_with_checksum;
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

def create_code128hex_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 upc = str(upc).lower();
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
 if(len(upc) % 2):
  return False;
 if(len(upc) < 8):
  return False;
 if(not re.findall("([0-9a-f]+)", upc)):
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
 upc = upc.lower();
 if(not re.findall("[0-9a-f]{2}", upc)):
  return False;
 upc_matches = re.findall("[0-9a-f]{2}", upc);
 upc_to_dec = list([int(x, 16) for x in upc_matches]);
 upc_size_add = ((len(upc_matches) * 11) + (len(re.findall("6c", upc)) * 2)) * barwidth[0];
 if(pilsupport and imageoutlib=="pillow"):
  upc_preimg = Image.new("RGB", ((29 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1])));
  upc_img = ImageDraw.Draw(upc_preimg);
  upc_img.rectangle([(0, 0), ((29 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]))], fill=barcolor[2]);
 if(cairosupport and (imageoutlib=="cairo" or imageoutlib=="cairosvg")):
  if(outfileext=="SVG"):
   upc_preimg = cairo.SVGSurface(None, (29 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  elif(outfileext=="PDF"):
   upc_preimg = cairo.PDFSurface(None, (29 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
  elif(outfileext=="PS" or outfileext=="EPS"):
   upc_preimg = cairo.PSSurface(None, (29 * barwidth[0]) + addonsize, barheightadd + (9 * barwidth[1]));
   if(outfileext=="EPS"):
    upc_preimg.set_eps(True);
   else:
    upc_preimg.set_eps(False);
  else:
   upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (29 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  upc_img = cairo.Context (upc_preimg);
  upc_img.set_antialias(cairo.ANTIALIAS_NONE);
  upc_img.rectangle(0, 0, (29 * barwidth[0]) + upc_size_add, barheight[1] + (9 * barwidth[1]));
  upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2]);
  upc_img.fill();
 upc_array = { 'upc': upc, 'code': [ ] };
 LineSize = barheight[0];
 if(hidetext):
  LineSize = barheight[1];
 start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
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
 cur_set = 0;
 hextocharsetone = { '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': " ", '41': " ", '42': " ", '43': " ", '44': " ", '45': " ", '46': " ", '47': " ", '48': " ", '49': " ", '4a': " ", '4b': " ", '4c': " ", '4d': " ", '4e': " ", '4f': " ", '50': " ", '51': " ", '52': " ", '53': " ", '54': " ", '55': " ", '56': " ", '57': " ", '58': " ", '59': " ", '5a': " ", '5b': " ", '5c': " ", '5d': " ", '5e': " ", '5f': " ", '60': " ", '61': " ", '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " " };
 hextocharsettwo = { '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': " ", '60': " ", '61': " ", '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " " };
 hextocharsetthree = { '00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '0a': "10", '0b': "11", '0c': "12", '0d': "13", '0e': "14", '0f': "15", '10': "16", '11': "17", '12': "18", '13': "19", '14': "20", '15': "21", '16': "22", '17': "23", '18': "24", '19': "25", '1a': "26", '1b': "27", '1c': "28", '1d': "29", '1e': "30", '1f': "31", '20': "32", '21': "33", '22': "34", '23': "35", '24': "36", '25': "37", '26': "38", '27': "39", '28': "40", '29': "41", '2a': "42", '2b': "43", '2c': "44", '2d': "45", '2e': "46", '2f': "47", '30': "48", '31': "49", '32': "50", '33': "51", '34': "52", '35': "53", '36': "54", '37': "55", '38': "56", '39': "57", '3a': "58", '3b': "59", '3c': "60", '3d': "61", '3e': "62", '3f': "63", '40': "64", '41': "65", '42': "66", '43': "67", '44': "68", '45': "69", '46': "70", '47': "71", '48': "72", '49': "73", '4a': "74", '4b': "75", '4c': "76", '4d': "77", '4e': "78", '4f': "79", '50': "80", '51': "81", '52': "82", '53': "83", '54': "84", '55': "85", '56': "86", '57': "87", '58': "88", '59': "89", '5a': "90", '5b': "91", '5c': "92", '5d': "93", '5e': "94", '5f': "95", '60': "96", '61': "97", '62': "98", '63': "99", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " " };
 hextocharsetfour = { '00': "32", '00': "194", '00': "207", '00': "212", '00': "252", '01': "33", '02': "34", '03': "35", '04': "36", '05': "37", '06': "38", '07': "39", '08': "40", '09': "41", '0a': "42", '0b': "43", '0c': "44", '0d': "45", '0e': "46", '0f': "47", '10': "48", '11': "49", '12': "50", '13': "51", '14': "52", '15': "53", '16': "54", '17': "55", '18': "56", '19': "57", '1a': "58", '1b': "59", '1c': "60", '1d': "61", '1e': "62", '1f': "63", '20': "64", '21': "65", '22': "66", '23': "67", '24': "68", '25': "69", '26': "70", '27': "71", '28': "72", '29': "73", '2a': "74", '2b': "75", '2c': "76", '2d': "77", '2e': "78", '2f': "79", '30': "80", '31': "81", '32': "82", '33': "83", '34': "84", '35': "85", '36': "86", '37': "87", '38': "88", '39': "89", '3a': "90", '3b': "91", '3c': "92", '3d': "93", '3e': "94", '3f': "95", '40': "96", '41': "97", '42': "98", '43': "99", '44': "100", '45': "101", '46': "102", '47': "103", '48': "104", '49': "105", '4a': "106", '4b': "107", '4c': "108", '4d': "109", '4e': "110", '4f': "111", '50': "112", '51': "113", '52': "114", '53': "115", '54': "116", '55': "117", '56': "118", '57': "119", '58': "120", '59': "121", '5a': "122", '5b': "123", '5c': "124", '5d': "125", '5e': "126", '5f': "195", '5f': "200", '5f': "240", '60': "196", '60': "201", '60': "241", '61': "197", '61': "202", '61': "242", '62': "198", '62': "203", '62': "243", '63': "199", '63': "204", '63': "244", '64': "200", '64': "205", '64': "245", '65': "201", '65': "206", '65': "246", '66': "202", '66': "207", '66': "247", '67': "203", '67': "208", '67': "248", '68': "204", '68': "209", '68': "249", '69': "205", '69': "210", '69': "250", '6a': "127", '6b': "128", '6c': "129" };
 hextoaltdigit = { '00': 32, '00': 194, '00': 207, '00': 212, '00': 252, '01': 33, '02': 34, '03': 35, '04': 36, '05': 37, '06': 38, '07': 39, '08': 40, '09': 41, '0a': 42, '0b': 43, '0c': 44, '0d': 45, '0e': 46, '0f': 47, '10': 48, '11': 49, '12': 50, '13': 51, '14': 52, '15': 53, '16': 54, '17': 55, '18': 56, '19': 57, '1a': 58, '1b': 59, '1c': 60, '1d': 61, '1e': 62, '1f': 63, '20': 64, '21': 65, '22': 66, '23': 67, '24': 68, '25': 69, '26': 70, '27': 71, '28': 72, '29': 73, '2a': 74, '2b': 75, '2c': 76, '2d': 77, '2e': 78, '2f': 79, '30': 80, '31': 81, '32': 82, '33': 83, '34': 84, '35': 85, '36': 86, '37': 87, '38': 88, '39': 89, '3a': 90, '3b': 91, '3c': 92, '3d': 93, '3e': 94, '3f': 95, '40': 96, '41': 97, '42': 98, '43': 99, '44': 100, '45': 101, '46': 102, '47': 103, '48': 104, '49': 105, '4a': 106, '4b': 107, '4c': 108, '4d': 109, '4e': 110, '4f': 111, '50': 112, '51': 113, '52': 114, '53': 115, '54': 116, '55': 117, '56': 118, '57': 119, '58': 120, '59': 121, '5a': 122, '5b': 123, '5c': 124, '5d': 125, '5e': 126, '5f': 195, '5f': 200, '5f': 240, '60': 196, '60': 201, '60': 241, '61': 197, '61': 202, '61': 242, '62': 198, '62': 203, '62': 243, '63': 199, '63': 204, '63': 244, '64': 200, '64': 205, '64': 245, '65': 201, '65': 206, '65': 246, '66': 202, '66': 207, '66': 247, '67': 203, '67': 208, '67': 248, '68': 204, '68': 209, '68': 249, '69': 205, '69': 210, '69': 250, '6a': "127", '6b': "128", '6c': "129" };
 hextodecnum = { '00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9, '0a': 10, '0b': 11, '0c': 12, '0d': 13, '0e': 14, '0f': 15, '10': 16, '11': 17, '12': 18, '13': 19, '14': 20, '15': 21, '16': 22, '17': 23, '18': 24, '19': 25, '1a': 26, '1b': 27, '1c': 28, '1d': 29, '1e': 30, '1f': 31, '20': 32, '21': 33, '22': 34, '23': 35, '24': 36, '25': 37, '26': 38, '27': 39, '28': 40, '29': 41, '2a': 42, '2b': 43, '2c': 44, '2d': 45, '2e': 46, '2f': 47, '30': 48, '31': 49, '32': 50, '33': 51, '34': 52, '35': 53, '36': 54, '37': 55, '38': 56, '39': 57, '3a': 58, '3b': 59, '3c': 60, '3d': 61, '3e': 62, '3f': 63, '40': 64, '41': 65, '42': 66, '43': 67, '44': 68, '45': 69, '46': 70, '47': 71, '48': 72, '49': 73, '4a': 74, '4b': 75, '4c': 76, '4d': 77, '4e': 78, '4f': 79, '50': 80, '51': 81, '52': 82, '53': 83, '54': 84, '55': 85, '56': 86, '57': 87, '58': 88, '59': 89, '5a': 90, '5b': 91, '5c': 92, '5d': 93, '5e': 94, '5f': 95, '60': 96, '61': 97, '62': 98, '63': 99, '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " " };
 decnumtohex = { 0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '0a', 11: '0b', 12: '0c', 13: '0d', 14: '0e', 15: '0f', 16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16', 23: '17', 24: '18', 25: '19', 26: '1a', 27: '1b', 28: '1c', 29: '1d', 30: '1e', 31: '1f', 32: '20', 33: '21', 34: '22', 35: '23', 36: '24', 37: '25', 38: '26', 39: '27', 40: '28', 41: '29', 42: '2a', 43: '2b', 44: '2c', 45: '2d', 46: '2e', 47: '2f', 48: '30', 49: '31', 50: '32', 51: '33', 52: '34', 53: '35', 54: '36', 55: '37', 56: '38', 57: '39', 58: '3a', 59: '3b', 60: '3c', 61: '3d', 62: '3e', 63: '3f', 64: '40', 65: '41', 66: '42', 67: '43', 68: '44', 69: '45', 70: '46', 71: '47', 72: '48', 73: '49', 74: '4a', 75: '4b', 76: '4c', 77: '4d', 78: '4e', 79: '4f', 80: '50', 81: '51', 82: '52', 83: '53', 84: '54', 85: '55', 86: '56', 87: '57', 88: '58', 89: '59', 90: '5a', 91: '5b', 92: '5c', 93: '5d', 94: '5e', 95: '5f', 95: '5f', 95: '5f', 96: '60', 96: '60', 96: '60', 97: '61', 97: '61', 97: '61', 98: '62', 98: '62', 98: '62', 99: '63', 99: '63', 99: '63' };
 decnumalttohex = { 32: '00', 194: '00', 207: '00', 212: '00', 252: '00', 33: '01', 34: '02', 35: '03', 36: '04', 37: '05', 38: '06', 39: '07', 40: '08', 41: '09', 42: '0a', 43: '0b', 44: '0c', 45: '0d', 46: '0e', 47: '0f', 48: '10', 49: '11', 50: '12', 51: '13', 52: '14', 53: '15', 54: '16', 55: '17', 56: '18', 57: '19', 58: '1a', 59: '1b', 60: '1c', 61: '1d', 62: '1e', 63: '1f', 64: '20', 65: '21', 66: '22', 67: '23', 68: '24', 69: '25', 70: '26', 71: '27', 72: '28', 73: '29', 74: '2a', 75: '2b', 76: '2c', 77: '2d', 78: '2e', 79: '2f', 80: '30', 81: '31', 82: '32', 83: '33', 84: '34', 85: '35', 86: '36', 87: '37', 88: '38', 89: '39', 90: '3a', 91: '3b', 92: '3c', 93: '3d', 94: '3e', 95: '3f', 96: '40', 97: '41', 98: '42', 99: '43', 100: '44', 101: '45', 102: '46', 103: '47', 104: '48', 105: '49', 106: '4a', 107: '4b', 108: '4c', 109: '4d', 110: '4e', 111: '4f', 112: '50', 113: '51', 114: '52', 115: '53', 116: '54', 117: '55', 118: '56', 119: '57', 120: '58', 121: '59', 122: '5a', 123: '5b', 124: '5c', 125: '5d', 126: '5e', 195: '5f', 200: '5f', 240: '5f', 196: '60', 201: '60', 241: '60', 197: '61', 202: '61', 242: '61', 198: '62', 203: '62', 243: '62', 199: '63', 204: '63', 244: '63', 200: '64', 205: '64', 245: '64', 201: '65', 206: '65', 246: '65', 202: '66', 207: '66', 247: '66', 203: '67', 208: '67', 248: '67', 204: '68', 209: '68', 249: '68', 205: '69', 210: '69', 250: '69' };
 codecharset = [hextocharsetone, hextocharsettwo, hextocharsetthree,  hextocharsetfour];
 upc_print = [];
 shift_cur_set = False;
 start_shift = 0;
 while (NumZero < len(upc_matches)):
  old_cur_set = cur_set;
  if(start_shift==1):
   cur_set = shift_cur_set;
  left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="00"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="01"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="02"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="03"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="04"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="05"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="06"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="07"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="08"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="09"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="0a"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0b"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="0c"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="0d"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="0e"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="0f"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="10"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="11"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="12"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="13"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="14"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="15"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="16"):
   left_barcolor =  [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="17"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="18"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="19"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="1a"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="1b"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="1c"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="1d"):
   left_barcolor =  [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="1e"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="1f"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="20"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="21"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="22"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="23"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="24"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="25"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="26"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="27"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="28"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="29"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="2a"):
   left_barcolor =  [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="2b"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="2c"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="2d"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="2e"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="2f"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="30"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="31"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="32"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="33"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="34"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="35"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="36"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="37"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="38"):
   left_barcolor =  [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="39"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="3a"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="3b"):
   left_barcolor =  [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="3c"):
   left_barcolor =  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="3d"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="3e"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="3f"):
   left_barcolor =  [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="40"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="41"):
   left_barcolor =  [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="42"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="43"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="44"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="45"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="46"):
   left_barcolor =  [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="47"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="48"):
   left_barcolor =  [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="49"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="4a"):
   left_barcolor =  [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="4b"):
   left_barcolor =  [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="4c"):
   left_barcolor =  [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0];
  if(upc_matches[NumZero]=="4d"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="4e"):
   left_barcolor =  [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="4f"):
   left_barcolor =  [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="50"):
   left_barcolor =  [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="51"):
   left_barcolor =  [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0];
  if(upc_matches[NumZero]=="52"):
   left_barcolor =  [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="53"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="54"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="55"):
   left_barcolor =  [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="56"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="57"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0];
  if(upc_matches[NumZero]=="58"):
   left_barcolor =  [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="59"):
   left_barcolor =  [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="5a"):
   left_barcolor =  [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="5b"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0];
  if(upc_matches[NumZero]=="5c"):
   left_barcolor =  [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="5d"):
   left_barcolor =  [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="5e"):
   left_barcolor =  [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="5f"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="60"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0];
  if(upc_matches[NumZero]=="61"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="62"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0];
   old_cur_set = cur_set;
   if(cur_set==0):
    cur_set = 1;
   if(cur_set==1):
    cur_set = 0;
   shift_cur_set = cur_set;
   start_shift = 1;
   cur_set = old_cur_set;
  if(cur_set==0 and upc_to_dec[NumZero]<64):
   upc_print.append(codecharset[cur_set][upc_matches[NumZero]]);
  elif(cur_set==1 and upc_to_dec[NumZero]<95):
   upc_print.append(codecharset[cur_set][upc_matches[NumZero]]);
  elif(cur_set==2 and upc_to_dec[NumZero]<100):
   upc_print.append(codecharset[cur_set][upc_matches[NumZero]]);
  else:
   upc_print.append(" ");
  if(upc_matches[NumZero]=="63"):
   left_barcolor =  [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0];
   if(cur_set==0 or cur_set==1):
    cur_set = 2;
  if(upc_matches[NumZero]=="64"):
   left_barcolor =  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0];
   if(cur_set==0 or cur_set==2):
    cur_set = 1;
  if(upc_matches[NumZero]=="65"):
   left_barcolor =  [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0];
   if(cur_set==1 or cur_set==2):
    cur_set = 0;
  if(upc_matches[NumZero]=="66"):
   left_barcolor =  [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0];
  if(upc_matches[NumZero]=="67"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0];
   cur_set = 0;
  if(upc_matches[NumZero]=="68"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0];
   cur_set = 1;
  if(upc_matches[NumZero]=="69"):
   left_barcolor =  [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0];
   cur_set = 2;
  if(upc_matches[NumZero]=="6a"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0];
  if(upc_matches[NumZero]=="6b"):
   left_barcolor =  [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0];
  if(upc_matches[NumZero]=="6c"):
   left_barcolor =  [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1];
  if(upc_matches[NumZero]=="6d"):
   left_barcolor =  [];
   cur_set = 3;
  if(start_shift==1):
   cur_set = old_cur_set;
   start_shift = 0;
  InnerUPCNum = 0;
  while (InnerUPCNum < len(left_barcolor)):
   if(left_barcolor[InnerUPCNum]==1):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[0], imageoutlib);
   if(left_barcolor[InnerUPCNum]==0):
    drawColorLine(upc_img, LineStart, 4, LineStart, LineSize, barwidth[0], barcolor[2], imageoutlib);
   LineStart += barwidth[0];
   BarNum += 1;
   InnerUPCNum += 1;
  NumZero += 1;
 end_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
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
  new_upc_img = upc_preimg.resize(((34 + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize)), Image.NEAREST); # use nearest neighbour
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
    new_upc_preimg = cairo.SVGSurface(imgoutfile, ((34 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PDF"):
    new_upc_preimg = cairo.PDFSurface(imgoutfile, ((34 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
   elif(outfileext=="PS" or outfileext=="EPS"):
    new_upc_preimg = cairo.PSSurface(imgoutfile, ((34 * barwidth[0]) + addonsize) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize));
    if(outfileext=="EPS"):
     new_upc_preimg.set_eps(True);
    else:
     new_upc_preimg.set_eps(False);
   else:
    new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (34 + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize));
  else:
   new_upc_preimg = cairo.ImageSurface(cairo.FORMAT_RGB24, (34 + upc_size_add) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize), (barheight[1] + (9 * barwidth[1])) * int(resize));
  new_upc_img = cairo.Context(new_upc_preimg);
  new_upc_img.set_source(upc_imgpat);
  new_upc_img.paint();
  upc_img = new_upc_img;
 if(not hidetext):
  NumTxtZero = 0;
  LineTxtStart = 16;
  while (NumTxtZero < len(upc_print)):
   if(len(upc_print[NumTxtZero])==1):
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (16 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib);
    LineTxtStart += 11 * int(resize);
   if(len(upc_print[NumTxtZero])==2):
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (16 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero][0], barcolor[1], "ocrb", imageoutlib);
    LineTxtStart += 6 * int(resize);
    drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (16 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), upc_print[NumTxtZero][1], barcolor[1], "ocrb", imageoutlib);
    LineTxtStart += 5 * int(resize);
   NumTxtZero += 1;
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

def draw_code128hex_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code128hex_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def create_code128alt_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
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
 if(len(upc) < 4):
  return False;
 upc = convert_ascii_code128_to_hex_code128(upc);
 return create_code128hex_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def draw_code128alt_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128alt_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code128alt_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128alt_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def create_code128dec_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
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
 if(len(upc) < 12):
  return False;
 if(not re.findall("[0-9]{3}", upc)):
  return False;
 upc_matches = re.findall("[0-9]{3}", upc);
 il = len(upc_matches);
 i = 0;
 upcout = "";
 while(i < il):
  dectohex = format(int(upc_matches[i]), 'x');
  dectohexzero = str(dectohex).zfill(2);
  if(len(dectohexzero)>2):
   return False;
  upcout = upcout+str(dectohexzero);
  i = i + 1;
 upc = upcout;
 return create_code128hex_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def draw_code128dec_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128dec_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code128dec_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128dec_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def create_code128_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
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
 if(len(upc) < 4):
  return False;
 upc = convert_text_to_hex_code128_with_checksum(upc);
 return create_code128hex_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def draw_code128_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code128_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def create_code128man_barcode(upc,outfile="./code128.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
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
 if(len(upc) < 4):
  return False;
 upc = convert_text_to_hex_code128_manual_with_checksum(upc);
 return create_code128hex_barcode(upc,outfile,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def draw_code128man_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128man_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);

def encode_code128man_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),barwidth=(1, 1),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)),imageoutlib="pillow"):
 return create_code128man_barcode(upc,None,resize,hideinfo,barheight,barwidth,textxy,barcolor,imageoutlib);
