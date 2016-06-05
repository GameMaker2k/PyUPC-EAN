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

distvertoupname = {'10.0': "Buster", '9.0': "Stretch", '8.0': "Jessie", '7.0': "Wheezy", '6.0': "Squeeze", '5.0': "Lenny", '4.0': "Etch", '3.1': "Sarge", '3.0': "Woody", '2.2': "Potato", '2.1': "Slink", '2.0': "Hamm", '1.3': "Bo", '1.2': "Rex", '1.1': "Buzz"};
distvertoname = {'10.0': "buster", '9.0': "stretch", '8.0': "jessie", '7.0': "wheezy", '6.0': "squeeze", '5.0': "lenny", '4.0': "etch", '3.1': "sarge", '3.0': "woody", '2.2': "potato", '2.1': "slink", '2.0': "hamm", '1.3': "bo", '1.2': "rex", '1.1': "buzz"};
distnamelist = distvertoname.values();
distnametover = {'buster': "10.0", 'stretch': "9.0", 'jessie': "8.0", 'wheezy': "7.0", 'squeeze': "6.0", 'lenny': "5.0", 'etch': "4.0", 'sarge': "3.1", 'woody': "3.0", 'potato': "2.2", 'slink': "2.1", 'hamm': "2.0", 'bo': "1.3", 'rex': "1.2", 'buzz': "1.1"};
distupnametover = {'Buster': "10.0", 'Stretch': "9.0", 'Jessie': "8.0", 'Wheezy': "7.0", 'Squeeze': "6.0", 'Lenny': "5.0", 'Etch': "4.0", 'Sarge': "3.1", 'Woody': "3.0", 'Potato': "2.2", 'Slink': "2.1", 'Hamm': "2.0", 'Bo': "1.3", 'Rex': "1.2", 'Buzz': "1.1"};
distnamelistalt = distnametover.keys();

debian_oldstable = "wheezy";
debian_stable = "jessie";
debian_testing = "stretch";
debian_nexttesting = "buster";

parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = profullname);
parser.add_argument("-s", "--source", default = os.path.realpath(os.getcwd()), help = "source dir");
parser.add_argument("-g", "--getsource", action = "store_true", help = "get source dir");
parser.add_argument("-p", "--getparent", action = "store_true", help = "get parent dir");
parser.add_argument("-t", "--gettarname", action = "store_true", help = "get tar name");
parser.add_argument("-d", "--getdirname", action = "store_true", help = "get dir name");
parser.add_argument("-c", "--codename", default = debian_stable, help = "enter release code name");
parser.add_argument("-e", "--getpkgsource", action = "store_true", help = "get pkg source");
getargs = parser.parse_args();
getargs.source = os.path.realpath(getargs.source);
pkgsetuppy = os.path.realpath(getargs.source+os.path.sep+"setup.py");
pyexecpath = os.path.realpath(sys.executable);
if(not os.path.exists(getargs.source) or not os.path.isdir(getargs.source)):
 raise Exception("Could not find directory.");
if(not os.path.exists(pkgsetuppy) or not os.path.isfile(pkgsetuppy)):
 raise Exception("Could not find setup.py in directory.");

getargs.codename = getargs.codename.lower();
if(not getargs.codename in distnamelist):
 print("Could not build for debian "+getargs.distro+" codename.");
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
if(getargs.codename=="squeeze" or getargs.codename=="wheezy"): 
 if(sys.version[0]=="2"):
  pkgbuilddepends = "python-setuptools, python-all, python-imaging, debhelper, dh-python, devscripts";
 if(sys.version[0]=="3"):
  pkgbuilddepends = "python3-setuptools, python3-all, python3-imaging, debhelper, dh-python, devscripts";
pkgstandardsversion = "3.9.5";
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
