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

    $FileInfo: pypac-gen.py - Last Update: 6/1/2016 Ver. 0.2.0 RC 1 - Author: cooldude2k $
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

__version_info__ = (0, 2, 0, "rc1")
if (__version_info__[3] is not None):
    __version__ = str(__version_info__[0]) + "." + str(__version_info__[1]) + "." + str(
        __version_info__[2]) + "+" + str(__version_info__[3])
if (__version_info__[3] is None):
    __version__ = str(__version_info__[
        0]) + "." + str(__version_info__[1]) + "." + str(__version_info__[2])

proname = "pypac-gen"
prover = __version__
profullname = proname + " " + prover


def which_exec(execfile):
    for path in os.environ["PATH"].split(":"):
        if os.path.exists(path + "/" + execfile):
            return path + "/" + execfile


parser = argparse.ArgumentParser(conflict_handler="resolve", add_help=True)
parser.add_argument("-v", "--version", action="version", version=profullname)
parser.add_argument(
    "-s", "--source", default=os.path.realpath(os.getcwd()), help="source dir")
parser.add_argument("-g", "--getsource",
                    action="store_true", help="get source dir")
parser.add_argument("-p", "--getparent",
                    action="store_true", help="get parent dir")
parser.add_argument("-t", "--gettarname",
                    action="store_true", help="get tar name")
parser.add_argument("-d", "--getdirname",
                    action="store_true", help="get dir name")
parser.add_argument("-e", "--getpkgsource",
                    action="store_true", help="get pkg source")
getargs = parser.parse_args()
getargs.source = os.path.realpath(getargs.source)
pkgsetuppy = os.path.realpath(getargs.source + os.path.sep + "setup.py")
pyexecpath = os.path.realpath(sys.executable)
if (not os.path.exists(getargs.source) or not os.path.isdir(getargs.source)):
    raise Exception("Could not find directory.")
if (not os.path.exists(pkgsetuppy) or not os.path.isfile(pkgsetuppy)):
    raise Exception("Could not find setup.py in directory.")

