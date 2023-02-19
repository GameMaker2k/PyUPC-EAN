# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 2/19/2023 Ver. 2.7.22 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres):
 barcodejson = pkg_resources.resource_filename(__name__, "barcodes.json");
 barcodexsl = pkg_resources.resource_filename(__name__, "barcodes.xsl");
 barcodexml = pkg_resources.resource_filename(__name__, "barcodes.xml");
 bcxmlpath = os.path.dirname(barcodejson);

if(not pkgres):
 barcodejson = os.path.dirname(__file__)+os.sep+"barcodes.json";
 barcodexsl = os.path.dirname(__file__)+os.sep+"barcodes.xsl";
 barcodexml = os.path.dirname(__file__)+os.sep+"barcodes.xml";
 bcxmlpath = os.path.dirname(barcodejson);
