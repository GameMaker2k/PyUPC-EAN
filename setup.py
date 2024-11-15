#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2023 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: setup.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

import re
import os
import sys
import time
import datetime
import platform
import pkg_resources
from setuptools import setup, find_packages

install_requires = []
extras_requires = []
# https://github.com/mapproxy/mapproxy/blob/master/setup.py


def pillow_installed():
    """Check if Pillow is installed"""
    pillow_req = pkg_resources.Requirement.parse('Pillow')
    try:
        pkg_resources.get_provider(pillow_req)
    except pkg_resources.DistributionNotFound:
        return False
    else:
        return True


# depend in Pillow if it is installed, otherwise depend on PIL
if pillow_installed():
    extras_requires.append('Pillow')
else:
    extras_requires.append('PIL')
extras_requires.append('pycairo')
extras_requires_dict = {'drawing_barcodes':  extras_requires}

pygenbuildinfo = True
# Open and read the version info file in a Python 2/3 compatible way
verinfofilename = os.path.realpath("." + os.path.sep + "upcean" + os.path.sep + "versioninfo.py")

# Use `with` to ensure the file is properly closed after reading
# In Python 2, open defaults to text mode; in Python 3, it’s better to specify encoding
open_kwargs = {'encoding': 'utf-8'} if sys.version_info[0] >= 3 else {}
with open(verinfofilename, "r", **open_kwargs) as verinfofile:
    verinfodata = verinfofile.read()

# Define the regex pattern for extracting version info
# We ensure the pattern works correctly in both Python 2 and 3 by escaping the strings properly
version_pattern = "__version_info__ = \(\s*(\\d+)\s*,\s*(\\d+)\s*,\s*(\\d+)\s*,\s*['\"]([\w\s]+)['\"]\s*,\s*(\\d+)\s*\)"
setuppy_verinfo = re.findall(version_pattern, verinfodata)[0]

# If version info is found, process it; handle the case where no match is found
if setuppy_verinfo:
    setuppy_verinfo_exp = setuppy_verinfo
else:
    print("Version info not found.")
    setuppy_verinfo_exp = None  # Handle missing version info gracefully

# Define the regex pattern for extracting version date info
date_pattern = "__version_date_info__ = \(\s*(\\d+)\s*,\s*(\\d+)\s*,\s*(\\d+)\s*,\s*['\"]([\w\s]+)['\"]\s*,\s*(\\d+)\s*\)"
setuppy_dateinfo = re.findall(date_pattern, verinfodata)[0]

# If date info is found, process it; handle the case where no match is found
if setuppy_dateinfo:
    setuppy_dateinfo_exp = setuppy_dateinfo
else:
    print("Date info not found.")
    setuppy_dateinfo_exp = None  # Handle missing date info gracefully

pymodule = {}
pymodule['version'] = str(setuppy_verinfo_exp[0])+"." + \
    str(setuppy_verinfo_exp[1])+"."+str(setuppy_verinfo_exp[2])
pymodule['versionrc'] = int(setuppy_verinfo_exp[4])
pymodule['versionlist'] = (int(setuppy_verinfo_exp[0]), int(setuppy_verinfo_exp[1]), int(
    setuppy_verinfo_exp[2]), str(setuppy_verinfo_exp[3]), int(setuppy_verinfo_exp[4]))
pymodule['verdate'] = str(setuppy_dateinfo_exp[0])+"." + \
    str(setuppy_dateinfo_exp[1])+"."+str(setuppy_dateinfo_exp[2])
pymodule['verdaterc'] = int(setuppy_dateinfo_exp[4])
pymodule['verdatelist'] = (int(setuppy_dateinfo_exp[0]), int(setuppy_dateinfo_exp[1]), int(
    setuppy_dateinfo_exp[2]), str(setuppy_dateinfo_exp[3]), int(setuppy_dateinfo_exp[4]))
