'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: versioninfo.py - Last Update: 12/25/2014 Ver. 2.7.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;

__author__ = "Kazuki Przyborowski";
__copyright__ = "Copyright 2011-2014, Game Maker 2k";
__credits__ = ["Kazuki Przyborowski", "Game Maker 2k"];
__license__ = "Revised BSD License";
__maintainer__ = "Kazuki Przyborowski";
__email__ = "kazuki.przyborowski@gmail.com";
__status__ = "Production";
__project__ = "PyUPC-EAN";
__project_url__ = "https://pypi.python.org/pypi/PyUPC-EAN";
__version_info__ = (2, 7, 8, "RC 1");
__revision__ = __version_info__[3];
if(__version_info__[3] is not None):
 __version__ = "{major}.{minor}.{build} {release}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2], release=__version_info__[3]);
if(__version_info__[3] is None):
 __version__ = "{major}.{minor}.{build}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2]);
__version_alt__ = "{major}.{minor}.{build}".format(major=__version_info__[0], minor=__version_info__[1], build=__version_info__[2]);
def version_info():
 global __version_info__;
 if(__version_info__[3] is not None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": __version_info__[3]};
 if(__version_info__[3] is None):
  return {"major": __version_info__[0], "minor": __version_info__[1], "build": __version_info__[2], "release": None};
__version_date_info__ = (2014, 12, 25, "RC 1");
def version_date():
 global __version_info__;
 if(__version_date_info__[3] is not None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": __version_date_info__[3]};
 if(__version_date_info__[3] is None):
  return {"year":__version_date_info__[0], "month": __version_date_info__[1], "day": __version_date_info__[2], "release": None};
__version_date__ = "{year}.{month}.{day}".format(year=__version_date_info__[0], month=__version_date_info__[1], day=__version_date_info__[2]);
__version_date_alt__ = "{year}.{month}.{day} {release}".format(year=__version_date_info__[0], month=__version_date_info__[1], day=__version_date_info__[2], release=__version_date_info__[2]);
