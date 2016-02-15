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

    $FileInfo: pyrpm-gen.py - Last Update: 2/15/2016 Ver. 0.1.7 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, datetime, argparse;

__version_info__ = (0, 1, 7, "rc1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+"+"+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

proname = "pyrpm-gen";
prover = __version__;
profullname = proname+" "+prover;
buildsystem = "python_distutils";

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

rpmpkg_file_setuppy = open(pkgsetuppy, "r");
rpmpkg_string_setuppy = rpmpkg_file_setuppy.read();
setuppy_verinfo = re.findall("Ver\. ([0-9]+)\.([0-9]+)\.([0-9]+) RC ([0-9]+)", str(rpmpkg_string_setuppy))[0];
setuppy_author = re.findall(" author \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_authoremail = re.findall(" author_email \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_maintainer = re.findall(" maintainer \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_maintaineremail = re.findall(" maintainer_email \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_description = re.findall(" description \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_license = re.findall(" license \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_keywords = re.findall(" keywords \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_url = re.findall(" url \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_downloadurl = re.findall(" download_url \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_longdescription = re.findall(" long_description \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
setuppy_platforms = re.findall(" platforms \= \'(.*)\'\,", str(rpmpkg_string_setuppy))[0];
rpmpkg_file_setuppy.close();

if(sys.version[0]=="2"):
 pkgsource = "Py2UPC-EAN";
if(sys.version[0]=="3"):
 pkgsource = "Py3UPC-EAN";
pkgupstreamname = "PyUPC-EAN";
pkgveralt = setuppy_verinfo[0]+"."+setuppy_verinfo[1]+"."+setuppy_verinfo[2];
pkgver = pkgveralt+"-"+setuppy_verinfo[3];
pkgverrel = setuppy_verinfo[3];
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
 pkgrequires = "python27, python27-imaging";
if(sys.version[0]=="3"):
 pkgrequires = "python34, python27-imaging";
pkgstandardsversion = "3.9.5";
if(sys.version[0]=="2"):
 pkgpackage = "python-pyupcean";
if(sys.version[0]=="3"):
 pkgpackage = "python3-pyupcean";
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
 print(pkgsource+"-"+pkgveralt);
 sys.exit();
if(getargs.gettarname==True):
 print(pkgsource+"-"+pkgveralt+".tar.gz");
 sys.exit();

print("generating red hat package build directory");

rpmpkg_rpmbuild_dir = os.path.realpath(getargs.source+os.path.sep+"rpmbuild");
print("creating directory "+rpmpkg_rpmbuild_dir);
if(not os.path.exists(rpmpkg_rpmbuild_dir)):
 os.makedirs(rpmpkg_rpmbuild_dir);
os.chmod(rpmpkg_rpmbuild_dir, int("0755", 8));

rpmpkg_build_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"BUILD");
print("creating directory "+rpmpkg_build_dir);
if(not os.path.exists(rpmpkg_build_dir)):
 os.makedirs(rpmpkg_build_dir);
os.chmod(rpmpkg_build_dir, int("0755", 8));

rpmpkg_buildroot_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"BUILDROOT");
print("creating directory "+rpmpkg_buildroot_dir);
if(not os.path.exists(rpmpkg_buildroot_dir)):
 os.makedirs(rpmpkg_buildroot_dir);
os.chmod(rpmpkg_buildroot_dir, int("0755", 8));

rpmpkg_rpms_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"RPMS");
print("creating directory "+rpmpkg_rpms_dir);
if(not os.path.exists(rpmpkg_rpms_dir)):
 os.makedirs(rpmpkg_rpms_dir);
os.chmod(rpmpkg_rpms_dir, int("0755", 8));

rpmpkg_sources_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"SOURCES");
print("creating directory "+rpmpkg_sources_dir);
if(not os.path.exists(rpmpkg_sources_dir)):
 os.makedirs(rpmpkg_sources_dir);
os.chmod(rpmpkg_sources_dir, int("0755", 8));

rpmpkg_specs_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"SPECS");
print("creating directory "+rpmpkg_specs_dir);
if(not os.path.exists(rpmpkg_specs_dir)):
 os.makedirs(rpmpkg_specs_dir);
os.chmod(rpmpkg_specs_dir, int("0755", 8));

rpmpkg_rpmspec_file = os.path.realpath(rpmpkg_specs_dir+os.path.sep+pkgsource+".spec");
print("generating file "+rpmpkg_rpmspec_file);
rpmpkg_string_temp = "# This file was automatically generated by "+profullname+" at\n";
rpmpkg_string_temp += "# "+pkgtzstr+"\n\n";
rpmpkg_string_temp += "%define name "+pkgsource+"\n";
if(sys.version[0]=="2"):
 rpmpkg_string_temp += "%define proname python-pyupcean\n";
if(sys.version[0]=="3"):
 rpmpkg_string_temp += "%define proname python3-pyupcean\n";
rpmpkg_string_temp += "%define requires "+pkgrequires+"\n";
rpmpkg_string_temp += "%define version "+pkgveralt+"\n";
rpmpkg_string_temp += "%define unmangled_version "+pkgveralt+"\n";
rpmpkg_string_temp += "%define unmangled_version "+pkgveralt+"\n";
rpmpkg_string_temp += "%define release "+pkgverrel+"\n";
rpmpkg_string_temp += "%define _topdir "+rpmpkg_rpmbuild_dir+"\n\n";
rpmpkg_string_temp += "Summary: "+setuppy_description+".\n";
rpmpkg_string_temp += "Name: %{name}\n";
rpmpkg_string_temp += "Provides: %{proname}\n";
rpmpkg_string_temp += "Version: %{version}\n";
rpmpkg_string_temp += "Release: %{release}\n";
rpmpkg_string_temp += "Requires: %{requires}\n";
rpmpkg_string_temp += "Source0: %{name}-%{unmangled_version}.tar.gz\n";
rpmpkg_string_temp += "License: "+setuppy_license+"\n";
rpmpkg_string_temp += "Group: Development/Libraries\n";
rpmpkg_string_temp += "BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot\n";
rpmpkg_string_temp += "Prefix: %{_prefix}\n";
rpmpkg_string_temp += "BuildArch: noarch\n";
rpmpkg_string_temp += "Vendor: "+pkgauthor+"\n";
rpmpkg_string_temp += "Packager: "+pkgmaintainer+"\n";
rpmpkg_string_temp += "Url: "+pkghomepage+"\n\n";
rpmpkg_string_temp += "%description\n";
rpmpkg_string_temp += setuppy_longdescription+".\n\n";
rpmpkg_string_temp += "%prep\n";
rpmpkg_string_temp += "%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}\n\n";
if(sys.version[0]=="2"):
 rpmpkg_string_temp += "%build\n";
 rpmpkg_string_temp += "python2 setup.py build\n\n";
 rpmpkg_string_temp += "%install\n";
 rpmpkg_string_temp += "python2 setup.py install --single-version-externally-managed -O1 --root=\"$RPM_BUILD_ROOT\" --record=\"INSTALLED_FILES\"\n\n";
if(sys.version[0]=="3"):
 rpmpkg_string_temp += "%build\n";
 rpmpkg_string_temp += "python3 setup.py build\n\n";
 rpmpkg_string_temp += "%install\n";
 rpmpkg_string_temp += "python3 setup.py install --single-version-externally-managed -O1 --root=\"$RPM_BUILD_ROOT\" --record=\"INSTALLED_FILES\"\n\n";
rpmpkg_string_temp += "%clean\n";
rpmpkg_string_temp += "rm -rf $RPM_BUILD_ROOT\n\n";
rpmpkg_string_temp += "%files -f INSTALLED_FILES\n";
rpmpkg_string_temp += "%defattr(-,root,root)\n";
rpmpkg_file_temp = open(rpmpkg_rpmspec_file, "w");
rpmpkg_file_temp.write(rpmpkg_string_temp);
rpmpkg_file_temp.close();
os.chmod(rpmpkg_rpmspec_file, int("0644", 8));

rpmpkg_srpms_dir = os.path.realpath(rpmpkg_rpmbuild_dir+os.path.sep+"SRPMS");
print("creating directory "+rpmpkg_srpms_dir);
if(not os.path.exists(rpmpkg_srpms_dir)):
 os.makedirs(rpmpkg_srpms_dir);
os.chmod(rpmpkg_srpms_dir, int("0755", 8));