pymodule['name'] = 'PyUPC-EAN'
pymodule['author'] = 'Kazuki Przyborowski'
pymodule['authoremail'] = 'kazuki.przyborowski@gmail.com'
pymodule['maintainer'] = 'Kazuki Przyborowski'
pymodule['maintaineremail'] = 'kazuki.przyborowski@gmail.com'
pymodule['description'] = 'A barcode library/module for python.'
pymodule['license'] = 'Revised BSD License'
pymodule['keywords'] = 'python barcode pyupc-ean pyupcean barcodegenerator barcode-generator barcodelibrary barcode-library barcodes codabar msi code11 code-11 code39 code-39 code93 code-93 code128 code-128 ean ean13 ean-13 ean2 ean-2 ean5 ean-5 ean8 ean-8 itf itf14 itf-14 stf upc upca upc-a upce upc-e gtin2 gtin-2 gtin5 gtin-5 gtin8 gtin-8 gtin12 gtin-12 gtin13 gtin-13 gtin14 gtin-14 ocr-a ocra ocr-b ocrb'
pymodule['url'] = 'https://github.com/GameMaker2k/PyUPC-EAN'
pymodule['downloadurl'] = 'https://github.com/GameMaker2k/PyUPC-EAN/archive/master.tar.gz'
pymodule['packages'] = find_packages()
pymodule['packagedata'] = {'upcean/fonts': ['*.otf', '*.ttf'],
                           'upcean/xml': ['*.dtd', '*.xsl', '*.xsd', '*.rng', '*.rnc']}
pymodule['includepackagedata'] = True
pymodule['installrequires'] = install_requires
pymodule['extrasrequires'] = extras_requires_dict
pymodule['longdescription'] = 'PyUPC-EAN is a barcode library/module for Python. It supports the barcode formats upc-e, upc-a, ean-13, ean-8, ean-2, ean-5, itf14, codabar, code11, code39, code93, code128, code-128, and msi.'
pymodule['platforms'] = 'OS Independent'
pymodule['zipsafe'] = False
# pymodule['pymodules'] = [y for x in os.walk("upcean") for y in glob.glob(os.path.join(x[0], '*.py'))];
pymodule['pymodules'] = []
pymodule['classifiers'] = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: OS/2',
    'Operating System :: OS Independent',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Office/Business',
    'Topic :: Office/Business :: Financial',
    'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    'Topic :: Utilities',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
if(len(sys.argv) > 1 and (sys.argv[1] == "versioninfo" or sys.argv[1] == "getversioninfo")):
    import json
    pymodule_data = json.dumps(pymodule)
    print(pymodule_data)
    sys.exit()
if(len(sys.argv) > 1 and (sys.argv[1] == "sourceinfo" or sys.argv[1] == "getsourceinfo")):
    srcinfofilename = os.path.realpath("."+os.path.sep+pkg_resources.to_filename(
        pymodule['name'])+".egg-info"+os.path.sep+"SOURCES.txt")
    srcinfofile = open(srcinfofilename, "r")
    srcinfodata = srcinfofile.read()
    srcinfofile.close()
    srcinfolist = srcinfodata.split('\n')
    srcfilelist = ""
    srcpdir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    for ifile in srcinfolist:
        srcfilelist = "."+os.path.sep+srcpdir+os.path.sep+ifile+" "+srcfilelist
    print(srcfilelist)
    sys.exit()
if(len(sys.argv) > 1 and sys.argv[1] == "cleansourceinfo"):
    os.system("rm -rfv \""+os.path.realpath("."+os.path.sep+"dist\""))
    os.system("rm -rfv \""+os.path.realpath("."+os.path.sep +
              pkg_resources.to_filename(pymodule['name'])+".egg-info\""))
    sys.exit()

