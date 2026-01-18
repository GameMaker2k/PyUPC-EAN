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

    $FileInfo: __init__.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import os
import sys
import tempfile
import atexit
import shutil

# Process-lifetime extract dir (only used when resources aren't on the filesystem)
_EXTRACT_DIR = None

def _get_extract_dir():
    global _EXTRACT_DIR
    if _EXTRACT_DIR is None:
        _EXTRACT_DIR = tempfile.mkdtemp(prefix="gm2k-sgml-")
        atexit.register(lambda: shutil.rmtree(_EXTRACT_DIR, ignore_errors=True))
    return _EXTRACT_DIR

def _atomic_write(path, data):
    tmp = path + ".tmp"
    f = open(tmp, "wb")
    try:
        f.write(data)
    finally:
        f.close()

    try:
        # Py3
        os.replace(tmp, path)
    except Exception:
        # Py2 / fallback
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        os.rename(tmp, path)

def resource_path(package_name, filename):
    """
    Return a REAL filesystem path to a resource inside this package.

    - If package is installed normally on disk: returns the existing path (no copy).
    - If package is imported from zip/egg: extracts to a temp dir once and returns that path.
    - Falls back to pkg_resources if needed.
    """
    files = None
    try:
        try:
            from importlib.resources import files as _files
            files = _files
        except Exception:
            from importlib_resources import files as _files
            files = _files
    except Exception:
        files = None

    if files is not None:
        try:
            ref = files(package_name).joinpath(filename)

            # If backed by filesystem, return that path
            try:
                return os.fspath(ref)  # Py3 only
            except Exception:
                out = os.path.join(_get_extract_dir(), filename)
                if not os.path.exists(out):
                    data = ref.read_bytes()
                    _atomic_write(out, data)
                return out
        except Exception:
            pass

    # setuptools fallback
    try:
        import pkg_resources
        return pkg_resources.resource_filename(package_name, filename)
    except Exception:
        pass

    # last resort: __file__ relative (works only when not zipped)
    mod = sys.modules.get(package_name)
    base = os.path.dirname(getattr(mod, "__file__", __file__))
    return os.path.join(base, filename)


# ---- SGML/DTD resource ----
barcodedtd = resource_path(__name__, "barcodes.dtd")
bcxmlpath = os.path.dirname(barcodedtd)
