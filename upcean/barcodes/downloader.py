'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2016 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: downloader.py - Last Update: 3/1/2016 Ver. 2.7.13 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import re, os, sys, urllib, gzip, time, cgi, imp;
import logging as log;
haverequests = False;
try:
 imp.find_module('requests');
 haverequests = True;
 import requests;
except ImportError:
 haverequests = False;
havemechanize = False;
try:
 imp.find_module('mechanize');
 havemechanize = True;
 import mechanize;
except ImportError:
 havemechanize = False;
if(sys.version[0]=="2"):
 try:
  from cStringIO import StringIO;
 except ImportError:
  from StringIO import StringIO;
 # From http://python-future.org/compatible_idioms.html
 from urlparse import urlparse;
 from urllib import urlencode;
 from urllib2 import urlopen, Request, HTTPError;
 import urllib2, urlparse, cookielib;
if(sys.version[0]>="3"):
 from io import StringIO, BytesIO;
 # From http://python-future.org/compatible_idioms.html
 from urllib.parse import urlparse, urlencode
 from urllib.request import urlopen, Request
 from urllib.error import HTTPError
 import urllib.request as urllib2;
 import urllib.parse as urlparse;
 import http.cookiejar as cookielib;

geturls_cj = cookielib.CookieJar();
geturls_ua_firefox_windows7 = "Mozilla/5.0 (Windows NT 6.1; rv:44.0) Gecko/20100101 Firefox/44.0";
geturls_ua_seamonkey_windows7 = "Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0 SeaMonkey/2.39";
geturls_ua_chrome_windows7 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36";
geturls_ua_chromium_windows7 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/48.0.2564.116 Chrome/48.0.2564.116 Safari/537.36";
geturls_ua_midori_windows7 = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/538.15 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/538.15 Midori/0.5";
geturls_ua_internet_explorer_windows7 = "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko";
geturls_ua_googlebot_google = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";
geturls_ua_googlebot_google_old = "Googlebot/2.1 (+http://www.google.com/bot.html)";
geturls_ua = geturls_ua_firefox_windows7;
geturls_headers_firefox_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_firefox_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_seamonkey_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_seamonkey_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_chrome_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_chrome_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_chromium_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_chromium_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_midori_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_midori_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_internet_explorer_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_internet_explorer_windows7, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_googlebot_google = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_googlebot_google, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers_googlebot_google_old = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_googlebot_google_old, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"};
geturls_headers = geturls_headers_firefox_windows7;
geturls_download_sleep = 0;

def add_url_param(url, **params):
 n=3;
 parts = list(urlparse.urlsplit(url));
 d = dict(cgi.parse_qsl(parts[n])); # use cgi.parse_qs for list values
 d.update(params);
 parts[n]=urlencode(d);
 return urlparse.urlunsplit(parts);

