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

    $FileInfo: functions.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

import os
import sys
import logging

def VerbosePrintOut(dbgtxt, outtype="log", dbgenable=True, dgblevel=20):
    if(not dbgenable):
        return True
    log_functions = {
        "print": print,
        "log": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical,
        "exception": logging.exception,
        "logalt": lambda x: logging.log(dgblevel, x),
        "debug": logging.debug
    }
    log_function = log_functions.get(outtype)
    if(log_function):
        log_function(dbgtxt)
        return True
    return False


def VerbosePrintOutReturn(dbgtxt, outtype="log", dbgenable=True, dgblevel=20):
    VerbosePrintOut(dbgtxt, outtype, dbgenable, dgblevel)
    return dbgtxt

def RemoveWindowsPath(dpath):
    """
    Normalizes a path by converting Windows-style separators to Unix-style and stripping trailing slashes.
    """
    if dpath is None:
        dpath = ""
    if os.sep != "/":
        dpath = dpath.replace(os.path.sep, "/")
    dpath = dpath.rstrip("/")
    if dpath in [".", ".."]:
        dpath = dpath + "/"
    return dpath

def NormalizeRelativePath(inpath):
    """
    Ensures the path is relative unless it is absolute. Prepares consistent relative paths.
    """
    inpath = RemoveWindowsPath(inpath)
    if os.path.isabs(inpath):
        outpath = inpath
    else:
        if inpath.startswith("./") or inpath.startswith("../"):
            outpath = inpath
        else:
            outpath = "./" + inpath
    return outpath


def PrependPath(base_dir, child_path):
    # Check if base_dir is None or empty, if so, return child_path as is
    if not base_dir:
        return child_path
    # Ensure base_dir ends with exactly one slash
    if not base_dir.endswith('/'):
        base_dir += '/'
    # Check if child_path starts with ./ or ../ (indicating a relative path)
    if child_path.startswith('./') or child_path.startswith('../'):
        # For relative paths, we don't alter the child_path
        return base_dir + child_path
    else:
        # For non-relative paths, ensure there's no starting slash on child_path to avoid double slashes
        return base_dir + child_path.lstrip('/')

def GetTotalSize(file_list):
    """
    Calculate the total size of all files in the provided list.
    
    Parameters:
        file_list (list): List of file paths.

    Returns:
        int: Total size of all files in bytes.
    """
    total_size = 0
    for item in file_list:
        if os.path.isfile(item):  # Ensure it's a file
            try:
                total_size += os.path.getsize(item)
            except OSError:
                sys.stderr.write("Error accessing file {}: {}\n".format(item, e))
    return total_size

def create_alias_function_alt(prefix, base_name, suffix, target_function, positional_overrides=None):
    """
    Creates a new function in the global namespace that wraps 'target_function',
    allowing optional overrides of specific positional arguments via 'positional_overrides'.

    :param prefix: String prefix for the new function's name
    :param base_name: Base string to use in the new function's name
    :param suffix: String suffix for the new function's name
    :param target_function: The function to be wrapped/aliased
    :param positional_overrides: Optional dict {index: new_value} for overriding specific positional arguments
    """
    # Define a new function that wraps the target function
    def alias_function(*args, **kwargs):
        # Convert args to a list so we can modify specific positions
        args_list = list(args)

        # If there are positional overrides, apply them
        if positional_overrides:
            for index, value in positional_overrides.items():
                # Only apply if the index is within the bounds of the original arguments
                if 0 <= index < len(args_list):
                    args_list[index] = value

        # Call the target function with possibly modified arguments
        return target_function(*args_list, **kwargs)

    # Create the function name by combining the prefix, base name, and the suffix
    function_name = "{}{}{}".format(prefix, base_name, suffix)

    # Add the new function to the global namespace
    globals()[function_name] = alias_function


def create_alias_function(prefix, base_name, suffix, target_function, positional_overrides=None):
    """
    Creates a new function in the global namespace that wraps 'target_function',
    allowing optional overrides of specific positional arguments via 'positional_overrides'.

    :param prefix: String prefix for the new function's name
    :param base_name: Base string to use in the new function's name
    :param suffix: String suffix for the new function's name
    :param target_function: The function to be wrapped/aliased
    :param positional_overrides: Optional dict {index: new_value} for overriding specific positional arguments
    """
    # Define a new function that wraps the target function
    def alias_function(*args, **kwargs):
        # Convert args to a list so we can modify specific positions
        args_list = list(args)

        # If there are positional overrides, apply them
        if positional_overrides:
            for index, value in positional_overrides.items():
                if 0 <= index < len(args_list):
                    args_list[index] = value

        # Call the target function with possibly modified arguments
        return target_function(*args_list, **kwargs)

    # Create the function name by combining the prefix, base_name, and suffix
    function_name = "{}{}{}".format(prefix, base_name, suffix)

    # Add the new function to the global namespace
    globals()[function_name] = alias_function
