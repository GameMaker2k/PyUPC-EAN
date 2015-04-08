#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: setup.py - Last Update: 1/15/2015 Ver. 2.7.10 RC 1  - Author: cooldude2k $
'''

import os;
from setuptools import setup, find_packages;
import pkg_resources, time, datetime, platform;

install_requires = [];
# https://github.com/mapproxy/mapproxy/blob/master/setup.py
def pillow_installed():
 """Check if Pillow is installed"""
 pillow_req = pkg_resources.Requirement.parse('Pillow');
 try:
  pkg_resources.get_provider(pillow_req);
 except pkg_resources.DistributionNotFound:
  return False;
 else:
  return True;
# depend in Pillow if it is installed, otherwise depend on PIL
if pillow_installed():
 install_requires.append('Pillow');
else:
 install_requires.append('PIL');

verinfofile = open("."+os.path.sep+"upcean"+os.path.sep+"versioninfo.py", "r");
verinfodata = verinfofile.read();
verinfofile.close();
mycurtime = datetime.datetime.now();
mycurtimetuple = mycurtime.timetuple();
mycurtimestamp = int(time.mktime(mycurtimetuple));
verinfodata = verinfodata.replace('__build_time__ = {"timestamp": None, "year": None, "month": None, "day": None, "hour": None, "minute": None, "second": None};', '__build_time__ = {"timestamp": '+str(mycurtimestamp)+', "year": '+str(mycurtimetuple[0])+', "month": '+str(mycurtimetuple[1])+', "day": '+str(mycurtimetuple[2])+', "hour": '+str(mycurtimetuple[3])+', "minute": '+str(mycurtimetuple[4])+', "second": '+str(mycurtimetuple[5])+'};');
utccurtime = datetime.datetime.utcnow();
utccurtimetuple = utccurtime.timetuple();
utccurtimestamp = int(time.mktime(utccurtimetuple));
verinfodata = verinfodata.replace('__build_time_utc__ = {"timestamp": None, "year": None, "month": None, "day": None, "hour": None, "minute": None, "second": None};', '__build_time_utc__ = {"timestamp": '+str(utccurtimestamp)+', "year": '+str(utccurtimetuple[0])+', "month": '+str(utccurtimetuple[1])+', "day": '+str(utccurtimetuple[2])+', "hour": '+str(utccurtimetuple[3])+', "minute": '+str(utccurtimetuple[4])+', "second": '+str(utccurtimetuple[5])+'};');
verinfodata = verinfodata.replace('__build_python_info__ = {"python_branch": None, "python_build": None, "python_compiler": None, "python_implementation": None, "python_revision": None, "python_version": None, "python_version_tuple": None, "release": None, "system": None, "uname": None, "version": None, "win32_ver": None};', '__build_python_info__ = {"python_branch": "'+str(platform.python_branch())+'", "python_build": '+str(platform.python_build())+', "python_compiler": "'+str(platform.python_compiler())+'", "python_implementation": "'+str(platform.python_implementation())+'", "python_revision": "'+str(platform.python_revision())+'", "python_version": "'+str(platform.python_version())+'", "python_version_tuple": '+str(platform.python_version_tuple())+', "release": "'+str(platform.release())+'", "system": "'+str(platform.system())+'", "uname": '+str(platform.uname())+', "version": "'+str(platform.version())+'", "win32_ver": '+str(platform.win32_ver())+'};');
verinfofile = open("."+os.path.sep+"upcean"+os.path.sep+"versioninfo.py", "w");
verinfofile.write(verinfodata);
verinfofile.close();
setup(
 name = 'PyUPC-EAN',
 version = '2.7.10',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 maintainer = 'Kazuki Przyborowski',
 maintainer_email = 'kazuki.przyborowski@gmail.com',
 description = 'A barcode library/module for python.',
 license = 'Revised BSD License',
 keywords = 'barcode barcodegenerator barcodes codabar msi code11 code-11 code39 code-39 code93 code-93 ean ean13 ean-13 ean2 ean-2 ean5 ean-5 ean8 ean-8 itf itf14 itf-14 stf upc upca upc-a upce upc-e',
 url = 'https://github.com/GameMaker2k/PyUPC-EAN',
 download_url = 'https://github.com/GameMaker2k/PyUPC-EAN/archive/master.tar.gz',
 packages = find_packages(),
 package_data = {'upcean': ['*.otf', '*.ttf', '*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc'], 'upcean/fonts': ['*.otf', '*.ttf'], 'upcean/xml': ['*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc']},
 include_package_data = True,
 install_requires = [install_requires],
 long_description = 'PyUPC-EAN is a barcode library/module for Python. It supports the barcode formats upc-e, upc-a, ean-13, ean-8, ean-2, ean-5, itf14, codabar, code11, code39, code93, and msi.',
 platforms = 'OS Independent',
 zip_safe = False,
 classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Customer Service',
  'Intended Audience :: Developers',
  'Intended Audience :: Other Audience',
  'License :: OSI Approved',
  'License :: OSI Approved :: BSD License',
  'Natural Language :: English',
  'Operating System :: MacOS',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: OS/2',
  'Operating System :: OS Independent',
  'Operating System :: POSIX',
  'Operating System :: Unix',
  'Programming Language :: Python',
  'Topic :: Multimedia :: Graphics',
  'Topic :: Office/Business',
  'Topic :: Office/Business :: Financial',
  'Topic :: Office/Business :: Financial :: Point-Of-Sale',
  'Topic :: Utilities',
  'Topic :: Software Development',
  'Topic :: Software Development :: Libraries',
  'Topic :: Software Development :: Libraries :: Python Modules',
 ],
)
