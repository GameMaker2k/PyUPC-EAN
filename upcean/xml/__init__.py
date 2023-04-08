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

    $FileInfo: __init__.py - Last Update: 4/7/2023 Ver. 2.9.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres):
 barcodedtd = pkg_resources.resource_filename(__name__, "barcodes.dtd");
 barcodexsl = pkg_resources.resource_filename(__name__, "barcodes.xsl");
 barcodexsd = pkg_resources.resource_filename(__name__, "barcodes.xsd");
 barcoderng = pkg_resources.resource_filename(__name__, "barcodes.rng");
 barcodernc = pkg_resources.resource_filename(__name__, "barcodes.rnc");
 bcxmlpath = os.path.dirname(barcodedtd);

if(not pkgres):
 barcodedtd = os.path.dirname(__file__)+os.sep+"barcodes.dtd";
 barcodexsl = os.path.dirname(__file__)+os.sep+"barcodes.xsl";
 barcodexsd = os.path.dirname(__file__)+os.sep+"barcodes.xsd";
 barcoderng = os.path.dirname(__file__)+os.sep+"barcodes.rng";
 barcodernc = os.path.dirname(__file__)+os.sep+"barcodes.rnc";
 bcxmlpath = os.path.dirname(barcodedtd);
