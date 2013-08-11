# -*- coding: utf-8 -*- 

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: getsfname.py - Last Update: 08/10/2013 Ver. 2.4.4 RC 1  - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import sys, os, re;

def get_save_filename(outfile):
 if(outfile is None or isinstance(outfile, bool) or isinstance(outfile, file)):
  return outfile;
 return (outfile, "PNG");
