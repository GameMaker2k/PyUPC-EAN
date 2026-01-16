# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: support.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import upcean.functions
import platform
import inspect
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json
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


# --------------------
# Config selection flags
# --------------------
__use_env_file__ = True
__use_ini_file__ = True
__use_ini_name__ = "upcean.ini"
__use_json_file__ = False
__use_json_name__ = "upcean.json"

# If both enabled, prefer INI (your existing behavior)
if __use_ini_file__ and __use_json_file__:
    __use_json_file__ = False


# --------------------
# Find config file path
# --------------------
if ('PYUPCEAN_CONFIG_FILE' in os.environ and
        os.path.exists(os.environ['PYUPCEAN_CONFIG_FILE']) and
        __use_env_file__):
    scriptconf = os.environ['PYUPCEAN_CONFIG_FILE']
else:
    prescriptpath = get_importing_script_path()
    if prescriptpath is not None:
        if __use_ini_file__ and not __use_json_file__:
            scriptconf = os.path.join(os.path.dirname(prescriptpath), __use_ini_name__)
        elif __use_json_file__ and not __use_ini_file__:
            scriptconf = os.path.join(os.path.dirname(prescriptpath), __use_json_name__)
        else:
            scriptconf = ""
            prescriptpath = None
    else:
        scriptconf = ""

if os.path.exists(scriptconf):
    __config_file__ = scriptconf
elif __use_ini_file__ and not __use_json_file__:
    __config_file__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), __use_ini_name__)
elif (not __use_ini_file__) and __use_json_file__:
    __config_file__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), __use_json_name__)
else:
    __config_file__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), __use_ini_name__)


# --------------------
# Defaults
# --------------------
DEFAULTS = {
    "enable_tkintersupport": True,
    "enable_pilsupport": True,
    "enable_drawsvgsupport": True,
    "enable_cairosupport": True,
    "enable_qahirahsupport": True,
    "enable_cairosvgsupport": False,
    "enable_wandsupport": True,
    "enable_magicksupport": True,
    "enable_pgmagicksupport": True,
    "enable_cv2support": True,
    "enable_skimagesupport": True,
    "enable_internal_svgwrite": False,
}


def _as_bool(value, default_value):
    """Coerce JSON values (bool/int/str) into bool safely for Py2/3."""
    if isinstance(value, bool):
        return value
    # Py2: bool is a subclass of int, but we already handled bool above.
    if isinstance(value, (int, float)):
        return bool(value)
    try:
        basestring  # py2
        string_types = (basestring,)
    except NameError:
        string_types = (str,)  # py3

    if isinstance(value, string_types):
        s = value.strip().lower()
        if s in ("1", "true", "yes", "y", "on"):
            return True
        if s in ("0", "false", "no", "n", "off"):
            return False
    return default_value


def load_settings(config_path):
    settings = dict(DEFAULTS)

    if not config_path or not os.path.exists(config_path):
        return settings

    ext = os.path.splitext(config_path)[1].lower()

    # Decide format:
    # - If JSON enabled and file looks like .json OR INI disabled -> JSON
    # - Else if INI enabled -> INI
    use_json = (__use_json_file__ and (ext == ".json" or not __use_ini_file__))
    use_ini = (__use_ini_file__ and not use_json)

    if use_json:
        if json is None:
            return settings  # json module missing (very rare)
        try:
            # Py2: no encoding arg; Py3: use encoding.
            try:
                f = open(config_path, "r", encoding="utf-8")
            except TypeError:
                f = open(config_path, "r")
            with f:
                data = json.load(f)
        except Exception:
            return settings

        # Support {"main": {...}} or flat {"enable_x": ...}
        if isinstance(data, dict) and "main" in data and isinstance(data.get("main"), dict):
            main = data["main"]
        elif isinstance(data, dict):
            main = data
        else:
            main = {}

        for k, dflt in DEFAULTS.items():
            settings[k] = _as_bool(main.get(k, dflt), dflt)

        return settings

    if use_ini:
        try:
            config = configparser.ConfigParser()
            config.read(config_path)
        except Exception:
            return settings

        for k, dflt in DEFAULTS.items():
            # getboolean fallback exists in py3; in py2 it's not always available as a kwarg.
            try:
                settings[k] = config.getboolean("main", k, fallback=dflt)  # py3
            except TypeError:
                # py2: emulate fallback
                try:
                    settings[k] = config.getboolean("main", k)
                except Exception:
                    settings[k] = dflt
            except Exception:
                settings[k] = dflt

        return settings

    return settings


# --------------------
# Apply settings to variables (same names you already use)
# --------------------
_settings = load_settings(__config_file__)

enable_tkintersupport    = _settings["enable_tkintersupport"]
enable_pilsupport        = _settings["enable_pilsupport"]
enable_drawsvgsupport    = _settings["enable_drawsvgsupport"]
enable_cairosupport      = _settings["enable_cairosupport"]
enable_qahirahsupport    = _settings["enable_qahirahsupport"]
enable_cairosvgsupport   = _settings["enable_cairosvgsupport"]
enable_wandsupport       = _settings["enable_wandsupport"]
enable_magicksupport     = _settings["enable_magicksupport"]
enable_pgmagicksupport   = _settings["enable_pgmagicksupport"]
enable_cv2support        = _settings["enable_cv2support"]
enable_skimagesupport    = _settings["enable_skimagesupport"]
enable_internal_svgwrite = _settings["enable_internal_svgwrite"]

