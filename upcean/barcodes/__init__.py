'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2014 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 10/16/2014 Ver. 2.6.7 RC 2 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, re, os, json, platform;
try:
 import xml.etree.cElementTree as cElementTree;
except ImportError:
 import xml.etree.ElementTree as cElementTree;
if(sys.version[0]=="2"):
 try:
  from cStringIO import StringIO;
 except ImportError:
  from StringIO import StringIO;
 import urllib2, urlparse;
if(sys.version[0]=="3"):
 from io import StringIO;
 import urllib.request as urllib2;
 import urllib.parse as urlparse;
from xml.sax.saxutils import XMLGenerator;
from upcean import __project__, __project_url__, __version__, __version_alt__, __version_info__, __version_date__, __version_date_info__, __version_date_alt__;

import upcean.validate, upcean.convert, upcean.getprefix, upcean.getsfname;
import upcean.barcodes.ean2, upcean.barcodes.ean5, upcean.barcodes.upca, upcean.barcodes.upce, upcean.barcodes.ean13, upcean.barcodes.ean8, upcean.barcodes.itf, upcean.barcodes.itf14;
import upcean.barcodes.code11, upcean.barcodes.code39, upcean.barcodes.code93, upcean.barcodes.codabar, upcean.barcodes.msi;
import upcean.fonts, upcean.xml;
from upcean.barcodes import *;
''' // Code for validating UPC/EAN by Kazuki Przyborowski '''
from upcean.validate import *;
''' // Code for converting UPC/EAN by Kazuki Przyborowski '''
from upcean.convert import *;
''' // Code for getting GS1 Prefix EAN-8/EAN-13/ITF-14 by Kazuki Przyborowski '''
from upcean.getprefix import *;
''' // Code for getting save file name and type by Kazuki Przyborowski '''
from upcean.getsfname import *;
''' // Code for making EAN-2 supplement by Kazuki Przyborowski '''
from upcean.barcodes.ean2 import *;
''' // Code for making EAN-5 supplement by Kazuki Przyborowski '''
from upcean.barcodes.ean5 import *;
''' // Code for making UPC-A by Kazuki Przyborowski '''
from upcean.barcodes.upca import *;
''' // Code for making UPC-E by Kazuki Przyborowski '''
from upcean.barcodes.upce import *;
''' // Code for making EAN-13 by Kazuki Przyborowski '''
from upcean.barcodes.ean13 import *;
''' // Code for making EAN-8 by Kazuki Przyborowski '''
from upcean.barcodes.ean8 import *;
''' // Code for making Standard 2 of 5 by Kazuki Przyborowski '''
from upcean.barcodes.stf import *;
''' // Code for making Interleaved 2 of 5 by Kazuki Przyborowski '''
from upcean.barcodes.itf import *;
''' // Code for making ITF-14 by Kazuki Przyborowski '''
from upcean.barcodes.itf14 import *;
''' // Code for making Code 11 by Kazuki Przyborowski '''
from upcean.barcodes.code11 import *;
''' // Code for making Code 39 by Kazuki Przyborowski '''
from upcean.barcodes.code39 import *;
''' // Code for making Code 93 by Kazuki Przyborowski '''
from upcean.barcodes.code93 import *;
''' // Code for making Codabar by Kazuki Przyborowski '''
from upcean.barcodes.codabar import *;
''' // Code for making Modified Plessey by Kazuki Przyborowski '''
from upcean.barcodes.msi import *;
''' // Import extra stuff '''
from upcean.fonts import *;
from upcean.xml import *;

''' User-Agent string for http/https requests '''
useragent_string = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(proname=__project__, prover=__version_alt__, prourl=__project_url__);
useragent_string_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) Python/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyver=platform.python_version(), proname=__project__, prover=__version_alt__);

