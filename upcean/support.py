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

    $FileInfo: support.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import platform
import inspect
try:
    import configparser
except ImportError:
    try:
        import SafeConfigParser as configparser
    except ImportError:
        import ConfigParser as configparser
from upcean.versioninfo import getcuryear, __author__, __copyright__, __credits__, __copyright_year__, __license__, __license_string__, __maintainer__, __email__, __status__, __project__, __project_url__, __version_info__, __build_time__, __build_time_utc__, __build_python_info__, __build_python_is_set__, get_build_python_info, __revision__, __version__, __version_alt__, version_info, __version_date_info__, __version_date__, __version_date_alt__, version_date

def get_importing_script_path():
    # Inspect the stack and get the frame of the caller
    stack = inspect.stack()
    for frame_info in stack:
        # In Python 2, frame_info is a tuple; in Python 3, it's a named tuple
        filename = frame_info[1] if isinstance(frame_info, tuple) else frame_info.filename
        if filename != __file__:  # Ignore current module's file
            return os.path.abspath(filename)
    return None

scriptconf = os.path.join(os.path.dirname(get_importing_script_path()), "upcean.ini")
if os.path.exists(scriptconf):
    __config_file__ = scriptconf
else:
    __config_file__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "upcean.ini")
__use_ini_file__ = True

if os.path.exists(__config_file__) and __use_ini_file__:
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read(__config_file__)
    # Accessing values from the config file
    enable_pilsupport = config.getboolean('main', 'enable_pilsupport')
    enable_cairosupport = config.getboolean('main', 'enable_cairosupport')
    enable_qahirahsupport = config.getboolean('main', 'enable_qahirahsupport')
    enable_cairosvgsupport = config.getboolean('main', 'enable_cairosvgsupport')
    enable_wandsupport = config.getboolean('main', 'enable_wandsupport')
    enable_magicksupport = config.getboolean('main', 'enable_magicksupport')
    enable_pgmagicksupport = config.getboolean('main', 'enable_pgmagicksupport')
else:
    enable_pilsupport = True
    enable_cairosupport = True
    enable_qahirahsupport = True
    enable_cairosvgsupport = True
    enable_wandsupport = True
    enable_magicksupport = True
    enable_pgmagicksupport = True

''' // Barcode Support List '''
bctype_dict = {'EAN2': "ean2", 'UPC2': "upc2", 'UPCS2': "ean2", 'EAN5': "ean5", 'UPC5': "upc5", 'UPCS5': "ean5", 'UPCA': "upca", 'UPCAEan': "upcaean", 'UPCE': "upce", 'EAN13': "ean13", 'EAN8': "ean8", 'STF': "stf", 'ITF': "itf", 'ITF6': "itf6", 'ITF14': "itf14",
               'CODE11': "code11", 'CODE39': "code39", 'CODE93': "code93", 'CODE128': "code128", 'CODE128Alt': "code128alt", 'CODE128Dec': "code128dec", 'CODE128Hex': "code128hex", 'CODE128Man': "code128man", 'CODABAR': "codabar", 'MSI': "msi", "GOODWILL": "goodwill"}
bctype_dict_alt = {'ean2': "EAN2", 'ean5': "EAN5", 'upc2': "UPC2", 'upc5': "UPC5", 'upca': "UPCA", 'upcaean': "UPCAEan", 'upce': "UPCE", 'ean13': "EAN13", 'ean8': "EAN8", 'stf': "STF", 'itf': "ITF", 'itf6': "ITF6", 'itf14': "ITF14", 'code11': "CODE11",
                   'code39': "CODE39", 'code93': "CODE93", 'code128': "CODE128", 'code128alt': "CODE128Alt", 'code128dec': "CODE128Dec", 'code128hex': "CODE128Hex", 'code128man': "CODE128Man", 'codabar': "CODABAR", 'msi': "MSI", "goodwill": "GOODWILL"}
bctype_list = ["ean2", "upc2", "ean5", "upc5", "upca", "upcaean", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14",
               "code11", "code39", "code93", "code128", "code128alt", "code128dec", "code128hex", "code128man", "codabar", "msi"]
PROVIDED_BARCODES = bctype_list
bctype_tuple = ("ean2", "upc2", "ean5", "upc5", "upca", "upcaean", "upce", "ean13", "ean8", "stf", "itf",
                "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dect", "codabar", "msi")
