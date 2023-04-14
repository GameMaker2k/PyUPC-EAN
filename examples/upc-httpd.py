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

    $FileInfo: httpd.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1  - Author: cooldude2k $
'''

import tempfile, uuid, re, os, sys, cherrypy, upcean, argparse, time, datetime;
from PIL import Image, ImageDraw, ImageFont;
try:
 from io import StringIO, BytesIO;
except ImportError:
 try:
  from cStringIO import StringIO;
  from cStringIO import StringIO as BytesIO;
 except ImportError:
  from StringIO import StringIO;
  from StringIO import StringIO as BytesIO;
parser = argparse.ArgumentParser(description="A web server that draws barcodes with PyUPC-EAN powered by CherryPy web server.");
parser.add_argument("--port", "--port-number", default=8080, help="port number to use for server.");
parser.add_argument("--host", "--host-name", default="127.0.0.1", help="host name to use for server.");
parser.add_argument("--verbose", "--verbose-mode", help="show log on terminal screen.", action="store_true");
parser.add_argument("--gzip", "--gzip-mode", help="enable gzip http requests.", action="store_true");
parser.add_argument("--gzipfilter", "--gzipfilter-mode", help="enable gzipfilter mode.", action="store_true");
parser.add_argument("--accesslog", "--accesslog-file", help="location to store access log file.");
parser.add_argument("--errorlog", "--errorlog-file", help="location to store error log file.");
parser.add_argument("--timeout", "--response-timeout", default=6000, help="the number of seconds to allow responses to run.");
parser.add_argument("--environment", "--server-environment", default="production", help="The server.environment entry controls how CherryPy should run.");
getargs = parser.parse_args();
if(getargs.port is not None):
 port = int(getargs.port);
else:
 port = 8080;
if(getargs.host is not None):
 host = str(getargs.host);
else:
 host = "127.0.0.1";
if(getargs.timeout is not None):
 timeout = int(getargs.timeout);
else:
 timeout = 6000;
if(getargs.accesslog is not None):
 accesslog = str(getargs.accesslog);
else:
 accesslog = "./access.log";
if(getargs.errorlog is not None):
 errorlog = str(getargs.errorlog);
else:
 errorlog = "./errors.log";
if(getargs.environment is not None):
 serv_environ = str(getargs.environment);
else:
 serv_environ = "production";
pro_app_name = "Barcode Generator 2k";
pro_app_subname = "(PyUPC-EAN)";
pro_app_version = upcean.__version__;
radsta=0;
radmax=360;
radinc=5;
radout="\n";
while(radsta<=radmax):
 if(radsta==0):
  radout += "<option value=\""+str(radsta)+"\" selected=\"selected\">"+str(radsta)+" &#176;</option>\n";
 if(radsta>0):
  radout += "<option value=\""+str(radsta)+"\">"+str(radsta)+" &#176;</option>\n";
 radsta = radsta + radinc;
ServerSignature = "<address><a href=\"https://github.com/GameMaker2k/PyUPC-EAN\" title=\"PyUPC-EAN barcode generator\">PyUPC-EAN</a>/%s (<a href=\"http://www.cherrypy.org/\" title=\"CherryPy python web server\">CherryPy</a>/%s)</address>" % (upcean.__version__, cherrypy.__version__);
IndexHTMLCode = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n<head>\n<title> "+pro_app_name+" "+pro_app_subname+" </title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"Content-Language\" content=\"en\" />\n<meta name=\"generator\" content=\"CherryPy\" />\n<meta name=\"author\" content=\"Game Maker 2k\" />\n<meta name=\"keywords\" content=\"barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar,msi\" />\n<meta name=\"description\" content=\"Barcode Generator with PyUPC-EAN\" /><meta name=\"resource-type\" content=\"document\" />\n<meta name=\"distribution\" content=\"global\" />\n<link rel=\"Generator\" href=\"http://www.cherrypy.org/\" title=\"CherryPy\" />\n</head>\n<body>\n<form name=\"upcean\" id=\"upcean\" method=\"get\" action=\"/upcean/\" onsubmit=\"location.href='/generate/'+upcean.bctype.value+'/'+upcean.size.value+'/'+upcean.rotate.value+'/'+upcean.upc.value+'.'+upcean.imgtype.value; return false;\">\n<fieldset>\n<legend>Barcode Info: </legend>\n<label style=\"cursor: pointer;\" for=\"upc\">Enter UPC/EAN: </label><br />\n<input type=\"text\" id=\"upc\" name=\"upc\" /><br />\n<label style=\"cursor: pointer;\" for=\"imgtype\">Select a image type: </label><br />\n<select id=\"imgtype\" name=\"imgtype\">\n<option value=\"png\" selected=\"selected\">PNG Image</option>\n<option value=\"gif\">GIF Image</option>\n<option value=\"jpeg\">JPEG Image</option>\n<option value=\"bmp\">BMP Image</option>\n<option value=\"tiff\">TIFF Image</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"size\">Select barcode size: </label><br />\n<select id=\"size\" name=\"size\">\n<option value=\"1\" selected=\"selected\">1x</option>\n<option value=\"2\">2x</option>\n<option value=\"3\">3x</option>\n<option value=\"4\">4x</option>\n<option value=\"5\">5x</option>\n<option value=\"6\">6x</option>\n<option value=\"7\">7x</option>\n<option value=\"8\">8x</option>\n<option value=\"9\">9x</option>\n<option value=\"10\">10x</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"bctype\">Select barcode type: </label><br />\n<select id=\"bctype\" name=\"bctype\">\n<option value=\"upca\" selected=\"selected\">UPC-A</option>\n<option value=\"upce\">UPC-E</option>\n<option value=\"ean13\">EAN-13</option>\n<option value=\"ean8\">EAN-8</option>\n<option value=\"ean2\">EAN-2</option>\n<option value=\"ean5\">EAN-5</option>\n<option value=\"stf\">STF</option>\n<option value=\"itf\">ITF</option>\n<option value=\"itf14\">ITF-14</option>\n<option value=\"code11\">Code 11</option>\n<option value=\"code39\">Code 39</option>\n<option value=\"code93\">Code 93</option>\n<option value=\"codabar\">Codabar</option>\n<option value=\"msi\">MSI</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"rotate\">Select degrees to rotate image by: </label><br />\n<select id=\"rotate\" name=\"rotate\">"+radout+"</select><br />\n<input type=\"submit\" value=\"Generate\" />\n</fieldset>\n</form><br />\n"+ServerSignature+"\n</body>\n</html>";
class GenerateIndexPage(object):
 def index(self):
  cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
  return IndexHTMLCode;
 index.exposed = True;
 def generate(self, bctype, bcsize, bcrotate, imgtype):
  if(sys.version[0]=="2"):
   imgdata = StringIO();
  if(sys.version[0]>="3"):
   imgdata = BytesIO();
  try:
   bctype;
  except KeyError:
   bctype = "upca";
  try:
   bcsize;
  except KeyError:
   bcsize = 1;
  try:
   imgtype;
  except KeyError:
   imgtype = "png";
  upc = os.path.splitext(imgtype)[0];
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = upcean.getsfname.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type'] = "image/png";
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type'] = "image/gif";
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type'] = "image/jpeg";
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type'] = "image/bmp";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type'] = "image/x-portable-pixmap";
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type'] = "image/tiff";
  if(upc is not None and (int(bcrotate)==0 or bcrotate is None)):
   if(bctype.lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(bctype.lower(),upc,int(bcsize)).save(imgdata, file_ext[1]);
  if(upc is not None and (int(bcrotate)>0 or int(bcrotate)<0)):
   if(bctype.lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(bctype.lower(),upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(upc is not None):
   imgdata.seek(0);
   return imgdata.read();
 generate.exposed = True;
class GenerateBarcodes(object):
 def index(self, **params):
  if(sys.version[0]=="2"):
   imgdata = StringIO();
  if(sys.version[0]>="3"):
   imgdata = BytesIO();
  try:
   params['bctype'];
  except KeyError:
   params['bctype'] = "upca";
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
  file_ext = upcean.getsfname.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+params['imgtype'].lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type'] = "image/png";
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type'] = "image/gif";
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type'] = "image/jpeg";
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type'] = "image/bmp";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type'] = "image/x-portable-pixmap";
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type'] = "image/tiff";
  if(params['upc'] is not None and (int(params['rotate'])==0 or params['rotate'] is None)):
   if(params['bctype'].lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(params['bctype'].lower(),params['upc'],int(params['size'])).save(imgdata, file_ext[1]);
  if(params['upc'] is not None and (int(params['rotate'])>0 or int(params['rotate'])<0)):
   if(params['bctype'].lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(params['bctype'].lower(),params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(params['upc'] is not None):
   imgdata.seek(0);
   return imgdata.read();
  if(params['upc'] is None):
   cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
   return IndexHTMLCode;
 index.exposed = True;
 def generate(self, bctype, bcsize, bcrotate, imgtype):
  if(sys.version[0]=="2"):
   imgdata = StringIO();
  if(sys.version[0]>="3"):
   imgdata = BytesIO();
  try:
   bctype;
  except KeyError:
   bctype = "upca";
  try:
   bcsize;
  except KeyError:
   bcsize = 1;
  try:
   imgtype;
  except KeyError:
   imgtype = "png";
  upc = os.path.splitext(imgtype)[0];
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = upcean.getsfname.get_save_filename(tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower());
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type'] = "image/png";
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type'] = "image/gif";
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type'] = "image/jpeg";
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type'] = "image/bmp";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type'] = "application/postscript";
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type'] = "image/x-portable-pixmap";
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type'] = "image/tiff";
  if(upc is not None and (int(bcrotate)==0 or bcrotate is None)):
   if(params['bctype'].lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(params['bctype'].lower(),upc,int(bcsize)).save(imgdata, file_ext[1]);
  if(upc is not None and (int(bcrotate)>0 or int(bcrotate)<0)):
   if(params['bctype'].lower() in upcean.support.supported_barcodes("tuple")):
    upcean.encode.validate_draw_barcode(params['bctype'].lower(),upc,int(bcsize)).rotate(int(bcrotate), Image.BICUBIC, True).save(imgdata, file_ext[1]);
  if(upc is not None):
   imgdata.seek(0);
   return imgdata.read();
 generate.exposed = True;
cherrypy.config.update({"environment": serv_environ,
                        "log.error_file": errorlog,
                        "log.access_file": accesslog,
                        "log.screen": getargs.verbose,
                        "gzipfilter.on": getargs.gzipfilter,
                        "tools.gzip.on": getargs.gzip,
                        "tools.gzip.mime_types": ['text/*'],
                        "server.socket_host": host,
                        "server.socket_port": port,
                        "response.timeout": timeout,
                        });
cherrypy.root = GenerateIndexPage();
cherrypy.root.upcean = GenerateBarcodes();
cherrypy.quickstart(cherrypy.root);