'''
// UPC Resources and Info
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code
// Source: http://en.wikipedia.org/wiki/Global_Trade_Item_Number
// Source: http://en.wikipedia.org/wiki/Barcode
// Source: http://www.ucancode.net/CPP_Library_Control_Tool/Draw-Print-encode-UPCA-barcode-UPCE-barcode-EAN13-barcode-VC-Code.htm
// Source: http://en.wikipedia.org/wiki/International_Article_Number
// Source: http://www.upcdatabase.com/docs/
// Source: http://www.accipiter.org/projects/cat.php
// Source: http://www.accipiter.org/download/kittycode.js
// Source: http://uscan.sourceforge.net/upc.txt
// Source: http://www.adams1.com/upccode.html
// Source: http://www.documentmedia.com/Media/PublicationsArticles/QuietZone.pdf
// Source: http://zxing.org/w/decode.jspx
// Source: http://code.google.com/p/zxing/
// Source: http://www.terryburton.co.uk/barcodewriter/generator/
// Source: http://en.wikipedia.org/wiki/Interleaved_2_of_5
// Source: http://www.gs1au.org/assets/documents/info/user_manuals/barcode_technical_details/ITF_14_Barcode_Structure.pdf
// Source: http://www.barcodeisland.com/
'''

def check_if_string(strtext):
 if(sys.version[0]=="2"):
  if(isinstance(strtext, basestring)):
   return True;
 if(sys.version[0]=="3"):
  if(isinstance(strtext, str)):
   return True;
 return False;

'''
// Shortcut Codes by Kazuki Przyborowski
'''
def create_barcode(bctype,upc,outfile="./barcode.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 if(hasattr(upcean, "create_"+bctype+"_barcode") and callable(getattr(upcean, "create_"+bctype+"_barcode"))):
  return getattr(upcean, "create_"+bctype+"_barcode")(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
 if(not hasattr(upcean, "create_"+bctype+"_barcode") or not callable(getattr(upcean, "create_"+bctype+"_barcode"))):
  return False;
 return False;
def draw_barcode(bctype,upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_barcode(bctype,upc,None,resize,hideinfo,barheight,textxy,barcolor);

'''
// Create barcodes from XML file
'''
def create_barcode_from_xml_file(xmlfile, draw=False):
 global useragent_string;
 if(check_if_string(xmlfile) and re.findall("^(http|https)\:\/\/", xmlfile)):
  xmlheaders = {'User-Agent': useragent_string};
  try:
   tree = cElementTree.ElementTree(file=urllib2.urlopen(urllib2.Request(xmlfile, None, xmlheaders)));
  except cElementTree.ParseError: 
   return False;
 else:
  try:
   tree = cElementTree.ElementTree(file=xmlfile);
  except cElementTree.ParseError: 
   return False;
 root = tree.getroot();
 bcdrawlist = [];
 for child in root:
  if(child.tag=="python"):
   exec(child.text);
  if(child.tag=="barcode"):
   if(draw==True):
    xmlbarcode = {"bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": None};
   if(draw==False):
    if('file' in child.attrib):
     xmlbarcode = {"bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": child.attrib['file']};
    if('file' not in child.attrib):
     xmlbarcode = {"bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": None};
   if('size' in child.attrib):
    xmlbarcode.update({"resize": int(child.attrib['size'])});
   if('hideinfo' in child.attrib):
    hidebcinfo = child.attrib['hideinfo'].split();
    hidebcinfoval = [];
    if(hidebcinfo[0]=="0"):
     hidebcinfoval.append(False);
    if(hidebcinfo[0]=="1"):
     hidebcinfoval.append(True);
    if(hidebcinfo[1]=="0"):
     hidebcinfoval.append(False);
    if(hidebcinfo[1]=="1"):
     hidebcinfoval.append(True);
    if(hidebcinfo[2]=="0"):
     hidebcinfoval.append(False);
    if(hidebcinfo[2]=="1"):
     hidebcinfoval.append(True);
    xmlbarcode.update({"hideinfo": tuple(hidebcinfoval)});
   if('height' in child.attrib):
    xmlbarcode.update({"barheight": tuple(map(int, child.attrib['height'].split()))});
   if('textxy' in child.attrib):
    xmlbarcode.update({"textxy": tuple(map(int, child.attrib['textxy'].split()))});
   if('color' in child.attrib):
    colorsplit = child.attrib['color'].split();
    colorsplit1 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0]);
    colorsplit1 = colorsplit1[0];
    colorlist1 = (int(colorsplit1[0], 16), int(colorsplit1[1], 16), int(colorsplit1[2], 16));
    colorsplit2 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1]);
    colorsplit2 = colorsplit2[0];
    colorlist2 = (int(colorsplit2[0], 16), int(colorsplit2[1], 16), int(colorsplit2[2], 16));
    colorsplit3 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2]);
    colorsplit3 = colorsplit3[0];
    colorlist3 = (int(colorsplit3[0], 16), int(colorsplit3[1], 16), int(colorsplit3[2], 16));
    colorlist = (colorlist1, colorlist2, colorlist3);
    xmlbarcode.update({"barcolor": colorlist});
   bcstatinfo = upcean.create_barcode(**xmlbarcode);
   if(draw==True or 'file' not in child.attrib):
    bcdrawlist.append(bcstatinfo);
   if(bcstatinfo==False):
    return False;
 if(draw==True or (draw==False and len(bcdrawlist)>0)):
  return bcdrawlist;
 if(draw==False and len(bcdrawlist)==0):
  return True;