if(pygenbuildinfo):
    mycurtime = datetime.datetime.now()
    mycurtimetuple = mycurtime.timetuple()
    mycurtimestamp = int(time.mktime(mycurtimetuple))
    '''verinfodata = verinfodata.replace('__build_time__ = {"timestamp": None, "year": None, "month": None, "day": None, "hour": None, "minute": None, "second": None};', '__build_time__ = {"timestamp": '+str(mycurtimestamp)+', "year": '+str(mycurtimetuple[0])+', "month": '+str(mycurtimetuple[1])+', "day": '+str(mycurtimetuple[2])+', "hour": '+str(mycurtimetuple[3])+', "minute": '+str(mycurtimetuple[4])+', "second": '+str(mycurtimetuple[5])+'};');'''
    verinfodata = re.sub("__build_time__ \= \{.*\}\;", '__build_time__ = {"timestamp": '+str(mycurtimestamp)+', "year": '+str(mycurtimetuple[0])+', "month": '+str(
        mycurtimetuple[1])+', "day": '+str(mycurtimetuple[2])+', "hour": '+str(mycurtimetuple[3])+', "minute": '+str(mycurtimetuple[4])+', "second": '+str(mycurtimetuple[5])+'};', verinfodata)
    utccurtime = datetime.datetime.utcnow()
    utccurtimetuple = utccurtime.timetuple()
    utccurtimestamp = int(time.mktime(utccurtimetuple))
    '''verinfodata = verinfodata.replace('__build_time_utc__ = {"timestamp": None, "year": None, "month": None, "day": None, "hour": None, "minute": None, "second": None};', '__build_time_utc__ = {"timestamp": '+str(utccurtimestamp)+', "year": '+str(utccurtimetuple[0])+', "month": '+str(utccurtimetuple[1])+', "day": '+str(utccurtimetuple[2])+', "hour": '+str(utccurtimetuple[3])+', "minute": '+str(utccurtimetuple[4])+', "second": '+str(utccurtimetuple[5])+'};');'''
    verinfodata = re.sub("__build_time_utc__ \= \{.*\}\;", '__build_time_utc__ = {"timestamp": '+str(utccurtimestamp)+', "year": '+str(utccurtimetuple[0])+', "month": '+str(
        utccurtimetuple[1])+', "day": '+str(utccurtimetuple[2])+', "hour": '+str(utccurtimetuple[3])+', "minute": '+str(utccurtimetuple[4])+', "second": '+str(utccurtimetuple[5])+'};', verinfodata)
    linuxdist = None
    try:
        linuxdist = platform.linux_distribution()
    except AttributeError:
        linuxdist = None
    if(sys.version[0] == "2"):
        '''verinfodata = verinfodata.replace('__build_python_info__ = {"python_branch": None, "python_build": None, "python_compiler": None, "python_implementation": None, "python_revision": None, "python_version": None, "python_version_tuple": None, "release": None, "system": None, "uname": None, "machine": None, "node": None, "platform": None, "processor": None, "version": None, "java_ver": None, "win32_ver": None, "mac_ver": None, "linux_distribution": None, "libc_ver": None};', '__build_python_info__ = '+str({'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(), 'system': platform.system(), 'uname': platform.uname(), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'architecture': platform.architecture(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()})+';');'''
        verinfodata = re.sub("__build_python_info__ \= \{.*\}\;", '__build_python_info__ = '+str({'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(
        ), 'system': platform.system(), 'uname': platform.uname(), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'architecture': platform.architecture(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()})+';', verinfodata)
    if(sys.version[0] == "3"):
        '''verinfodata = verinfodata.replace('__build_python_info__ = {"python_branch": None, "python_build": None, "python_compiler": None, "python_implementation": None, "python_revision": None, "python_version": None, "python_version_tuple": None, "release": None, "system": None, "uname": None, "machine": None, "node": None, "platform": None, "processor": None, "version": None, "java_ver": None, "win32_ver": None, "mac_ver": None, "linux_distribution": None, "libc_ver": None};', '__build_python_info__ = '+str({'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(), 'system': platform.system(), 'uname': (platform.uname()[0], platform.uname()[1], platform.uname()[2], platform.uname()[3], platform.uname()[4], platform.uname()[5]), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'architecture': platform.architecture(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()})+';');'''
        verinfodata = re.sub("__build_python_info__ \= \{.*\}\;", '__build_python_info__ = '+str({'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(), 'system': platform.system(), 'uname': (
            platform.uname()[0], platform.uname()[1], platform.uname()[2], platform.uname()[3], platform.uname()[4], platform.uname()[5]), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'architecture': platform.architecture(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()})+';', verinfodata)
    '''verinfodata = verinfodata.replace('__build_python_is_set__ = False;', '__build_python_is_set__ = True;');'''
    verinfodata = re.sub("__build_python_is_set__ \= .*\;",
                         '__build_python_is_set__ = True;', verinfodata)
    verinfofile = open(verinfofilename, "w")
    verinfofile.write(verinfodata)
    verinfofile.close()

setup(
    name=pymodule['name'],
    version=pymodule['version'],
    author=pymodule['author'],
    author_email=pymodule['authoremail'],
    maintainer=pymodule['maintainer'],
    maintainer_email=pymodule['maintaineremail'],
    description=pymodule['description'],
    license=pymodule['license'],
    keywords=pymodule['keywords'],
    url=pymodule['url'],
    download_url=pymodule['downloadurl'],
    packages=pymodule['packages'],
    package_data=pymodule['packagedata'],
    include_package_data=pymodule['includepackagedata'],
    install_requires=pymodule['installrequires'],
    extras_require=pymodule['extrasrequires'],
    long_description=pymodule['longdescription'],
    platforms=pymodule['platforms'],
    zip_safe=pymodule['zipsafe'],
    py_modules=pymodule['pymodules'],
    classifiers=pymodule['classifiers']
)
