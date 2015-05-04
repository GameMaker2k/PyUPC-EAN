#!/usr/bin/env python3

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2015 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2015 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pypac-gen.py - Last Update: 4/27/2015 Ver. 0.1.7 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, datetime, argparse, hashlib;

__version_info__ = (0, 1, 7, "rc1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+"+"+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

proname = "pypac-gen";
prover = __version__;
profullname = proname+" "+prover;

parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = profullname);
parser.add_argument("-s", "--source", default = os.path.realpath(os.getcwd()), help = "source dir");
parser.add_argument("-g", "--getsource", action = "store_true", help = "get source dir");
parser.add_argument("-p", "--getparent", action = "store_true", help = "get parent dir");
parser.add_argument("-t", "--gettarname", action = "store_true", help = "get tar name");
parser.add_argument("-d", "--getdirname", action = "store_true", help = "get dir name");
getargs = parser.parse_args();
getargs.source = os.path.realpath(getargs.source);
pkgsetuppy = os.path.realpath(getargs.source+os.path.sep+"setup.py");
if(not os.path.exists(getargs.source) or not os.path.isdir(getargs.source)):
 raise Exception("Could not find directory.");
if(not os.path.exists(pkgsetuppy) or not os.path.isfile(pkgsetuppy)):
 raise Exception("Could not find setup.py in directory.");