def create_barcode_from_xml_string(xmlfile, draw=False):
 return create_barcode_from_xml_file(StringIO(xmlfile), draw);
def draw_barcode_from_xml_file(xmlfile):
 return create_barcode_from_xml_file(xmlfile, True);
def draw_barcode_from_xml_string(xmlfile):
 return create_barcode_from_xml_file(StringIO(xmlfile), True);

def create_barcode_from_json_file(jsonfile, draw=False):
 global useragent_string;
 if(check_if_string(jsonfile) and re.findall("^(http|https)\:\/\/", jsonfile)):
  jsonheaders = {'User-Agent': useragent_string};
  tree = json.load(urllib2.urlopen(urllib2.Request(jsonfile, None, jsonheaders)));
 else:
  if(check_if_string(jsonfile)):
   jsonfile = open(jsonfile, "rb");
  tree = json.load(jsonfile.read());
  jsonfile.close();
 try:
  bctree = tree['barcodes']['barcode'];
 except: 
  return False;
 bctreeln = len(bctree);
 bctreect = 0;
 bcdrawlist = [];
 while(bctreect < bctreeln):
  if(draw==True):
   jsonbarcode = {"bctype": bctree[bctreect]['type'], "upc": bctree[bctreect]['code'], "outfile": None};
  if(draw==False):
   if('file' in bctree[bctreect]):
    jsonbarcode = {"bctype": bctree[bctreect]['type'], "upc": bctree[bctreect]['code'], "outfile": bctree[bctreect]['file']};
   if('file' not in bctree[bctreect]):
    jsonbarcode = {"bctype": bctree[bctreect]['type'], "upc": bctree[bctreect]['code'], "outfile": None};
  if('size' in bctree[bctreect]):
   jsonbarcode.update({"resize": int(bctree[bctreect]['size'])});
  if('hideinfo' in bctree[bctreect]):
   hidebcinfo = bctree[bctreect]['hideinfo'].split();
   hidebcinfoval = [];
   if(hidebcinfo[0]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[0]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[1]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[1]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[2]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[2]=="1"):
    hidebcinfoval.append(True);
   jsonbarcode.update({"hideinfo": tuple(hidebcinfoval)});
  if('height' in bctree[bctreect]):
   jsonbarcode.update({"barheight": tuple(map(int, bctree[bctreect]['height'].split()))});
  if('textxy' in bctree[bctreect]):
   jsonbarcode.update({"textxy": tuple(map(int, bctree[bctreect]['textxy'].split()))});
  if('color' in bctree[bctreect]):
   colorsplit = bctree[bctreect]['color'].split();
   colorsplit1 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0]);
   colorsplit1 = colorsplit1[0];
   colorlist1 = (int(colorsplit1[0], 16), int(colorsplit1[1], 16), int(colorsplit1[2], 16));
   colorsplit2 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1]);
   colorsplit2 = colorsplit2[0];
   colorlist2 = (int(colorsplit2[0], 16), int(colorsplit2[1], 16), int(colorsplit2[2], 16));
   colorsplit3 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2]);
   colorsplit3 = colorsplit3[0];
   colorlist3 = (int(colorsplit3[0], 16), int(colorsplit3[1], 16), int(colorsplit3[2], 16));
   colorlist = (colorlist1, colorlist2, colorlist3);
   jsonbarcode.update({"barcolor": colorlist});
  bcstatinfo = upcean.create_barcode(**jsonbarcode);
  if(draw==True or 'file' not in bctree[bctreect]):
   bcdrawlist.append(bcstatinfo);
  if(bcstatinfo==False):
   return False;
  bctreect = bctreect + 1;
 if(draw==True or (draw==False and len(bcdrawlist)>0)):
  return bcdrawlist;
 if(draw==False and len(bcdrawlist)==0):
  return True;
