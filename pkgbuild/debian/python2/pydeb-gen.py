#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2015 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2015 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pydeb-gen.py - Last Update: 4/19/2015 Ver. 0.0.5 RC 2 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, datetime;

proname = "pydeb-gen";
prover = "0.0.5+rc2";
profullname = proname+" "+prover;

pkgsource = "pyupc-ean";
pkgver = "2.7.11-3";
pkgdistname = "wheezy";
pkgurgency = "urgency=low";
pkgmaintainername = "Kazuki Przyborowski";
pkgmaintaineremail = "kazuki.przyborowski@gmail.com";
pkgmaintainer = pkgmaintainername+" <"+pkgmaintaineremail+">";
pkghomepage = "https://github.com/GameMaker2k/PyUPC-EAN/";
pkgsection = "python";
pkgpriority = "optional";
pkgbuilddepends = "python-setuptools, python-all, python-imaging, debhelper";
pkgstandardsversion = "3.9.1";
pkgpackage = "python-pyupcean";
pkgarchitecture = "all";
pkgdepends = "${misc:Depends}, ${python:Depends}";
pkgdescription = "A barcode library/module for python.\n PyUPC-EAN is a barcode library/module for Python. It supports the barcode formats upc-e, upc-a, ean-13, ean-8, ean-2, ean-5, itf14, codabar, code11, code39, code93, and msi.";
pkgmycurtime = datetime.datetime.now();
pkgmycurtimetuple = pkgmycurtime.timetuple();
pkgutccurtime = datetime.datetime.utcnow();
pkgutccurtimetuple = pkgutccurtime.timetuple();
pkgtzhour = datetime.datetime.now().timetuple()[3] - datetime.datetime.utcnow().timetuple()[3];
if(pkgtzhour<0):
 pkgtzhourstr = "-"+str(abs(datetime.datetime.now().timetuple()[3]-datetime.datetime.utcnow().timetuple()[3])).zfill(2);
if(pkgtzhour>=0):
 pkgtzhourstr = str(abs(datetime.datetime.now().timetuple()[3]-datetime.datetime.utcnow().timetuple()[3])).zfill(2);
pkgtzminute = datetime.datetime.now().timetuple()[4] - datetime.datetime.utcnow().timetuple()[4];
pkgtzminutestr = str(pkgtzminute).zfill(2);
pkgtzstr = time.strftime("%a, %d %b %Y %H:%M:%S")+" "+pkgtzhourstr+pkgtzminutestr;

print("generating debian package build directory");

if(len(sys.argv)==1):
 debpkg_debian_dir = os.path.realpath(os.getcwd()+os.path.sep+"debian");
if(len(sys.argv)==2):
 getdebdir = os.path.realpath(sys.argv[1]);
 debpkg_debian_dir = os.path.realpath(getdebdir+os.path.sep+"debian");
print("creating directory "+debpkg_debian_dir);
if(not os.path.exists(debpkg_debian_dir)):
 os.makedirs(debpkg_debian_dir);

