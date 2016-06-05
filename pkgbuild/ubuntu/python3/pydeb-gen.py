#!/usr/bin/env python3

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2016 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pydeb-gen.py - Last Update: 6/1/2016 Ver. 0.2.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, datetime, argparse, subprocess, json;

__version_info__ = (0, 2, 0, "rc1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+"+"+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

proname = "pydeb-gen";
prover = __version__;
profullname = proname+" "+prover;
buildsystem = "pybuild";

distupnametover = {'Warty': "4.10", 'Hoary': "5.04", 'Breezy': "5.10", 'Dapper': "6.06", 'Edgy': "6.10", 'Feisty': "7.04", 'Gutsy': "7.10", 'Hardy': "8.04", 'Intrepid': "8.10", 'Jaunty': "9.04", 'Karmic': "9.10", 'Lucid': "10.04", 'Maverick': "10.10", 'Natty': "11.04", 'Oneiric': "11.10", 'Precise': "12.04", 'Quantal': "12.10", 'Raring': "13.04", 'Saucy': "13.10", 'Trusty': "14.04", 'Utopic': "14.10", 'Vivid': "15.04", 'Wily': "15.10", 'Xenial': "16.04", 'Yakkety': "16.10"};
distnametover = {'warty': "4.10", 'hoary': "5.04", 'breezy': "5.10", 'dapper': "6.06", 'edgy': "6.10", 'feisty': "7.04", 'gutsy': "7.10", 'hardy': "8.04", 'intrepid': "8.10", 'jaunty': "9.04", 'karmic': "9.10", 'lucid': "10.04", 'maverick': "10.10", 'natty': "11.04", 'oneiric': "11.10", 'precise': "12.04", 'quantal': "12.10", 'raring': "13.04", 'saucy': "13.10", 'trusty': "14.04", 'utopic': "14.10", 'vivid': "15.04", 'wily': "15.10", 'xenial': "16.04", 'yakkety': "16.10"};
distnamelist = distnametover.keys();
distvertoname = {'4.10': "warty", '5.04': "hoary", '5.10': "breezy", '6.06': "dapper", '6.10': "edgy", '7.04': "feisty", '7.10': "gutsy", '8.04': "hardy", '8.10': "intrepid", '9.04': "jaunty", '9.10': "karmic", '10.04': "lucid", '10.10': "maverick", '11.04': "natty", '11.10': "oneiric", '12.04': "precise", '12.10': "quantal", '13.04': "raring", '13.10': "saucy", '14.04': "trusty", '14.10': "utopic", '15.04': "vivid", '15.10': "wily", '16.04': "xenial", '16.10': "yakkety"};
distvertoupname = {'4.10': "Warty", '5.04': "Hoary", '5.10': "Breezy", '6.06': "Dapper", '6.10': "Edgy", '7.04': "Feisty", '7.10': "Gutsy", '8.04': "Hardy", '8.10': "Intrepid", '9.04': "Jaunty", '9.10': "Karmic", '10.04': "Lucid", '10.10': "Maverick", '11.04': "Natty", '11.10': "Oneiric", '12.04': "Precise", '12.10': "Quantal", '13.04': "Raring", '13.10': "Saucy", '14.04': "Trusty", '14.10': "Utopic", '15.04': "Vivid", '15.10': "Wily", '16.04': "Xenial", '16.10': "Yakkety"};
distnamelistalt = distnametover.values();
distnametoveralt = {'Warty Warthog': "4.10", 'Hoary Hedgehog': "5.04", 'Breezy Badger': "5.10", 'Dapper Drake': "6.06", 'Edgy Eft': "6.10", 
'Feisty Fawn': "7.04", 'Gutsy Gibbon': "7.10", 'Hardy Heron': "8.04", 'Intrepid Ibex': "8.10", 'Jaunty Jackalope': "9.04", 'Karmic Koala': "9.10", 'Lucid Lynx': "10.04", 'Maverick Meerkat': "10.10", 'Natty Narwhal': "11.04", 'Oneiric Ocelot': "11.10", 'Precise Pangolin': "12.04", 'Quantal Quetzal': "12.10", 'Raring Ringtail': "13.04", 'Saucy Salamander': "13.10", 'Trusty Tahr': "14.04", 'Utopic Unicorn': "14.10", 'Vivid Vervet': "15.04", 'Wily Werewolf': "15.10", 'Xenial Xerus': "16.04", 'Yakkety Yak': "16.10"};
distvertonamealt = {'4.10': "Warty Warthog", '5.04': "Hoary Hedgehog", '5.10': "Breezy Badger", '6.06': "Dapper Drake", '6.10': "Edgy Eft", 
'7.04': "Feisty Fawn", '7.10': "Gutsy Gibbon", '8.04': "Hardy Heron", '8.10': "Intrepid Ibex", '9.04': "Jaunty Jackalope", '9.10': "Karmic Koala", '10.04': "Lucid Lynx", '10.10': "Maverick Meerkat", '11.04': "Natty Narwhal", '11.10': "Oneiric Ocelot", '12.04': "Precise Pangolin", '12.10': "Quantal Quetzal", '13.04': "Raring Ringtail", '13.10': "Saucy Salamander", '14.04': "Trusty Tahr", '14.10': "Utopic Unicorn", '15.04': "Vivid Vervet", '15.10': "Wily Werewolf", '16.04': "Xenial Xerus", '16.10': "Yakkety Yak"};

lmdistvertoname = {'1.0': "ada", '2.0': "barbara", '2.1': "bea", '2.2': "bianca", '3.0': "cassandra", '3.1': "celena", '4.0': "daryna", '5': "elyssa", '6': "felicia", '7': "gloria", '8': "helena", '9': "isadora", '10': "julia", '11': "katya", '12': "lisa", '13': "maya", '14': "nadia", '15': "olivia", '16': "petra", '17': "qiana", '17.1': "rebecca", '17.2': "rafaela", '17.3': "rosa", '18': "sarah"};
lmdistvertonamealt = {'1.0': "Ada", '2.0': "Barbara", '2.1': "Bea", '2.2': "Bianca", '3.0': "Cassandra", '3.1': "Celena", '4.0': "Daryna", '5': "Elyssa", '6': "Felicia", '7': "Gloria", '8': "Helena", '9': "Isadora", '10': "Julia", '11': "Katya", '12': "Lisa", '13': "Maya", '14': "Nadia", '15': "Olivia", '16': "Petra", '17': "Qiana", '17.1': "Rebecca", '17.2': "Rafaela", '17.3': "Rosa", '18': "Sarah"};
distlmnametouname = {"ada": "dapper", "barbara": "edgy", "bea": "edgy", "bianca": "edgy", "cassandra": "feisty", "celena": "feisty", "daryna": "gutsy", "elyssa": "hardy", "felicia": "intrepid", "gloria": "jaunty", "helena": "karmic", "isadora": "lucid", "julia": "maverick", "katya": "natty", "lisa": "oneiric", "maya": "precise", "nadia": "quantal", "olivia": "raring", "petra": "saucy", "qiana": "trusty", "rebecca": "trusty", "rafaela": "trusty", "rosa": "trusty", "sarah": "xenial"};
distlmnametounamealt = {"Ada": "Dapper", "Barbara": "Edgy", "Bea": "Edgy", "Bianca": "Edgy", "Cassandra": "Feisty", "Celena": "Feisty", "Daryna": "Gutsy", "Elyssa": "Hardy", "Felicia": "Intrepid", "Gloria": "Jaunty", "Helena": "Karmic", "Isadora": "Lucid", "Julia": "Maverick", "Katya": "Natty", "Lisa": "Oneiric", "Maya": "Precise", "Nadia": "Quantal", "Olivia": "Raring", "Petra": "Saucy", "Qiana": "Trusty", "Rebecca": "Trusty", "Rafaela": "Trusty", "Rosa": "Trusty", "Sarah": "Xenial"};

ubuntu_oldstable = "wily";
ubuntu_stable = "xenial";
ubuntu_testing = "yakkety";
linuxmint_ubuntu_stable = "xenial";

parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = profullname);
parser.add_argument("-s", "--source", default = os.path.realpath(os.getcwd()), help = "source dir");
parser.add_argument("-g", "--getsource", action = "store_true", help = "get source dir");
parser.add_argument("-p", "--getparent", action = "store_true", help = "get parent dir");
parser.add_argument("-t", "--gettarname", action = "store_true", help = "get tar name");
parser.add_argument("-d", "--getdirname", action = "store_true", help = "get dir name");
parser.add_argument("-c", "--codename", default = ubuntu_stable, help = "enter release code name");
parser.add_argument("-e", "--getpkgsource", action = "store_true", help = "get pkg source");
getargs = parser.parse_args();
getargs.source = os.path.realpath(getargs.source);
pkgsetuppy = os.path.realpath(getargs.source+os.path.sep+"setup.py");
pyexecpath = os.path.realpath(sys.executable);
if(not os.path.exists(getargs.source) or not os.path.isdir(getargs.source)):
 raise Exception("Could not find directory.");
