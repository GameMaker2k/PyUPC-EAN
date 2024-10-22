#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2015-2024 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2015-2024 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: downloader.py - Last Update: 10/17/2024 Ver. 0.9.6 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import socket
import shutil
import logging
import platform

from upcean.versioninfo import getcuryear, __author__, __copyright__, __credits__, __copyright_year__, __license__, __license_string__, __maintainer__, __email__, __status__, __project__, __project_url__, __version_info__, __build_time__, __build_time_utc__, __build_python_info__, __build_python_is_set__, get_build_python_info, __revision__, __version__, __version_alt__, version_info, __version_date_info__, __version_date__, __version_date_alt__, version_date

# FTP Support
ftpssl = True
try:
    from ftplib import FTP, FTP_TLS
except ImportError:
    ftpssl = False
    from ftplib import FTP

try:
    basestring
except NameError:
    basestring = str

# URL Parsing
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

# Paramiko support
haveparamiko = False
try:
    import paramiko
    haveparamiko = True
except ImportError:
    pass

# PySFTP support
havepysftp = False
try:
    import pysftp
    havepysftp = True
except ImportError:
    pass

# Requests support
haverequests = False
try:
    import requests
    haverequests = True
    import urllib3
    logging.getLogger("urllib3").setLevel(logging.WARNING)
except ImportError:
    pass

# HTTPX support
havehttpx = False
try:
    import httpx
    havehttpx = True
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
except ImportError:
    pass

# HTTP and URL parsing
try:
    from urllib.request import Request, build_opener, HTTPBasicAuthHandler
    from urllib.parse import urlparse
except ImportError:
    from urllib2 import Request, build_opener, HTTPBasicAuthHandler
    from urlparse import urlparse

# StringIO and BytesIO
try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

__use_pysftp__ = False
if(not havepysftp):
    __use_pysftp__ = False
__use_http_lib__ = "httpx"
if(__use_http_lib__ == "httpx" and haverequests and not havehttpx):
    __use_http_lib__ = "requests"
if(__use_http_lib__ == "requests" and havehttpx and not haverequests):
    __use_http_lib__ = "httpx"
if((__use_http_lib__ == "httpx" or __use_http_lib__ == "requests") and not havehttpx and not haverequests):
    __use_http_lib__ = "urllib"

windowsNT4_ua_string = "Windows NT 4.0"
windowsNT4_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                       'SEC-CH-UA-BITNESS': "32", 'SEC-CH-UA-PLATFORM': "4.0.0"}
windows2k_ua_string = "Windows NT 5.0"
windows2k_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                      'SEC-CH-UA-BITNESS': "32", 'SEC-CH-UA-PLATFORM': "5.0.0"}
windowsXP_ua_string = "Windows NT 5.1"
windowsXP_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                      'SEC-CH-UA-BITNESS': "32", 'SEC-CH-UA-PLATFORM': "5.1.0"}
windowsXP64_ua_string = "Windows NT 5.2; Win64; x64"
windowsXP64_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                        'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "5.1.0"}
windows7_ua_string = "Windows NT 6.1; Win64; x64"
windows7_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                     'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "6.1.0"}
windows8_ua_string = "Windows NT 6.2; Win64; x64"
windows8_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                     'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "6.2.0"}
windows81_ua_string = "Windows NT 6.3; Win64; x64"
windows81_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                      'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "6.3.0"}
windows10_ua_string = "Windows NT 10.0; Win64; x64"
windows10_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                      'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "10.0.0"}
windows11_ua_string = "Windows NT 11.0; Win64; x64"
windows11_ua_addon = {'SEC-CH-UA-PLATFORM': "Windows", 'SEC-CH-UA-ARCH': "x86",
                      'SEC-CH-UA-BITNESS': "64", 'SEC-CH-UA-PLATFORM': "11.0.0"}
geturls_ua_firefox_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    "; rv:109.0) Gecko/20100101 Firefox/117.0"
geturls_ua_seamonkey_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    "; rv:91.0) Gecko/20100101 Firefox/91.0 SeaMonkey/2.53.17"
geturls_ua_chrome_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
geturls_ua_chromium_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    ") AppleWebKit/537.36 (KHTML, like Gecko) Chromium/117.0.0.0 Chrome/117.0.0.0 Safari/537.36"
geturls_ua_palemoon_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    "; rv:102.0) Gecko/20100101 Goanna/6.3 Firefox/102.0 PaleMoon/32.4.0.1"
geturls_ua_opera_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0"
geturls_ua_vivaldi_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Vivaldi/6.2.3105.48"
geturls_ua_internet_explorer_windows7 = "Mozilla/5.0 (" + \
    windows7_ua_string+"; Trident/7.0; rv:11.0) like Gecko"
geturls_ua_microsoft_edge_windows7 = "Mozilla/5.0 ("+windows7_ua_string + \
    ") AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"
geturls_ua_upcean_python = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(
    proname=__project__, prover=__version__, prourl=__project_url__)
if(platform.python_implementation() != ""):
    py_implementation = platform.python_implementation()
if(platform.python_implementation() == ""):
    py_implementation = "Python"
geturls_ua_upcean_python_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system(
)+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp=py_implementation, pyver=platform.python_version(), proname=__project__, prover=__version__)
geturls_ua_googlebot_google = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
geturls_ua_googlebot_google_old = "Googlebot/2.1 (+http://www.google.com/bot.html)"
geturls_ua = geturls_ua_firefox_windows7
geturls_headers_firefox_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_firefox_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                    'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers_seamonkey_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_seamonkey_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                      'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers_chrome_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_chrome_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7",
                                   'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close", 'SEC-CH-UA': "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"", 'SEC-CH-UA-FULL-VERSION': "117.0.5938.63"}
geturls_headers_chrome_windows7.update(windows7_ua_addon)
geturls_headers_chromium_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_chromium_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                     'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close", 'SEC-CH-UA': "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"24\"", 'SEC-CH-UA-FULL-VERSION': "117.0.5938.63"}
geturls_headers_chromium_windows7.update(windows7_ua_addon)
geturls_headers_palemoon_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_palemoon_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                     'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers_opera_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_opera_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7",
                                  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close", 'SEC-CH-UA': "\"Chromium\";v=\"116\", \"Not;A=Brand\";v=\"8\", \"Opera\";v=\"102\"", 'SEC-CH-UA-FULL-VERSION': "102.0.4880.56"}
geturls_headers_opera_windows7.update(windows7_ua_addon)
geturls_headers_vivaldi_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_vivaldi_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7",
                                    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close", 'SEC-CH-UA': "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Vivaldi\";v=\"6.2\"", 'SEC-CH-UA-FULL-VERSION': "6.2.3105.48"}
geturls_headers_vivaldi_windows7.update(windows7_ua_addon)
geturls_headers_internet_explorer_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_internet_explorer_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language':
                                              "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers_microsoft_edge_windows7 = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_microsoft_edge_windows7, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7",
                                           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close", 'SEC-CH-UA': "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"", 'SEC-CH-UA-FULL-VERSION': "117.0.2045.31"}
geturls_headers_microsoft_edge_windows7.update(windows7_ua_addon)
geturls_headers_upcean_python = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_upcean_python, 'Accept-Encoding': "none", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close",
                                   'SEC-CH-UA': "\""+__project__+"\";v=\""+str(__version__)+"\", \"Not;A=Brand\";v=\"8\", \""+py_implementation+"\";v=\""+str(platform.release())+"\"", 'SEC-CH-UA-FULL-VERSION': str(__version__), 'SEC-CH-UA-PLATFORM': ""+py_implementation+"", 'SEC-CH-UA-ARCH': ""+platform.machine()+"", 'SEC-CH-UA-PLATFORM': str(__version__), 'SEC-CH-UA-BITNESS': str(PyBitness)}
geturls_headers_upcean_python_alt = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_upcean_python_alt, 'Accept-Encoding': "none", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close",
                                       'SEC-CH-UA': "\""+__project__+"\";v=\""+str(__version__)+"\", \"Not;A=Brand\";v=\"8\", \""+py_implementation+"\";v=\""+str(platform.release())+"\"", 'SEC-CH-UA-FULL-VERSION': str(__version__), 'SEC-CH-UA-PLATFORM': ""+py_implementation+"", 'SEC-CH-UA-ARCH': ""+platform.machine()+"", 'SEC-CH-UA-PLATFORM': str(__version__), 'SEC-CH-UA-BITNESS': str(PyBitness)}
geturls_headers_googlebot_google = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_googlebot_google, 'Accept-Encoding': "none", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                    'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers_googlebot_google_old = {'Referer': "http://google.com/", 'User-Agent': geturls_ua_googlebot_google_old, 'Accept-Encoding': "none", 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6",
                                        'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}
geturls_headers = geturls_headers_firefox_windows7
geturls_download_sleep = 0


def download_file_from_ftp_file(url):
    urlparts = urlparse(url)
    file_name = os.path.basename(urlparts.path)
    file_dir = os.path.dirname(urlparts.path)
    if(urlparts.username is not None):
        ftp_username = urlparts.username
    else:
        ftp_username = "anonymous"
    if(urlparts.password is not None):
        ftp_password = urlparts.password
    elif(urlparts.password is None and urlparts.username == "anonymous"):
        ftp_password = "anonymous"
    else:
        ftp_password = ""
    if(urlparts.scheme == "ftp"):
        ftp = FTP()
    elif(urlparts.scheme == "ftps" and ftpssl):
        ftp = FTP_TLS()
    else:
        return False
    if(urlparts.scheme == "sftp"):
        if(__use_pysftp__):
            return download_file_from_pysftp_file(url)
        else:
            return download_file_from_sftp_file(url)
    elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return download_file_from_http_file(url)
    ftp_port = urlparts.port
    if(urlparts.port is None):
        ftp_port = 21
    try:
        ftp.connect(urlparts.hostname, ftp_port)
    except socket.gaierror:
        log.info("Error With URL "+url)
        return False
    except socket.timeout:
        log.info("Error With URL "+url)
        return False
    ftp.login(urlparts.username, urlparts.password)
    if(urlparts.scheme == "ftps"):
        ftp.prot_p()
    ftpfile = BytesIO()
    ftp.retrbinary("RETR "+urlparts.path, ftpfile.write)
    #ftp.storbinary("STOR "+urlparts.path, ftpfile.write);
    ftp.close()
    ftpfile.seek(0, 0)
    return ftpfile


