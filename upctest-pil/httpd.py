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

    $FileInfo: httpd.py - Last Update: 06/11/2013 Ver. 2.4.2 RC 3  - Author: cooldude2k $
'''

import re, os, sys, cherrypy, upcean, StringIO
from PIL import Image, ImageDraw, ImageFont
if sys.argv[1:]:
 port = int(sys.argv[1])
else:
 port = 8000
if sys.argv[2:]:
 host = str(sys.argv[2])
else:
 host = "127.0.0.1"
class GenerateBarcodes(object):
 def index(self, **params):
  imgdata = StringIO.StringIO()
  try:
   params['bctype']
  except KeyError:
   params['bctype'] = "barcode"
  try:
   params['size']
  except KeyError:
   params['size'] = 1
  try:
   params['imgtype']
  except KeyError:
   params['imgtype'] = "png"
  try:
   params['rotate']
  except KeyError:
   params['rotate'] = 0
  try:
   params['upc']
  except KeyError:
   params['upc'] = "000000000000"
  file_ext = upcean.get_save_filename("./test."+params['imgtype'].lower())
  if(file_ext[1]=="PNG"):
   cherrypy.response.headers['Content-Type']= 'image/png'
  if(file_ext[1]=="GIF"):
   cherrypy.response.headers['Content-Type']= 'image/gif'
  if(file_ext[1]=="JPEG"):
   cherrypy.response.headers['Content-Type']= 'image/jpeg'
  if(file_ext[1]=="BMP"):
   cherrypy.response.headers['Content-Type']= 'image/bmp'
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript'
  if(file_ext[1]=="EPS"):
   cherrypy.response.headers['Content-Type']= 'application/postscript'
  if(file_ext[1]=="PPM"):
   cherrypy.response.headers['Content-Type']= 'image/x-portable-pixmap'
  if(file_ext[1]=="TIFF"):
   cherrypy.response.headers['Content-Type']= 'image/tiff'
  if(int(params['rotate'])==0 or params['rotate']==None):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).save(imgdata, file_ext[1])
  if(int(params['rotate'])>0 or int(params['rotate'])<0):  
   if(params['bctype'].lower()=="barcode"):
    upcean.draw_barcode(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="upca"):
    upcean.draw_upca(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="upce"):
    upcean.draw_upce(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean13"):
    upcean.draw_ean13(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean8"):
    upcean.draw_ean8(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean2" and len(params['upc'])==2):
    upcean.draw_ean2(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="ean5" and len(params['upc'])==5):
    upcean.draw_ean5(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="stf"):
    upcean.draw_stf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="itf" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="itf14" and not (len(params['upc']) % 2) and len(params['upc']) > 5):
    upcean.draw_itf14(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code11" and len(params['upc']) > 0 and re.findall("([0-9\-]+)", params['upc'])):
    upcean.draw_code11(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code39" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code39(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="code93" and len(params['upc']) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", params['upc'])):
    upcean.draw_code93(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
   if(params['bctype'].lower()=="codabar" and len(params['upc']) > 0 and re.findall("^([a-dA-DeEnN\*tT])([0-9\-\$\:\/\.\+]+)([a-dA-DeEnN\*tT])$", params['upc'])):
    upcean.draw_codabar(params['upc'],int(params['size'])).rotate(int(params['rotate']), Image.BICUBIC, True).save(imgdata, file_ext[1])
  imgdata.seek(0)
  return imgdata.buf
 index.exposed = True
cherrypy.config.update({'environment': 'production',
                        'log.error_file': "./errors.log",
                        'log.access_file': "./access.log",
                        'log.screen': True,
                        'server.socket_host': host,
                        'server.socket_port': port,
                        'response.timeout': 6000,
                        }) 
cherrypy.quickstart(GenerateBarcodes())