bctype_name = {'ean2': "EAN-2", 'ean5': "EAN-5", 'upc2': "EAN-2 Sup", 'upc5': "EAN-5 Sup", 'upca': "UPC-A", 'upcaean': "UPC-AEan", 'upce': "UPC-E", 'ean13': "EAN-13", 'ean8': "EAN-8", 'stf': "STF", 'itf': "ITF", 'itf6': "ITF-6", 'itf14': "ITF-14", "code11": "Code 11",
               "code39": "Code 39", "code93": "Code 93", "code128": "Code 128", "code128alt": "Code 128 Alt", "code128dec": "Code 128 Dec", "code128hex": "Code 128 Hex", "code128man": "Code 128 Man", 'codabar': "Codabar", 'msi': "MSI", "goodwill": "GOODWILL"}


def supported_barcodes(return_type="dict"):
    if(return_type == "dict"):
        return {'EAN2': "ean2", 'UPC2': "upc2", 'UPCS2': "ean2", 'EAN5': "ean5", 'UPC5': "upc5", 'UPCS5': "ean5", 'UPCA': "upca", 'UPCA': "upcaean", 'UPCE': "upce", 'EAN13': "ean13", 'EAN8': "ean8", 'STF': "stf", 'ITF': "itf", 'ITF6': "itf6", 'ITF14': "itf14", 'CODE11': "code11", 'CODE39': "code39", 'CODE93': "code93", 'CODE128': "code128", 'CODE128Alt': "code128alt", 'CODE128Dec': "code128dec", 'CODE128Hex': "code128hex", 'CODE128Man': "code128man", 'CODABAR': "codabar", 'MSI': "msi", "GOODWILL": "goodwill"}
    if(return_type == "list"):
        return ["ean2", "upc2", "ean5", "upc5", "upca", "upcaean", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dec", "code128hex", "code128man", "codabar", "msi", "goodwill"]
    if(return_type == "tuple"):
        return ("ean2", "upc2", "ean5", "upc5", "upca", "upcaean", "upce", "ean13", "ean8", "stf", "itf", "itf6", "itf14", "code11", "code39", "code93", "code128", "code128alt", "code128dec", "code128hex", "code128man", "codabar", "msi", "goodwill")
    return False


def barcode_support(return_type="dict"):
    return supported_barcodes(return_type)


def get_barcode_name(barcode_type="upca"):
    bctype_name = {'ean2': "EAN-2", 'ean5': "EAN-5", 'upc2': "EAN-2 Sup", 'upc5': "EAN-5 Sup", 'upca': "UPC-A", 'upcaean': "UPC-AEan", 'upce': "UPC-E", 'ean13': "EAN-13", 'ean8': "EAN-8", 'stf': "STF", 'itf': "ITF", 'itf6': "ITF-6", 'itf14': "ITF-14", "code11": "Code 11",
                   "code39": "Code 39", "code93": "Code 93", "code128": "Code 128", "code128alt": "Code 128 Alt", "code128dec": "Code 128 Dec", "code128hex": "Code 128 Hex", "code128man": "Code 128 Man", 'codabar': "Codabar", 'msi': "MSI", "goodwill": "GOODWILL"}
    return bctype_name.get(barcode_type, False)

enable_pillowsupport = enable_pilsupport

if(enable_qahirahsupport):
    def check_for_qahirah():
        # Qahirah Support Check
        qahirahsupport = True
        try:
            import qahirah
            qahirahsupport = True
        except ImportError:
            qahirahsupport = False
        return qahirahsupport
else:
    def check_for_qahirah():
        qahirahsupport = False
        return False

if(enable_cairosupport):
    def check_for_cairo():
        # Cairo Support Check
        cairosupport = True
        try:
            import cairo
            cairosupport = True
        except ImportError:
            try:
                import cairocffi as cairo
                cairosupport = True
            except ImportError:
                cairosupport = False
        return cairosupport
else:
    def check_for_cairo():
        cairosupport = False
        return False

if(enable_cairosvgsupport):
    def check_for_cairosvg():
        cairosvgsupport = True
        try:
            import cairosvg
            cairosvgsupport = True
        except ImportError:
            cairosvgsupport = False
        return cairosvgsupport
else:
    def check_for_cairosvg():
        cairosvgsupport = False
        return False

def check_for_svgwrite():
    # SVGWrite Support Check
    svgwritesupport = True
    try:
        import svgwrite
        svgwritesupport = True
    except ImportError:
        try:
            import upcean.svgcreate as svgwrite
            svgwritesupport = True
        except ImportError:
            svgwritesupport = False
    return svgwritesupport

if(enable_pilsupport):
    def check_for_pil():
        # PIL Support Check
        pilsupport = True
        try:
            import PIL
            pilsupport = True
        except ImportError:
            try:
                import Image
                pilsupport = True
            except ImportError:
                try:
                    from PIL import Image, ImageDraw, ImageFont
                    pilsupport = True
                except ImportError:
                    pilsupport = False
                return pilsupport
        return pilsupport
else:
    def check_for_pil():
        pilsupport = False
        return False

if(enable_pillowsupport):
    def check_for_pillow():
        # Pillow Support Check
        pilsupport = check_for_pil()
        if(not pilsupport):
            return pilsupport
        if(pilsupport):
            from PIL import Image
            try:
                pil_ver = Image.PILLOW_VERSION
                pil_is_pillow = True
            except AttributeError:
                try:
                    pil_ver = Image.__version__
                    pil_is_pillow = True
                except AttributeError:
                    pil_is_pillow = False
                except NameError:
                    pil_is_pillow = False
            except NameError:
                try:
                    pil_ver = Image.__version__
                    pil_is_pillow = True
                except AttributeError:
                    pil_is_pillow = False
                except NameError:
                    pil_is_pillow = False
        return pil_is_pillow
else:
    def check_for_pillow():
        pil_is_pillow = False
        return False


if(enable_wandsupport):
    def check_for_wand():
        wandsupport = True
        try:
            import wand
            wandsupport = True
        except ImportError:
            wandsupport = False
        return wandsupport
else:
    def check_for_wand():
        wandsupport = False
        return False


if(enable_magicksupport):
    def check_for_magick():
        magicksupport = True
        try:
            import PythonMagick
            magicksupport = True
        except ImportError:
            magicksupport = False
        return magicksupport
else:
    def check_for_magick():
        magicksupport = False
        return False

if(enable_pgmagicksupport):
    def check_for_pgmagick():
        pgmagicksupport = True
        try:
            import pgmagick
            pgmagicksupport = True
        except ImportError:
            pgmagicksupport = False
        return pgmagicksupport
else:
    def check_for_pgmagick():
        pgmagicksupport = False
        return False


def check_pil_is_pillow():
    pilsupport = False
    if(check_for_pil()):
        pilsupport = True
    pil_is_pillow = False
    if(pilsupport is True and check_for_pillow() is True):
        pil_is_pillow = True
    if(pilsupport is False or (pilsupport is True and check_for_pillow() is False)):
        pil_is_pillow = False
    return pil_is_pillow


def check_if_pil_is_pillow():
    pil_is_pillow = check_pil_is_pillow()
    return pil_is_pillow


def check_for_pil_only():
    pilsupport = False
    if(check_for_pil()):
        pilsupport = True
    pil_is_not_pillow = False
    if((pilsupport is True and check_for_pillow() is True) or pilsupport is False):
        pil_is_not_pillow = False
    if(pilsupport is True and check_for_pillow() is False):
        pil_is_not_pillow = True
    return pil_is_pillow


def check_only_for_pil():
    pil_is_not_pillow = check_pil_is_pillow()
    return pil_is_not_pillow


def check_pil_is_not_pillow():
    pil_is_not_pillow = check_pil_is_pillow()
    return pil_is_not_pillow


def check_if_pil_is_not_pillow():
    pil_is_not_pillow = check_pil_is_pillow()
    return pil_is_not_pillow


def get_pil_version(infotype=None):
    pilsupport = check_for_pil()
    if(not pilsupport):
        return pilsupport
    if(pilsupport):
        from PIL import Image
        try:
            pillow_ver = Image.PILLOW_VERSION
            pillow_ver = pillow_ver.split(".")
            pillow_ver = [int(x) for x in pillow_ver]
            pil_is_pillow = True
        except AttributeError:
            pillow_ver = None
            pil_is_pillow = False
        except NameError:
            pillow_ver = None
            pil_is_pillow = False
        try:
            pil_ver = Image.VERSION
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
        except AttributeError:
            pil_ver = None
        except NameError:
            pil_ver = None
        if(pillow_ver is None and pil_ver is not None):
            pil_info = {'pil_ver': pil_ver, 'pil_is_pillow': pil_is_pillow}
            return pil_info.get(infotype, pil_info)
        if(pillow_ver is not None and pil_ver is not None):
            pil_info = {'pil_ver': pil_ver, 'pillow_ver': pillow_ver,
                        'pil_is_pillow': pil_is_pillow}
            return pil_info.get(infotype, pil_info)
        if(pillow_ver is not None and pil_ver is None):
            pil_info = {'pillow_ver': pillow_ver,
                        'pil_is_pillow': pil_is_pillow}
            return pil_info.get(infotype, pil_info)


def get_pillow_version(infotype=None):
    pilsupport = check_for_pil()
    if(not pilsupport):
        return pilsupport
    if(pilsupport):
        from PIL import Image
        try:
            pillow_ver = Image.PILLOW_VERSION
            pillow_ver = pillow_ver.split(".")
            pillow_ver = [int(x) for x in pillow_ver]
            pil_is_pillow = True
        except AttributeError:
            try:
                pillow_ver = Image.__version__
                pil_is_pillow = True
            except AttributeError:
                pillow_ver = None
                pil_is_pillow = False
            except NameError:
                pillow_ver = None
                pil_is_pillow = False
        except NameError:
            try:
                pillow_ver = Image.__version__
                pil_is_pillow = True
            except AttributeError:
                pillow_ver = None
                pil_is_pillow = False
            except NameError:
                pillow_ver = None
                pil_is_pillow = False
        if(pillow_ver is None):
            return False
        if(pillow_ver is not None):
            pillow_info = {'pillow_ver': pillow_ver,
                           'pil_is_pillow': pil_is_pillow}
            return pillow_info.get(infotype, pillow_info)


def get_cairo_version(infotype=None):
    cairosupport = check_for_cairo()
    if(not cairosupport):
        return cairosupport
    if(cairosupport):
        import cairo
        cairo_ver = cairo.version
        cairo_info = {'cairo_ver': cairo_ver}
        return cairo_info.get(infotype, cairo_info)

def get_svgwrite_version(infotype=None):
    svgwritesupport = check_for_svgwrite()
    if(not svgwritesupport):
        return svgwritesupport
    if(svgwritesupport):
        import svgwrite
        svgwrite_ver = svgwrite.version
        svgwrite_str_ver = svgwrite.VERSION
        svgwrite_info = {'svgwrite_ver': svgwrite_ver, 'svgwrite_str_ver': svgwrite_str_ver}
        return svgwrite_info.get(infotype, svgwrite_info)

linuxdist = None
try:
    linuxdist = platform.linux_distribution()
except AttributeError:
    linuxdist = None

python_info = {'python_branch': platform.python_branch(), 'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_revision': platform.python_revision(), 'python_version': platform.python_version(), 'python_version_tuple': platform.python_version_tuple(), 'release': platform.release(), 'system': platform.system(
), 'uname': platform.uname(), 'architecture': platform.architecture(), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(), 'version': platform.version(), 'java_ver': platform.java_ver(), 'win32_ver': platform.win32_ver(), 'mac_ver': platform.mac_ver(), 'linux_distribution': linuxdist, 'libc_ver': platform.libc_ver()}
if(not __build_python_is_set__):
    __build_python_info__ = python_info


def get_python_info(infotype=None):
    global python_info
    python_info = python_info
    if(infotype is None):
        return python_info
    if(infotype is not None):
        return python_info.get(infotype, python_info)


pilsupport = check_for_pil()
pillowsupport = check_for_pillow()
cairosupport = check_for_cairo()
qahirahsupport = check_for_qahirah()
cairosvgsupport = check_for_cairosvg()
svgwritesupport = check_for_svgwrite()
wandsupport = check_for_wand()
magicksupport = check_for_magick()
pgmagicksupport = check_for_pgmagick()

defaultdraw = None
if((pilsupport or pillowsupport) and defaultdraw is None):
    defaultdraw = "pillow"
if(cairosupport and defaultdraw is None):
    defaultdraw = "cairo"
if(qahirahsupport and defaultdraw is None):
    defaultdraw = "qahirah"
if(wandsupport and defaultdraw is None):
    defaultdraw = "wand"
if(magicksupport and defaultdraw is None):
    defaultdraw = "magick"
if(pgmagicksupport and defaultdraw is None):
    defaultdraw = "pgmagick"
if(svgwritesupport and defaultdraw is None):
    defaultdraw = "svgwrite"
if(defaultdraw is None):
    defaultdraw = "svgwrite"