if(not os.path.exists(pkgsetuppy) or not os.path.isfile(pkgsetuppy)):
 raise Exception("Could not find setup.py in directory.");

getargs.codename = distlmnametouname.get(getargs.codename, getargs.codename);
getargs.codename = distlmnametounamealt.get(getargs.codename, getargs.codename);
getargs.codename = getargs.codename.lower();
if(not getargs.codename in distnamelist):
 print("Could not build for ubuntu "+getargs.distro+" codename.");
 sys.exit();

pypkgenlistp = subprocess.Popen([pyexecpath, pkgsetuppy, "getversioninfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
pypkgenout, pypkgenerr = pypkgenlistp.communicate();
if(sys.version[0]=="3"):
 pypkgenout = pypkgenout.decode('utf-8');
pymodule = json.loads(pypkgenout);
setuppy_verinfo = pymodule['versionlist'];
setuppy_author = pymodule['author'];
setuppy_authoremail = pymodule['authoremail'];
setuppy_maintainer = pymodule['maintainer'];
setuppy_maintaineremail = pymodule['maintaineremail'];
setuppy_description = pymodule['description'];
setuppy_license = pymodule['license'];
setuppy_keywords = pymodule['keywords'];
setuppy_url = pymodule['url'];
setuppy_downloadurl = pymodule['downloadurl'];
setuppy_longdescription = pymodule['longdescription'];
setuppy_platforms = pymodule['platforms'];

if(sys.version[0]=="2"):
 pkgsource = "py2upc-ean";
if(sys.version[0]=="3"):
 pkgsource = "py3upc-ean";
pkgupstreamname = "PyUPC-EAN";
pkgveralt = str(setuppy_verinfo[0])+"."+str(setuppy_verinfo[1])+"."+str(setuppy_verinfo[2]);
pkgver = str(pkgveralt)+"rc"+str(setuppy_verinfo[4])+"~"+getargs.codename+str(distnametover.get(getargs.codename, "1").replace(".", ""));
pkgdistname = getargs.codename;
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
 pkgbuilddepends = "python-setuptools, python-all, python-pil, debhelper, dh-python, devscripts";
if(sys.version[0]=="3"):
 pkgbuilddepends = "python3-setuptools, python3-all, python3-pil, debhelper, dh-python, devscripts";
if(getargs.codename=="lucid" or getargs.codename=="precise"): 
 if(sys.version[0]=="2"):
  pkgbuilddepends = "python-setuptools, python-all, python-imaging, debhelper, dh-python, devscripts";
 if(sys.version[0]=="3"):
  pkgbuilddepends = "python3-setuptools, python3-all, python3-imaging, debhelper, dh-python, devscripts";
pkgstandardsversion = "3.9.8";
if(sys.version[0]=="2"):
 pkgpackage = "python-pyupcean";
 pkgoldname = "python-upcean";
if(sys.version[0]=="3"):
 pkgpackage = "python3-pyupcean";
 pkgoldname = "python3-upcean";
pkgarchitecture = "all";
if(sys.version[0]=="2"):
 pkgdepends = "${misc:Depends}, ${python:Depends}";
if(sys.version[0]=="3"):
 pkgdepends = "${misc:Depends}, ${python3:Depends}";
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
if(getargs.getpkgsource==True):
 print(pkgsource);
 sys.exit();

print("generating debian package build directory");

debpkg_debian_dir = os.path.realpath(getargs.source+os.path.sep+"debian");
print("creating directory "+debpkg_debian_dir);
if(not os.path.exists(debpkg_debian_dir)):
 os.makedirs(debpkg_debian_dir);
os.chmod(debpkg_debian_dir, int("0755", 8));

debpkg_changelog_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"changelog");
print("generating file "+debpkg_changelog_file);
debpkg_string_temp = pkgsource+" ("+pkgver+") "+pkgdistname+"; "+pkgurgency+"\n\n";
debpkg_string_temp += "  * source package automatically created by "+profullname+"\n\n";
debpkg_string_temp += " -- "+pkgmaintainer+"  "+pkgtzstr+"\n";
debpkg_file_temp = open(debpkg_changelog_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_changelog_file, int("0644", 8));

debpkg_compat_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"compat");
print("generating file "+debpkg_compat_file);
debpkg_string_temp = "9\n";
debpkg_file_temp = open(debpkg_compat_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_compat_file, int("0644", 8));

