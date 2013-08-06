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

setup(
 name = 'PyUPC-EAN',
 version = '2.4.2.3',
 author = 'Kazuki Przyborowski',
 author_email = 'kazuki.przyborowski@gmail.com',
 description = 'A barcode library/module for python.',
 license = 'BSD',
 keywords = 'barcode barcodegenerator barcodes codabar code11 code11 code39 code93 code93 ean ean13 ean2 ean5 ean8 itf itf14 stf upc upca upce',
 url = 'https://github.com/GameMaker2k/PyUPC-EAN',
 packages=['upcean'],
 package_data={'upcean': ['*.otf']},
 include_package_data=True,
 install_requires=['cairo'],
 long_description='A barcode library/module for python.',
 classifiers=[
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Environment :: Console',
  'Natural Language :: English',
  'Operating System :: OS Independent',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: POSIX',
  'Operating System :: Unix ',
  'Programming Language :: Python',
  'Topic :: Multimedia :: Graphics',
  'Topic :: Software Development :: Libraries :: Python Modules',
  'Topic :: Office/Business',
  'Topic :: Utilities',
  'License :: OSI Approved :: BSD License',
 ],
)
