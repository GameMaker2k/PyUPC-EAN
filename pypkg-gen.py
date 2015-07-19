'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2015 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2015 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: pypkg-gen.py - Last Update: 4/27/2015 Ver. 0.1.7 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, os, sys, time, datetime, argparse, subprocess;

__version_info__ = (0, 1, 7, "rc1");
if(__version_info__[3]!=None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])+"+"+str(__version_info__[3]);
if(__version_info__[3]==None):
 __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2]);

proname = "pypkg-gen";
prover = __version__;
profullname = proname+" "+prover;

parser = argparse.ArgumentParser(conflict_handler = "resolve", add_help = True);
parser.add_argument("-v", "--version", action = "version", version = profullname);
parser.add_argument("-s", "--source", default = os.path.realpath(os.getcwd()), help = "source dir");
parser.add_argument("-d", "--distro", default = "debian", help = "enter linux distribution name");
parser.add_argument("-c", "--codename", default = "jessie", help = "enter release code name");
getargs = parser.parse_args();

def which_exec(execfile):
 for path in os.environ["PATH"].split(":"):
  if os.path.exists(path + "/" + execfile):
   return path + "/" + execfile;
bashlocatout = which_exec("bash");

getargs.source = os.path.realpath(getargs.source);
getargs.codename = getargs.codename.lower();
getargs.distro = getargs.distro.lower();

if(sys.version[0]=="2"):
 getpyver = "python2";
if(sys.version[0]=="3"):
 getpyver = "python3";

if(getargs.distro=="debian" or getargs.distro=="ubuntu"):
 pypkgpath = os.path.realpath(getargs.source+os.path.sep+"pkgbuild"+os.path.sep+getargs.distro+os.path.sep+getpyver+os.path.sep+"pydeb-gen.sh");
 pypkgenlistp = subprocess.Popen([bashlocatout, pypkgpath, getargs.source, getargs.codename], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 pypkgenout, pypkgenerr = pypkgenlistp.communicate();
 print(pypkgenout);
 pypkgenlistp.wait();

if(getargs.distro=="archlinux"):
 pypkgpath = os.path.realpath(getargs.source+os.path.sep+"pkgbuild"+os.path.sep+getargs.distro+os.path.sep+getpyver+os.path.sep+"pypac-gen.sh");
 pypkgenlistp = subprocess.Popen([bashlocatout, pypkgpath, getargs.source, getargs.codename], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 pypkgenout, pypkgenerr = pypkgenlistp.communicate();
 print(pypkgenout);
 pypkgenlistp.wait();

if(getargs.distro=="redhat"):
 pypkgpath = os.path.realpath(getargs.source+os.path.sep+"pkgbuild"+os.path.sep+getargs.distro+os.path.sep+getpyver+os.path.sep+"pyrpm-gen.sh");
 pypkgenlistp = subprocess.Popen([bashlocatout, pypkgpath, getargs.source, getargs.codename], stdout=subprocess.PIPE, stderr=subprocess.PIPE);
 pypkgenout, pypkgenerr = pypkgenlistp.communicate();
 print(pypkgenout);
 pypkgenlistp.wait();