debpkg_control_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"control");
print("generating file "+debpkg_control_file);
debpkg_string_temp = "Source: "+pkgsource+"\n";
debpkg_string_temp += "Maintainer: "+pkgmaintainer+"\n";
debpkg_string_temp += "Homepage: "+pkghomepage+"\n";
debpkg_string_temp += "Vcs-Git: "+pkggiturl+"\n";
debpkg_string_temp += "Vcs-Browser: "+pkghomepage+"\n";
debpkg_string_temp += "Section: "+pkgsection+"\n";
debpkg_string_temp += "Priority: "+pkgpriority+"\n";
debpkg_string_temp += "Build-Depends: "+pkgbuilddepends+"\n";
debpkg_string_temp += "Standards-Version: "+pkgstandardsversion+"\n\n";
debpkg_string_temp += "Package: "+pkgpackage+"\n";
debpkg_string_temp += "Architecture: "+pkgarchitecture+"\n";
debpkg_string_temp += "Depends: "+pkgdepends+"\n";
debpkg_string_temp += "Replaces: "+pkgoldname+"\n";
debpkg_string_temp += "Description: "+pkgdescription+"\n";
debpkg_file_temp = open(debpkg_control_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_control_file, int("0644", 8));

debpkg_copyright_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"copyright");
print("generating file "+debpkg_copyright_file);
debpkg_string_temp = "Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n";
debpkg_string_temp += "Upstream-Name: "+pkgupstreamname+"\n";
debpkg_string_temp += "Source: "+pkghomepage+"\n\n";
debpkg_string_temp += "Files: *\n";
debpkg_string_temp += "Copyright: Copyright 2011-2016 "+pkgauthor+"\n";
debpkg_string_temp += "License: BSD\n\n";
debpkg_string_temp += "License: BSD\n";
debpkg_string_temp += "		    Revised BSD License\n\n";
debpkg_string_temp += "Copyright (C) 2011-2016 Game Maker 2k. \n";
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
debpkg_file_temp = open(debpkg_copyright_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_copyright_file, int("0644", 8));

