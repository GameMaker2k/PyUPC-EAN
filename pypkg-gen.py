#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2016 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2016 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pypkg-gen.py - Last Update: 6/1/2016 Ver. 0.2.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, platform, datetime, argparse, subprocess;

__version_info__ = (0, 2, 0, "rc1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+"+"+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

proname = "pypkg-gen";
prover = __version__;
profullname = proname+" "+prover;

def which_exec(execfile):
 for path in os.environ["PATH"].split(":"):
  if os.path.exists(path + "/" + execfile):
   return path + "/" + execfile;

linuxdist = [None];
try:
 linuxdist = platform.linux_distribution();
except AttributeError:
 linuxdist = [None];
getlinuxdist = linuxdist;
setdistroname = "debian";
setdistrocname = "jessie";
if(getlinuxdist[0] is not None and (getlinuxdist[0].lower()=="debian" or getlinuxdist[0].lower()=="ubuntu" or getlinuxdist[0].lower()=="linuxmint")):
 setdistroname = getlinuxdist[0].lower();
 setdistrocname = getlinuxdist[2].lower();
 if(setdistrocname==""):
  lsblocatout = which_exec("lsb_release");
  pylsblistp = subprocess.Popen([lsblocatout, "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
  pylsbout, pylsberr = pylsblistp.communicate();
  if(sys.version[0]=="3"):
   pylsbout = pylsbout.decode("utf-8");
  pylsb_esc = re.escape("Codename:")+'([a-zA-Z\t+\s+]+)';
  pylsbname = re.findall(pylsb_esc, pylsbout)[0].lower();
  setdistrocname = pylsbname.strip();
if(getlinuxdist[0] is not None and getlinuxdist[0].lower()=="archlinux"):
 setdistroname = getlinuxdist[0].lower();
 setdistrocname = None;
parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = profullname);
parser.add_argument("-s", "--source", default = os.path.realpath(os.getcwd()), help = "source dir");
parser.add_argument("-d", "--distro", default = setdistroname, help = "enter linux distribution name");
parser.add_argument("-c", "--codename", default = setdistrocname, help = "enter release code name");
parser.add_argument("-p", "--pyver", default = sys.version[0], help = "enter version of python to use");
getargs = parser.parse_args();

bashlocatout = which_exec("bash");

getargs.source = os.path.realpath(getargs.source);
getargs.codename = getargs.codename.lower();
getargs.distro = getargs.distro.lower();

if(getargs.pyver=="2"):
 getpyver = "python2";
if(getargs.pyver=="3"):
 getpyver = "python3";
if(getargs.pyver!="2" and getargs.pyver!="3"):
 if(sys.version[0]=="2"):
  getpyver = "python2";
 if(sys.version[0]=="3"):
  getpyver = "python3";

get_pkgbuild_dir = os.path.realpath(getargs.source+os.path.sep+"pkgbuild");
get_pkgbuild_dist_pre_list = [d for d in os.listdir(get_pkgbuild_dir) if os.path.isdir(os.path.join(get_pkgbuild_dir, d))];
get_pkgbuild_dist_list = [];
for dists in get_pkgbuild_dist_pre_list:
 tmp_pkgbuild_python = os.path.realpath(get_pkgbuild_dir+os.path.sep+dists+os.path.sep+getpyver);
 if(os.path.exists(tmp_pkgbuild_python) and os.path.isdir(tmp_pkgbuild_python)):
  get_pkgbuild_dist_list.append(dists);
if(not getargs.distro in get_pkgbuild_dist_list):
 print("Could not build for "+getargs.distro+" distro.");
 sys.exit();

if(getargs.distro=="debian" or getargs.distro=="ubuntu" or getargs.distro=="linuxmint"):
 pypkgpath = os.path.realpath(getargs.source+os.path.sep+"pkgbuild"+os.path.sep+getargs.distro+os.path.sep+getpyver+os.path.sep+"pydeb-gen.sh");
 pypkgenlistp = subprocess.Popen([bashlocatout, pypkgpath, getargs.source, getargs.codename], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 pypkgenout, pypkgenerr = pypkgenlistp.communicate();
 if(sys.version[0]=="3"):
  pypkgenout = pypkgenout.decode("utf-8");
 print(pypkgenout);
 pypkgenlistp.wait();

if(getargs.distro=="archlinux"):
 pypkgpath = os.path.realpath(getargs.source+os.path.sep+"pkgbuild"+os.path.sep+getargs.distro+os.path.sep+getpyver+os.path.sep+"pypac-gen.sh");
 pypkgenlistp = subprocess.Popen([bashlocatout, pypkgpath, getargs.source, getargs.codename], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 pypkgenout, pypkgenerr = pypkgenlistp.communicate();
 if(sys.version[0]=="3"):
  pypkgenout = pypkgenout.decode("utf-8");
 print(pypkgenout);
 pypkgenlistp.wait();
