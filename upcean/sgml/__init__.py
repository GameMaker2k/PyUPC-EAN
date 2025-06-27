# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 6/27/2025 Ver. 2.20.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os

implib = False
pkgres = False
try:
    import importlib.resources
    implib = True
except ImportError:
    implib = False
    try:
        import pkg_resources
        pkgres = True
    except ImportError:
        pkgres = False

if(implib):
    barcodedtd = os.path.join(
        importlib.resources.files(__name__), "barcodes.dtd")
    bcxmlpath = os.path.dirname(barcodedtd)
elif(pkgres):
    barcodedtd = pkg_resources.resource_filename(__name__, "barcodes.dtd")
    bcxmlpath = os.path.dirname(barcodedtd)
elif(not pkgres):
    barcodedtd = os.path.dirname(__file__)+os.sep+"barcodes.dtd"
    bcxmlpath = os.path.dirname(barcodedtd)
else:
    barcodedtd = os.path.dirname(__file__)+os.sep+"barcodes.dtd"
    bcxmlpath = os.path.dirname(barcodedtd)