debpkg_rules_file = os.path.realpath(debpkg_debian_dir+os.path.sep+"rules");
print("generating file "+debpkg_rules_file);
if(sys.version[0]=="2" and (buildsystem=="python" or buildsystem=="python_distutils")):
 debpkg_string_temp = "#!/usr/bin/make -f\n\n";
 debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 debpkg_string_temp += "# "+pkgtzstr+"\n\n";
 debpkg_string_temp += "%:\n";
 debpkg_string_temp += "	dh $@ --with python2 --buildsystem=python_distutils\n";
if(sys.version[0]=="3" and (buildsystem=="python" or buildsystem=="python_distutils")):
 debpkg_string_temp = "#!/usr/bin/make -f\n\n";
 debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 debpkg_string_temp += "# "+pkgtzstr+"\n\n";
 debpkg_string_temp += "%:\n";
 debpkg_string_temp += "	dh $@ --with python3\n";
 debpkg_string_temp += "override_dh_auto_build:\n";
 debpkg_string_temp += "	python3 setup.py build\n\n";
 debpkg_string_temp += "override_dh_auto_test:\n";
 debpkg_string_temp += "	python3 setup.py test\n\n";
 debpkg_string_temp += "override_dh_auto_install:\n";
 debpkg_string_temp += "	python3 setup.py install \\\n";
 debpkg_string_temp += "        --force --root=$(CURDIR)/debian/"+pkgpackage+" \\\n";
 debpkg_string_temp += "        --no-compile -O0 --install-layout=deb\n\n";
 debpkg_string_temp += "override_dh_auto_clean:\n";
 debpkg_string_temp += "	python3 setup.py clean\n";