pypkgenlistp = subprocess.Popen([pyexecpath,
                                 pkgsetuppy,
                                 "getversioninfo"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
pypkgenout, pypkgenerr = pypkgenlistp.communicate()
if (sys.version[0] == "3"):
    pypkgenout = pypkgenout.decode('utf-8')
pymodule = json.loads(pypkgenout)
setuppy_verinfo = pymodule['versionlist']
setuppy_author = pymodule['author']
setuppy_authoremail = pymodule['authoremail']
setuppy_maintainer = pymodule['maintainer']
setuppy_maintaineremail = pymodule['maintaineremail']
setuppy_description = pymodule['description']
setuppy_license = pymodule['license']
setuppy_keywords = pymodule['keywords']
setuppy_url = pymodule['url']
setuppy_downloadurl = pymodule['downloadurl']
setuppy_longdescription = pymodule['longdescription']
setuppy_platforms = pymodule['platforms']

if (sys.version[0] == "2"):
    pkgsource = "py2upc-ean"
if (sys.version[0] == "3"):
    pkgsource = "py3upc-ean"
pkgupstreamname = "PyUPC-EAN"
pkgveralt = str(setuppy_verinfo[0]) + "." + \
    str(setuppy_verinfo[1]) + "." + str(setuppy_verinfo[2])
pkgveraltrel = str(setuppy_verinfo[4])
pkgver = str(pkgveralt) + "-rc" + str(setuppy_verinfo[4])
pkgurgency = "urgency=low"
pkgauthorname = setuppy_author
pkgauthoremail = setuppy_authoremail
pkgauthoremailalt = setuppy_authoremail.replace(
    "@", "[at]").replace(".", "[dot]")
pkgauthor = pkgauthorname + " <" + pkgauthoremail + ">"
pkgauthoralt = pkgauthorname + " <" + pkgauthoremailalt + ">"
pkgmaintainername = setuppy_maintainer
pkgmaintaineremail = setuppy_maintaineremail
pkgmaintaineremailalt = setuppy_maintaineremail.replace(
    "@", "[at]").replace(".", "[dot]")
pkgmaintainer = pkgmaintainername + " <" + pkgmaintaineremail + ">"
pkgmaintaineralt = pkgmaintainername + " <" + pkgmaintaineremailalt + ">"
pkggiturl = "https://github.com/GameMaker2k/PyUPC-EAN.git"
pkghomepage = setuppy_url
pkgsection = "python"
pkgpriority = "optional"
if (sys.version[0] == "2"):
    pkgbuilddepends = "'python2' 'python2-pillow'"
if (sys.version[0] == "3"):
    pkgbuilddepends = "'python' 'python-pillow'"
pkgstandardsversion = "3.9.8"
if (sys.version[0] == "2"):
    pkgpackage = "python2-pyupcean"
    pkgoldname = "python2-upcean"
if (sys.version[0] == "3"):
    pkgpackage = "python-pyupcean"
    pkgoldname = "python-upcean"
pkgarchitecture = "'any' 'i686' 'x86_64'"
if (sys.version[0] == "2"):
    pkgdepends = "'python2-setuptools'"
if (sys.version[0] == "3"):
    pkgdepends = "'python-setuptools'"
pkgdescription = setuppy_description + "\n " + setuppy_longdescription
pkgtzstr = time.strftime("%a, %d %b %Y %H:%M:%S %z")

if (getargs.getsource):
    print(getargs.source)
    sys.exit()
if (getargs.getparent):
    print(os.path.realpath(os.path.dirname(getargs.source)))
    sys.exit()
if (getargs.getdirname):
    print(pkgsource + "_" + pkgveralt + ".orig")
    sys.exit()
if (getargs.gettarname):
    print(pkgsource + "_" + pkgveralt + ".orig.tar.gz")
    sys.exit()
if (getargs.getpkgsource):
    print(pkgsource)
    sys.exit()

print("generating arch linux package build directory")

pacpkg_pkgbuild_dir = os.path.realpath(
    getargs.source + os.path.sep + pkgsource)
print("creating directory " + pacpkg_pkgbuild_dir)
if (not os.path.exists(pacpkg_pkgbuild_dir)):
    os.makedirs(pacpkg_pkgbuild_dir)
os.chmod(pacpkg_pkgbuild_dir, int("0755", 8))

gzparentdir = os.path.realpath(os.path.dirname(getargs.source))
filetargz = open(os.path.realpath(gzparentdir + os.path.sep +
                 pkgsource + "_" + pkgveralt + ".orig.tar.gz"), "rb")
filetargzmd5 = hashlib.md5(filetargz.read()).hexdigest()
filetargz.seek(0)
filetargzsha1 = hashlib.sha1(filetargz.read()).hexdigest()
filetargz.seek(0)
filetargzsha224 = hashlib.sha224(filetargz.read()).hexdigest()
filetargz.seek(0)
filetargzsha256 = hashlib.sha256(filetargz.read()).hexdigest()
filetargz.seek(0)
filetargzsha384 = hashlib.sha384(filetargz.read()).hexdigest()
filetargz.seek(0)
filetargzsha512 = hashlib.sha512(filetargz.read()).hexdigest()
filetargz.close()

pacpkg_pkgbuild_file = os.path.realpath(
    pacpkg_pkgbuild_dir + os.path.sep + "PKGBUILD")
print("generating file " + pacpkg_pkgbuild_file)
if (sys.version[0] == "2"):
    pacpkg_string_temp = "# Maintainer: " + pkgmaintaineralt + "\n"
    pacpkg_string_temp += "# This file was automatically generated by " + \
        profullname + " at\n"
    pacpkg_string_temp += "# " + pkgtzstr + "\n\n"
    pacpkg_string_temp += "pkgname=" + pkgpackage + "\n"
    pacpkg_string_temp += "pkgver=" + pkgveralt + "\n"
    pacpkg_string_temp += "pkgrel=" + pkgveraltrel + "\n"
    pacpkg_string_temp += "pkgdesc='" + setuppy_description + "'\n"
    pacpkg_string_temp += "url='" + setuppy_url + "'\n"
    pacpkg_string_temp += "arch=(" + pkgarchitecture + ")\n"
    pacpkg_string_temp += "license=('" + setuppy_license + "')\n"
    pacpkg_string_temp += "groups=()\n"
    pacpkg_string_temp += "depends=(" + pkgbuilddepends + ")\n"
    pacpkg_string_temp += "optdepends=()\n"
    pacpkg_string_temp += "makedepends=(" + pkgdepends + ")\n"
    pacpkg_string_temp += "conflicts=()\n"
    pacpkg_string_temp += "replaces=('" + pkgoldname + "')\n"
    pacpkg_string_temp += "backup=()\n"
    pacpkg_string_temp += "options=(!strip !emptydirs)\n"
    pacpkg_string_temp += "install=''\n"
    pacpkg_string_temp += "source=('." + os.path.sep + \
        pkgsource + "_" + pkgveralt + ".orig.tar.gz')\n"
    pacpkg_string_temp += "md5sums=('" + filetargzmd5 + "')\n"
    pacpkg_string_temp += "sha1sums=('" + filetargzsha1 + "')\n"
    pacpkg_string_temp += "sha224sums=('" + filetargzsha224 + "')\n"
    pacpkg_string_temp += "sha256sums=('" + filetargzsha256 + "')\n"
    pacpkg_string_temp += "sha384sums=('" + filetargzsha384 + "')\n"
    pacpkg_string_temp += "sha512sums=('" + filetargzsha512 + "')\n\n"
    pacpkg_string_temp += "build() {\n"
    pacpkg_string_temp += "  cd \"${srcdir}/" + \
        pkgsource + "_${pkgver}.orig\"\n"
    pacpkg_string_temp += "  python2 ./setup.py build\n"
    pacpkg_string_temp += "}\n\n"
    pacpkg_string_temp += "package() {\n"
    pacpkg_string_temp += "  cd \"${srcdir}/" + \
        pkgsource + "_${pkgver}.orig\"\n"
    pacpkg_string_temp += "  python2 ./setup.py install --root=\"${pkgdir}\" --optimize=1\n"
    pacpkg_string_temp += "}\n\n"
    pacpkg_string_temp += "# vim:set ts=2 sw=2 et:\n"
if (sys.version[0] == "3"):
    pacpkg_string_temp = "# Maintainer: " + pkgmaintaineralt + "\n"
    pacpkg_string_temp += "# This file was automatically generated by " + \
        profullname + " at\n"
    pacpkg_string_temp += "# " + pkgtzstr + "\n\n"
    pacpkg_string_temp += "pkgname=" + pkgpackage + "\n"
    pacpkg_string_temp += "pkgver=" + pkgveralt + "\n"
    pacpkg_string_temp += "pkgrel=" + pkgveraltrel + "\n"
    pacpkg_string_temp += "pkgdesc='" + setuppy_description + "'\n"
    pacpkg_string_temp += "url='" + setuppy_url + "'\n"
    pacpkg_string_temp += "arch=(" + pkgarchitecture + ")\n"
    pacpkg_string_temp += "license=('" + setuppy_license + "')\n"
    pacpkg_string_temp += "groups=()\n"
    pacpkg_string_temp += "depends=(" + pkgbuilddepends + ")\n"
    pacpkg_string_temp += "optdepends=()\n"
    pacpkg_string_temp += "makedepends=(" + pkgdepends + ")\n"
    pacpkg_string_temp += "conflicts=()\n"
    pacpkg_string_temp += "replaces=('" + pkgoldname + "')\n"
    pacpkg_string_temp += "backup=()\n"
    pacpkg_string_temp += "options=(!strip !emptydirs)\n"
    pacpkg_string_temp += "install=''\n"
    pacpkg_string_temp += "source=('." + os.path.sep + \
        pkgsource + "_" + pkgveralt + ".orig.tar.gz')\n"
    pacpkg_string_temp += "md5sums=('" + filetargzmd5 + "')\n"
    pacpkg_string_temp += "sha1sums=('" + filetargzsha1 + "')\n"
    pacpkg_string_temp += "sha224sums=('" + filetargzsha224 + "')\n"
    pacpkg_string_temp += "sha256sums=('" + filetargzsha256 + "')\n"
    pacpkg_string_temp += "sha384sums=('" + filetargzsha384 + "')\n"
    pacpkg_string_temp += "sha512sums=('" + filetargzsha512 + "')\n\n"
    pacpkg_string_temp += "build() {\n"
    pacpkg_string_temp += "  cd \"${srcdir}/" + \
        pkgsource + "_${pkgver}.orig\"\n"
    pacpkg_string_temp += "  python3 ./setup.py build\n"
    pacpkg_string_temp += "}\n\n"
    pacpkg_string_temp += "package() {\n"
    pacpkg_string_temp += "  cd \"${srcdir}/" + \
        pkgsource + "_${pkgver}.orig\"\n"
    pacpkg_string_temp += "  python3 ./setup.py install --root=\"${pkgdir}\" --optimize=1\n"
    pacpkg_string_temp += "}\n\n"
    pacpkg_string_temp += "# vim:set ts=2 sw=2 et:\n"
pacpkg_file_temp = open(pacpkg_pkgbuild_file, "w")
pacpkg_file_temp.write(pacpkg_string_temp)
pacpkg_file_temp.close()
os.chmod(pacpkg_pkgbuild_file, int("0755", 8))
