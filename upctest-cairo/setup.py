#!/usr/bin/env python

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
