#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pyverinfo.py - Last Update: 6/27/2025 Ver. 2.20.0 RC 1 - Author: cooldude2k $
'''

import re
import os
import sys
import json
import subprocess

pyexecpath = os.path.realpath(sys.executable)
pkgsetuppy = os.path.realpath("."+os.path.sep+"setup.py")
pypkgenlistp = subprocess.Popen(
    [pyexecpath, pkgsetuppy, "getversioninfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pypkgenout, pypkgenerr = pypkgenlistp.communicate()
if(sys.version[0] == "3"):
    pypkgenout = pypkgenout.decode('utf-8')
pyconfiginfo = json.loads(pypkgenout)
print(pypkgenout)