debpkg_changelog_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"changelog");
print("generating file "+debpkg_changelog_file);
debpkg_string_temp = pkgsource+" ("+pkgver+") "+pkgdistname+"; "+pkgurgency+"\n\n";
debpkg_string_temp += "  * source package automatically created by "+profullname+"\n\n";
debpkg_string_temp += " -- "+pkgmaintainer+"  "+pkgtzstr+"\n";
debpkg_file_temp = open(debpkg_changelog_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_compat_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"compat");
print("generating file "+debpkg_compat_file);
debpkg_string_temp = "7\n";
debpkg_file_temp = open(debpkg_compat_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_control_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"control");
print("generating file "+debpkg_control_file);
debpkg_string_temp = "Source: "+pkgsource+"\n";
debpkg_string_temp += "Maintainer: "+pkgmaintainer+"\n";
debpkg_string_temp += "Homepage: "+pkghomepage+"\n";
debpkg_string_temp += "Section: "+pkgsection+"\n";
debpkg_string_temp += "Priority: "+pkgpriority+"\n";
debpkg_string_temp += "Build-Depends: "+pkgbuilddepends+"\n";
debpkg_string_temp += "Standards-Version: "+pkgstandardsversion+"\n\n";
debpkg_string_temp += "Package: "+pkgpackage+"\n";
debpkg_string_temp += "Architecture: "+pkgarchitecture+"\n";
debpkg_string_temp += "Depends: "+pkgdepends+"\n";
debpkg_string_temp += "Description: "+pkgdescription+"\n";
debpkg_file_temp = open(debpkg_control_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_copyright_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"copyright");
print("generating file "+debpkg_copyright_file);
debpkg_string_temp = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n";
debpkg_string_temp += "		    Revised BSD License\n\n";
debpkg_string_temp += "Copyright (C) 2011-2015 Game Maker 2k. \n";
debpkg_string_temp += "All rights reserved.\n\n";
debpkg_string_temp += "Redistribution and use in source and binary forms, with or without\n";
debpkg_string_temp += "modification, are permitted provided that the following conditions are met:\n\n";
debpkg_string_temp += "  1. Redistributions of source code must retain the above copyright notice,\n";
debpkg_string_temp += "     this list of conditions and the following disclaimer.\n\n";
debpkg_string_temp += "  2. Redistributions in binary form must reproduce the above copyright \n";
debpkg_string_temp += "     notice, this list of conditions and the following disclaimer in \n";
debpkg_string_temp += "     the documentation and/or other materials provided with the distribution.\n\n";
debpkg_string_temp += "  3. Neither the name of Game Maker 2k nor the names of its contributors\n";
debpkg_string_temp += "     may be used to endorse or promote products derived from this software\n";
debpkg_string_temp += "     without specific prior written permission.\n\n";
debpkg_string_temp += "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" \n";
debpkg_string_temp += "AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE \n";
debpkg_string_temp += "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE \n";
debpkg_string_temp += "ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE \n";
debpkg_string_temp += "LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR \n";
debpkg_string_temp += "CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF \n";
debpkg_string_temp += "SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS \n";
debpkg_string_temp += "INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN \n";
debpkg_string_temp += "CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) \n";
debpkg_string_temp += "ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF \n";
debpkg_string_temp += "THE POSSIBILITY OF SUCH DAMAGE.\n\n";
debpkg_string_temp += "The views and conclusions contained in the software and documentation are those of the\n";
debpkg_string_temp += "authors and should not be interpreted as representing official policies, either expressed\n";
debpkg_string_temp += "or implied, of Game Maker 2k.\n";
debpkg_string_temp += "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n";
debpkg_file_temp = open(debpkg_copyright_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_rules_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"rules");
print("generating file "+debpkg_rules_file);
debpkg_string_temp = "#!/usr/bin/make -f\n\n";
debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
debpkg_string_temp += "# "+pkgtzstr+"\n\n";
debpkg_string_temp += "%:\n";
debpkg_string_temp += "	dh $@ --with python2 --buildsystem=python_distutils\n";
debpkg_file_temp = open(debpkg_rules_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_source_dir = os.path.realpath(debpkg_debian_dir+os.path.sep+"source");
print("creating directory "+debpkg_source_dir);
if(not os.path.exists(debpkg_source_dir)):
 os.makedirs(debpkg_source_dir);

debpkg_format_file = os.path.realpath(debpkg_source_dir+os.path.sep+"format");
print("generating file "+debpkg_format_file);
debpkg_string_temp = "3.0 (native)\n";
debpkg_file_temp = open(debpkg_format_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();

debpkg_options_file = os.path.realpath(debpkg_source_dir+os.path.sep+"options");
print("generating file "+debpkg_options_file);
debpkg_string_temp = "extend-diff-ignore=\"\\.egg-info\"\n";
debpkg_file_temp = open(debpkg_options_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