def create_barcode_from_json_string(xmlfile, draw=False):
 return create_barcode_from_json(StringIO(jsonfile), draw);
def draw_barcode_from_json_file(jsonfile):
 return create_barcode_from_json_file(jsonfile, True);
def draw_barcode_from_json_string(xmlfile):
 return create_barcode_from_json_file(StringIO(jsonfile), True);

def convert_from_json_to_xml_file(jsonfile, xmlfile=None):
 global useragent_string;
 if(check_if_string(jsonfile) and re.findall("^(http|https)\:\/\/", jsonfile)):
  jsonheaders = {'User-Agent': useragent_string};
  tree = json.load(urllib2.urlopen(urllib2.Request(jsonfile, None, jsonheaders)));
 else:
  if(check_if_string(jsonfile)):
   jsonfile = open(jsonfile, "rb");
  tree = json.load(jsonfile.read());
  jsonfile.close();
 try:
  bctree = tree['barcodes']['barcode'];
 except: 
  return False;
 bctreeln = len(bctree);
 bctreect = 0;
 bcdrawlist = [];
 xmlout=StringIO();
 upcxml=XMLGenerator(xmlout, "utf-8");
 upcxml.startDocument();
 upcxml.startElement("barcodes", {});
 upcxml.characters("\n");
 while(bctreect < bctreeln):
  upcxml.characters(" ");
  upcxml.startElement("barcode", bctree[bctreect]);
  upcxml.endElement("barcode");
  upcxml.characters("\n");
  bctreect = bctreect + 1;
 upcxml.endElement("barcodes");
 upcxml.endDocument();
 if(xmlfile!=None):
  xmlofile = open(xmlfile, "w+b");
  xmlofile.write(xmlout.getvalue());
  xmlofile.close();
  return True;
 if(xmlfile==None):
  return xmlout.getvalue();
def convert_from_json_to_xml_string(jsonfile, xmlfile=None):
 return convert_from_json_to_xml_file(StringIO(jsonfile), xmlfile);

