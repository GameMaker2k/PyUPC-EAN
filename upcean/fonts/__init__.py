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

    $FileInfo: __init__.py - Last Update: 10/31/2014 Ver. 2.7.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import sys, re, os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres==True):
 fontpathocra = pkg_resources.resource_filename(__name__, "OCRA.otf");
 fontpathocraalt = pkg_resources.resource_filename(__name__, "OCRA.ttf");
 fontpathocrb = pkg_resources.resource_filename(__name__, "OCRB.otf");
 fontpathocrbalt = pkg_resources.resource_filename(__name__, "OCRB.ttf");
 fontpath = os.path.dirname(fontpathocrb);
if(pkgres==False):
 fontpathocra = os.path.dirname(__file__)+os.sep+"OCRA.otf";
 fontpathocraalt = os.path.dirname(__file__)+os.sep+"OCRA.ttf";
 fontpathocrb = os.path.dirname(__file__)+os.sep+"OCRB.otf";
 fontpathocrbalt = os.path.dirname(__file__)+os.sep+"OCRB.ttf";
 fontpath = os.path.dirname(fontpathocrb);