if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "pretkinter.py")):
    enable_tkintersupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "prepil.py")):
    enable_pilsupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "predrawsvg.py")):
    enable_drawsvgsupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "precairo.py")):
    enable_cairosupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "preqahirah.py")):
    enable_qahirahsupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "prewand.py")):
    enable_wandsupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "premagick.py")):
    enable_magicksupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "prepgmagick.py")):
    enable_pgmagicksupport = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "precv2.py")):
    enable_cv2support = False
if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "predraw", "preskimage.py")):
    enable_skimagesupport = False

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

if(not enable_internal_svgwrite):
    def check_for_svgwrite():
        # SVGWrite Support Check
        svgwritesupport = True
        try:
            import upcean.svgwrite as svgwrite
            svgwritesupport = True
        except ImportError:
            try:
                import upcean.svgcreate as svgwrite
                svgwritesupport = True
            except ImportError:
                svgwritesupport = False
        return svgwritesupport
else:
    def check_for_svgwrite():
        svgwritesupport = True
        try:
            import upcean.svgcreate as svgwrite
            svgwritesupport = True
        except ImportError:
            svgwritesupport = False
        return svgwritesupport

if enable_tkintersupport:
    def check_for_tkinter():
        # tkinter Support Check
        tkintersupport = True
        try:
            import tkinter
            from tkinter import font as tkFont
            tkintersupport = True
        except ImportError:
            try:
                import Tkinter as tkinter
                import tkFont
                tkintersupport = True
            except ImportError:
                tkintersupport = False
        return tkintersupport
else:
    def check_for_tkinter():
        tkintersupport = False
        return False

if(enable_drawsvgsupport):
    def check_for_drawsvg():
        drawsvgsupport = True
        try:
            import drawsvg
            drawsvgsupport = True
        except ImportError:
            drawsvgsupport = True
            return drawsvgsupport
        return drawsvgsupport
else:
    def check_for_drawsvg():
        drawsvgsupport = False
        return False

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


if(enable_cv2support):
    def check_for_cv2():
        cv2support = True
        try:
            import cv2
            import numpy as np
            cv2support = True
        except ImportError:
            cv2support = False
        return cv2support
else:
    def check_for_cv2():
        cv2support = False
        return False


if(enable_skimagesupport):
    def check_for_skimage():
        skimagesupport = True
        try:
            import skimage
            import numpy as np
            skimagesupport = True
        except ImportError:
            skimagesupport = False
        return skimagesupport
else:
    def check_for_skimage():
        skimagesupport = False
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

imagelibsupport = []
tkintersupport = check_for_tkinter()
if(tkintersupport):
    imagelibsupport.append("tkinter")
pilsupport = check_for_pil()
if(pilsupport):
    imagelibsupport.append("pil")
pillowsupport = check_for_pillow()
if(pillowsupport):
    imagelibsupport.append("pillow")
drawsvgsupport = check_for_drawsvg()
if(drawsvgsupport):
    imagelibsupport.append("drawsvg")
cairosupport = check_for_cairo()
if(cairosupport):
    imagelibsupport.append("cairo")
    imagelibsupport.append("cairosvg")
qahirahsupport = check_for_qahirah()
if(qahirahsupport):
    imagelibsupport.append("qahirah")
cairosvgsupport = check_for_cairosvg()
#if(cairosvgsupport):
#    imagelibsupport.append("cairosvg")
svgwritesupport = check_for_svgwrite()
if(svgwritesupport):
    imagelibsupport.append("svgwrite")
wandsupport = check_for_wand()
if(wandsupport):
    imagelibsupport.append("wand")
magicksupport = check_for_magick()
if(magicksupport):
    imagelibsupport.append("magick")
pgmagicksupport = check_for_pgmagick()
if(pgmagicksupport):
    imagelibsupport.append("pgmagick")
cv2support = check_for_cv2()
if(cv2support):
    imagelibsupport.append("cv2")
skimagesupport = check_for_skimage()
if(skimagesupport):
    imagelibsupport.append("skimage")

def list_available_image_backends():
    """
    Return a copy of the list of available and usable image backends.
    """
    return list(imagelibsupport)

defaultdraw = None
if((pilsupport or pillowsupport) and defaultdraw is None):
    defaultdraw = "pillow"
if(drawsvgsupport and defaultdraw is None):
    defaultdraw = "drawsvg"
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
if(cv2support and defaultdraw is None):
    defaultdraw = "cv2"
if(skimagesupport and defaultdraw is None):
    defaultdraw = "skimage"
if(svgwritesupport and defaultdraw is None):
    defaultdraw = "svgwrite"
if(defaultdraw is None):
    defaultdraw = "svgwrite"