def make_http_headers_from_dict_to_list(headers={'Referer': "http://google.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
 if isinstance(headers, dict):
  returnval = [];
  if(sys.version[0]=="2"):
   for headkey, headvalue in headers.iteritems():
    returnval.append((headkey, headvalue));
  if(sys.version[0]>="3"):
   for headkey, headvalue in headers.items():
    returnval.append((headkey, headvalue));
 elif isinstance(headers, list):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def make_http_headers_from_dict_to_pycurl(headers={'Referer': "http://google.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': "gzip, deflate", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
 if isinstance(headers, dict):
  returnval = [];
  if(sys.version[0]=="2"):
   for headkey, headvalue in headers.iteritems():
    returnval.append(headkey+": "+headvalue);
  if(sys.version[0]>="3"):
   for headkey, headvalue in headers.items():
    returnval.append(headkey+": "+headvalue);
 elif isinstance(headers, list):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def make_http_headers_from_list_to_dict(headers=[("Referer", "http://google.com/"), ("User-Agent", geturls_ua), ("Accept-Encoding", "gzip, deflate"), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")]):
 if isinstance(headers, list):
  returnval = {};
  mli = 0;
  mlil = len(headers);
  while(mli<mlil):
   returnval.update({headers[mli][0]: headers[mli][1]});
   mli = mli + 1;
 elif isinstance(headers, dict):
  returnval = headers;
 else:
  returnval = False;
 return returnval;

def download_from_url(httpurl, httpheaders, httpcookie, httplibuse="urllib", sleep=-1):
 global geturls_download_sleep, haverequests;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", buffersize=262144, sleep=-1):
 global geturls_download_sleep, haverequests;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_to_file(httpurl, httpheaders, httpcookie, httplibuse="urllib", outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
 global geturls_download_sleep, haverequests;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(httplibuse=="urllib1" or httplibuse=="urllib2"):
  httplibuse = "urllib";
 if(haverequests==False and httplibuse=="requests"):
  httplibuse = "urllib";
 if(havemechanize==False and httplibuse=="mechanize"):
  httplibuse = "urllib";
 if(httplibuse=="urllib"):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 elif(httplibuse=="requests"):
  returnval = download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 elif(httplibuse=="mechanize"):
  returnval = download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile, outpath, buffersize, sleep);
 else:
  returnval = False;
 return returnval;

def download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if isinstance(httpheaders, dict):
  httpheaders = make_http_headers_from_dict_to_list(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 log.info("Downloading URL "+httpurl);
 if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
  if(sys.version[0]=="2"):
   strbuf = StringIO(geturls_text.read());
  if(sys.version[0]>="3"):
   strbuf = BytesIO(geturls_text.read());
  gzstrbuf = gzip.GzipFile(fileobj=strbuf);
  returnval_content = gzstrbuf.read()[:];
 if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
  returnval_content = geturls_text.read()[:];
 returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.getcode()};
 geturls_text.close();
 return returnval;

def download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize=262144, sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 geturls_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(httpcookie));
 if isinstance(httpheaders, dict):
  httpheaders = make_http_headers_from_dict_to_list(httpheaders);
 geturls_opener.addheaders = httpheaders;
 time.sleep(sleep);
 geturls_text = geturls_opener.open(httpurl);
 downloadsize = int(geturls_text.info().get('Content-Length'));
 if downloadsize is None: downloadsize = 0;
 fulldatasize = 0;
 log.info("Downloading URL "+httpurl);
 with tempfile.NamedTemporaryFile('wb+', prefix="pyupcean-", delete=False) as f:
  tmpfilename = f.name;
  returnval = {'Type': "File", 'Filename': tmpfilename, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.getcode()};
  while True:
   databytes = geturls_text.read(buffersize);
   if not databytes: break;
   datasize = len(databytes);
   fulldatasize = datasize + fulldatasize;
   percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
   log.info("Downloading "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
   f.write(databytes);
  f.close();
 geturls_text.close();
 returnval.update({'Filesize': os.path.getsize(tmpfilename)});
 return returnval;

def download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
 global geturls_download_sleep;
 if(sleep<0):
  sleep = geturls_download_sleep;
 if(not outfile=="-"):
  outpath = outpath.rstrip(os.path.sep);
  filepath = os.path.realpath(outpath+os.path.sep+outfile);
  if(not os.path.exists(outpath)):
   os.makedirs(outpath);
  if(os.path.exists(outpath) and os.path.isfile(outpath)):
   return False;
  if(os.path.exists(filepath) and os.path.isdir(filepath)):
   return False;
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  log.info("Moving file "+tmpfilename+" to "+filepath);
  shutil.move(tmpfilename, filepath);
  if(os.path.exists(tmpfilename)==True):
   os.remove(tmpfilename);
  returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 if(outfile=="-" and sys.version[0]=="2"):
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  with open(tmpfilename, 'rb') as ft:
   f = StringIO();
   while True:
    databytes = ft.read(buffersize[1]);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
    f.write(databytes);
   f.close();
   ft.close();
   os.remove(tmpfilename);
  returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 if(outfile=="-" and sys.version[0]>="3"):
  pretmpfilename = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
  tmpfilename = pretmpfilename['Filename'];
  downloadsize = os.path.getsize(tmpfilename);
  fulldatasize = 0;
  with open(tmpfilename, 'rb') as ft:
   f = BytesIO();
   while True:
    databytes = ft.read(buffersize[1]);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
    f.write(databytes);
   f.close();
   ft.close();
   os.remove(tmpfilename);
  returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
 return returnval;

if(haverequests==True):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list_to_dict(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders, cookies=httpcookie);
  log.info("Downloading URL "+httpurl);
  if(geturls_text.headers.get('Content-Type')=="gzip" or geturls_text.headers.get('Content-Type')=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.content);
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.content);
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval_content = gzstrbuf.content[:];
  if(geturls_text.headers.get('Content-Type')!="gzip" and geturls_text.headers.get('Content-Type')!="deflate"):
   returnval_content = geturls_text.content[:];
  returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.headers), 'URL': geturls_text.url, 'Code': geturls_text.status_code};
  geturls_text.close();
  return returnval;

if(haverequests==False):
 def download_from_url_with_requests(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize=262144, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if isinstance(httpheaders, list):
   httpheaders = make_http_headers_from_list_to_dict(httpheaders);
  time.sleep(sleep);
  geturls_text = requests.get(httpurl, headers=httpheaders, cookies=httpcookie, stream=True);
  downloadsize = int(geturls_text.headers.get('Content-Length'));
  if downloadsize is None: downloadsize = 0;
  fulldatasize = 0;
  log.info("Downloading URL "+httpurl);
  with tempfile.NamedTemporaryFile('wb+', prefix="pyupcean-", delete=False) as f:
   tmpfilename = f.name;
   returnval = {'Type': "File", 'Filename': tmpfilename, 'Headers': dict(geturls_text.headers), 'URL': geturls_text.url, 'Code': geturls_text.status_code};
   for databytes in geturls_text.iter_content(chunk_size=buffersize):
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    log.info("Downloading "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
    f.write(databytes);
   f.close();
  geturls_text.close();
  returnval.update({'Filesize': os.path.getsize(tmpfilename)});
  return returnval;

if(haverequests==False):
 def download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize=262144, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep)
  return returnval;

if(haverequests==True):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(not outfile=="-"):
   outpath = outpath.rstrip(os.path.sep);
   filepath = os.path.realpath(outpath+os.path.sep+outfile);
   if(not os.path.exists(outpath)):
    os.makedirs(outpath);
   if(os.path.exists(outpath) and os.path.isfile(outpath)):
    return False;
   if(os.path.exists(filepath) and os.path.isdir(filepath)):
    return False;
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   log.info("Moving file "+tmpfilename+" to "+filepath);
   shutil.move(tmpfilename, filepath);
   if(os.path.exists(tmpfilename)==True):
    os.remove(tmpfilename);
   returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]=="2"):
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   with open(tmpfilename, 'rb') as ft:
    f = StringIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
     f.write(databytes);
    f.close();
    ft.close();
    os.remove(tmpfilename);
   returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]>="3"):
   pretmpfilename = download_from_url_file_with_requests(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   with open(tmpfilename, 'rb') as ft:
    f = BytesIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
     f.write(databytes);
    f.close();
    ft.close();
    os.remove(tmpfilename);
   returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  return returnval;

if(haverequests==False):
 def download_from_url_to_file_with_requests(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, outfile, outpath, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  geturls_opener = mechanize.Browser();
  if isinstance(httpheaders, dict):
   httpheaders = make_http_headers_from_dict_to_list(httpheaders);
  time.sleep(sleep);
  geturls_opener.addheaders = httpheaders;
  geturls_opener.set_cookiejar(httpcookie);
  geturls_opener.set_handle_robots(False);
  geturls_text = geturls_opener.open(httpurl);
  log.info("Downloading URL "+httpurl);
  if(geturls_text.info().get("Content-Encoding")=="gzip" or geturls_text.info().get("Content-Encoding")=="deflate"):
   if(sys.version[0]=="2"):
    strbuf = StringIO(geturls_text.read());
   if(sys.version[0]>="3"):
    strbuf = BytesIO(geturls_text.read());
   gzstrbuf = gzip.GzipFile(fileobj=strbuf);
   returnval_content = gzstrbuf.read()[:];
  if(geturls_text.info().get("Content-Encoding")!="gzip" and geturls_text.info().get("Content-Encoding")!="deflate"):
   returnval_content = geturls_text.read()[:];
  returnval = {'Type': "Content", 'Content': returnval_content, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.code};
  geturls_text.close();
  return returnval;

if(havemechanize==False):
 def download_from_url_with_mechanize(httpurl, httpheaders, httpcookie, sleep=-1):
  returnval = download_from_url_with_urllib(httpurl, httpheaders, httpcookie, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize=262144, sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  geturls_opener = mechanize.Browser();
  if isinstance(httpheaders, dict):
   httpheaders = make_http_headers_from_dict_to_list(httpheaders);
  time.sleep(sleep);
  geturls_opener.addheaders = httpheaders;
  geturls_opener.set_cookiejar(httpcookie);
  geturls_opener.set_handle_robots(False);
  geturls_text = geturls_opener.open(httpurl);
  downloadsize = int(geturls_text.info().get('Content-Length'));
  if downloadsize is None: downloadsize = 0;
  fulldatasize = 0;
  log.info("Downloading URL "+httpurl);
  with tempfile.NamedTemporaryFile('wb+', prefix="pyupcean-", delete=False) as f:
   tmpfilename = f.name;
   returnval = {'Type': "File", 'Filename': tmpfilename, 'Headers': dict(geturls_text.info()), 'URL': geturls_text.geturl(), 'Code': geturls_text.code};
   while True:
    databytes = geturls_text.read(buffersize);
    if not databytes: break;
    datasize = len(databytes);
    fulldatasize = datasize + fulldatasize;
    percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
    log.info("Downloading "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
    f.write(databytes);
   f.close();
  geturls_text.close();
  returnval.update({'Filesize': os.path.getsize(tmpfilename)});
  return returnval;

if(havemechanize==False):
 def download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize=262144, sleep=-1):
  returnval = download_from_url_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, sleep)
  return returnval;

if(havemechanize==True):
 def download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
  global geturls_download_sleep;
  if(sleep<0):
   sleep = geturls_download_sleep;
  if(not outfile=="-"):
   outpath = outpath.rstrip(os.path.sep);
   filepath = os.path.realpath(outpath+os.path.sep+outfile);
   if(not os.path.exists(outpath)):
    os.makedirs(outpath);
   if(os.path.exists(outpath) and os.path.isfile(outpath)):
    return False;
   if(os.path.exists(filepath) and os.path.isdir(filepath)):
    return False;
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   log.info("Moving file "+tmpfilename+" to "+filepath);
   shutil.move(tmpfilename, filepath);
   if(os.path.exists(tmpfilename)==True):
    os.remove(tmpfilename);
   returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]=="2"):
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   with open(tmpfilename, 'rb') as ft:
    f = StringIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
     f.write(databytes);
    f.close();
    ft.close();
    os.remove(tmpfilename);
   returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  if(outfile=="-" and sys.version[0]>="3"):
   pretmpfilename = download_from_url_file_with_mechanize(httpurl, httpheaders, httpcookie, buffersize[0], sleep);
   tmpfilename = pretmpfilename['Filename'];
   downloadsize = os.path.getsize(tmpfilename);
   fulldatasize = 0;
   with open(tmpfilename, 'rb') as ft:
    f = BytesIO();
    while True:
     databytes = ft.read(buffersize[1]);
     if not databytes: break;
     datasize = len(databytes);
     fulldatasize = datasize + fulldatasize;
     percentage = str("{0:.2f}".format(float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%";
     log.info("Copying "+str(fulldatasize)+" / "+str(downloadsize)+" bytes. "+str(percentage)+" done.");
     f.write(databytes);
    f.close();
    ft.close();
    os.remove(tmpfilename);
   returnval = {'Type': "Content", 'Content': f.getvalue(), 'Contentsize': downloadsize, 'Headers': pretmpfilename['Headers'], 'URL': pretmpfilename['URL'], 'Code': pretmpfilename['Code']};
  return returnval;

if(havemechanize==False):
 def download_from_url_to_file_with_mechanize(httpurl, httpheaders, httpcookie, outfile="-", outpath=os.getcwd(), buffersize=[262144, 262144], sleep=-1):
  returnval = download_from_url_to_file_with_urllib(httpurl, httpheaders, httpcookie, buffersize, outfile, outpath, sleep)
  return returnval;
