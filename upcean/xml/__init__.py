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

    $FileInfo: __init__.py - Last Update: 10/21/2014 Ver. 2.6.9 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import sys, re, os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres==True):
 barcodedtd = pkg_resources.resource_filename(__name__, "barcodes.dtd");
 barcodexsl = pkg_resources.resource_filename(__name__, "barcodes.xsl");
 barcodexsd = pkg_resources.resource_filename(__name__, "barcodes.xsd");
 barcoderng = pkg_resources.resource_filename(__name__, "barcodes.rng");
 barcodernc = pkg_resources.resource_filename(__name__, "barcodes.rnc");
 bcxmlpath = os.path.dirname(barcodedtd);

if(pkgres==False):
 barcodedtd = os.path.dirname(__file__)+os.sep+"barcodes.dtd";
 barcodexsl = os.path.dirname(__file__)+os.sep+"barcodes.xsl";
 barcodexsd = os.path.dirname(__file__)+os.sep+"barcodes.xsd";
 barcoderng = os.path.dirname(__file__)+os.sep+"barcodes.rng";
 barcodernc = os.path.dirname(__file__)+os.sep+"barcodes.rnc";
 bcxmlpath = os.path.dirname(barcodedtd);
