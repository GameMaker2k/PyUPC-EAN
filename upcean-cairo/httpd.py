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

    $FileInfo: httpd.py - Last Update: 11/23/2013 Ver. 2.5.0 RC 1  - Author: cooldude2k $
'''

import tempfile, uuid, re, os, sys, cherrypy, upcean, StringIO, argparse, time, datetime, cairo;
parser = argparse.ArgumentParser(description="A web server that draws barcodes with PyUPC-EAN powered by CherryPy web server.");
parser.add_argument("--port", "--port-number", help="port number to use for server.");
parser.add_argument("--host", "--host-name", help="host name to use for server.");
parser.add_argument("--verbose", "--verbose-mode", help="show log on terminal screen.", action="store_true");
parser.add_argument("--accesslog", "--accesslog-file", help="location to store access log file.");
parser.add_argument("--errorlog", "--errorlog-file", help="location to store error log file.");
parser.add_argument("--timeout", "--response-timeout", help="the number of seconds to allow responses to run.");
parser.add_argument("--environment", "--server-environment", help="The server.environment entry controls how CherryPy should run.");
getargs = parser.parse_args();
if(getargs.port!=None):
 port = int(getargs.port);
else:
 port = 8080;
if(getargs.host!=None):
 host = str(getargs.host);
else:
 host = "0.0.0.0";
if(getargs.accesslog!=None):
 accesslog = str(getargs.accesslog);
else:
 accesslog = "./access.log";
if(getargs.errorlog!=None):
 errorlog = str(getargs.errorlog);
else:
 errorlog = "./errors.log";
if(getargs.environment!=None):
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
IndexHTMLCode = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\" xml:lang=\"en\">\n<head>\n<title> "+pro_app_name+" "+pro_app_subname+" </title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"Content-Language\" content=\"en\" />\n<meta name=\"generator\" content=\"CherryPy\" />\n<meta name=\"author\" content=\"Game Maker 2k\" />\n<meta name=\"keywords\" content=\"barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar,msi\" />\n<meta name=\"description\" content=\"Barcode Generator with PyUPC-EAN\" /><meta name=\"resource-type\" content=\"document\" />\n<meta name=\"distribution\" content=\"global\" />\n<link rel=\"Generator\" href=\"http://www.cherrypy.org/\" title=\"CherryPy\" />\n</head>\n<body>\n<form name=\"upcean\" id=\"upcean\" method=\"get\" action=\"/upcean/\" onsubmit=\"location.href='/generate/'+upcean.bctype.value+'/'+upcean.size.value+'/'+upcean.rotate.value+'/'+upcean.upc.value+'.'+upcean.imgtype.value; return false;\">\n<fieldset>\n<legend>Barcode Info: </legend>\n<label style=\"cursor: pointer;\" for=\"upc\">Enter UPC/EAN: </label><br />\n<input type=\"text\" id=\"upc\" name=\"upc\" /><br />\n<label style=\"cursor: pointer;\" for=\"size\">Select barcode size: </label><br />\n<select id=\"size\" name=\"size\">\n<option value=\"1\" selected=\"selected\">1x</option>\n<option value=\"2\">2x</option>\n<option value=\"3\">3x</option>\n<option value=\"4\">4x</option>\n<option value=\"5\">5x</option>\n<option value=\"6\">6x</option>\n<option value=\"7\">7x</option>\n<option value=\"8\">8x</option>\n<option value=\"9\">9x</option>\n<option value=\"10\">10x</option>\n</select><br />\n<label style=\"cursor: pointer;\" for=\"bctype\">Select barcode type: </label><br />\n<select id=\"bctype\" name=\"bctype\">\n<option value=\"barcode\" selected=\"selected\">Barcode</option>\n<option value=\"upca\">UPC-A</option>\n<option value=\"upce\">UPC-E</option>\n<option value=\"ean13\">EAN-13</option>\n<option value=\"ean8\">EAN-8</option>\n<option value=\"ean2\">EAN-2</option>\n<option value=\"ean5\">EAN-5</option>\n<option value=\"stf\">STF</option>\n<option value=\"itf\">ITF</option>\n<option value=\"itf14\">ITF-14</option>\n<option value=\"code11\">Code 11</option>\n<option value=\"code39\">Code 39</option>\n<option value=\"code93\">Code 93</option>\n<option value=\"codabar\">Codabar</option>\n<option value=\"msi\">MSI</option>\n</select><br />\n<input type=\"hidden\" id=\"rotate\" name=\"rotate\" style=\"display: none;\" value=\"0\" />\n<input type=\"hidden\" id=\"imgtype\" name=\"imgtype\" style=\"display: none;\" value=\"png\" />\n<input type=\"submit\" value=\"Generate\" />\n</fieldset>\n</form><br />\n"+ServerSignature+"\n</body>\n</html>";
class GenerateIndexPage(object):
 def index(self):
  cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
  return IndexHTMLCode;
 index.exposed = True;
 def generate(self, bctype, bcsize, bcrotate, imgtype):
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
  upc = os.path.splitext(imgtype)[0];
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = (tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower(), "PNG");
  cherrypy.response.headers['Content-Type'] = "image/png";
  if(upc!=None):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="msi" and len(upc) > 0 and re.findall("([0-9]+)", upc)):
    upcean.draw_msi(upc,int(bcsize)).write_to_png(imgdata);
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
  file_ext = (tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower(), "PNG");
  cherrypy.response.headers['Content-Type'] = "image/png";
  if(params['upc']!=None and (int(params['rotate'])==0 or params['rotate']==None)):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).write_to_png(imgdata);
   if(params['bctype'].lower()=="msi" and len(params['upc']) > 0 and re.findall("([0-9]+)", params['upc'])):
    upcean.draw_msi(params['upc'],int(params['size'])).write_to_png(imgdata);
  if(params['upc']!=None and (int(params['rotate'])>0 or int(params['rotate'])<0)):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
   if(params['bctype'].lower()=="msi" and len(params['upc']) > 0 and re.findall("([0-9]+)", params['upc'])):
    upcean.draw_msi(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).write_to_png(imgdata);
  if(params['upc']!=None):
   imgdata.seek(0);
   return imgdata.buf;
  if(params['upc']==None):
   cherrypy.response.headers['Content-Type']= 'text/html; charset=UTF-8';
   return IndexHTMLCode;
 index.exposed = True;
 def generate(self, bctype, bcsize, bcrotate, imgtype):
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
  upc = os.path.splitext(imgtype)[0];
  try:
   bcrotate;
  except KeyError:
   bcrotate = 0;
  try:
   upc;
  except KeyError:
   upc = None;
  file_ext = (tempfile.gettempdir()+os.sep+"temp_"+str(uuid.uuid4()).replace("-", "")+imgtype.lower(), "PNG");
  cherrypy.response.headers['Content-Type'] = "image/png";
  if(upc!=None):  
   if(bctype.lower()=="barcode"):
    upcean.draw_barcode(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="upca"):
    upcean.draw_upca(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="upce"):
    upcean.draw_upce(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean13"):
    upcean.draw_ean13(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean8"):
    upcean.draw_ean8(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean2" and len(upc)==2):
    upcean.draw_ean2(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="ean5" and len(upc)==5):
    upcean.draw_ean5(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="stf"):
    upcean.draw_stf(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="itf" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="itf14" and not (len(upc) % 2) and len(upc) > 5):
    upcean.draw_itf14(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code11" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_code11(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code39" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code39(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="code93" and len(upc) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", upc)):
    upcean.draw_code93(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="codabar" and len(upc) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", upc)):
    upcean.draw_codabar(upc,int(bcsize)).write_to_png(imgdata);
   if(bctype.lower()=="msi" and len(upc) > 0 and re.findall("([0-9\-]+)", upc)):
    upcean.draw_msi(upc,int(bcsize)).write_to_png(imgdata);
  if(upc!=None):
   imgdata.seek(0);
   return imgdata.buf;
 generate.exposed = True;
cherrypy.config.update({"environment": serv_environ,
                        "log.error_file": errorlog,
                        "log.access_file": accesslog,
                        "log.screen": getargs.verbose,
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
