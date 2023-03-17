# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2020 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2020 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: barcode.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.support, upcean.getprefix.getprefix;

''' // Code for decoding UPC-A by Kazuki Przyborowski '''
from upcean.decode.upca import *;
''' // Code for decoding UPC-E by Kazuki Przyborowski '''
from upcean.decode.upce import *;
''' // Code for decoding EAN-13 by Kazuki Przyborowski '''
from upcean.decode.ean13 import *;
''' // Code for decoding EAN-8 by Kazuki Przyborowski '''
from upcean.decode.ean8 import *;