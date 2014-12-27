'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __main__.py - Last Update: 12/27/2014 Ver. 2.7.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
from upcean.versioninfo import __author__, __copyright__, __credits__, __email__, __license__, __license_string__, __maintainer__, __project__, __project_url__, __revision__, __status__, __version__, __version_alt__, __version_date__, __version_date_alt__, __version_date_info__, __version_info__, version_date, version_info;
import argparse;

parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = "{projectname} {copyrightstr}; #Release {projectver} {projectdate}".format(projectname=__project__, copyrightstr=__copyright__, projectver=__version__, projectdate=__version_date__));
parser.add_argument("-l", "--license", action = "store_true", help = "print license file");
getargs = parser.parse_args();

print("{licensestr}".format(licensestr=__license_string__));
