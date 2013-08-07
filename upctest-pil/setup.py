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

    $FileInfo: setup.py - Last Update: 08/06/2013 Ver. 2.4.3 RC 3  - Author: cooldude2k $
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
 version = '2.4.3.3',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 description = 'A barcode library/module for python.',
 license = 'BSD',
 keywords = 'barcode barcodegenerator barcodes codabar code11 code11 code39 code93 code93 ean ean13 ean2 ean5 ean8 itf itf14 stf upc upca upce',
 url = 'https://github.com/GameMaker2k/PyUPC-EAN',
 packages=['upcean'],
 package_data={'upcean': ['*.otf']},
 include_package_data=True,
 install_requires=[install_requires],
 long_description='A barcode library/module for python.',
 classifiers=[
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