def download_file_from_ftp_string(url):
    ftpfile = download_file_from_ftp_file(url)
    return ftpfile.read()


def upload_file_to_ftp_file(ftpfile, url):
    urlparts = urlparse(url)
    file_name = os.path.basename(urlparts.path)
    file_dir = os.path.dirname(urlparts.path)
    if(urlparts.username is not None):
        ftp_username = urlparts.username
    else:
        ftp_username = "anonymous"
    if(urlparts.password is not None):
        ftp_password = urlparts.password
    elif(urlparts.password is None and urlparts.username == "anonymous"):
        ftp_password = "anonymous"
    else:
        ftp_password = ""
    if(urlparts.scheme == "ftp"):
        ftp = FTP()
    elif(urlparts.scheme == "ftps" and ftpssl):
        ftp = FTP_TLS()
    else:
        return False
    if(urlparts.scheme == "sftp"):
        if(__use_pysftp__):
            return upload_file_to_pysftp_file(url)
        else:
            return upload_file_to_sftp_file(url)
    elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    ftp_port = urlparts.port
    if(urlparts.port is None):
        ftp_port = 21
    try:
        ftp.connect(urlparts.hostname, ftp_port)
    except socket.gaierror:
        log.info("Error With URL "+url)
        return False
    except socket.timeout:
        log.info("Error With URL "+url)
        return False
    ftp.login(urlparts.username, urlparts.password)
    if(urlparts.scheme == "ftps"):
        ftp.prot_p()
    ftp.storbinary("STOR "+urlparts.path, ftpfile)
    ftp.close()
    ftpfile.seek(0, 0)
    return ftpfile


def upload_file_to_ftp_string(ftpstring, url):
    ftpfileo = BytesIO(ftpstring)
    ftpfile = upload_file_to_ftp_file(ftpfileo, url)
    ftpfileo.close()
    return ftpfile


class RawIteratorWrapper:
    def __init__(self, iterator):
        self.iterator = iterator
        self.buffer = b""
        self._iterator_exhausted = False

    def read(self, size=-1):
        if self._iterator_exhausted:
            return b''
        while size < 0 or len(self.buffer) < size:
            try:
                chunk = next(self.iterator)
                self.buffer += chunk
            except StopIteration:
                self._iterator_exhausted = True
                break
        if size < 0:
            size = len(self.buffer)
        result, self.buffer = self.buffer[:size], self.buffer[size:]
        return result


def download_file_from_http_file(url, headers=None, usehttp=__use_http_lib__):
    if headers is None:
        headers = {}
    # Parse the URL to extract username and password if present
    urlparts = urlparse(url)
    username = urlparts.username
    password = urlparts.password
    # Rebuild the URL without the username and password
    netloc = urlparts.hostname
    if urlparts.scheme == "sftp":
        if __use_pysftp__:
            return download_file_from_pysftp_file(url)
        else:
            return download_file_from_sftp_file(url)
    elif urlparts.scheme == "ftp" or urlparts.scheme == "ftps":
        return download_file_from_ftp_file(url)
    if urlparts.port:
        netloc += ':' + str(urlparts.port)
    rebuilt_url = urlunparse((urlparts.scheme, netloc, urlparts.path,
                             urlparts.params, urlparts.query, urlparts.fragment))
    # Create a temporary file object
    httpfile = BytesIO()
    if usehttp == 'requests' and haverequests:
        # Use the requests library if selected and available
        if username and password:
            response = requests.get(rebuilt_url, headers=headers, auth=(
                username, password), stream=True)
        else:
            response = requests.get(rebuilt_url, headers=headers, stream=True)
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, httpfile)
    elif usehttp == 'httpx' and havehttpx:
        # Use httpx if selected and available
        with httpx.Client(follow_redirects=True) as client:
            if username and password:
                response = client.get(
                    rebuilt_url, headers=headers, auth=(username, password))
            else:
                response = client.get(rebuilt_url, headers=headers)
            raw_wrapper = RawIteratorWrapper(response.iter_bytes())
            shutil.copyfileobj(raw_wrapper, httpfile)
    else:
        # Use urllib as a fallback
        # Build a Request object for urllib
        request = Request(rebuilt_url, headers=headers)
        # Create an opener object for handling URLs
        if username and password:
            # Create a password manager
            password_mgr = HTTPPasswordMgrWithDefaultRealm()
            # Add the username and password
            password_mgr.add_password(None, rebuilt_url, username, password)
            # Create an authentication handler using the password manager
            auth_handler = HTTPBasicAuthHandler(password_mgr)
            # Build the opener with the authentication handler
            opener = build_opener(auth_handler)
        else:
            opener = build_opener()
        response = opener.open(request)
        shutil.copyfileobj(response, httpfile)
    # Reset file pointer to the start
    httpfile.seek(0, 0)
    # Return the temporary file object
    return httpfile


def download_file_from_http_string(url, headers=geturls_ua_upcean_python_alt, usehttp=__use_http_lib__):
    httpfile = download_file_from_http_file(url, headers, usehttp)
    return httpfile.read()


if(haveparamiko):
    def download_file_from_sftp_file(url):
        urlparts = urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme == "ftp"):
            return download_file_from_ftp_file(url)
        elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return download_file_from_http_file(url)
        if(urlparts.scheme != "sftp"):
            return False
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(urlparts.hostname, port=sftp_port,
                        username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+url)
            return False
        except socket.timeout:
            log.info("Error With URL "+url)
            return False
        sftp = ssh.open_sftp()
        sftpfile = BytesIO()
        sftp.getfo(urlparts.path, sftpfile)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def download_file_from_sftp_file(url):
        return False

if(haveparamiko):
    def download_file_from_sftp_string(url):
        sftpfile = download_file_from_sftp_file(url)
        return sftpfile.read()
else:
    def download_file_from_sftp_string(url):
        return False

if(haveparamiko):
    def upload_file_to_sftp_file(sftpfile, url):
        urlparts = urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme == "ftp"):
            return upload_file_to_ftp_file(url)
        elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        if(urlparts.scheme != "sftp"):
            return False
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(urlparts.hostname, port=sftp_port,
                        username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+url)
            return False
        except socket.timeout:
            log.info("Error With URL "+url)
            return False
        sftp = ssh.open_sftp()
        sftp.putfo(sftpfile, urlparts.path)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def upload_file_to_sftp_file(sftpfile, url):
        return False

if(haveparamiko):
    def upload_file_to_sftp_string(sftpstring, url):
        sftpfileo = BytesIO(sftpstring)
        sftpfile = upload_file_to_sftp_files(ftpfileo, url)
        sftpfileo.close()
        return sftpfile
else:
    def upload_file_to_sftp_string(url):
        return False

if(havepysftp):
    def download_file_from_pysftp_file(url):
        urlparts = urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme == "ftp"):
            return download_file_from_ftp_file(url)
        elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return download_file_from_http_file(url)
        if(urlparts.scheme != "sftp"):
            return False
        try:
            pysftp.Connection(urlparts.hostname, port=sftp_port,
                              username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+url)
            return False
        except socket.timeout:
            log.info("Error With URL "+url)
            return False
        sftp = ssh.open_sftp()
        sftpfile = BytesIO()
        sftp.getfo(urlparts.path, sftpfile)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def download_file_from_pysftp_file(url):
        return False

if(havepysftp):
    def download_file_from_pysftp_string(url):
        sftpfile = download_file_from_pysftp_file(url)
        return sftpfile.read()
else:
    def download_file_from_pyftp_string(url):
        return False

