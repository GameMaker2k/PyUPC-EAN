#!/usr/bin/env python2

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2016 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: which.py - Last Update: 2/15/2016 Ver. 0.0.5 RC 3 - Author: cooldude2k $
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import os
import sys

__version_info__ = (0, 0, 5, "rc3")
if (__version_info__[3] is not None):
    __version__ = str(__version_info__[0]) + "." + str(__version_info__[1]) + "." + str(
        __version_info__[2]) + "+" + str(__version_info__[3])
if (__version_info__[3] is None):
    __version__ = str(__version_info__[
        0]) + "." + str(__version_info__[1]) + "." + str(__version_info__[2])

proname = "which"
prover = __version__
profullname = proname + " " + prover


def which_exec(execfile):
    for path in os.environ["PATH"].split(":"):
        if os.path.exists(path + "/" + execfile):
            return path + "/" + execfile


parser = argparse.ArgumentParser(conflict_handler="resolve", add_help=True)
parser.add_argument("-v", "--version", action="version", version=profullname)
parser.add_argument("filename", help="enter a file name/path")
getargs = parser.parse_args()
print(which_exec(getargs.filename))
