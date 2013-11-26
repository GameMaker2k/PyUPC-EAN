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

    $FileInfo: setup.py - Last Update: 11/25/2013 Ver. 2.5.0 RC 3  - Author: cooldude2k $
'''

import os;
from setuptools import setup;

setup(
 name = 'PyUPC-EAN',
 version = '2.5.0.3',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 maintainer = 'Kazuki Przyborowski',
 maintainer_email = 'kazuki.przyborowski@gmail.com',
 description = 'A barcode library/module for python.',
 license = 'Revised BSD License',
 keywords = 'barcode barcodegenerator barcodes codabar msi code11 code-11 code39 code-39 code93 code-93 ean ean13 ean-13 ean2 ean-2 ean5 ean-5 ean8 ean-8 itf itf14 itf-14 stf upc upca upc-a upce upc-e',
 url = 'https://github.com/GameMaker2k/PyUPC-EAN',
 download_url = 'https://github.com/GameMaker2k/PyUPC-EAN/archive/master.tar.gz',
 packages= ['upcean'],
 package_data = {'upcean': ['*.otf']},
 include_package_data = True,
 install_requires = ['cairo'],
 long_description = 'A barcode library/module for python.',
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