pacpkg_file_setuppy = open(pkgsetuppy, "r");
pacpkg_string_setuppy = pacpkg_file_setuppy.read();
setuppy_verinfo = re.findall("Ver\. ([0-9]+)\.([0-9]+)\.([0-9]+) RC ([0-9]+)", str(pacpkg_string_setuppy))[0];
setuppy_author = re.findall(" author \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_authoremail = re.findall(" author_email \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_maintainer = re.findall(" maintainer \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_maintaineremail = re.findall(" maintainer_email \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_description = re.findall(" description \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_license = re.findall(" license \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_keywords = re.findall(" keywords \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_url = re.findall(" url \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_downloadurl = re.findall(" download_url \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_longdescription = re.findall(" long_description \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
setuppy_platforms = re.findall(" platforms \= \'(.*)\'\,", str(pacpkg_string_setuppy))[0];
pacpkg_file_setuppy.close();

if(sys.version[0]=="2"):
 pkgsource = "py2upc-ean";
if(sys.version[0]=="3"):
 pkgsource = "py3upc-ean";
pkgupstreamname = "PyUPC-EAN";
pkgveralt = setuppy_verinfo[0]+"."+setuppy_verinfo[1]+"."+setuppy_verinfo[2];
pkgveraltrel = setuppy_verinfo[3];
pkgver = pkgveralt+"-rc"+setuppy_verinfo[3];
pkgurgency = "urgency=low";
pkgauthorname = setuppy_author;
pkgauthoremail = setuppy_authoremail;
pkgauthor = pkgauthorname+" <"+pkgauthoremail+">";
pkgmaintainername = setuppy_maintainer;
pkgmaintaineremail = setuppy_maintaineremail;
pkgmaintainer = pkgmaintainername+" <"+pkgmaintaineremail+">";
pkggiturl = "https://github.com/GameMaker2k/PyUPC-EAN.git";
pkghomepage = setuppy_url;
pkgsection = "python";
pkgpriority = "optional";
if(sys.version[0]=="2"):
 pkgbuilddepends = "'python2' 'python2-pillow'";
if(sys.version[0]=="3"):
 pkgbuilddepends = "'python' 'python-pillow'";
pkgstandardsversion = "3.9.5";
if(sys.version[0]=="2"):
 pkgpackage = "python2-pyupcean";
if(sys.version[0]=="3"):
 pkgpackage = "python-pyupcean";
pkgarchitecture = "'any' 'i686' 'x86_64'";
if(sys.version[0]=="2"):
 pkgdepends = "'python2-setuptools'";
if(sys.version[0]=="3"):
 pkgdepends = "'python-setuptools'";
pkgdescription = setuppy_description+"\n "+setuppy_longdescription;
pkgtzstr = time.strftime("%a, %d %b %Y %H:%M:%S %z");

if(getargs.getsource==True):
 print(getargs.source);
 sys.exit();
if(getargs.getparent==True):
 print(os.path.realpath(os.path.dirname(getargs.source)));
 sys.exit();
if(getargs.getdirname==True):
 print(pkgsource+"_"+pkgveralt+".orig");
 sys.exit();
if(getargs.gettarname==True):
 print(pkgsource+"_"+pkgveralt+".orig.tar.gz");
 sys.exit();

print("generating PKGBUILD build directory");

pacpkg_pkgbuild_dir = os.path.realpath(getargs.source+os.path.sep+pkgsource);
print("creating directory "+pacpkg_pkgbuild_dir);
if(not os.path.exists(pacpkg_pkgbuild_dir)):
 os.makedirs(pacpkg_pkgbuild_dir);
os.chmod(pacpkg_pkgbuild_dir, int("0755", 8));

gzparentdir = os.path.realpath(os.path.dirname(getargs.source));
filetargz = open(os.path.realpath(gzparentdir+os.path.sep+pkgsource+"_"+pkgveralt+".orig.tar.gz"), "rb");
filetargzmd5 = hashlib.md5(filetargz.read()).hexdigest();
filetargz.seek(0);
filetargzsha1 = hashlib.sha1(filetargz.read()).hexdigest();
filetargz.seek(0);
filetargzsha224 = hashlib.sha224(filetargz.read()).hexdigest();
filetargz.seek(0);
filetargzsha256 = hashlib.sha256(filetargz.read()).hexdigest();
filetargz.seek(0);
filetargzsha384 = hashlib.sha384(filetargz.read()).hexdigest();
filetargz.seek(0);
filetargzsha512 = hashlib.sha512(filetargz.read()).hexdigest();
filetargz.close();

pacpkg_pkgbuild_file = os.path.realpath(pacpkg_pkgbuild_dir+os.path.sep+"PKGBUILD");
print("generating file "+pacpkg_pkgbuild_file);
if(sys.version[0]=="2"):
 pacpkg_string_temp = "# Maintainer: "+pkgmaintainer+"\n";
 pacpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 pacpkg_string_temp += "# "+pkgtzstr+"\n\n";
 pacpkg_string_temp += "pkgname="+pkgpackage+"\n";
 pacpkg_string_temp += "pkgver="+pkgveralt+"\n";
 pacpkg_string_temp += "pkgrel="+pkgveraltrel+"\n";
 pacpkg_string_temp += "pkgdesc='"+setuppy_description+"'\n";
 pacpkg_string_temp += "url='"+setuppy_url+"'\n";
 pacpkg_string_temp += "arch=("+pkgarchitecture+")\n";
 pacpkg_string_temp += "license=('"+setuppy_license+"')\n";
 pacpkg_string_temp += "depends=("+pkgbuilddepends+")\n";
 pacpkg_string_temp += "makedepends=("+pkgdepends+")\n";
 pacpkg_string_temp += "conflicts=()\n";
 pacpkg_string_temp += "replaces=()\n";
 pacpkg_string_temp += "backup=()\n";
 pacpkg_string_temp += "install=''\n";
 pacpkg_string_temp += "source=('."+os.path.sep+pkgsource+"_"+pkgveralt+".orig.tar.gz')\n";
 pacpkg_string_temp += "md5sums=('"+filetargzmd5+"')\n";
 pacpkg_string_temp += "sha1sums=('"+filetargzsha1+"')\n";
 pacpkg_string_temp += "sha224sums=('"+filetargzsha224+"')\n";
 pacpkg_string_temp += "sha256sums=('"+filetargzsha256+"')\n";
 pacpkg_string_temp += "sha384sums=('"+filetargzsha384+"')\n";
 pacpkg_string_temp += "sha512sums=('"+filetargzsha512+"')\n\n";
 pacpkg_string_temp += "build() {\n";
 pacpkg_string_temp += "  cd \"${srcdir}/"+pkgsource+"_"+pkgveralt+".orig\"\n";
 pacpkg_string_temp += "  /usr/bin/python2 ./setup.py build\n";
 pacpkg_string_temp += "}\n\n";
 pacpkg_string_temp += "package() {\n";
 pacpkg_string_temp += "  cd \"${srcdir}/"+pkgsource+"_"+pkgveralt+".orig\"\n";
 pacpkg_string_temp += "  /usr/bin/python2 ./setup.py install --root \"${pkgdir}\"\n";
 pacpkg_string_temp += "}\n\n";
 pacpkg_string_temp += "# vim:set ts=2 sw=2 et:\n";
if(sys.version[0]=="3"):
 pacpkg_string_temp = "# Maintainer: Kazuki Przyborowski <kazukiprzyborowski[at]gmail[dot]com>\n";
 pacpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 pacpkg_string_temp += "# "+pkgtzstr+"\n\n";
 pacpkg_string_temp += "pkgname="+pkgpackage+"\n";
 pacpkg_string_temp += "pkgver="+pkgveralt+"\n";
 pacpkg_string_temp += "pkgrel="+pkgveraltrel+"\n";
 pacpkg_string_temp += "pkgdesc='"+setuppy_description+"'\n";
 pacpkg_string_temp += "url='"+setuppy_url+"'\n";
 pacpkg_string_temp += "arch=("+pkgarchitecture+")\n";
 pacpkg_string_temp += "license=('"+setuppy_license+"')\n";
 pacpkg_string_temp += "depends=("+pkgbuilddepends+")\n";
 pacpkg_string_temp += "makedepends=("+pkgdepends+")\n";
 pacpkg_string_temp += "conflicts=()\n";
 pacpkg_string_temp += "replaces=()\n";
 pacpkg_string_temp += "backup=()\n";
 pacpkg_string_temp += "install=''\n";
 pacpkg_string_temp += "source=('."+os.path.sep+pkgsource+"_"+pkgveralt+".orig.tar.gz')\n";
 pacpkg_string_temp += "md5sums=('"+filetargzmd5+"')\n";
 pacpkg_string_temp += "sha1sums=('"+filetargzsha1+"')\n";
 pacpkg_string_temp += "sha224sums=('"+filetargzsha224+"')\n";
 pacpkg_string_temp += "sha256sums=('"+filetargzsha256+"')\n";
 pacpkg_string_temp += "sha384sums=('"+filetargzsha384+"')\n";
 pacpkg_string_temp += "sha512sums=('"+filetargzsha512+"')\n\n";
 pacpkg_string_temp += "build() {\n";
 pacpkg_string_temp += "  cd \"${srcdir}/"+pkgsource+"_"+pkgveralt+".orig\"\n";
 pacpkg_string_temp += "  /usr/bin/python3 ./setup.py build\n";
 pacpkg_string_temp += "}\n\n";
 pacpkg_string_temp += "package() {\n";
 pacpkg_string_temp += "  cd \"${srcdir}/"+pkgsource+"_"+pkgveralt+".orig\"\n";
 pacpkg_string_temp += "  /usr/bin/python3 ./setup.py install --root \"${pkgdir}\"\n";
 pacpkg_string_temp += "}\n\n";
 pacpkg_string_temp += "# vim:set ts=2 sw=2 et:\n";
pacpkg_file_temp = open(pacpkg_pkgbuild_file, "w");
pacpkg_file_temp.write(pacpkg_string_temp);
pacpkg_file_temp.close();
os.chmod(pacpkg_pkgbuild_file, int("0755", 8));
