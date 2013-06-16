#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: httpd.py - Last Update: 06/16/2013 Ver. 2.4.2 RC 3  - Author: cooldude2k $
'''

import tempfile, uuid, re, os, sys, cherrypy, upcean, StringIO, argparse;
from PIL import Image, ImageDraw, ImageFont;
parser = argparse.ArgumentParser(description="A web server that draws barcodes with PyUPC-EAN powered by CherryPy web server.");
parser.add_argument("--port", "--port-number", help="port number to use for server.");
parser.add_argument("--host", "--host-name", help="host name to use for server.");
getargs = parser.parse_args();
if(getargs.port!=None):
 port = int(getargs.port);
else:
 port = 8080;
if(getargs.host!=None):
 host = str(getargs.host);
else:
 host = "0.0.0.0";
class GenerateIndexPage(object):
 def index(self):
  cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
  ServerSignature = "<address><a href=\"https://github.com/GameMaker2k/PyUPC-EAN\" title=\"PyUPC-EAN barcode generator\">PyUPC-EAN</a>/%s (<a href=\"http://www.cherrypy.org/\" title=\"CherryPy python web server\">CherryPy</a>/%s)</address>" % (upcean.__version__, cherrypy.__version__);
  return "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n<head>\n<title> Barcode Generator 2k (PyUPC-EAN) </title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"Content-Language\" content=\"en\" />\n<meta name=\"generator\" content=\"CherryPy\" />\n<meta name=\"author\" content=\"Game Maker 2k\" />\n<meta name=\"keywords\" content=\"barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar\" />\n<meta name=\"description\" content=\"Barcode Generator with PyUPC-EAN\" /><meta name=\"resource-type\" content=\"document\" />\n<meta name=\"distribution\" content=\"global\" />\n<link rel=\"Generator\" href=\"http://www.cherrypy.org/\" title=\"CherryPy\" />\n</head>\n<body>\n<form name=\"upcean\" id=\"upcean\" method=\"get\" action=\"/upcean/\" onsubmit=\"location.href='/generate/'+upcean.upc.value+'/'+upcean.bctype.value+'/'+upcean.size.value+'/'+upcean.rotate.value+'/'+upcean.upc.value+'.'+upcean.imgtype.value; return false;\">\n<fieldset>\n<legend>Barcode Info: </legend>\n<label style=\"cursor: pointer;\" for=\"upc\">Enter UPC/EAN: </label><br />\n<input type=\"text\" id=\"upc\" name=\"upc\" /><br />\n<label style=\"cursor: pointer;\" for=\"imgtype\">Select and image type: </label><br />\n<select id=\"imgtype\" name=\"imgtype\">\n<option value=\"png\" selected=\"selected\">PNG Image</option>\n<option value=\"gif\">GIF Image</option>\n<option value=\"jpeg\">JPEG Image</option>\n<option value=\"bmp\">BMP Image</option>\n<option value=\"tiff\">TIFF Image</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"size\">Select barcode size: </label><br />\n<select id=\"size\" name=\"size\">\n<option value=\"1\" selected=\"selected\">1x</option>\n<option value=\"2\">2x</option>\n<option value=\"3\">3x</option>\n<option value=\"4\">4x</option>\n<option value=\"5\">5x</option>\n<option value=\"6\">6x</option>\n<option value=\"7\">7x</option>\n<option value=\"8\">8x</option>\n<option value=\"9\">9x</option>\n<option value=\"10\">10x</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"bctype\">Select barcode type: </label><br />\n<select id=\"bctype\" name=\"bctype\">\n<option value=\"barcode\" selected=\"selected\">Barcode</option>\n<option value=\"upca\">UPC-A</option>\n<option value=\"upce\">UPC-E</option>\n<option value=\"ean13\">EAN-13</option>\n<option value=\"ean8\">EAN-8</option>\n<option value=\"ean2\">EAN-2</option>\n<option value=\"ean5\">EAN-5</option>\n<option value=\"stf\">STF</option>\n<option value=\"itf\">ITF</option>\n<option value=\"itf14\">ITF-14</option>\n<option value=\"code11\">Code 11</option>\n<option value=\"code39\">Code 39</option>\n<option value=\"code93\">Code 93</option>\n<option value=\"codabar\">Codabar</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"rotate\">Select degrees to rotate image by: </label><br />\n<select id=\"rotate\" name=\"rotate\">\n<option value=\"0\" selected=\"selected\">0 &#176;</option>\n<option value=\"45\">45 &#176;</option>\n<option value=\"90\">90 &#176;</option>\n<option value=\"135\">135 &#176;</option>\n<option value=\"180\">180 &#176;</option>\n<option value=\"225\">225 &#176;</option>\n<option value=\"270\">270 &#176;</option>\n<option value=\"315\">315 &#176;</option>\n<option value=\"360\">360 &#176;</option>\n</select><br />\n<input type=\"submit\" />\n</fieldset>\n</form><br />\n"+ServerSignature+"\n</body>\n</html>";
 index.exposed = True;
 def generate(self, upc, bctype, bcsize, bcrotate, imgtype):
  imgdata = StringIO.StringIO();
  try:
   bctype;
  except KeyError:
   bctype = "barcode";
  try:
   bcsize;
  except KeyError:
   bcsize = 1;
  try:
   imgtype;
  except KeyError:
   imgtype = "png";
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = upcean.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type']= 'image/png';
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type']= 'image/gif';
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type']= 'image/jpeg';
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type']= 'image/bmp';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type']= 'image/x-portable-pixmap';
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type']= 'image/tiff';
  if(upc!=None and (int(bcrotate)==0 or bcrotate==None)):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).save(imgdata, file_ext[1]);
  if(upc!=None and (int(bcrotate)>0 or int(bcrotate)<0)):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(upc!=None):
   imgdata.seek(0);
   return imgdata.buf;
 generate.exposed = True;

class GenerateBarcodes(object):
 def index(self, **params):
  imgdata = StringIO.StringIO();
  try:
   params['bctype'];
  except KeyError:
   params['bctype'] = "barcode";
  try:
   params['size'];
  except KeyError:
   params['size'] = 1;
  try:
   params['imgtype'];
  except KeyError:
   params['imgtype'] = "png";
  try:
   params['rotate'];
  except KeyError:
   params['rotate'] = 0;
  try:
   params['upc'];
  except KeyError:
   params['upc'] = None;
  file_ext = upcean.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+params['imgtype'].lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type']= 'image/png';
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type']= 'image/gif';
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type']= 'image/jpeg';
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type']= 'image/bmp';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type']= 'image/x-portable-pixmap';
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type']= 'image/tiff';
  if(params['upc']!=None and (int(params['rotate'])==0 or params['rotate']==None)):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
  if(params['upc']!=None and (int(params['rotate'])>0 or int(params['rotate'])<0)):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(params['upc']!=None):
   imgdata.seek(0);
   return imgdata.buf;
  if(params['upc']==None):
   cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
   ServerSignature = "<address><a href=\"https://github.com/GameMaker2k/PyUPC-EAN\" title=\"PyUPC-EAN barcode generator\">PyUPC-EAN</a>/%s (<a href=\"http://www.cherrypy.org/\" title=\"CherryPy python web server\">CherryPy</a>/%s)</address>" % (upcean.__version__, cherrypy.__version__);
   return "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n<head>\n<title> Barcode Generator 2k (PyUPC-EAN) </title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"Content-Language\" content=\"en\" />\n<meta name=\"generator\" content=\"CherryPy\" />\n<meta name=\"author\" content=\"Game Maker 2k\" />\n<meta name=\"keywords\" content=\"barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar\" />\n<meta name=\"description\" content=\"Barcode Generator with PyUPC-EAN\" /><meta name=\"resource-type\" content=\"document\" />\n<meta name=\"distribution\" content=\"global\" />\n<link rel=\"Generator\" href=\"http://www.cherrypy.org/\" title=\"CherryPy\" />\n</head>\n<body>\n<form name=\"upcean\" id=\"upcean\" method=\"get\" action=\"/upcean/\" onsubmit=\"location.href='/generate/'+upcean.upc.value+'/'+upcean.bctype.value+'/'+upcean.size.value+'/'+upcean.rotate.value+'/'+upcean.upc.value+'.'+upcean.imgtype.value; return false;\">\n<fieldset>\n<legend>Barcode Info: </legend>\n<label style=\"cursor: pointer;\" for=\"upc\">Enter UPC/EAN: </label><br />\n<input type=\"text\" id=\"upc\" name=\"upc\" /><br />\n<label style=\"cursor: pointer;\" for=\"imgtype\">Select and image type: </label><br />\n<select id=\"imgtype\" name=\"imgtype\">\n<option value=\"png\" selected=\"selected\">PNG Image</option>\n<option value=\"gif\">GIF Image</option>\n<option value=\"jpeg\">JPEG Image</option>\n<option value=\"bmp\">BMP Image</option>\n<option value=\"tiff\">TIFF Image</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"size\">Select barcode size: </label><br />\n<select id=\"size\" name=\"size\">\n<option value=\"1\" selected=\"selected\">1x</option>\n<option value=\"2\">2x</option>\n<option value=\"3\">3x</option>\n<option value=\"4\">4x</option>\n<option value=\"5\">5x</option>\n<option value=\"6\">6x</option>\n<option value=\"7\">7x</option>\n<option value=\"8\">8x</option>\n<option value=\"9\">9x</option>\n<option value=\"10\">10x</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"bctype\">Select barcode type: </label><br />\n<select id=\"bctype\" name=\"bctype\">\n<option value=\"barcode\" selected=\"selected\">Barcode</option>\n<option value=\"upca\">UPC-A</option>\n<option value=\"upce\">UPC-E</option>\n<option value=\"ean13\">EAN-13</option>\n<option value=\"ean8\">EAN-8</option>\n<option value=\"ean2\">EAN-2</option>\n<option value=\"ean5\">EAN-5</option>\n<option value=\"stf\">STF</option>\n<option value=\"itf\">ITF</option>\n<option value=\"itf14\">ITF-14</option>\n<option value=\"code11\">Code 11</option>\n<option value=\"code39\">Code 39</option>\n<option value=\"code93\">Code 93</option>\n<option value=\"codabar\">Codabar</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"rotate\">Select degrees to rotate image by: </label><br />\n<select id=\"rotate\" name=\"rotate\">\n<option value=\"0\" selected=\"selected\">0 &#176;</option>\n<option value=\"45\">45 &#176;</option>\n<option value=\"90\">90 &#176;</option>\n<option value=\"135\">135 &#176;</option>\n<option value=\"180\">180 &#176;</option>\n<option value=\"225\">225 &#176;</option>\n<option value=\"270\">270 &#176;</option>\n<option value=\"315\">315 &#176;</option>\n<option value=\"360\">360 &#176;</option>\n</select><br />\n<input type=\"submit\" />\n</fieldset>\n</form><br />\n"+ServerSignature+"\n</body>\n</html>";
 index.exposed = True;
 def generate(self, upc, bctype, bcsize, bcrotate, imgtype):
  imgdata = StringIO.StringIO();
  try:
   bctype;
  except KeyError:
   bctype = "barcode";
  try:
   bcsize;
  except KeyError:
   bcsize = 1;
  try:
   imgtype;
  except KeyError:
   imgtype = "png";
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = upcean.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type']= 'image/png';
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type']= 'image/gif';
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type']= 'image/jpeg';
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type']= 'image/bmp';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript';
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type']= 'image/x-portable-pixmap';
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type']= 'image/tiff';
  if(upc!=None and (int(bcrotate)==0 or bcrotate==None)):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).save(imgdata, file_ext[1]);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).save(imgdata, file_ext[1]);
  if(upc!=None and (int(bcrotate)>0 or int(bcrotate)<0)):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(upc!=None):
   imgdata.seek(0);
   return imgdata.buf;
 generate.exposed = True;

cherrypy.config.update({"environment": "production",
                        "log.error_file": "./errors.log",
                        "log.access_file": "./access.log",
                        "log.screen": True,
                        "gzipfilter.on": True,
                        "tools.gzip.on": True,
                        "tools.gzip.mime_types": ['text/*'],
                        "server.socket_host": host,
                        "server.socket_port": port,
                        "response.timeout": 6000,
                        });
cherrypy.root = GenerateIndexPage();
cherrypy.root.upcean = GenerateBarcodes();
cherrypy.quickstart(cherrypy.root);