if(sys.version[0]=="2" and (buildsystem=="pybuild" or buildsystem=="python_build")):
 debpkg_string_temp = "#!/usr/bin/make -f\n\n";
 debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 debpkg_string_temp += "# "+pkgtzstr+"\n\n";
 debpkg_string_temp += "%:\n";
 debpkg_string_temp += "	dh $@ --with python2 --buildsystem=pybuild\n";
if(sys.version[0]=="3" and (buildsystem=="pybuild" or buildsystem=="python_build")):
 debpkg_string_temp = "#!/usr/bin/make -f\n\n";
 debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 debpkg_string_temp += "# "+pkgtzstr+"\n\n";
 debpkg_string_temp += "%:\n";
 debpkg_string_temp += "	dh $@ --with python3 --buildsystem=pybuild\n";
if((sys.version[0]=="2" or sys.version[0]=="3") and buildsystem=="cmake"):
 debpkg_string_temp = "#!/usr/bin/make -f\n\n";
 debpkg_string_temp += "# This file was automatically generated by "+profullname+" at\n";
 debpkg_string_temp += "# "+pkgtzstr+"\n\n";
 debpkg_string_temp += "%:\n";
 debpkg_string_temp += "	dh $@ --buildsystem=cmake --parallel\n";
debpkg_file_temp = open(debpkg_rules_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_rules_file, int("0755", 8));

debpkg_source_dir = os.path.realpath(debpkg_debian_dir+os.path.sep+"source");
print("creating directory "+debpkg_source_dir);
if(not os.path.exists(debpkg_source_dir)):
 os.makedirs(debpkg_source_dir);
os.chmod(debpkg_source_dir, int("0755", 8));

debpkg_format_file = os.path.realpath(debpkg_source_dir+os.path.sep+"format");
print("generating file "+debpkg_format_file);
debpkg_string_temp = "3.0 (native)\n";
debpkg_file_temp = open(debpkg_format_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_format_file, int("0644", 8));

debpkg_options_file = os.path.realpath(debpkg_source_dir+os.path.sep+"options");
print("generating file "+debpkg_options_file);
debpkg_string_temp = "extend-diff-ignore=\"\\.egg-info\"\n";
debpkg_file_temp = open(debpkg_options_file, "w");
debpkg_file_temp.write(debpkg_string_temp);
debpkg_file_temp.close();
os.chmod(debpkg_options_file, int("0644", 8));
