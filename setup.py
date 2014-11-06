#!/usr/bin/env python

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

    $FileInfo: setup.py - Last Update: 11/05/2014 Ver. 2.7.5 RC 1  - Author: cooldude2k $
'''

import os;
from setuptools import setup;
import pkg_resources;

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

setup(
 name = 'PyUPC-EAN',
 version = '2.7.5',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 maintainer = 'Kazuki Przyborowski',
 maintainer_email = 'kazuki.przyborowski@gmail.com',
 description = 'A barcode library/module for python.',
 license = 'Revised BSD License',
 keywords = 'barcode barcodegenerator barcodes codabar msi code11 code-11 code39 code-39 code93 code-93 ean ean13 ean-13 ean2 ean-2 ean5 ean-5 ean8 ean-8 itf itf14 itf-14 stf upc upca upc-a upce upc-e',
 url = 'https://github.com/GameMaker2k/PyUPC-EAN',
 download_url = 'https://github.com/GameMaker2k/PyUPC-EAN/archive/master.tar.gz',
 packages = ['upcean', 'upcean/validate', 'upcean/convert', 'upcean/barcodes', 'upcean/fonts', 'upcean/xml'],
 package_data = {'upcean/fonts': ['*.otf', '*.ttf'], 'upcean/xml': ['*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc']},
 include_package_data = True,
 install_requires = [install_requires],
 long_description = 'PyUPC-EAN is a barcode library/module for Python. It supports the barcode formats upc-e, upc-a, ean-13, ean-8, ean-2, ean-5, itf14, codabar, code11, code39, code93, and msi.',
 platforms = 'OS Independent',
 zip_safe = True,
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
