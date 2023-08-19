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

    $FileInfo: getsfname.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean.support;
pilsupport = upcean.support.check_for_pil();
pillowsupport = upcean.support.check_for_pillow();
cairosupport = upcean.support.check_for_cairo();
if(pilsupport or cairosupport):
 from upcean.encode.predraw import get_save_filename;
