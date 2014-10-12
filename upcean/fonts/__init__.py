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

    $FileInfo: __init__.py - Last Update: 10/12/2014 Ver. 2.6.5 RC 1 - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, re, os;

try:
 import pkg_resources;
 pkgres = True;
except ImportError:
 pkgres = False;

if(pkgres==True):
 fontpathocra = pkg_resources.resource_filename(__name__, "OCRA.otf");
 fontpathocrb = pkg_resources.resource_filename(__name__, "OCRB.otf");
 fontpatha = os.path.dirname(fontpathocra);
 fontpathb = os.path.dirname(fontpathocrb);
 fontpath = fontpathb;
if(pkgres==False):
 fontpathocra = os.path.dirname(__file__)+os.sep+"OCRA.otf";
 fontpathocrb = os.path.dirname(__file__)+os.sep+"OCRB.otf";
 fontpatha = os.path.dirname(fontpathocra);
 fontpathb = os.path.dirname(fontpathocrb);
 fontpath = fontpathb;