def create_barcode_from_qs_file(qsfile, draw=False):
 global useragent_string;
 if(check_if_string(qsfile) and re.findall("^(http|https)\:\/\/", qsfile)):
  qsheaders = {'User-Agent': useragent_string};
  tree = urlparse.parse_qs(urllib2.urlopen(urllib2.Request(qsfile, None, qsheaders)).read());
 else:
  if(check_if_string(qsfile)):
   qsfile = open(qsfile, "rb");
  tree = urlparse.parse_qs(qsfile.read());
  jsonfile.close();
 bctree = tree;
 if(len(bctree['type'])<len(bctree['code']) or len(bctree['type'])==len(bctree['code'])):
  bctreeln = len(bctree['type']);
 if(len(bctree['code'])<len(bctree['type'])):
  bctreeln = len(bctree['code']);
 bctreect = 0;
 bcdrawlist = [];
 while(bctreect < bctreeln):
  qsbarcode = {}
  nofilesave = False;
  if(draw==True):
   nofilesave = True;
   qsbarcode.update({"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None});
  if(draw==False):
   try:
    nofilesave = False;
    qsbarcode.update({"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": bctree['file'][bctreect]});
   except KeyError:
    nofilesave = True;
    qsbarcode.update({"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None});
   except IndexError:
    nofilesave = True;
    qsbarcode.update({"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None});
  try:
   qsbarcode.update({"resize": int(bctree['size'][bctreect])});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   hidebcinfo = bctree['hideinfo'][bctreect].split();
   hidebcinfoval = [];
   if(hidebcinfo[0]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[0]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[1]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[1]=="1"):
    hidebcinfoval.append(True);
   if(hidebcinfo[2]=="0"):
    hidebcinfoval.append(False);
   if(hidebcinfo[2]=="1"):
    hidebcinfoval.append(True);
   qsbarcode.update({"hideinfo": tuple(hidebcinfoval)});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"barheight": int(bctree['height'][bctreect])});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"textxy": int(bctree['textxy'][bctreect])});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   colorsplit = bctree['color'][bctreect].split();
   colorsplit1 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0]);
   colorsplit1 = colorsplit1[0];
   colorlist1 = (int(colorsplit1[0], 16), int(colorsplit1[1], 16), int(colorsplit1[2], 16));
   colorsplit2 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1]);
   colorsplit2 = colorsplit2[0];
   colorlist2 = (int(colorsplit2[0], 16), int(colorsplit2[1], 16), int(colorsplit2[2], 16));
   colorsplit3 = re.findall("^\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2]);
   colorsplit3 = colorsplit3[0];
   colorlist3 = (int(colorsplit3[0], 16), int(colorsplit3[1], 16), int(colorsplit3[2], 16));
   colorlist = (colorlist1, colorlist2, colorlist3);
   qsbarcode.update({"barcolor": colorlist});
  except KeyError:
   pass;
  except IndexError:
   pass;
  bcstatinfo = upcean.create_barcode(**qsbarcode);
  if(draw==True or nofilesave == True):
   bcdrawlist.append(bcstatinfo);
  if(bcstatinfo==False):
   return False;
  bctreect = bctreect + 1;
 if(draw==True or (draw==False and len(bcdrawlist)>0)):
  return bcdrawlist;
 if(draw==False and len(bcdrawlist)==0):
  return True;
def create_barcode_from_qs_string(qsfile, draw=False):
 return create_barcode_from_qs_file(StringIO(qsfile), draw);
def draw_barcode_from_qs_file(qsfile):
 return create_barcode_from_qs_file(qsfile, True);
def draw_barcode_from_qs_string(qsfile):
 return create_barcode_from_qs_file(StringIO(qsfile), True);

def convert_from_qs_to_xml_file(qsfile, xmlfile=None):
 global useragent_string;
 if(check_if_string(qsfile) and re.findall("^(http|https)\:\/\/", qsfile)):
  qsheaders = {'User-Agent': useragent_string};
  tree = urlparse.parse_qs(urllib2.urlopen(urllib2.Request(qsfile, None, qsheaders)).read());
 else:
  if(check_if_string(qsfile)):
   qsfile = open(qsfile, "rb");
  tree = urlparse.parse_qs(qsfile.read());
  qsfile.close();
 bctree = tree;
 bctreeln = len(bctree);
 if(len(bctree['type'])<len(bctree['code']) or len(bctree['type'])==len(bctree['code'])):
  bctreeln = len(bctree['type']);
 if(len(bctree['code'])<len(bctree['type'])):
  bctreeln = len(bctree['code']);
 bctreect = 0;
 bcdrawlist = [];
 xmlout=StringIO();
 upcxml=XMLGenerator(xmlout, "utf-8");
 upcxml.startDocument();
 upcxml.startElement("barcodes", {});
 upcxml.characters("\n");
 while(bctreect < bctreeln):
  qsbarcode = {}
  qsbarcode.update({"type": bctree['type'][bctreect], "code": bctree['code'][bctreect]});
  try:
   qsbarcode.update({"file": bctree['file'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"size": bctree['size'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"hideinfo": bctree['hideinfo'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"barheight": bctree['barheight'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"textxy": bctree['textxy'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  try:
   qsbarcode.update({"color": bctree['color'][bctreect]});
  except KeyError:
   pass;
  except IndexError:
   pass;
  upcxml.characters(" ");
  upcxml.startElement("barcode", qsbarcode);
  upcxml.endElement("barcode");
  upcxml.characters("\n");
  bctreect = bctreect + 1;
 upcxml.endElement("barcodes");
 upcxml.endDocument();
 if(xmlfile!=None):
  xmlofile = open(xmlfile, "w+b");
  xmlofile.write(xmlout.getvalue());
  xmlofile.close();
  return True;
 if(xmlfile==None):
  return xmlout.getvalue();
def convert_from_qs_to_xml_string(qsfile, xmlfile=None):
 return convert_from_qs_to_xml_file(StringIO(qsfile), xmlfile);

def create_issn13_barcode_from_issn8(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_issn8_to_issn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13_barcode_from_issn8(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode_from_issn8(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_issn13_barcode(upc,outfile="./issn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode_from_issn8(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_issn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_issn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_isbn13_barcode_from_isbn10(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_isbn10_to_isbn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13_barcode_from_isbn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode_from_isbn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_isbn13_barcode(upc,outfile="./isbn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode_from_isbn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_isbn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_isbn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_ismn13_barcode_from_ismn10(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(convert_ismn10_to_ismn13(upc),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13_barcode_from_ismn10(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode_from_ismn10(upc,None,resize,hideinfo,barheight,textxy,barcolor);
def create_ismn13_barcode(upc,outfile="./ismn13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode_from_ismn10(upc,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_ismn13_barcode(upc,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ismn13_barcode(upc,None,resize,hideinfo,barheight,textxy,barcolor);

def create_vw_barcode_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_vw_to_upca_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_upca(code,price,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_ean13(code,price,outfile="./vw-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_vw_to_ean13_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_vw_barcode_to_itf14(code,price,outfile="./vw-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_vw_to_itf14_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_vw_barcode_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_vw_barcode_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_goodwill_barcode_upca(code,price,outfile="./goodwill-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_goodwill_to_upca_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_upca(code,price,outfile="./goodwill-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_upca(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_upca(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_ean13(code,price,outfile="./goodwill-ean13.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_goodwill_to_ean13_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_ean13(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_to_ean13(code,price,None,resize,hideinfo,barheight,textxy,barcolor);
def create_goodwill_barcode_to_itf14(code,price,outfile="./goodwill-itf14.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_goodwill_to_itf14_barcode(code, price),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_goodwill_barcode_to_itf14(code,price,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_goodwill_barcode_to_itf14(code,price,None,resize,hideinfo,barheight,textxy,barcolor);

def create_coupon_barcode_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_upca_barcode(make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_upca(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_upca(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_upca(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_ean13_barcode(make_coupon_to_ean13_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_to_ean13(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
def create_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,outfile="./vw-upca.png",resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_itf14_barcode(make_coupon_to_itf14_barcode(numbersystem, manufacturer, family, value),outfile,resize,hideinfo,barheight,textxy,barcolor);
def draw_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,resize=1,hideinfo=(False, False, False),barheight=(48, 54),textxy=(1, 1, 1),barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255))):
 return create_coupon_barcode_to_itf14(numbersystem,manufacturer,family,value,None,resize,hideinfo,barheight,textxy,barcolor);