if(havepysftp):
    def upload_file_to_pysftp_file(sftpfile, url):
        urlparts = urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme == "ftp"):
            return upload_file_to_ftp_file(url)
        elif(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        if(urlparts.scheme != "sftp"):
            return False
        try:
            pysftp.Connection(urlparts.hostname, port=sftp_port,
                              username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+url)
            return False
        except socket.timeout:
            log.info("Error With URL "+url)
            return False
        sftp = ssh.open_sftp()
        sftp.putfo(sftpfile, urlparts.path)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def upload_file_to_pysftp_file(sftpfile, url):
        return False

if(havepysftp):
    def upload_file_to_pysftp_string(sftpstring, url):
        sftpfileo = BytesIO(sftpstring)
        sftpfile = upload_file_to_pysftp_files(ftpfileo, url)
        sftpfileo.close()
        return sftpfile
else:
    def upload_file_to_pysftp_string(url):
        return False

def download_file_from_internet_file(url, headers=geturls_ua_upcean_python_alt, usehttp=__use_http_lib__):
    urlparts = urlparse(url)
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return download_file_from_http_file(url, headers, usehttp)
    elif(urlparts.scheme == "ftp" or urlparts.scheme == "ftps"):
        return download_file_from_ftp_file(url)
    elif(urlparts.scheme == "sftp"):
        if(__use_pysftp__ and havepysftp):
            return download_file_from_pysftp_file(url)
        else:
            return download_file_from_sftp_file(url)
    else:
        return False
    return False


def download_file_from_internet_string(url, headers=geturls_ua_upcean_python_alt, usehttp=__use_http_lib__):
    urlparts = urlparse(url)
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return download_file_from_http_string(url, headers, usehttp)
    elif(urlparts.scheme == "ftp" or urlparts.scheme == "ftps"):
        return download_file_from_ftp_string(url)
    elif(urlparts.scheme == "sftp"):
        if(__use_pysftp__ and havepysftp):
            return download_file_from_pysftp_string(url)
        else:
            return download_file_from_sftp_string(url)
    else:
        return False
    return False


def upload_file_to_internet_file(ifp, url):
    urlparts = urlparse(url)
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    elif(urlparts.scheme == "ftp" or urlparts.scheme == "ftps"):
        return upload_file_to_ftp_file(ifp, url)
    elif(urlparts.scheme == "sftp"):
        if(__use_pysftp__ and havepysftp):
            return upload_file_to_pysftp_file(ifp, url)
        else:
            return upload_file_to_sftp_file(ifp, url)
    else:
        return False
    return False


def upload_file_to_internet_string(ifp, url):
    urlparts = urlparse(url)
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    elif(urlparts.scheme == "ftp" or urlparts.scheme == "ftps"):
        return upload_file_to_ftp_string(ifp, url)
    elif(urlparts.scheme == "sftp"):
        if(__use_pysftp__ and havepysftp):
            return upload_file_to_pysftp_string(ifp, url)
        else:
            return upload_file_to_sftp_string(ifp, url)
    else:
        return False
    return False

            return path + "/" + execfile


def listize(varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newlistreg = {}
    newlistrev = {}
    newlistfull = {}
    while(il < ix):
        newlistreg.update({ilx: varlist[il]})
        newlistrev.update({varlist[il]: ilx})
        ilx = ilx + 1
        il = il + 1
    newlistfull = {1: newlistreg, 2: newlistrev,
                   'reg': newlistreg, 'rev': newlistrev}
    return newlistfull


def twolistize(varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newlistnamereg = {}
    newlistnamerev = {}
    newlistdescreg = {}
    newlistdescrev = {}
    newlistfull = {}
    while(il < ix):
        newlistnamereg.update({ilx: varlist[il][0].strip()})
        newlistnamerev.update({varlist[il][0].strip(): ilx})
        newlistdescreg.update({ilx: varlist[il][1].strip()})
        newlistdescrev.update({varlist[il][1].strip(): ilx})
        ilx = ilx + 1
        il = il + 1
    newlistnametmp = {1: newlistnamereg, 2: newlistnamerev,
                      'reg': newlistnamereg, 'rev': newlistnamerev}
    newlistdesctmp = {1: newlistdescreg, 2: newlistdescrev,
                      'reg': newlistdescreg, 'rev': newlistdescrev}
    newlistfull = {1: newlistnametmp, 2: newlistdesctmp,
                   'name': newlistnametmp, 'desc': newlistdesctmp}
    return newlistfull


def arglistize(proexec, *varlist):
    il = 0
    ix = len(varlist)
    ilx = 1
    newarglist = [proexec]
    while(il < ix):
        if varlist[il][0] is not None:
            newarglist.append(varlist[il][0])
        if varlist[il][1] is not None:
            newarglist.append(varlist[il][1])
        il = il + 1
    return newarglist


def fix_header_names(header_dict):
    if(sys.version[0] == "2"):
        header_dict = {k.title(): v for k, v in header_dict.iteritems()}
    if(sys.version[0] >= "3"):
        header_dict = {k.title(): v for k, v in header_dict.items()}
    return header_dict

# hms_string by ArcGIS Python Recipes
# https://arcpy.wordpress.com/2012/04/20/146/


def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.0
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

# get_readable_size by Lipis
# http://stackoverflow.com/posts/14998888/revisions


def get_readable_size(bytes, precision=1, unit="IEC"):
    unit = unit.upper()
    if(unit != "IEC" and unit != "SI"):
        unit = "IEC"
    if(unit == "IEC"):
        units = [" B", " KiB", " MiB", " GiB", " TiB", " PiB", " EiB", " ZiB"]
        unitswos = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]
        unitsize = 1024.0
    if(unit == "SI"):
        units = [" B", " kB", " MB", " GB", " TB", " PB", " EB", " ZB"]
        unitswos = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB"]
        unitsize = 1000.0
    return_val = {}
    orgbytes = bytes
    for unit in units:
        if abs(bytes) < unitsize:
            strformat = "%3."+str(precision)+"f%s"
            pre_return_val = (strformat % (bytes, unit))
            pre_return_val = re.sub(
                r"([0]+) ([A-Za-z]+)", r" \2", pre_return_val)
            pre_return_val = re.sub(r"\. ([A-Za-z]+)", r" \1", pre_return_val)
            alt_return_val = pre_return_val.split()
            return_val = {'Bytes': orgbytes, 'ReadableWithSuffix': pre_return_val,
                          'ReadableWithoutSuffix': alt_return_val[0], 'ReadableSuffix': alt_return_val[1]}
            return return_val
        bytes /= unitsize
    strformat = "%."+str(precision)+"f%s"
    pre_return_val = (strformat % (bytes, "YiB"))
    pre_return_val = re.sub(r"([0]+) ([A-Za-z]+)", r" \2", pre_return_val)
    pre_return_val = re.sub(r"\. ([A-Za-z]+)", r" \1", pre_return_val)
    alt_return_val = pre_return_val.split()
    return_val = {'Bytes': orgbytes, 'ReadableWithSuffix': pre_return_val,
                  'ReadableWithoutSuffix': alt_return_val[0], 'ReadableSuffix': alt_return_val[1]}
    return return_val


def get_readable_size_from_file(infile, precision=1, unit="IEC", usehashes=False, usehashtypes="md5,sha1"):
    unit = unit.upper()
    usehashtypes = usehashtypes.lower()
    getfilesize = os.path.getsize(infile)
    return_val = get_readable_size(getfilesize, precision, unit)
    if(usehashes):
        hashtypelist = usehashtypes.split(",")
        openfile = open(infile, "rb")
        filecontents = openfile.read()
        openfile.close()
        listnumcount = 0
        listnumend = len(hashtypelist)
        while(listnumcount < listnumend):
            hashtypelistlow = hashtypelist[listnumcount].strip()
            hashtypelistup = hashtypelistlow.upper()
            filehash = hashlib.new(hashtypelistup)
            filehash.update(filecontents)
            filegethash = filehash.hexdigest()
            return_val.update({hashtypelistup: filegethash})
            listnumcount += 1
    return return_val


def get_readable_size_from_string(instring, precision=1, unit="IEC", usehashes=False, usehashtypes="md5,sha1"):
    unit = unit.upper()
    usehashtypes = usehashtypes.lower()
    getfilesize = len(instring)
    return_val = get_readable_size(getfilesize, precision, unit)
    if(usehashes):
        hashtypelist = usehashtypes.split(",")
        listnumcount = 0
        listnumend = len(hashtypelist)
        while(listnumcount < listnumend):
            hashtypelistlow = hashtypelist[listnumcount].strip()
            hashtypelistup = hashtypelistlow.upper()
            filehash = hashlib.new(hashtypelistup)
            if(sys.version[0] == "2"):
                filehash.update(instring)
            if(sys.version[0] >= "3"):
                filehash.update(instring.encode('utf-8'))
            filegethash = filehash.hexdigest()
            return_val.update({hashtypelistup: filegethash})
            listnumcount += 1
    return return_val


def http_status_to_reason(code):
    reasons = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'IM Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        421: 'Misdirected Request',
        422: 'Unprocessable Entity',
        423: 'Locked',
        424: 'Failed Dependency',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required'
    }
    return reasons.get(code, 'Unknown Status Code')


def ftp_status_to_reason(code):
    reasons = {
        110: 'Restart marker reply',
        120: 'Service ready in nnn minutes',
        125: 'Data connection already open; transfer starting',
        150: 'File status okay; about to open data connection',
        200: 'Command okay',
        202: 'Command not implemented, superfluous at this site',
        211: 'System status, or system help reply',
        212: 'Directory status',
        213: 'File status',
        214: 'Help message',
        215: 'NAME system type',
        220: 'Service ready for new user',
        221: 'Service closing control connection',
        225: 'Data connection open; no transfer in progress',
        226: 'Closing data connection',
        227: 'Entering Passive Mode',
        230: 'User logged in, proceed',
        250: 'Requested file action okay, completed',
        257: '"PATHNAME" created',
        331: 'User name okay, need password',
        332: 'Need account for login',
        350: 'Requested file action pending further information',
        421: 'Service not available, closing control connection',
        425: 'Can\'t open data connection',
        426: 'Connection closed; transfer aborted',
        450: 'Requested file action not taken',
        451: 'Requested action aborted. Local error in processing',
        452: 'Requested action not taken. Insufficient storage space in system',
        500: 'Syntax error, command unrecognized',
        501: 'Syntax error in parameters or arguments',
        502: 'Command not implemented',
        503: 'Bad sequence of commands',
        504: 'Command not implemented for that parameter',
        530: 'Not logged in',
        532: 'Need account for storing files',
        550: 'Requested action not taken. File unavailable',
        551: 'Requested action aborted. Page type unknown',
        552: 'Requested file action aborted. Exceeded storage allocation',
        553: 'Requested action not taken. File name not allowed'
    }
    return reasons.get(code, 'Unknown Status Code')


def sftp_status_to_reason(code):
    reasons = {
        0: 'SSH_FX_OK',
        1: 'SSH_FX_EOF',
        2: 'SSH_FX_NO_SUCH_FILE',
        3: 'SSH_FX_PERMISSION_DENIED',
        4: 'SSH_FX_FAILURE',
        5: 'SSH_FX_BAD_MESSAGE',
        6: 'SSH_FX_NO_CONNECTION',
        7: 'SSH_FX_CONNECTION_LOST',
        8: 'SSH_FX_OP_UNSUPPORTED'
    }
    return reasons.get(code, 'Unknown Status Code')


def make_http_headers_from_dict_to_list(headers={'Referer': "http://google.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
    if isinstance(headers, dict):
        returnval = []
        if(sys.version[0] == "2"):
            for headkey, headvalue in headers.iteritems():
                returnval.append((headkey, headvalue))
        if(sys.version[0] >= "3"):
            for headkey, headvalue in headers.items():
                returnval.append((headkey, headvalue))
    elif isinstance(headers, list):
        returnval = headers
    else:
        returnval = False
    return returnval


def make_http_headers_from_dict_to_pycurl(headers={'Referer': "http://google.com/", 'User-Agent': geturls_ua, 'Accept-Encoding': compression_supported, 'Accept-Language': "en-US,en;q=0.8,en-CA,en-GB;q=0.6", 'Accept-Charset': "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7", 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'Connection': "close"}):
    if isinstance(headers, dict):
        returnval = []
        if(sys.version[0] == "2"):
            for headkey, headvalue in headers.iteritems():
                returnval.append(headkey+": "+headvalue)
        if(sys.version[0] >= "3"):
            for headkey, headvalue in headers.items():
                returnval.append(headkey+": "+headvalue)
    elif isinstance(headers, list):
        returnval = headers
    else:
        returnval = False
    return returnval


def make_http_headers_from_pycurl_to_dict(headers):
    header_dict = {}
    headers = headers.strip().split('\r\n')
    for header in headers:
        parts = header.split(': ', 1)
        if(len(parts) == 2):
            key, value = parts
            header_dict[key.title()] = value
    return header_dict


def make_http_headers_from_list_to_dict(headers=[("Referer", "http://google.com/"), ("User-Agent", geturls_ua), ("Accept-Encoding", compression_supported), ("Accept-Language", "en-US,en;q=0.8,en-CA,en-GB;q=0.6"), ("Accept-Charset", "ISO-8859-1,ISO-8859-15,utf-8;q=0.7,*;q=0.7"), ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"), ("Connection", "close")]):
    if isinstance(headers, list):
        returnval = {}
        mli = 0
        mlil = len(headers)
        while(mli < mlil):
            returnval.update({headers[mli][0]: headers[mli][1]})
            mli = mli + 1
    elif isinstance(headers, dict):
        returnval = headers
    else:
        returnval = False
    return returnval


def get_httplib_support(checkvalue=None):
    global haverequests, havemechanize, havehttplib2, haveurllib3, havehttpx, havehttpcore, haveparamiko, havepysftp
    returnval = []
    returnval.append("ftp")
    returnval.append("httplib")
    if(havehttplib2):
        returnval.append("httplib2")
    returnval.append("urllib")
    if(haveurllib3):
        returnval.append("urllib3")
        returnval.append("request3")
    returnval.append("request")
    if(haverequests):
        returnval.append("requests")
    if(haveaiohttp):
        returnval.append("aiohttp")
    if(havehttpx):
        returnval.append("httpx")
        returnval.append("httpx2")
    if(havemechanize):
        returnval.append("mechanize")
    if(havepycurl):
        returnval.append("pycurl")
        if(hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
            returnval.append("pycurl2")
        if(hasattr(pycurl, "CURL_HTTP_VERSION_3_0")):
            returnval.append("pycurl3")
    if(haveparamiko):
        returnval.append("sftp")
    if(havepysftp):
        returnval.append("pysftp")
    if(not checkvalue is None):
        if(checkvalue == "urllib1" or checkvalue == "urllib2"):
            checkvalue = "urllib"
        if(checkvalue == "httplib1"):
            checkvalue = "httplib"
        if(checkvalue in returnval):
            returnval = True
        else:
            returnval = False
    return returnval


def check_httplib_support(checkvalue="urllib"):
    if(checkvalue == "urllib1" or checkvalue == "urllib2"):
        checkvalue = "urllib"
    if(checkvalue == "httplib1"):
        checkvalue = "httplib"
    returnval = get_httplib_support(checkvalue)
    return returnval


def get_httplib_support_list():
    returnval = get_httplib_support(None)
    return returnval


def download_from_url(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", buffersize=524288, sleep=-1, timeout=10):
    global geturls_download_sleep, havezstd, havebrotli, haveaiohttp, haverequests, havemechanize, havepycurl, havehttplib2, haveurllib3, havehttpx, havehttpcore, haveparamiko, havepysftp
    if(sleep < 0):
        sleep = geturls_download_sleep
    if(timeout <= 0):
        timeout = 10
    if(httplibuse == "urllib1" or httplibuse == "urllib2" or httplibuse == "request"):
        httplibuse = "urllib"
    if(httplibuse == "httplib1"):
        httplibuse = "httplib"
    if(not haverequests and httplibuse == "requests"):
        httplibuse = "urllib"
    if(not haveaiohttp and httplibuse == "aiohttp"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx2"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore2"):
        httplibuse = "urllib"
    if(not havemechanize and httplibuse == "mechanize"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl2"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl2" and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havepycurl and httplibuse == "pycurl3"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl2"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havehttplib2 and httplibuse == "httplib2"):
        httplibuse = "httplib"
    if(not haveparamiko and httplibuse == "sftp"):
        httplibuse = "ftp"
    if(not havepysftp and httplibuse == "pysftp"):
        httplibuse = "ftp"
    urlparts = urlparse.urlparse(httpurl)
    if(isinstance(httpheaders, list)):
        httpheaders = make_http_headers_from_list_to_dict(httpheaders)
    httpheaders = fix_header_names(httpheaders)
    if(httpuseragent is not None):
        if('User-Agent' in httpheaders):
            httpheaders['User-Agent'] = httpuseragent
        else:
            httpuseragent.update({'User-Agent': httpuseragent})
    if(httpreferer is not None):
        if('Referer' in httpheaders):
            httpheaders['Referer'] = httpreferer
        else:
            httpuseragent.update({'Referer': httpreferer})
    if(urlparts.username is not None or urlparts.password is not None):
        if(sys.version[0] == "2"):
            inurlencode = b64encode(
                str(urlparts.username+":"+urlparts.password))
        if(sys.version[0] >= "3"):
            inurlencode = b64encode(
                str(urlparts.username+":"+urlparts.password).encode()).decode("UTF-8")
        httpheaders.update({'Authorization': "Basic "+inurlencode})
    geturls_opener = build_opener(HTTPCookieProcessor(httpcookie))
    if(httplibuse == "urllib" or httplibuse == "mechanize"):
        if(isinstance(httpheaders, dict)):
            httpheaders = make_http_headers_from_dict_to_list(httpheaders)
    if(httplibuse == "pycurl" or httplibuse == "pycurl2" or httplibuse == "pycurl3"):
        if(isinstance(httpheaders, dict)):
            httpheaders = make_http_headers_from_dict_to_pycurl(httpheaders)
    geturls_opener.addheaders = httpheaders
    time.sleep(sleep)
    if(postdata is not None and not isinstance(postdata, dict)):
        postdata = urlencode(postdata)
    if(httplibuse == "urllib" or httplibuse == "request"):
        geturls_request = Request(httpurl)
        try:
            if(httpmethod == "GET"):
                geturls_text = geturls_opener.open(geturls_request)
            elif(httpmethod == "POST"):
                geturls_text = geturls_opener.open(
                    geturls_request, data=postdata)
            else:
                geturls_text = geturls_opener.open(geturls_request)
        except HTTPError as geturls_text_error:
            geturls_text = geturls_text_error
            log.info("Error With URL "+httpurl)
        except URLError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.getcode()
        try:
            httpcodereason = geturls_text.reason
        except AttributeError:
            httpcodereason = http_status_to_reason(geturls_text.getcode())
        try:
            httpversionout = geturls_text.version
        except AttributeError:
            httpversionout = "1.1"
        httpmethodout = geturls_request.get_method()
        httpurlout = geturls_text.geturl()
        httpheaderout = geturls_text.info()
        httpheadersentout = httpheaders
    elif(httplibuse == "httplib"):
        if(urlparts[0] == "http"):
            httpconn = HTTPConnection(urlparts[1], timeout=timeout)
        elif(urlparts[0] == "https"):
            httpconn = HTTPSConnection(urlparts[1], timeout=timeout)
        else:
            return False
        if(postdata is not None and not isinstance(postdata, dict)):
            postdata = urlencode(postdata)
        try:
            if(httpmethod == "GET"):
                httpconn.request("GET", urlparts[2], headers=httpheaders)
            elif(httpmethod == "POST"):
                httpconn.request(
                    "GET", urlparts[2], body=postdata, headers=httpheaders)
            else:
                httpconn.request("GET", urlparts[2], headers=httpheaders)
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except BlockingIOError:
            log.info("Error With URL "+httpurl)
            return False
        geturls_text = httpconn.getresponse()
        httpcodeout = geturls_text.status
        httpcodereason = geturls_text.reason
        if(geturls_text.version == "10"):
            httpversionout = "1.0"
        else:
            httpversionout = "1.1"
        httpmethodout = geturls_text._method
        httpurlout = httpurl
        httpheaderout = geturls_text.getheaders()
        httpheadersentout = httpheaders
    elif(httplibuse == "httplib2"):
        if(urlparts[0] == "http"):
            httpconn = HTTPConnectionWithTimeout(urlparts[1], timeout=timeout)
        elif(urlparts[0] == "https"):
            httpconn = HTTPSConnectionWithTimeout(urlparts[1], timeout=timeout)
        else:
            return False
        if(postdata is not None and not isinstance(postdata, dict)):
            postdata = urlencode(postdata)
        try:
            if(httpmethod == "GET"):
                httpconn.request("GET", urlparts[2], headers=httpheaders)
            elif(httpmethod == "POST"):
                httpconn.request(
                    "GET", urlparts[2], body=postdata, headers=httpheaders)
            else:
                httpconn.request("GET", urlparts[2], headers=httpheaders)
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except BlockingIOError:
            log.info("Error With URL "+httpurl)
            return False
        geturls_text = httpconn.getresponse()
        httpcodeout = geturls_text.status
        httpcodereason = geturls_text.reason
        if(geturls_text.version == "10"):
            httpversionout = "1.0"
        else:
            httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = httpurl
        httpheaderout = geturls_text.getheaders()
        httpheadersentout = httpheaders
    elif(httplibuse == "urllib3" or httplibuse == "request3"):
        timeout = urllib3.util.Timeout(connect=timeout, read=timeout)
        urllib_pool = urllib3.PoolManager(headers=httpheaders, timeout=timeout)
        try:
            if(httpmethod == "GET"):
                geturls_text = urllib_pool.request(
                    "GET", httpurl, headers=httpheaders, preload_content=False)
            elif(httpmethod == "POST"):
                geturls_text = urllib_pool.request(
                    "POST", httpurl, body=postdata, headers=httpheaders, preload_content=False)
            else:
                geturls_text = urllib_pool.request(
                    "GET", httpurl, headers=httpheaders, preload_content=False)
        except urllib3.exceptions.ConnectTimeoutError:
            log.info("Error With URL "+httpurl)
            return False
        except urllib3.exceptions.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except urllib3.exceptions.MaxRetryError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except ValueError:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status
        httpcodereason = geturls_text.reason
        if(geturls_text.version == "10"):
            httpversionout = "1.0"
        else:
            httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = geturls_text.geturl()
        httpheaderout = geturls_text.info()
        httpheadersentout = httpheaders
    elif(httplibuse == "requests"):
        try:
            reqsession = requests.Session()
            if(httpmethod == "GET"):
                geturls_text = reqsession.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
            elif(httpmethod == "POST"):
                geturls_text = reqsession.post(
                    httpurl, timeout=timeout, data=postdata, headers=httpheaders, cookies=httpcookie)
            else:
                geturls_text = reqsession.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
        except requests.exceptions.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except requests.exceptions.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status_code
        httpcodereason = geturls_text.reason
        if(geturls_text.raw.version == "10"):
            httpversionout = "1.0"
        else:
            httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = geturls_text.url
        httpheaderout = geturls_text.headers
        httpheadersentout = geturls_text.request.headers
    elif(httplibuse == "aiohttp"):
        try:
            reqsession = aiohttp.ClientSession(cookie_jar=httpcookie, headers=httpheaders,
                                               timeout=timeout, read_timeout=timeout, conn_timeout=timeout, read_bufsize=buffersize)
            if(httpmethod == "GET"):
                geturls_text = reqsession.get(httpurl)
            elif(httpmethod == "POST"):
                geturls_text = reqsession.post(httpurl, data=postdata)
            else:
                geturls_text = reqsession.get(httpurl)
        except aiohttp.exceptions.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except aiohttp.exceptions.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status
        httpcodereason = geturls_text.reason
        httpversionout = geturls_text.version
        httpmethodout = geturls_text.method
        httpurlout = geturls_text.url
        httpheaderout = geturls_text.headers
        httpheadersentout = geturls_text.request_info.headers
    elif(httplibuse == "httpx"):
        try:
            if(httpmethod == "GET"):
                httpx_pool = httpx.Client(
                    http1=True, http2=False, trust_env=True)
                geturls_text = httpx_pool.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
            elif(httpmethod == "POST"):
                httpx_pool = httpx.Client(
                    http1=True, http2=False, trust_env=True)
                geturls_text = httpx_pool.post(
                    httpurl, timeout=timeout, data=postdata, headers=httpheaders, cookies=httpcookie)
            else:
                httpx_pool = httpx.Client(
                    http1=True, http2=False, trust_env=True)
                geturls_text = httpx_pool.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
        except httpx.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except httpx.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status_code
        try:
            httpcodereason = geturls_text.reason_phrase
        except:
            httpcodereason = http_status_to_reason(geturls_text.status_code)
        httpversionout = geturls_text.http_version
        httpmethodout = httpmethod
        httpurlout = str(geturls_text.url)
        httpheaderout = geturls_text.headers
        httpheadersentout = geturls_text.request.headers
    elif(httplibuse == "httpx2"):
        try:
            if(httpmethod == "GET"):
                httpx_pool = httpx.Client(
                    http1=True, http2=True, trust_env=True)
                geturls_text = httpx_pool.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
            elif(httpmethod == "POST"):
                httpx_pool = httpx.Client(
                    http1=True, http2=True, trust_env=True)
                geturls_text = httpx_pool.post(
                    httpurl, timeout=timeout, data=postdata, headers=httpheaders, cookies=httpcookie)
            else:
                httpx_pool = httpx.Client(
                    http1=True, http2=True, trust_env=True)
                geturls_text = httpx_pool.get(
                    httpurl, timeout=timeout, headers=httpheaders, cookies=httpcookie)
        except httpx.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except httpx.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status_code
        try:
            httpcodereason = geturls_text.reason_phrase
        except:
            httpcodereason = http_status_to_reason(geturls_text.status_code)
        httpversionout = geturls_text.http_version
        httpmethodout = httpmethod
        httpurlout = str(geturls_text.url)
        httpheaderout = geturls_text.headers
        httpheadersentout = geturls_text.request.headers
    elif(httplibuse == "httpcore"):
        try:
            if(httpmethod == "GET"):
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=False)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, headers=httpheaders)
            elif(httpmethod == "POST"):
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=False)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, data=postdata, headers=httpheaders)
            else:
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=False)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, headers=httpheaders)
        except httpcore.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except httpcore.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status
        httpcodereason = http_status_to_reason(geturls_text.status)
        httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = str(httpurl)
        httpheaderout = geturls_text.headers
        httpheadersentout = httpheaders
    elif(httplibuse == "httpcore2"):
        try:
            if(httpmethod == "GET"):
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=True)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, headers=httpheaders)
            elif(httpmethod == "POST"):
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=True)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, data=postdata, headers=httpheaders)
            else:
                httpx_pool = httpcore.ConnectionPool(http1=True, http2=True)
                geturls_text = httpx_pool.request(
                    "GET", httpurl, headers=httpheaders)
        except httpcore.ConnectTimeout:
            log.info("Error With URL "+httpurl)
            return False
        except httpcore.ConnectError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.status
        httpcodereason = http_status_to_reason(geturls_text.status)
        httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = str(httpurl)
        httpheaderout = geturls_text.headers
        httpheadersentout = httpheaders
    elif(httplibuse == "mechanize"):
        geturls_opener = mechanize.Browser()
        if(isinstance(httpheaders, dict)):
            httpheaders = make_http_headers_from_dict_to_list(httpheaders)
        time.sleep(sleep)
        geturls_opener.addheaders = httpheaders
        geturls_opener.set_cookiejar(httpcookie)
        geturls_opener.set_handle_robots(False)
        if(postdata is not None and not isinstance(postdata, dict)):
            postdata = urlencode(postdata)
        try:
            if(httpmethod == "GET"):
                geturls_text = geturls_opener.open(httpurl)
            elif(httpmethod == "POST"):
                geturls_text = geturls_opener.open(httpurl, data=postdata)
            else:
                geturls_text = geturls_opener.open(httpurl)
        except mechanize.HTTPError as geturls_text_error:
            geturls_text = geturls_text_error
            log.info("Error With URL "+httpurl)
        except URLError:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.code
        httpcodereason = geturls_text.msg
        httpversionout = "1.1"
        httpmethodout = httpmethod
        httpurlout = geturls_text.geturl()
        httpheaderout = geturls_text.info()
        reqhead = geturls_opener.request
        httpheadersentout = reqhead.header_items()
    elif(httplibuse == "pycurl"):
        retrieved_body = BytesIO()
        retrieved_headers = BytesIO()
        try:
            if(httpmethod == "GET"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_1_1)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            elif(httpmethod == "POST"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_1_1)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.setopt(geturls_text.POST, True)
                geturls_text.setopt(geturls_text.POSTFIELDS, postdata)
                geturls_text.perform()
            else:
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_1_1)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            retrieved_headers.seek(0)
            if(sys.version[0] == "2"):
                pycurlhead = retrieved_headers.read()
            if(sys.version[0] >= "3"):
                pycurlhead = retrieved_headers.read().decode('UTF-8')
            pyhttpverinfo = re.findall(
                r'^HTTP/([0-9.]+) (\d+)(?: ([A-Za-z\s]+))?$', pycurlhead.splitlines()[0].strip().rstrip('\r\n'))[0]
            pycurlheadersout = make_http_headers_from_pycurl_to_dict(
                pycurlhead)
            retrieved_body.seek(0)
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except ValueError:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.getinfo(geturls_text.HTTP_CODE)
        httpcodereason = http_status_to_reason(
            geturls_text.getinfo(geturls_text.HTTP_CODE))
        httpversionout = pyhttpverinfo[0]
        httpmethodout = httpmethod
        httpurlout = geturls_text.getinfo(geturls_text.EFFECTIVE_URL)
        httpheaderout = pycurlheadersout
        httpheadersentout = httpheaders
    elif(httplibuse == "pycurl2"):
        retrieved_body = BytesIO()
        retrieved_headers = BytesIO()
        try:
            if(httpmethod == "GET"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_2_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            elif(httpmethod == "POST"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_2_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.setopt(geturls_text.POST, True)
                geturls_text.setopt(geturls_text.POSTFIELDS, postdata)
                geturls_text.perform()
            else:
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_2_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            retrieved_headers.seek(0)
            if(sys.version[0] == "2"):
                pycurlhead = retrieved_headers.read()
            if(sys.version[0] >= "3"):
                pycurlhead = retrieved_headers.read().decode('UTF-8')
            pyhttpverinfo = re.findall(
                r'^HTTP/([0-9.]+) (\d+)(?: ([A-Za-z\s]+))?$', pycurlhead.splitlines()[0].strip())[0]
            pycurlheadersout = make_http_headers_from_pycurl_to_dict(
                pycurlhead)
            retrieved_body.seek(0)
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except ValueError:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.getinfo(geturls_text.HTTP_CODE)
        httpcodereason = http_status_to_reason(
            geturls_text.getinfo(geturls_text.HTTP_CODE))
        httpversionout = pyhttpverinfo[0]
        httpmethodout = httpmethod
        httpurlout = geturls_text.getinfo(geturls_text.EFFECTIVE_URL)
        httpheaderout = pycurlheadersout
        httpheadersentout = httpheaders
    elif(httplibuse == "pycurl3"):
        retrieved_body = BytesIO()
        retrieved_headers = BytesIO()
        try:
            if(httpmethod == "GET"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_3_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            elif(httpmethod == "POST"):
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_3_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.setopt(geturls_text.POST, True)
                geturls_text.setopt(geturls_text.POSTFIELDS, postdata)
                geturls_text.perform()
            else:
                geturls_text = pycurl.Curl()
                geturls_text.setopt(geturls_text.HTTP_VERSION,
                                    geturls_text.CURL_HTTP_VERSION_3_0)
                geturls_text.setopt(geturls_text.URL, httpurl)
                geturls_text.setopt(
                    geturls_text.WRITEFUNCTION, retrieved_body.write)
                geturls_text.setopt(geturls_text.HTTPHEADER, httpheaders)
                geturls_text.setopt(
                    geturls_text.HEADERFUNCTION, retrieved_headers.write)
                geturls_text.setopt(geturls_text.FOLLOWLOCATION, True)
                geturls_text.setopt(geturls_text.TIMEOUT, timeout)
                geturls_text.perform()
            retrieved_headers.seek(0)
            if(sys.version[0] == "2"):
                pycurlhead = retrieved_headers.read()
            if(sys.version[0] >= "3"):
                pycurlhead = retrieved_headers.read().decode('UTF-8')
            pyhttpverinfo = re.findall(
                r'^HTTP/([0-9.]+) (\d+)(?: ([A-Za-z\s]+))?$', pycurlhead.splitlines()[0].strip().rstrip('\r\n'))[0]
            pycurlheadersout = make_http_headers_from_pycurl_to_dict(
                pycurlhead)
            retrieved_body.seek(0)
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except ValueError:
            log.info("Error With URL "+httpurl)
            return False
        httpcodeout = geturls_text.getinfo(geturls_text.HTTP_CODE)
        httpcodereason = http_status_to_reason(
            geturls_text.getinfo(geturls_text.HTTP_CODE))
        httpversionout = pyhttpverinfo[0]
        httpmethodout = httpmethod
        httpurlout = geturls_text.getinfo(geturls_text.EFFECTIVE_URL)
        httpheaderout = pycurlheadersout
        httpheadersentout = httpheaders
    elif(httplibuse == "ftp"):
        geturls_text = download_file_from_ftp_file(httpurl)
        if(not geturls_text):
            return False
        downloadsize = None
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        returnval = {'Type': "Content", 'Content': returnval_content, 'Contentsize': fulldatasize, 'ContentsizeAlt': {'IEC': get_readable_size(
            fulldatasize, 2, "IEC"), 'SI': get_readable_size(fulldatasize, 2, "SI")}, 'Headers': None, 'Version': None, 'Method': None, 'HeadersSent': None, 'URL': httpurl, 'Code': None}
        geturls_text.close()
    elif(httplibuse == "sftp"):
        geturls_text = download_file_from_sftp_file(httpurl)
        if(not geturls_text):
            return False
        downloadsize = None
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        returnval = {'Type': "Content", 'Content': returnval_content, 'Contentsize': fulldatasize, 'ContentsizeAlt': {'IEC': get_readable_size(
            fulldatasize, 2, "IEC"), 'SI': get_readable_size(fulldatasize, 2, "SI")}, 'Headers': None, 'Version': None, 'Method': None, 'HeadersSent': None, 'URL': httpurl, 'Code': None}
        geturls_text.close()
        return returnval
    elif(httplibuse == "pysftp"):
        geturls_text = download_file_from_pysftp_file(httpurl)
        if(not geturls_text):
            return False
        downloadsize = None
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        returnval = {'Type': "Content", 'Content': returnval_content, 'Contentsize': fulldatasize, 'ContentsizeAlt': {'IEC': get_readable_size(
            fulldatasize, 2, "IEC"), 'SI': get_readable_size(fulldatasize, 2, "SI")}, 'Headers': None, 'Version': None, 'Method': None, 'HeadersSent': None, 'URL': httpurl, 'Code': None}
        geturls_text.close()
        return returnval
    else:
        returnval = False
    if(isinstance(httpheaderout, list) and (httplibuse != "pycurl" and httplibuse != "pycurl2" and httplibuse != "pycurl3")):
        httpheaderout = dict(
            make_http_headers_from_list_to_dict(httpheaderout))
    if(isinstance(httpheaderout, list) and (httplibuse == "pycurl" or httplibuse == "pycurl2" or httplibuse == "pycurl3")):
        httpheaderout = dict(make_http_headers_from_pycurl_to_dict(
            "\r\n".join(httpheaderout)))
    if(sys.version[0] == "2"):
        try:
            prehttpheaderout = httpheaderout
            httpheaderkeys = httpheaderout.keys()
            imax = len(httpheaderkeys)
            ic = 0
            httpheaderout = {}
            while(ic < imax):
                httpheaderout.update(
                    {httpheaderkeys[ic]: prehttpheaderout[httpheaderkeys[ic]]})
                ic += 1
        except AttributeError:
            pass
    httpheaderout = fix_header_names(httpheaderout)
    if(isinstance(httpheadersentout, list) and (httplibuse != "pycurl" and httplibuse != "pycurl2" and httplibuse != "pycurl3")):
        httpheadersentout = dict(
            make_http_headers_from_list_to_dict(httpheadersentout))
    if(isinstance(httpheadersentout, list) and (httplibuse == "pycurl" or httplibuse == "pycurl2" or httplibuse == "pycurl3")):
        httpheadersentout = dict(make_http_headers_from_pycurl_to_dict(
            "\r\n".join(httpheadersentout)))
    httpheadersentout = fix_header_names(httpheadersentout)
    log.info("Downloading URL "+httpurl)
    if(httplibuse == "urllib" or httplibuse == "request" or httplibuse == "request3" or httplibuse == "aiohttp" or httplibuse == "httplib" or httplibuse == "httplib2" or httplibuse == "urllib3" or httplibuse == "mechanize"):
        downloadsize = httpheaderout.get('Content-Length')
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        geturls_text.close()
        if(httpheaderout.get("Content-Encoding") == "gzip"):
            try:
                returnval_content = zlib.decompress(
                    returnval_content, 16+zlib.MAX_WBITS)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "deflate"):
            try:
                returnval_content = zlib.decompress(returnval_content)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "br" and havebrotli):
            try:
                returnval_content = brotli.decompress(returnval_content)
            except brotli.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "zstd" and havezstd):
            try:
                returnval_content = zstandard.decompress(returnval_content)
            except zstandard.error:
                pass
        elif((httpheaderout.get("Content-Encoding") == "lzma" or httpheaderout.get("Content-Encoding") == "xz") and havelzma):
            try:
                returnval_content = lzma.decompress(returnval_content)
            except zstandard.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "bzip2"):
            try:
                returnval_content = bz2.decompress(returnval_content)
            except zstandard.error:
                pass
    elif(httplibuse == "httpx" or httplibuse == "httpx2" or httplibuse == "httpcore" or httplibuse == "httpcore2"):
        downloadsize = httpheaderout.get('Content-Length')
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.read()
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
                break
            strbuf.seek(0)
            returnval_content = strbuf.read()
        geturls_text.close()
        if(httpheaderout.get("Content-Encoding") == "gzip"):
            try:
                returnval_content = zlib.decompress(
                    returnval_content, 16+zlib.MAX_WBITS)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "deflate"):
            try:
                returnval_content = zlib.decompress(returnval_content)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "br" and havebrotli):
            try:
                returnval_content = brotli.decompress(returnval_content)
            except brotli.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "zstd" and havezstd):
            try:
                returnval_content = zstandard.decompress(returnval_content)
            except zstandard.error:
                pass
        elif((httpheaderout.get("Content-Encoding") == "lzma" or httpheaderout.get("Content-Encoding") == "xz") and havelzma):
            try:
                returnval_content = lzma.decompress(returnval_content)
            except zstandard.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "bzip2"):
            try:
                returnval_content = bz2.decompress(returnval_content)
            except zstandard.error:
                pass
    elif(httplibuse == "requests"):
        log.info("Downloading URL "+httpurl)
        downloadsize = httpheaderout.get('Content-Length')
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = geturls_text.raw.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        geturls_text.close()
        if(httpheaderout.get("Content-Encoding") == "gzip"):
            try:
                returnval_content = zlib.decompress(
                    returnval_content, 16+zlib.MAX_WBITS)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "deflate"):
            try:
                returnval_content = zlib.decompress(returnval_content)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "br" and havebrotli):
            try:
                returnval_content = brotli.decompress(returnval_content)
            except brotli.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "zstd" and havezstd):
            try:
                returnval_content = zstandard.decompress(returnval_content)
            except zstandard.error:
                pass
        elif((httpheaderout.get("Content-Encoding") == "lzma" or httpheaderout.get("Content-Encoding") == "xz") and havelzma):
            try:
                returnval_content = lzma.decompress(returnval_content)
            except zstandard.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "bzip2"):
            try:
                returnval_content = bz2.decompress(returnval_content)
            except zstandard.error:
                pass
    elif(httplibuse == "pycurl" or httplibuse == "pycurl2" or httplibuse == "pycurl3"):
        log.info("Downloading URL "+httpurl)
        downloadsize = httpheaderout.get('Content-Length')
        if(downloadsize is not None):
            downloadsize = int(downloadsize)
        if downloadsize is None:
            downloadsize = 0
        fulldatasize = 0
        prevdownsize = 0
        log.info("Downloading URL "+httpurl)
        with BytesIO() as strbuf:
            while True:
                databytes = retrieved_body.read(buffersize)
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Downloading "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Downloaded "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                strbuf.write(databytes)
            strbuf.seek(0)
            returnval_content = strbuf.read()
        geturls_text.close()
        if(httpheaderout.get("Content-Encoding") == "gzip"):
            try:
                returnval_content = zlib.decompress(
                    returnval_content, 16+zlib.MAX_WBITS)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "deflate"):
            try:
                returnval_content = zlib.decompress(returnval_content)
            except zlib.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "br" and havebrotli):
            try:
                returnval_content = brotli.decompress(returnval_content)
            except brotli.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "zstd" and havezstd):
            try:
                returnval_content = zstandard.decompress(returnval_content)
            except zstandard.error:
                pass
        elif((httpheaderout.get("Content-Encoding") == "lzma" or httpheaderout.get("Content-Encoding") == "xz") and havelzma):
            try:
                returnval_content = lzma.decompress(returnval_content)
            except zstandard.error:
                pass
        elif(httpheaderout.get("Content-Encoding") == "bzip2"):
            try:
                returnval_content = bz2.decompress(returnval_content)
            except zstandard.error:
                pass
    elif(httplibuse == "ftp" or httplibuse == "sftp" or httplibuse == "pysftp"):
        pass
    else:
        returnval = False
    returnval = {'Type': "Content", 'Content': returnval_content, 'Contentsize': fulldatasize, 'ContentsizeAlt': {'IEC': get_readable_size(fulldatasize, 2, "IEC"), 'SI': get_readable_size(
        fulldatasize, 2, "SI")}, 'Headers': httpheaderout, 'Version': httpversionout, 'Method': httpmethodout, 'HeadersSent': httpheadersentout, 'URL': httpurlout, 'Code': httpcodeout, 'Reason': httpcodereason, 'HTTPLib': httplibuse}
    return returnval


