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

    $FileInfo: __init__.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres):
 fontpathocra = pkg_resources.resource_filename(__name__, "OCRA.otf");
 fontpathocraalt = pkg_resources.resource_filename(__name__, "OCRA.ttf");
 fontpathocrb = pkg_resources.resource_filename(__name__, "OCRB.otf");
 fontpathocrbalt = pkg_resources.resource_filename(__name__, "OCRB.ttf");
 fontpath = os.path.dirname(fontpathocrb);
if(not pkgres):
 fontpathocra = os.path.dirname(__file__)+os.sep+"OCRA.otf";
 fontpathocraalt = os.path.dirname(__file__)+os.sep+"OCRA.ttf";
 fontpathocrb = os.path.dirname(__file__)+os.sep+"OCRB.otf";
 fontpathocrbalt = os.path.dirname(__file__)+os.sep+"OCRB.ttf";
 fontpath = os.path.dirname(fontpathocrb);