def download_from_url_from_list(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", buffersize=524288, sleep=-1, timeout=10):
    if(isinstance(httpurl, list)):
        pass
    elif(isinstance(httpurl, tuple)):
        pass
    elif(isinstance(httpurl, dict)):
        httpurl = httpurl.values()
    else:
        httpurl = [httpurl]
    listsize = len(httpurl)
    listcount = 0
    returnval = []
    while(listcount < listsize):
        ouputval = download_from_url(httpurl[listcount], httpheaders, httpuseragent, httpreferer,
                                     httpcookie, httpmethod, postdata, httplibuse, buffersize, sleep, timeout)
        returnval.append(ouputval)
        listcount += 1
    return returnval


def download_from_url_file(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    global geturls_download_sleep, havezstd, havebrotli, tmpfileprefix, tmpfilesuffix, haveaiohttp, haverequests, havemechanize, havehttplib2, haveurllib3, havehttpx, havehttpcore, haveparamiko, havepysftp
    exec_time_start = time.time()
    myhash = hashlib.new("sha1")
    if(sys.version[0] == "2"):
        myhash.update(httpurl)
        myhash.update(str(buffersize))
        myhash.update(str(exec_time_start))
    if(sys.version[0] >= "3"):
        myhash.update(httpurl.encode('utf-8'))
        myhash.update(str(buffersize).encode('utf-8'))
        myhash.update(str(exec_time_start).encode('utf-8'))
    newtmpfilesuffix = tmpfilesuffix + str(myhash.hexdigest())
    if(sleep < 0):
        sleep = geturls_download_sleep
    if(timeout <= 0):
        timeout = 10
    if(httplibuse == "urllib1" or httplibuse == "urllib2" or httplibuse == "request"):
        httplibuse = "urllib"
    if(httplibuse == "httplib1"):
        httplibuse = "httplib"
    if(not haverequests and httplibuse == "requests"):
        httplibuse = "urllib"
    if(not haveaiohttp and httplibuse == "aiohttp"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx2"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore2"):
        httplibuse = "urllib"
    if(not havemechanize and httplibuse == "mechanize"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl2"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl2" and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havepycurl and httplibuse == "pycurl3"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl2"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havehttplib2 and httplibuse == "httplib2"):
        httplibuse = "httplib"
    if(not haveparamiko and httplibuse == "sftp"):
        httplibuse = "ftp"
    if(not haveparamiko and httplibuse == "pysftp"):
        httplibuse = "ftp"
    pretmpfilename = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, httplibuse, buffersize, sleep, timeout)
    if(not pretmpfilename):
        return False
    with tempfile.NamedTemporaryFile('wb+', prefix=tmpfileprefix, suffix=newtmpfilesuffix, delete=False) as f:
        tmpfilename = f.name
        try:
            os.utime(tmpfilename, (time.mktime(email.utils.parsedate_to_datetime(pretmpfilename.get('Headers').get('Last-Modified')).timetuple()),
                     time.mktime(email.utils.parsedate_to_datetime(pretmpfilename.get('Headers').get('Last-Modified')).timetuple())))
        except AttributeError:
            try:
                os.utime(tmpfilename, (time.mktime(datetime.datetime.strptime(pretmpfilename.get('Headers').get('Last-Modified'), "%a, %d %b %Y %H:%M:%S %Z").timetuple()),
                         time.mktime(datetime.datetime.strptime(pretmpfilename.get('Headers').get('Last-Modified'), "%a, %d %b %Y %H:%M:%S %Z").timetuple())))
            except ValueError:
                pass
        except ValueError:
            pass
        returnval = {'Type': "File", 'Filename': tmpfilename, 'Filesize': pretmpfilename.get('Contentsize'), 'FilesizeAlt': {'IEC': get_readable_size(pretmpfilename.get('Contentsize'), 2, "IEC"), 'SI': get_readable_size(pretmpfilename.get('Contentsize'), 2, "SI")}, 'Headers': pretmpfilename.get(
            'Headers'), 'Version': pretmpfilename.get('Version'), 'Method': pretmpfilename.get('Method'), 'HeadersSent': pretmpfilename.get('HeadersSent'), 'URL': pretmpfilename.get('URL'), 'Code': pretmpfilename.get('Code'), 'Reason': pretmpfilename.get('Reason'), 'HTTPLib': pretmpfilename.get('HTTPLib')}
        f.write(pretmpfilename.get('Content'))
        f.close()
    exec_time_end = time.time()
    log.info("It took "+hms_string(exec_time_start -
             exec_time_end)+" to download file.")
    returnval.update({'Filesize': os.path.getsize(tmpfilename), 'FilesizeAlt': {'IEC': get_readable_size(os.path.getsize(tmpfilename), 2, "IEC"), 'SI': get_readable_size(
        os.path.getsize(tmpfilename), 2, "SI")}, 'DownloadTime': float(exec_time_start - exec_time_end), 'DownloadTimeReadable': hms_string(exec_time_start - exec_time_end)})
    return returnval


def download_from_url_file_with_list(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    if(isinstance(httpurl, list)):
        pass
    elif(isinstance(httpurl, tuple)):
        pass
    elif(isinstance(httpurl, dict)):
        httpurl = httpurl.values()
    else:
        httpurl = [httpurl]
    listsize = len(httpurl)
    listcount = 0
    returnval = []
    while(listcount < listsize):
        ouputval = download_from_url_file(httpurl[listcount], httpheaders, httpuseragent, httpreferer,
                                          httpcookie, httpmethod, postdata, httplibuse, ranges, buffersize, sleep, timeout)
        returnval.append(ouputval)
        listcount += 1
    return returnval


def download_from_url_to_file(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    global geturls_download_sleep, havezstd, havebrotli, haveaiohttp, haverequests, havemechanize, havepycurl, havehttplib2, haveurllib3, havehttpx, havehttpcore, haveparamiko, havepysftp
    if(sleep < 0):
        sleep = geturls_download_sleep
    if(timeout <= 0):
        timeout = 10
    if(httplibuse == "urllib1" or httplibuse == "urllib2" or httplibuse == "request"):
        httplibuse = "urllib"
    if(httplibuse == "httplib1"):
        httplibuse = "httplib"
    if(not haverequests and httplibuse == "requests"):
        httplibuse = "urllib"
    if(not haveaiohttp and httplibuse == "aiohttp"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx"):
        httplibuse = "urllib"
    if(not havehttpx and httplibuse == "httpx2"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore"):
        httplibuse = "urllib"
    if(not havehttpcore and httplibuse == "httpcore2"):
        httplibuse = "urllib"
    if(not havemechanize and httplibuse == "mechanize"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl"):
        httplibuse = "urllib"
    if(not havepycurl and httplibuse == "pycurl2"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl2" and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havepycurl and httplibuse == "pycurl3"):
        httplibuse = "urllib"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl2"
    if(havepycurl and httplibuse == "pycurl3" and not hasattr(pycurl, "CURL_HTTP_VERSION_3_0") and not hasattr(pycurl, "CURL_HTTP_VERSION_2_0")):
        httplibuse = "pycurl"
    if(not havehttplib2 and httplibuse == "httplib2"):
        httplibuse = "httplib"
    if(not haveparamiko and httplibuse == "sftp"):
        httplibuse = "ftp"
    if(not havepysftp and httplibuse == "pysftp"):
        httplibuse = "ftp"
    if(not outfile == "-"):
        outpath = outpath.rstrip(os.path.sep)
        filepath = os.path.realpath(outpath+os.path.sep+outfile)
        if(not os.path.exists(outpath)):
            os.makedirs(outpath)
        if(os.path.exists(outpath) and os.path.isfile(outpath)):
            return False
        if(os.path.exists(filepath) and os.path.isdir(filepath)):
            return False
        pretmpfilename = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                                httpcookie, httpmethod, postdata, httplibuse, ranges, buffersize[0], sleep, timeout)
        if(not pretmpfilename):
            return False
        tmpfilename = pretmpfilename.get('Filename')
        downloadsize = int(os.path.getsize(tmpfilename))
        fulldatasize = 0
        log.info("Moving file "+tmpfilename+" to "+filepath)
        exec_time_start = time.time()
        shutil.move(tmpfilename, filepath)
        try:
            os.utime(filepath, (time.mktime(email.utils.parsedate_to_datetime(pretmpfilename.get('Headers').get('Last-Modified')).timetuple()),
                     time.mktime(email.utils.parsedate_to_datetime(pretmpfilename.get('Headers').get('Last-Modified')).timetuple())))
        except AttributeError:
            try:
                os.utime(filepath, (time.mktime(datetime.datetime.strptime(pretmpfilename.get('Headers').get('Last-Modified'), "%a, %d %b %Y %H:%M:%S %Z").timetuple()),
                         time.mktime(datetime.datetime.strptime(pretmpfilename.get('Headers').get('Last-Modified'), "%a, %d %b %Y %H:%M:%S %Z").timetuple())))
            except ValueError:
                pass
        except ValueError:
            pass
        exec_time_end = time.time()
        log.info("It took "+hms_string(exec_time_start -
                 exec_time_end)+" to move file.")
        if(os.path.exists(tmpfilename)):
            os.remove(tmpfilename)
        returnval = {'Type': "File", 'Filename': filepath, 'Filesize': downloadsize, 'FilesizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename.get('DownloadTime'), 'DownloadTimeReadable': pretmpfilename.get('DownloadTimeReadable'), 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(
            exec_time_start - exec_time_end), 'Headers': pretmpfilename.get('Headers'), 'Version': pretmpfilename.get('Version'), 'Method': pretmpfilename.get('Method'), 'Method': httpmethod, 'HeadersSent': pretmpfilename.get('HeadersSent'), 'URL': pretmpfilename.get('URL'), 'Code': pretmpfilename.get('Code'), 'Reason': pretmpfilename.get('Reason'), 'HTTPLib': pretmpfilename.get('HTTPLib')}
    if(outfile == "-"):
        pretmpfilename = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                                httpcookie, httpmethod, postdata, httplibuse, ranges, buffersize[0], sleep, timeout)
        tmpfilename = pretmpfilename.get('Filename')
        downloadsize = int(os.path.getsize(tmpfilename))
        fulldatasize = 0
        prevdownsize = 0
        exec_time_start = time.time()
        with open(tmpfilename, 'rb') as ft:
            f = BytesIO()
            while True:
                databytes = ft.read(buffersize[1])
                if not databytes:
                    break
                datasize = len(databytes)
                fulldatasize = datasize + fulldatasize
                percentage = ""
                if(downloadsize > 0):
                    percentage = str("{0:.2f}".format(
                        float(float(fulldatasize / downloadsize) * 100))).rstrip('0').rstrip('.')+"%"
                downloaddiff = fulldatasize - prevdownsize
                log.info("Copying "+get_readable_size(fulldatasize, 2, "SI")['ReadableWithSuffix']+" / "+get_readable_size(downloadsize, 2, "SI")[
                         'ReadableWithSuffix']+" "+str(percentage)+" / Copied "+get_readable_size(downloaddiff, 2, "IEC")['ReadableWithSuffix'])
                prevdownsize = fulldatasize
                f.write(databytes)
            f.seek(0)
            fdata = f.getvalue()
            f.close()
            ft.close()
            os.remove(tmpfilename)
            exec_time_end = time.time()
            log.info("It took "+hms_string(exec_time_start -
                     exec_time_end)+" to copy file.")
        returnval = {'Type': "Content", 'Content': fdata, 'Contentsize': downloadsize, 'ContentsizeAlt': {'IEC': get_readable_size(downloadsize, 2, "IEC"), 'SI': get_readable_size(downloadsize, 2, "SI")}, 'DownloadTime': pretmpfilename.get('DownloadTime'), 'DownloadTimeReadable': pretmpfilename.get('DownloadTimeReadable'), 'MoveFileTime': float(exec_time_start - exec_time_end), 'MoveFileTimeReadable': hms_string(
            exec_time_start - exec_time_end), 'Headers': pretmpfilename.get('Headers'), 'Version': pretmpfilename.get('Version'), 'Method': pretmpfilename.get('Method'), 'Method': httpmethod, 'HeadersSent': pretmpfilename.get('HeadersSent'), 'URL': pretmpfilename.get('URL'), 'Code': pretmpfilename.get('Code'), 'Reason': pretmpfilename.get('Reason'), 'HTTPLib': httplibuse}
    return returnval


def download_from_url_to_file_with_list(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, httplibuse="urllib", outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    if(isinstance(httpurl, list)):
        pass
    elif(isinstance(httpurl, tuple)):
        pass
    elif(isinstance(httpurl, dict)):
        httpurl = httpurl.values()
    else:
        httpurl = [httpurl]
    listsize = len(httpurl)
    listcount = 0
    returnval = []
    while(listcount < listsize):
        ouputval = download_from_url_to_file(httpurl[listcount], httpheaders, httpuseragent, httpreferer,
                                             httpcookie, httpmethod, postdata, httplibuse, outfile, outpath, ranges, buffersize, sleep, timeout)
        returnval.append(ouputval)
        listcount += 1
    return returnval


def download_from_url_with_urllib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "urllib", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_request(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "urllib", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_request3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "request3", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httplib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httplib", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httplib2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httplib2", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_urllib3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "urllib3", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_requests(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "requests", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_aiohttp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "aiohttp", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httpx(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httpx", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httpx2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httpx2", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httpcore(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httpcore", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_httpcore2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "httpcore2", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_mechanize(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "mechanize", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_pycurl(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "pycurl", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_pycurl2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "pycurl2", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_pycurl3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "pycurl3", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_ftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "ftp", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_sftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "sftp", buffersize, sleep, timeout)
    return returnval


def download_from_url_with_pysftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url(httpurl, httpheaders, httpuseragent, httpreferer,
                                  httpcookie, httpmethod, postdata, "pysftp", buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_urllib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "urllib", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_request(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "urllib", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_request3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "request3", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httplib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httplib", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httplib2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httplib2", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_urllib3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "urllib3", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_requests(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "requests", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_aiohttp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "aiohttp", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httpx(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httpx", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httpx2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httpx2", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httpcore(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httpcore", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_httpcore2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "httpcore2", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_mechanize(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "mechanize", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_pycurl(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "pycurl", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_pycurl2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "pycurl2", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_pycurl3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "pycurl3", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_ftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "ftp", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_sftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "sftp", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_file_with_pysftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, ranges=[None, None], buffersize=524288, sleep=-1, timeout=10):
    returnval = download_from_url_file(httpurl, httpheaders, httpuseragent, httpreferer,
                                       httpcookie, httpmethod, postdata, "pysftp", ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_urllib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "urllib", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_request(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "request", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_request3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "urllib", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httplib(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httplib", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httplib2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httplib2", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_urllib3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "urllib3", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_requests(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "requests", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_aiohttp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "aiohttp", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httpx(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httpx", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httpx2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httpx2", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httpcore(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httpcore", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_httpcore2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "httpcore2", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_mechanize(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "mechanize", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_pycurl(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "pycurl", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_pycurl2(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "pycurl2", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_pycurl3(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "pycurl3", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_ftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "ftp", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_sftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "sftp", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_from_url_to_file_with_pysftp(httpurl, httpheaders=geturls_headers, httpuseragent=None, httpreferer=None, httpcookie=geturls_cj, httpmethod="GET", postdata=None, outfile="-", outpath=os.getcwd(), ranges=[None, None], buffersize=[524288, 524288], sleep=-1, timeout=10):
    returnval = download_from_url_to_file(httpurl, httpheaders, httpuseragent, httpreferer, httpcookie,
                                          httpmethod, postdata, "pysftp", outfile, outpath, ranges, buffersize, sleep, timeout)
    return returnval


def download_file_from_ftp_file(url):
    urlparts = urlparse.urlparse(url)
    file_name = os.path.basename(urlparts.path)
    file_dir = os.path.dirname(urlparts.path)
    if(urlparts.username is not None):
        ftp_username = urlparts.username
    else:
        ftp_username = "anonymous"
    if(urlparts.password is not None):
        ftp_password = urlparts.password
    elif(urlparts.password is None and urlparts.username == "anonymous"):
        ftp_password = "anonymous"
    else:
        ftp_password = ""
    if(urlparts.scheme == "ftp"):
        ftp = FTP()
    elif(urlparts.scheme == "ftps"):
        ftp = FTP_TLS()
    else:
        return False
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    ftp_port = urlparts.port
    if(urlparts.port is None):
        ftp_port = 21
    try:
        ftp.connect(urlparts.hostname, ftp_port)
    except socket.gaierror:
        log.info("Error With URL "+httpurl)
        return False
    except socket.timeout:
        log.info("Error With URL "+httpurl)
        return False
    ftp.login(urlparts.username, urlparts.password)
    if(urlparts.scheme == "ftps"):
        ftp.prot_p()
    ftpfile = BytesIO()
    ftp.retrbinary("RETR "+urlparts.path, ftpfile.write)
    #ftp.storbinary("STOR "+urlparts.path, ftpfile.write);
    ftp.close()
    ftpfile.seek(0, 0)
    return ftpfile


def download_file_from_ftp_string(url):
    ftpfile = download_file_from_ftp_file(url)
    return ftpfile.read()


def upload_file_to_ftp_file(ftpfile, url):
    urlparts = urlparse.urlparse(url)
    file_name = os.path.basename(urlparts.path)
    file_dir = os.path.dirname(urlparts.path)
    if(urlparts.username is not None):
        ftp_username = urlparts.username
    else:
        ftp_username = "anonymous"
    if(urlparts.password is not None):
        ftp_password = urlparts.password
    elif(urlparts.password is None and urlparts.username == "anonymous"):
        ftp_password = "anonymous"
    else:
        ftp_password = ""
    if(urlparts.scheme == "ftp"):
        ftp = FTP()
    elif(urlparts.scheme == "ftps"):
        ftp = FTP_TLS()
    else:
        return False
    if(urlparts.scheme == "http" or urlparts.scheme == "https"):
        return False
    ftp_port = urlparts.port
    if(urlparts.port is None):
        ftp_port = 21
    try:
        ftp.connect(urlparts.hostname, ftp_port)
    except socket.gaierror:
        log.info("Error With URL "+httpurl)
        return False
    except socket.timeout:
        log.info("Error With URL "+httpurl)
        return False
    ftp.login(urlparts.username, urlparts.password)
    if(urlparts.scheme == "ftps"):
        ftp.prot_p()
    ftp.storbinary("STOR "+urlparts.path, ftpfile)
    ftp.close()
    ftpfile.seek(0, 0)
    return ftpfile


def upload_file_to_ftp_string(ftpstring, url):
    ftpfileo = BytesIO(ftpstring)
    ftpfile = upload_file_to_ftp_file(ftpfileo, url)
    ftpfileo.close()
    return ftpfile


if(haveparamiko):
    def download_file_from_sftp_file(url):
        urlparts = urlparse.urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        if(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme != "sftp"):
            return False
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(urlparts.hostname, port=sftp_port,
                        username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        sftp = ssh.open_sftp()
        sftpfile = BytesIO()
        sftp.getfo(urlparts.path, sftpfile)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def download_file_from_sftp_file(url):
        return False

if(haveparamiko):
    def download_file_from_sftp_string(url):
        sftpfile = download_file_from_sftp_file(url)
        return sftpfile.read()
else:
    def download_file_from_ftp_string(url):
        return False

if(haveparamiko):
    def upload_file_to_sftp_file(sftpfile, url):
        urlparts = urlparse.urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme != "sftp"):
            return False
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(urlparts.hostname, port=sftp_port,
                        username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        sftp = ssh.open_sftp()
        sftp.putfo(sftpfile, urlparts.path)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def upload_file_to_sftp_file(sftpfile, url):
        return False

if(haveparamiko):
    def upload_file_to_sftp_string(sftpstring, url):
        sftpfileo = BytesIO(sftpstring)
        sftpfile = upload_file_to_sftp_files(ftpfileo, url)
        sftpfileo.close()
        return sftpfile
else:
    def upload_file_to_sftp_string(url):
        return False


if(havepysftp):
    def download_file_from_pysftp_file(url):
        urlparts = urlparse.urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        if(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        sftp_port = urlparts.port
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme != "sftp"):
            return False
        try:
            pysftp.Connection(urlparts.hostname, port=sftp_port,
                              username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        sftp = ssh.open_sftp()
        sftpfile = BytesIO()
        sftp.getfo(urlparts.path, sftpfile)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def download_file_from_pysftp_file(url):
        return False

if(havepysftp):
    def download_file_from_pysftp_string(url):
        sftpfile = download_file_from_pysftp_file(url)
        return sftpfile.read()
else:
    def download_file_from_ftp_string(url):
        return False

if(havepysftp):
    def upload_file_to_pysftp_file(sftpfile, url):
        urlparts = urlparse.urlparse(url)
        file_name = os.path.basename(urlparts.path)
        file_dir = os.path.dirname(urlparts.path)
        sftp_port = urlparts.port
        if(urlparts.scheme == "http" or urlparts.scheme == "https"):
            return False
        if(urlparts.port is None):
            sftp_port = 22
        else:
            sftp_port = urlparts.port
        if(urlparts.username is not None):
            sftp_username = urlparts.username
        else:
            sftp_username = "anonymous"
        if(urlparts.password is not None):
            sftp_password = urlparts.password
        elif(urlparts.password is None and urlparts.username == "anonymous"):
            sftp_password = "anonymous"
        else:
            sftp_password = ""
        if(urlparts.scheme != "sftp"):
            return False
        try:
            pysftp.Connection(urlparts.hostname, port=sftp_port,
                              username=urlparts.username, password=urlparts.password)
        except paramiko.ssh_exception.SSHException:
            return False
        except socket.gaierror:
            log.info("Error With URL "+httpurl)
            return False
        except socket.timeout:
            log.info("Error With URL "+httpurl)
            return False
        sftp = ssh.open_sftp()
        sftp.putfo(sftpfile, urlparts.path)
        sftp.close()
        ssh.close()
        sftpfile.seek(0, 0)
        return sftpfile
else:
    def upload_file_to_pysftp_file(sftpfile, url):
        return False

if(havepysftp):
    def upload_file_to_pysftp_string(sftpstring, url):
        sftpfileo = BytesIO(sftpstring)
        sftpfile = upload_file_to_pysftp_files(ftpfileo, url)
        sftpfileo.close()
        return sftpfile
else:
    def upload_file_to_pysftp_string(url):
        return False
