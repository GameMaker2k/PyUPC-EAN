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

    $FileInfo: validate.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import string

'''
// Digital Root
// Source: http://en.wikipedia.org/wiki/Digital_root
'''


def get_digital_root(number):
    number = str(number)
    while(len(str(number)) > 1):
        subnum = list(str(number))
        PreCount = 0
        number = 0
        while (PreCount <= len(subnum)-1):
            number += int(subnum[PreCount])
            PreCount += 1
    return int(number)


def digital_root(number):
    # Special case for when number is 0, as 0 % 9 would also be 0
    if number == 0:
        return 0
    else:
        return number % 9 if number % 9 != 0 else 9


# Python 2/3 compatibility helpers
try:
    text_type = unicode  # Py2
except NameError:
    text_type = str      # Py3


def _to_text(x):
    """Convert input to a text string in both Python 2 and 3."""
    if isinstance(x, text_type):
        return x
    try:
        return text_type(x)
    except Exception:
        # Last resort for odd objects
        return text_type(str(x))


def _is_all_digits(s):
    # str.isdigit() works for ASCII digits; this keeps behavior simple & explicit
    # and avoids surprises with non-ASCII digit characters.
    for ch in s:
        if ch < '0' or ch > '9':
            return False
    return True


def validate_custom_checksum(serial, serial_len, return_check=False):
    """
    Validates (or computes) the checksum of a numeric serial using the custom algorithm.

    - If return_check is True: returns the calculated checksum digit as a string.
    - Otherwise:
        * If len(serial) == serial_len: returns True/False validation.
        * If len(serial) == serial_len - 1: returns the checksum digit as a string
          (so you can append it).
        * Else: returns False.
    """
    serial = _to_text(serial)
    serial_len = int(serial_len)
    base_len = serial_len - 1

    if serial_len <= 1:
        return False

    # Trim if too long (keep first serial_len chars)
    if len(serial) > serial_len:
        serial = serial[:serial_len]

    # Length must be either base_len (no checksum yet) or serial_len (includes checksum)
    if len(serial) not in (base_len, serial_len):
        return False

    if not _is_all_digits(serial):
        return False

    digits = [ord(ch) - 48 for ch in serial]  # faster than int(ch), Py2/3-safe

    # Sums by 0-based index parity
    odd_sum = sum(digits[0::2])
    even_sum = sum(digits[1::2])

    # Weighting depends on total expected length parity
    if serial_len % 2 == 0:
        total_sum = (odd_sum * 3) + even_sum
    else:
        total_sum = odd_sum + (even_sum * 3)

    checksum = (10 - (total_sum % 10)) % 10
    checksum_str = text_type(checksum)

    if return_check:
        return checksum_str

    # If full length provided, validate last digit. Otherwise return checksum digit.
    if len(serial) == serial_len:
        return checksum == digits[-1]
    else:
        return checksum_str


def get_custom_checksum(serial, serial_len):
    """Return the checksum digit (string)."""
    return validate_custom_checksum(serial, serial_len, return_check=True)


def fix_custom_checksum(serial, serial_len):
    """
    Return the serial (trimmed to base length) with the correct checksum appended.
    """
    serial = _to_text(serial)
    serial_len = int(serial_len)
    base_len = serial_len - 1

    if serial_len <= 1:
        return False

    # Trim to base length
    if len(serial) > base_len:
        serial = serial[:base_len]

    if len(serial) != base_len or not _is_all_digits(serial):
        return False

    return serial + get_custom_checksum(serial, serial_len)


'''
// Luhn Algorithm ( Luhn Formula )
// http://en.wikipedia.org/wiki/Luhn_algorithm#Implementation_of_standard_Mod_10
'''

def _luhn_check_digit_for_body(body_digits):
    """
    Compute Luhn mod-10 check digit for a list of ints (0-9) that excludes the check digit.
    """
    total = 0
    double = True  # rightmost body digit is doubled (because check digit would be to its right)

    for d in reversed(body_digits):
        if double:
            d2 = d * 2
            if d2 > 9:
                d2 -= 9
            total += d2
        else:
            total += d
        double = not double

    return (10 - (total % 10)) % 10


def validate_luhn_checksum(number, length=None, return_check=False):
    """
    Real Luhn (mod 10).

    Args:
        number: string/int containing digits
        length: optional total length (including check digit). If provided:
                - input longer than length is trimmed to length
                - input must be length or length-1 (body) to proceed
        return_check:
            True  -> return the computed check digit (string)
            False -> if full length present, return True/False
                     if body-only present, return check digit (string)
                     else False

    Returns:
        bool or check digit string, depending on inputs and return_check.
    """
    s = _to_text(number)

    if length is not None:
        length = int(length)
        if length <= 0:
            return False
        if len(s) > length:
            s = s[:length]
        # allow either body (length-1) or full (length)
        if len(s) not in (length - 1, length):
            return False

    if not s:
        return False
    if not _is_all_ascii_digits(s):
        return False

    digits = [ord(ch) - 48 for ch in s]

    # decide body vs full
    if length is not None and len(s) == length:
        body = digits[:-1]
        provided_check = digits[-1]
    else:
        # if length not provided, treat full string as "full" only if caller wants validation?
        # We'll use: if return_check -> compute for entire string as body (common use)
        # otherwise: if len>=2, treat last digit as check digit and validate.
        if return_check:
            body = digits
            provided_check = None
        else:
            if len(digits) < 2:
                return False
            body = digits[:-1]
            provided_check = digits[-1]

    check = _luhn_check_digit_for_body(body)
    check_s = text_type(check)

    if return_check:
        return check_s

    # If we have a provided check digit, validate; otherwise return the check digit.
    if provided_check is not None:
        return check == provided_check
    else:
        return check_s


def get_luhn_checksum(number, length=None):
    """
    Return Luhn check digit as a string.

    If length is provided, number is treated as a body of length-1 (or trimmed to length-1 elsewhere).
    If length is None, the entire input is treated as the body.
    """
    s = _to_text(number)
    if length is not None:
        length = int(length)
        if len(s) >= length:
            s = s[:length - 1]
    return validate_luhn_checksum(s, length=(len(s) + 1 if length is None else length), return_check=True)


def fix_luhn_checksum(number, length=None, pad=False):
    """
    Return the number with a correct Luhn check digit appended.

    If length is provided:
      - uses first length-1 digits as body (trims if too long)
      - optionally left-pads with zeros to length-1 if pad=True

    If length is None:
      - treats the entire input as the body and appends the check digit.
    """
    s = _to_text(number)

    if length is not None:
        length = int(length)
        if length <= 1:
            return False
        body_len = length - 1

        if len(s) > body_len:
            s = s[:body_len]
        elif pad and len(s) < body_len:
            s = ('0' * (body_len - len(s))) + s

        if len(s) != body_len or not _is_all_ascii_digits(s):
            return False

        return s + validate_luhn_checksum(s, length=length, return_check=True)

    # length is None: just append to whatever digits are there
    if not s or not _is_all_ascii_digits(s):
        return False
    return s + validate_luhn_checksum(s, return_check=True)


# ----------------------------
# UPC/EAN (mod 10 with weight 3)
# ----------------------------
def validate_upc_ean_checksum(code, length, return_check=False):
    code = _to_text(code)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(code) > length:
        code = code[:length]

    if len(code) not in (base_len, length):
        return False

    if not _is_all_ascii_digits(code):
        return False

    digits = [ord(ch) - 48 for ch in code]

    odd_sum = sum(digits[0::2])
    even_sum = sum(digits[1::2])

    # parity depends on TOTAL expected length
    if length % 2 == 0:
        total = odd_sum * 3 + even_sum
    else:
        total = odd_sum + even_sum * 3

    check = (10 - (total % 10)) % 10
    check_s = text_type(check)

    if return_check:
        return check_s

    if len(code) == length:
        return check == digits[-1]
    else:
        return check_s


def get_upc_ean_checksum(code, length):
    return validate_upc_ean_checksum(code, length, True)


def fix_upc_ean_checksum(code, length):
    code = _to_text(code)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(code) > base_len:
        code = code[:base_len]

    if len(code) != base_len or not _is_all_ascii_digits(code):
        return False

    return code + get_upc_ean_checksum(code, length)


# ----------------------------
# Luhn mod N (real version)
# Charset default: 0-9A-Z (base36)
# ----------------------------
DEFAULT_CHARSET = string.digits + string.ascii_uppercase


def validate_luhn_mod_n(code, length, charset=DEFAULT_CHARSET, return_check=False):
    code = _to_text(code).upper()
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(code) > length:
        code = code[:length]

    if len(code) not in (base_len, length):
        return False

    base = len(charset)
    char_to_index = dict((ch, i) for i, ch in enumerate(charset))

    # validate chars
    for ch in code:
        if ch not in char_to_index:
            return False

    def luhn_sum(indices):
        # Luhn mod N:
        # starting from rightmost, double every second digit (in base N)
        # if doubled >= N, subtract (N-1)
        total = 0
        double = False
        for v in reversed(indices):
            if double:
                v2 = v * 2
                if v2 >= base:
                    v2 -= (base - 1)
                total += v2
            else:
                total += v
            double = not double
        return total

    indices = [char_to_index[ch] for ch in code]

    if len(code) == length:
        body = indices[:-1]
    else:
        body = indices

    total = luhn_sum(body)

    check_index = (-total) % base
    check_char = charset[check_index]

    if return_check:
        return check_char

    if len(code) == length:
        return check_char == code[-1]
    else:
        return check_char


def get_luhn_mod_n_checksum(code, length, charset=DEFAULT_CHARSET):
    return validate_luhn_mod_n(code, length, charset=charset, return_check=True)


def fix_luhn_mod_n_checksum(code, length, charset=DEFAULT_CHARSET, pad=False):
    code = _to_text(code).upper()
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(code) > base_len:
        code = code[:base_len]
    elif pad and len(code) < base_len:
        # optional left padding with first charset char (usually '0')
        code = (charset[0] * (base_len - len(code))) + code

    check = get_luhn_mod_n_checksum(code, length, charset=charset)
    if check is False:
        return False
    return code + check


# ----------------------------
# Verhoeff (correct tables)
# ----------------------------
d_table = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0]
]

p_table = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,8,0,6,4,1,5],
    [7,0,4,6,9,1,3,2,5,8],
]

inv_table = [0,4,3,2,1,5,6,7,8,9]


def validate_verhoeff(number, length, return_check=False):
    number = _to_text(number)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(number) > length:
        number = number[:length]

    if len(number) not in (base_len, length):
        return False

    if not _is_all_ascii_digits(number):
        return False

    # compute check digit for body
    body = number[:-1] if len(number) == length else number

    c = 0
    for i, ch in enumerate(reversed(body)):
        c = d_table[c][p_table[(i + 1) % 8][ord(ch) - 48]]
    check = inv_table[c]
    check_s = text_type(check)

    if return_check:
        return check_s

    if len(number) == length:
        return number[-1] == check_s
    else:
        return check_s


def get_verhoeff_checksum(number, length):
    return validate_verhoeff(number, length, True)


def fix_verhoeff(number, length, pad=True):
    number = _to_text(number)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(number) > base_len:
        number = number[:base_len]
    elif pad and len(number) < base_len:
        number = ('0' * (base_len - len(number))) + number

    if not _is_all_ascii_digits(number) or len(number) != base_len:
        return False

    return number + get_verhoeff_checksum(number, length)


# ----------------------------
# Damm (correct check digit computation)
# ----------------------------
damm_table = [
    [0,3,1,7,5,9,8,6,4,2],
    [7,0,9,2,1,5,4,8,6,3],
    [4,2,0,6,8,7,1,3,5,9],
    [1,7,5,0,9,8,3,4,2,6],
    [6,1,2,3,0,4,5,9,7,8],
    [3,6,7,4,2,0,9,5,8,1],
    [5,8,6,9,7,2,0,1,3,4],
    [8,9,4,5,3,6,2,0,1,7],
    [9,4,3,8,6,1,7,2,0,5],
    [2,5,8,1,4,3,6,7,9,0]
]


def validate_damm(number, length, return_check=False):
    number = _to_text(number)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(number) > length:
        number = number[:length]

    if len(number) not in (base_len, length):
        return False

    if not _is_all_ascii_digits(number):
        return False

    body = number[:-1] if len(number) == length else number

    interim = 0
    for ch in body:
        interim = damm_table[interim][ord(ch) - 48]

    # check digit is the digit that brings state to 0
    row = damm_table[interim]
    check = row.index(0)
    check_s = text_type(check)

    if return_check:
        return check_s

    if len(number) == length:
        # validate by processing full number should end at 0
        interim2 = 0
        for ch in number:
            interim2 = damm_table[interim2][ord(ch) - 48]
        return interim2 == 0
    else:
        return check_s


def get_damm_checksum(number, length):
    return validate_damm(number, length, True)


def fix_damm(number, length, pad=True):
    number = _to_text(number)
    length = int(length)
    base_len = length - 1

    if length <= 1:
        return False

    if len(number) > base_len:
        number = number[:base_len]
    elif pad and len(number) < base_len:
        number = ('0' * (base_len - len(number))) + number

    if not _is_all_ascii_digits(number) or len(number) != base_len:
        return False

    return number + get_damm_checksum(number, length)


def validate_upca_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 12 digits if it's too long
    if len(upc) > 12:
        upc = re.findall("^\\d{12}", upc)[0]
    
    # Check for valid length (should be 11 or 12)
    if len(upc) not in {11, 12}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate the sum of odd and even positions
    odd_sum = sum(upc_digits[0::2]) * 3
    even_sum = sum(upc_digits[1::2][:-1] if len(upc) == 12 else upc_digits[1::2])
    
    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 12 digits, verify checksum
    return checksum == upc_digits[-1] if len(upc) == 12 else str(checksum)


def get_upca_checksum(upc):
    upc = str(upc)
    return validate_upca_checksum(upc, True)


def fix_upca_checksum(upc):
    upc = str(upc)
    if(len(upc) > 11):
        fix_matches = re.findall("^(\\d{11})", upc)
        upc = fix_matches[0]
    return upc+str(get_upca_checksum(upc))


def validate_upca_alt_checksum(upc, return_check=False):
    upc = str(upc)
    return validate_upc_ean_checksum(upc, 12, return_check)


def get_upca_alt_checksum(upc):
    upc = str(upc)
    return validate_upca_alt_checksum(upc, True)


def fix_upca_alt_checksum(upc):
    upc = str(upc)
    if(len(upc) > 11):
        fix_matches = re.findall("^(\\d{11})", upc)
        upc = fix_matches[0]
    return upc+str(get_upca_alt_checksum(upc))


def validate_ean13_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 13 digits if it's too long
    if len(upc) > 13:
        upc = re.findall(r"^\d{13}", upc)[0]
    
    # Check for valid length (should be 12 or 13)
    if len(upc) not in {12, 13}:
        return False

    # Convert UPC string to a list of integers (including checksum digit if present)
    upc_digits = [int(digit) for digit in upc]
    
    # Determine whether to exclude the checksum digit in calculations
    if len(upc) == 13:
        data_digits = upc_digits[:-1]  # Exclude checksum digit
    else:
        data_digits = upc_digits

    # Calculate the sum of odd and even positions
    odd_sum = sum(data_digits[::2])
    even_sum = sum(data_digits[1::2]) * 3

    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10

    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 13 digits, verify checksum using upc_digits[-1]
    return checksum == upc_digits[-1] if len(upc) == 13 else str(checksum)


def get_ean13_checksum(upc):
    upc = str(upc)
    return validate_ean13_checksum(upc, True)


def fix_ean13_checksum(upc):
    upc = str(upc)
    if(len(upc) > 12):
        fix_matches = re.findall("^(\\d{12})", upc)
        upc = fix_matches[0]
    return upc+str(get_ean13_checksum(upc))


def validate_ean13_alt_checksum(upc, return_check=False):
    upc = str(upc)
    return validate_upc_ean_checksum(upc, 13, return_check)


def get_ean13_alt_checksum(upc):
    upc = str(upc)
    return validate_ean13_alt_checksum(upc, True)


def fix_ean13_alt_checksum(upc):
    upc = str(upc)
    if(len(upc) > 12):
        fix_matches = re.findall("^(\\d{12})", upc)
        upc = fix_matches[0]
    return upc+str(get_ean13_alt_checksum(upc))


def validate_itf6_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 6 digits if it's too long
    if len(upc) > 6:
        upc = re.findall("^\\d{6}", upc)[0]
    
    # Check for valid length (should be 5 or 6)
    if len(upc) not in {5, 6}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate the checksum digit
    total_sum = (3 * upc_digits[0] + upc_digits[1] + 3 * upc_digits[2] + 
                 upc_digits[3] + 3 * upc_digits[4])
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 6 digits, verify checksum
    return checksum == upc_digits[-1] if len(upc) == 6 else str(checksum)


def get_itf6_checksum(upc):
    upc = str(upc)
    return validate_itf6_checksum(upc, True)


def fix_itf6_checksum(upc):
    upc = str(upc)
    if(len(upc) > 5):
        fix_matches = re.findall("^(\\d{5})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf6_checksum(upc))


def validate_itf6_alt_checksum(upc, return_check=False):
    upc = str(upc)
    return validate_upc_ean_checksum(upc, 6, return_check)


def get_itf6_checksum(upc):
    upc = str(upc)
    return validate_itf6_alt_checksum(upc, True)


def fix_itf6_alt_checksum(upc):
    upc = str(upc)
    if(len(upc) > 5):
        fix_matches = re.findall("^(\\d{5})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf6_alt_checksum(upc))


def validate_itf14_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 14 digits if it's too long
    if len(upc) > 14:
        upc = re.findall("^\\d{14}", upc)[0]
    
    # Check for valid length (should be 13 or 14)
    if len(upc) not in {13, 14}:
        return False

    # Convert UPC string to a list of integers (including checksum digit if present)
    upc_digits = [int(digit) for digit in upc]
    
    # Separate data digits (exclude checksum digit if present)
    if len(upc) == 14:
        data_digits = upc_digits[:-1]  # Exclude checksum digit
    else:
        data_digits = upc_digits       # Use all digits if checksum is not present

    # Calculate the sum of odd and even positioned digits
    # For ITF-14:
    # - Odd positions (1st, 3rd, ...) are multiplied by 3
    # - Even positions (2nd, 4th, ...) are added as is
    odd_sum = sum(data_digits[::2]) * 3       # Multiply sum of digits in odd positions by 3
    even_sum = sum(data_digits[1::2])         # Sum of digits in even positions

    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10

    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 14 digits, verify checksum using upc_digits[-1]
    return checksum == upc_digits[-1] if len(upc) == 14 else str(checksum)


def get_itf14_checksum(upc):
    upc = str(upc)
    return validate_itf14_checksum(upc, True)


def fix_itf14_checksum(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf14_checksum(upc))


def validate_itf14_alt_checksum(upc, return_check=False):
    upc = str(upc)
    return validate_upc_ean_checksum(upc, 14, return_check)


def get_itf14_checksum(upc):
    upc = str(upc)
    return validate_itf14_alt_checksum(upc, True)


def fix_itf14_alt_checksum(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf14_alt_checksum(upc))


def validate_itf_checksum(upc):
    upc = str(upc)
    
    # Trim UPC to 14 digits if it's too long
    if len(upc) > 14:
        upc = re.findall("^\\d{14}", upc)[0]
    
    # Check for valid length (should be 13 or 14)
    if len(upc) not in {13, 14}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate the sum of odd and even positioned digits
    odd_sum = sum(upc_digits[0::2]) * 3
    even_sum = sum(upc_digits[1::2])
    
    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum as a string
    return str(checksum)


def get_itf_checksum(upc):
    upc = str(upc)
    return validate_itf_checksum(upc, True)


def fix_itf_checksum(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf_checksum(upc))


def validate_itf_alt_checksum(upc, return_check=False):
    upc = str(upc)
    return validate_upc_ean_checksum(upc, 14, return_check)


def get_itf_alt_checksum(upc):
    upc = str(upc)
    return validate_itf_alt_checksum(upc, True)


def fix_itf_alt_checksum(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[0]
    return upc+str(get_itf_alt_checksum(upc))


def validate_stf_checksum(upc):
    CheckSum = validate_itf_checksum(upc)
    return str(CheckSum)


def get_stf_checksum(upc):
    CheckSum = get_itf_checksum(upc)
    return str(CheckSum)


def fix_stf_checksum(upc):
    CheckSum = fix_itf_checksum(upc)
    return str(CheckSum)


def validate_ean8_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 8 digits if it's too long
    if len(upc) > 8:
        upc = re.findall("^\\d{8}", upc)[0]
    
    # Check for valid length (should be 7 or 8)
    if len(upc) not in {7, 8}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate the sum of odd and even positioned digits
    odd_sum = sum(upc_digits[0::2]) * 3
    even_sum = sum(upc_digits[1::2][:-1] if len(upc) == 8 else upc_digits[1::2])
    
    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 8 digits, verify checksum
    return checksum == upc_digits[-1] if len(upc) == 8 else str(checksum)


def get_ean8_checksum(upc):
    upc = str(upc)
    return validate_ean8_checksum(upc, True)


def fix_ean8_checksum(upc):
    upc = str(upc)
    if(len(upc) > 7):
        fix_matches = re.findall("^(\\d{7})", upc)
        upc = fix_matches[0]
    return upc+str(get_ean8_checksum(upc))


def validate_upce_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 8 digits if it's too long
    if len(upc) > 8:
        upc = re.findall("^\\d{8}", upc)[0]
    
    # Validate length and check for number system 0 or 1
    if len(upc) not in {7, 8} or not re.match("^[01]", upc):
        return False

    # Extract CheckDigit if upc is 8 digits
    check_digit = int(upc[-1]) if len(upc) == 8 else None
    upc_digits = [int(digit) for digit in upc[:7]]
    
    # Calculate OddSum and EvenSum based on last digit (upc_digits[6])
    last_digit = upc_digits[6]
    if last_digit == 0:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 3, 5]) * 3
        even_sum = upc_digits[1] + upc_digits[4]
    elif last_digit == 1:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 3, 5]) * 3
        even_sum = upc_digits[1] + 1 + upc_digits[4]
    elif last_digit == 2:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 3, 5]) * 3
        even_sum = upc_digits[1] + 2 + upc_digits[4]
    elif last_digit == 3:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 5]) * 3
        even_sum = upc_digits[1] + upc_digits[3] + upc_digits[4]
    elif last_digit == 4:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 4, 5]) * 3
        even_sum = upc_digits[1] + upc_digits[3]
    elif last_digit in {5, 6, 7, 8, 9}:
        odd_sum = sum(upc_digits[i] for i in [0, 2, 4, 6]) * 3
        even_sum = upc_digits[1] + upc_digits[3] + upc_digits[5]
    
    # Calculate CheckSum
    total_sum = odd_sum + even_sum
    calculated_checksum = (10 - (total_sum % 10)) % 10
    
    # Return the calculated checksum if requested
    if return_check:
        return str(calculated_checksum)
    
    # Validate the checksum if upc is 8 digits
    return calculated_checksum == check_digit if len(upc) == 8 else str(calculated_checksum)


def get_upce_checksum(upc):
    upc = str(upc)
    return validate_upce_checksum(upc, True)


def fix_upce_checksum(upc):
    upc = str(upc)
    if(len(upc) > 7):
        fix_matches = re.findall("^(\\d{7})", upc)
        upc = fix_matches[0]
    return upc+str(get_upce_checksum(upc))


def validate_ean2_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 2 or 3 digits if it's too long
    if len(upc) > 3:
        upc = re.findall("^\\d{3}", upc)[0]
    
    # Check for valid length (should be 2 or 3)
    if len(upc) not in {2, 3}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc[:2]]
    
    # Calculate the checksum as the first digit modulo 4
    checksum = upc_digits[0] % 4
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 3 digits, validate the checksum
    return checksum == int(upc[2]) if len(upc) == 3 else str(checksum)


def get_ean2_checksum(upc):
    upc = str(upc)
    return validate_ean2_checksum(upc, True)


def fix_ean2_checksum(upc):
    upc = str(upc)
    if(len(upc) > 2):
        fix_matches = re.findall("^(\\d{2})", upc)
        upc = fix_matches[0]
    return upc+str(get_ean2_checksum(upc))


def validate_ean5_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 6 digits if it's too long
    if len(upc) > 6:
        upc = re.findall("^\\d{6}", upc)[0]
    
    # Check for valid length (should be 5 or 6)
    if len(upc) not in {5, 6}:
        return False

    # Extract digits and calculate checksum
    upc_digits = [int(digit) for digit in upc[:5]]
    checksum = (upc_digits[0] * 3 + upc_digits[1] * 9 + 
                upc_digits[2] * 3 + upc_digits[3] * 9 + 
                upc_digits[4] * 3) % 10

    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 6 digits, validate checksum
    return checksum == int(upc[5]) if len(upc) == 6 else str(checksum)


def get_ean5_checksum(upc):
    upc = str(upc)
    return validate_ean5_checksum(upc, True)


def fix_ean5_checksum(upc):
    upc = str(upc)
    if(len(upc) > 5):
        fix_matches = re.findall("^(\\d{5})", upc)
        upc = fix_matches[0]
    return upc+str(get_ean5_checksum(upc))

def validate_usbills_checksum(serial, return_check=False):
    """
    Validates the checksum of a U.S. bill serial number.
    
    :param serial: The serial number as a string or integer.
    :param return_check: Whether to return the calculated checksum instead of validating.
    :return: True/False for validation or the checksum digit if return_check is True.
    """
    serial = str(serial)
    
    # Ensure the serial number is at least 7 digits and no more than 10
    if len(serial) < 7 or len(serial) > 10:
        return False

    # Convert the serial string to a list of integers
    serial_digits = [int(digit) for digit in re.sub(r"\D", "", serial)]
    
    # Example: Custom checksum calculation for U.S. bills
    odd_sum = sum(serial_digits[0::2])
    even_sum = sum(serial_digits[1::2])
    total_sum = odd_sum * 3 + even_sum
    checksum = (10 - (total_sum % 10)) % 10

    # Return the checksum if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum
    return checksum == serial_digits[-1] if len(serial_digits) == 10 else False


def get_usbills_checksum(serial):
    """
    Gets the checksum digit for a U.S. bill serial number.
    
    :param serial: The serial number as a string or integer.
    :return: The checksum digit as a string.
    """
    return validate_usbills_checksum(serial, True)


def fix_usbills_checksum(serial):
    """
    Fixes the checksum for a U.S. bill serial number.
    
    :param serial: The serial number as a string or integer.
    :return: The serial number with a corrected checksum digit.
    """
    serial = str(serial)
    # Trim serial number to first 9 digits if it's too long
    if len(serial) > 9:
        serial = re.findall(r"^\d{9}", serial)[0]
    
    # Add the correct checksum digit
    return serial + str(get_usbills_checksum(serial))


'''
// Get USPS Checkdigit by MACY8167
// Source: http://www.mrexcel.com/forum/excel-questions/530675-usps-mod-10-check-digit.html
'''


def validate_usps_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 22 digits if it's too long
    if len(upc) > 22:
        upc = re.findall("^\\d{22}", upc)[0]
    
    # Check for valid length (should be 21 or 22)
    if len(upc) not in {21, 22}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate OddSum and EvenSum
    odd_sum = sum(upc_digits[0::2]) * 3
    even_sum = sum(upc_digits[1::2][:-1] if len(upc) == 22 else upc_digits[1::2])
    
    # Calculate the checksum digit
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # If UPC is 22 digits, validate checksum
    return checksum == upc_digits[-1] if len(upc) == 22 else str(checksum)


def get_usps_checksum(upc):
    upc = str(upc)
    return validate_usps_checksum(upc, True)


def fix_usps_checksum(upc):
    upc = str(upc)
    if(len(upc) > 21):
        fix_matches = re.findall("^(\\d{21})", upc)
        upc = fix_matches[0]
    return upc+str(get_usps_checksum(upc))


'''
// Get UPS Checkdigit and Info by stebo0728 and HolidayBows
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit?msg=2961884#xx2961884xx
'''


def validate_ups_checksum(upc, return_check=False):
    upc = str(upc).upper()
    
    # Check for "1Z" prefix and extract remaining 16 characters if present
    if not upc.startswith("1Z"):
        return False
    upc = upc[2:]
    
    # Trim UPC to 16 characters if too long
    if len(upc) > 16:
        upc = re.findall("^\\w{16}", upc)[0]
    
    # Check valid length (should be 15 or 16 after prefix removal)
    if len(upc) not in {15, 16}:
        return False

    # Calculate OddSum and EvenSum based on character positions
    odd_sum = sum((int(ch) if ch.isdigit() else (ord(ch) - 63) % 10) for ch in upc[::2])
    even_sum = sum((int(ch) * 2 if ch.isdigit() else ((ord(ch) - 63) % 10) * 2) for ch in upc[1::2][:7])

    # Calculate CheckSum
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum if UPC length is 16
    return checksum == int(upc[-1]) if len(upc) == 16 else str(checksum)


def get_ups_checksum(upc):
    upc = str(upc)
    return validate_ups_checksum(upc, True)


def fix_ups_checksum(upc):
    upc = str(upc)
    if(len(upc) > 17):
        fix_matches = re.findall("^(\\w{17})", upc)
        upc = fix_matches[0]
    return upc+str(get_ups_checksum(upc))


'''
// Get FEDEX Checkdigit by jbf777-ga
// Source: http://answers.google.com/answers/threadview/id/207899.html
'''


def validate_fedex_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 12 digits if it's too long
    if len(upc) > 12:
        upc = re.findall("^\\d{12}", upc)[0]
    
    # Check valid length (should be 11 or 12)
    if len(upc) not in {11, 12}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate OddSum and EvenSum using specific weight pattern
    odd_sum = sum(upc_digits[i] * weight for i, weight in zip(range(0, 11, 2), [3, 7, 1, 3, 7, 1]))
    even_sum = sum(upc_digits[i] * weight for i, weight in zip(range(1, 10, 2), [1, 3, 7, 1, 3]))
    
    # Calculate the checksum digit using modulo 11
    total_sum = odd_sum + even_sum
    checksum = total_sum % 11
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum if UPC length is 12
    return checksum == upc_digits[-1] if len(upc) == 12 else str(checksum)


def get_fedex_checksum(upc):
    upc = str(upc)
    return validate_fedex_checksum(upc, True)


def fix_fedex_checksum(upc):
    upc = str(upc)
    if(len(upc) > 11):
        fix_matches = re.findall("^(\\d{11})", upc)
        upc = fix_matches[0]
    return upc+str(get_fedex_checksum(upc))


'''
// IMEI (International Mobile Station Equipment Identity)
// Source: http://en.wikipedia.org/wiki/IMEI#Check_digit_computation
'''


def validate_imei_checksum(upc, return_check=False):
    upc = str(upc)
    
    # Trim UPC to 15 digits if it's too long
    if len(upc) > 15:
        upc = re.findall("^\\d{15}", upc)[0]
    
    # Check valid length (should be 14 or 15)
    if len(upc) not in {14, 15}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate UPC sum for Luhn algorithm with alternating digit root calculation
    total_sum = sum(upc_digits[i] if i % 2 == 0 else get_digital_root(upc_digits[i] * 2) for i in range(14))
    
    # Calculate the checksum digit to make the total sum a multiple of 10
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum if UPC length is 15
    return checksum == upc_digits[-1] if len(upc) == 15 else str(checksum)


def get_imei_checksum(upc):
    upc = str(upc)
    return validate_imei_checksum(upc, True)


def fix_imei_checksum(upc):
    upc = str(upc)
    if(len(upc) > 14):
        fix_matches = re.findall("^(\\d{14})", upc)
        upc = fix_matches[0]
    return upc+str(get_imei_checksum(upc))


'''
// Bank Card Numbers
// Source: http://tywkiwdbi.blogspot.com/2012/06/checksum-number-on-credit-card.html
// Source: http://en.wikipedia.org/wiki/Luhn_algorithm#Implementation_of_standard_Mod_10
'''



def validate_bcn_checksum(upc, return_check=False):
    # Remove hyphens and spaces
    upc = re.sub("[-\\s]", "", str(upc))
    
    # Trim UPC to 16 digits if it's too long
    if len(upc) > 16:
        upc = re.findall(r"^\\d{16}", upc)[0]
    
    # Check valid length (should be 15 or 16)
    if len(upc) not in {15, 16}:
        return False

    # Convert UPC string to a list of integers
    upc_digits = [int(digit) for digit in upc]
    
    # Calculate UPC sum with alternating digital root for Luhn algorithm
    total_sum = sum(get_digital_root(upc_digits[i] * 2) if i % 2 == 0 else upc_digits[i] for i in range(15))
    
    # Calculate the checksum digit to make the total sum a multiple of 10
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum if UPC length is 16
    return checksum == upc_digits[-1] if len(upc) == 16 else str(checksum)


def get_bcn_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    return validate_bcn_checksum(upc, True)


def fix_bcn_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(len(upc) > 15):
        fix_matches = re.findall("^(\\d{15})", upc)
        upc = fix_matches[0]
    return upc+str(get_bcn_checksum(upc))


'''
// Code 11
// Source: http://www.barcodeisland.com/code11.phtml
// Source: http://en.wikipedia.org/wiki/Code_11
'''


def get_code11_alt_checksum(upc):
    # Validate input
    if len(upc) < 1 or not re.match("^[0-9\\-]+$", upc):
        return False

    # Code11 mapping for values and characters
    code11_array = {str(i): i for i in range(10)}
    code11_array["-"] = 10

    def calculate_weighted_sum(upc_reversed, max_weight):
        """Calculate the weighted sum with a max weight limit."""
        return sum(((i % max_weight) + 1) * code11_array[char] for i, char in enumerate(upc_reversed))

    # First checksum calculation with max weight of 10
    upc_reversed = upc[::-1]
    checksum1 = list(code11_array.keys())[calculate_weighted_sum(upc_reversed, 10) % 11]

    # Second checksum calculation with max weight of 9
    checksum2 = list(code11_array.keys())[calculate_weighted_sum(upc_reversed, 9) % 11]

    # Return concatenated checksums
    return checksum1 + checksum2


'''
// Code 11
// Source: http://www.barcodeisland.com/code11.phtml
// Source: http://en.wikipedia.org/wiki/Code_11
'''


def get_code11_checksum(upc):
    # Validate input
    if len(upc) < 1 or not re.match("^[0-9\\-]+$", upc):
        return False

    # Code11 mapping for values and characters
    code11_array = {str(i): i for i in range(10)}
    code11_array["-"] = 10

    # Reverse the UPC and calculate the weighted sum
    upc_reversed = upc[::-1]
    upc_sum = sum((i % 10 + 1) * code11_array[char] for i, char in enumerate(upc_reversed))

    # Calculate and return the checksum
    checksum = list(code11_array.keys())[upc_sum % 11]
    return str(checksum)


'''
// Code 39
// Source: http://www.barcodeisland.com/code39.phtml
// Source: http://en.wikipedia.org/wiki/Code_39
'''


# Mapping for Code39 characters
CODE39_VALUES = {str(i): i for i in range(10)}
CODE39_VALUES.update({chr(65 + i): 10 + i for i in range(26)})  # A-Z
CODE39_VALUES.update({"-": 36, ".": 37, " ": 38, "$": 39, "/": 40, "+": 41, "%": 42})
CODE39_ARRAY = {v: k for k, v in CODE39_VALUES.items()}

def calculate_code39_checksum(upc, mod_value):
    # Validate input
    if len(upc) < 1 or not re.match("^[0-9A-Z\\-.\\$\\/\\+% ]+$", upc, re.IGNORECASE):
        return False

    # Calculate checksum based on mod_value
    upc_sum = sum(CODE39_VALUES[char] for char in upc.upper())
    checksum = CODE39_ARRAY[upc_sum % mod_value]
    return checksum

def get_code39_checksum_mod10(upc):
    return calculate_code39_checksum(upc, 10)

def get_code39_checksum_mod43(upc):
    return calculate_code39_checksum(upc, 43)

def get_code39_checksum(upc, getmod="43"):
    # Determine modulus based on getmod argument
    mod_value = 10 if getmod == "10" else 43
    return calculate_code39_checksum(upc, mod_value)


'''
// Code 93
// Source: http://www.barcodeisland.com/code93.phtml
// Source: http://en.wikipedia.org/wiki/Code_93
'''

# Mapping for Code93 characters and values
CODE93_VALUES = {str(i): i for i in range(10)}
CODE93_VALUES.update({chr(65 + i): 10 + i for i in range(26)})  # A-Z
CODE93_VALUES.update({"-": 36, ".": 37, " ": 38, "$": 39, "/": 40, "+": 41, "%": 42, "($)": 43, "(%)": 44, "(/)": 45, "(+)": 46})
CODE93_ARRAY = {v: k for k, v in CODE93_VALUES.items()}

def get_code93_checksum(upc):
    import re
    # Validate input
    if len(upc) < 1 or not re.match("^[0-9A-Z\\-\\.\\$\\/\\+% ]+$", upc, re.IGNORECASE):
        return False

    # Helper function to calculate weighted sum with specified max weight
    def calculate_weighted_sum(upc_reversed, max_weight):
        return sum(((i % max_weight) + 1) * CODE93_VALUES[char] for i, char in enumerate(upc_reversed))

    # Calculate first checksum with max weight of 20
    upc_reversed = upc[::-1].upper()
    checksum1_value = calculate_weighted_sum(upc_reversed, 20) % 47
    checksum1 = CODE93_ARRAY[checksum1_value]

    # Append the first checksum to the reversed input for the second calculation
    upc_with_checksum1 = checksum1 + upc_reversed

    # Calculate second checksum with max weight of 15
    checksum2_value = calculate_weighted_sum(upc_with_checksum1, 15) % 47
    checksum2 = CODE93_ARRAY[checksum2_value]

    # Return concatenated checksums
    return checksum1 + checksum2

def get_code93extended_checksum(upc):
    # Validate input
    pattern = "^[0-9A-Z\\-\\.\\$\\/\\+\\%]+|(\\(\\$\\)|\\(\\%\\)|\\(\\+\\)|\\(\\/\\))+$"
    if len(upc) < 1 or not re.match(pattern, upc, re.IGNORECASE):
        return False

    # Normalize the input to uppercase
    upc = upc.upper()

    # Parse sequences like ($), (%) into single characters for computation
    extended_map = {"($)": "$", "(%)": "%", "(+)": "+", "(/)": "/"}
    for key, value in extended_map.items():
        upc = upc.replace(key, value)

    # Helper function to calculate weighted sum with specified max weight
    def calculate_weighted_sum(upc_reversed, max_weight):
        return sum(((i % max_weight) + 1) * CODE93_VALUES[char] for i, char in enumerate(upc_reversed))

    # Calculate first checksum with max weight of 20
    upc_reversed = upc[::-1]
    checksum1_value = calculate_weighted_sum(upc_reversed, 20) % 47
    checksum1 = CODE93_ARRAY[checksum1_value]

    # Append the first checksum to the reversed input for the second calculation
    upc_with_checksum1 = checksum1 + upc_reversed

    # Calculate second checksum with max weight of 15
    checksum2_value = calculate_weighted_sum(upc_with_checksum1, 15) % 47
    checksum2 = CODE93_ARRAY[checksum2_value]

    # Return concatenated checksums
    return checksum1 + checksum2

'''
// Code 93
// Source: http://www.barcodeisland.com/code93.phtml
// Source: http://en.wikipedia.org/wiki/Code_93
'''


def get_code93_alt_checksum(upc):
    # Validate input
    if len(upc) < 1 or not re.match(r"^[0-9A-Z\\-\\.\\$\\/\\+% ]+$", upc, re.IGNORECASE):
        return False

    # Calculate the weighted sum with a maximum weight of 20
    upc_reversed = upc[::-1].upper()
    total_sum = sum(((i % 20) + 1) * CODE93_VALUES[char] for i, char in enumerate(upc_reversed))
    
    # Calculate the checksum character based on modulus 47
    checksum = CODE93_ARRAY[total_sum % 47]
    return checksum


'''
// Code 128
// Source: http://www.barcodeisland.com/code128.phtml
// Source: http://en.wikipedia.org/wiki/Code_128
'''


def get_code128_checksum(upc):
    # Validate input: hexadecimal string with even length and at least 6 characters
    if len(upc) < 6 or len(upc) % 2 != 0 or not re.match("^[0-9a-f]+$", upc, re.IGNORECASE):
        return False
    
    # Convert to lowercase and split into two-character hexadecimal parts
    upc_matches = re.findall("[0-9a-f]{2}", upc.lower())
    upc_to_dec = [int(x, 16) for x in upc_matches]
    
    # Calculate checksum with weighted sum
    checksum = upc_to_dec[0] if 102 < upc_to_dec[0] < 106 else 0
    for i, val in enumerate(upc_to_dec[1:], start=1):
        if not (i == len(upc_to_dec) - 1 and 105 < val < 108):  # Ignore last character if special code
            checksum += val * i

    # Return checksum as 2-digit hexadecimal string
    return format(checksum % 103, '02x')

def get_code128alt_checksum(upc):
    # Convert ASCII to hexadecimal and calculate checksum
    hex_upc = convert_ascii_code128_to_hex_code128(str(upc))
    return get_code128_checksum(hex_upc)

def get_code128dec_checksum(upc):
    # Validate input for decimal Code128 representation
    if len(upc) < 12 or not re.match("^\\d{3}+$", upc):
        return False
    
    # Convert each 3-digit decimal segment to 2-digit hexadecimal
    upc_hex = ''.join(format(int(upc[i:i+3]), '02x') for i in range(0, len(upc), 3))
    return get_code128_checksum(upc_hex)


'''
// MSI (Modified Plessey)
// Source: http://www.barcodeisland.com/msi.phtml
// Source: http://en.wikipedia.org/wiki/MSI_Barcode
'''


def get_msi_checksum_mod10(upc):
    upc_digits = [int(digit) for digit in str(upc)]
    
    # Split digits into odd and even indexed lists based on length
    odd_index_digits = upc_digits[1::2] if len(upc_digits) % 2 == 0 else upc_digits[::2]
    even_index_digits = upc_digits[::2] if len(upc_digits) % 2 == 0 else upc_digits[1::2]
    
    # Double odd indexed digits, split and sum
    odd_sum = sum(int(digit) for digit in ''.join(str(int(num) * 2) for num in odd_index_digits))
    even_sum = sum(even_index_digits)
    
    # Calculate and return the checksum
    total_sum = odd_sum + even_sum
    checksum = (10 - (total_sum % 10)) % 10
    return str(checksum)

def get_msi_checksum_mod11(upc, modtype="ibm"):
    # Set weight sequence based on modtype
    weights = (2, 3, 4, 5, 6, 7, 8, 9) if modtype.lower() == "ncr" else (2, 3, 4, 5, 6, 7)
    
    # Reverse UPC and calculate weighted sum
    upc_reversed = list(map(int, str(upc)[::-1]))
    weighted_sum = sum(num * weights[i % len(weights)] for i, num in enumerate(upc_reversed))
    
    # Calculate and return the checksum
    checksum = (11 - (weighted_sum % 11)) % 11
    return str(checksum)

def get_msi_checksum_mod1010(upc):
    # Apply mod 10 twice
    return get_msi_checksum_mod10(get_msi_checksum_mod10(upc))

def get_msi_checksum_mod1110(upc, modtype="ibm"):
    # Apply mod 11 then mod 10
    return get_msi_checksum_mod10(get_msi_checksum_mod11(upc, modtype))

def get_msi_checksum(upc, getmod="10", modtype="ibm"):
    # Select appropriate checksum calculation based on getmod value
    getmod = str(getmod)
    if getmod == "10":
        return get_msi_checksum_mod10(upc)
    elif getmod == "11":
        return get_msi_checksum_mod11(upc, modtype)
    elif getmod == "1010":
        return get_msi_checksum_mod1010(upc)
    elif getmod == "1110":
        return get_msi_checksum_mod1110(upc, modtype)
    return False


'''
// ISSN (International Standard Serial Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Serial_Number
'''


def validate_issn8_checksum(upc, return_check=False):
    # Remove hyphens and spaces
    upc = re.sub("[-\\s]", "", str(upc))
    
    # Validate length
    if len(upc) not in {7, 8}:
        return False

    # Convert ISSN to a list of integers
    upc_digits = [int(digit) for digit in upc[:7]]
    
    # Calculate weighted sum based on ISSN-8 rules
    total_sum = sum(upc_digits[i] * (8 - i) for i in range(7))
    
    # Calculate the checksum digit
    checksum = (11 - (total_sum % 11)) % 11
    
    # Return the checksum digit if requested
    if return_check:
        return str(checksum)

    # If ISSN is 8 digits, validate checksum
    return checksum == int(upc[7]) if len(upc) == 8 else str(checksum)


def get_issn8_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    return validate_issn8_checksum(upc, True)


def fix_issn8_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(len(upc) > 7):
        fix_matches = re.findall("^(\\d{7})", upc)
        upc = fix_matches[0]
    return upc+str(get_issn8_checksum(upc))


def validate_issn13_checksum(upc, return_check=False):
    upc = str(upc)
    if(not re.findall("^977(\\d{9})", upc)):
        return False
    if(re.findall("^977(\\d{9})", upc)):
        return validate_ean13_checksum(upc, return_check)


def get_issn13_checksum(upc):
    upc = str(upc)
    return validate_issn13_checksum(upc, True)


def fix_issn13_checksum(upc):
    upc = str(upc)
    if(not re.findall("^977(\\d{9})", upc)):
        return False
    if(re.findall("^977(\\d{9})", upc)):
        return fix_ean13_checksum(upc)


'''
// ISBN (International Standard Book Number)
// Source: http://en.wikipedia.org/wiki/ISBN
'''


def validate_isbn10_checksum(upc, return_check=False):
    # Remove hyphens and spaces
    upc = re.sub("[-\\s]", "", str(upc))
    
    # Validate length
    if len(upc) not in {9, 10}:
        return False

    # Calculate weighted sum for the first 9 digits
    upc_digits = [int(digit) for digit in upc[:9]]
    total_sum = sum(upc_digits[i] * (10 - i) for i in range(9))
    
    # Calculate checksum
    checksum = (11 - (total_sum % 11)) % 11
    checksum_char = "X" if checksum == 10 else str(checksum)
    
    # Return the checksum if requested
    if return_check:
        return checksum_char

    # If ISBN is 10 digits, validate checksum
    return checksum_char == upc[-1] if len(upc) == 10 else checksum_char


def get_isbn10_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    return validate_isbn10_checksum(upc, True)


def fix_isbn10_checksum(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(len(upc) > 9):
        fix_matches = re.findall("^(\\d{9})", upc)
        upc = fix_matches[1]
    return upc+str(get_isbn10_checksum(upc))


def validate_isbn13_checksum(upc, return_check=False):
    upc = str(upc)
    if(not re.findall("^(97[8-9])(\\d{9})", upc)):
        return False
    if(re.findall("^(97[8-9])(\\d{9})", upc)):
        return validate_ean13_checksum(upc, return_check)


def get_isbn13_checksum(upc):
    upc = str(upc)
    return validate_isbn13_checksum(upc, True)


def fix_isbn13_checksum(upc):
    upc = str(upc)
    if(not re.findall("^(97[8-9])(\\d{9})", upc)):
        return False
    if(re.findall("^(97[8-9])(\\d{9})", upc)):
        return fix_ean13_checksum(upc)


'''
// ISMN (International Standard Music Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Music_Number
// Source: http://www.ismn-international.org/whatis.html
// Source: http://www.ismn-international.org/manual_1998/chapter2.html
'''


def validate_ismn10_checksum(upc, return_check=False):
    # Remove "M" prefix, hyphens, and spaces
    upc = re.sub("[M-\\s]", "", str(upc))
    
    # Validate length (should be 8 or 9 digits after cleaning)
    if len(upc) not in {8, 9}:
        return False

    # Convert ISMN to a list of integers
    upc_digits = [int(digit) for digit in upc[:8]]
    
    # Calculate weighted sum with alternating weights 1 and 3, starting with 3 for 'M'
    total_sum = 3 + sum(upc_digits[i] * (3 if i % 2 == 1 else 1) for i in range(8))
    
    # Calculate checksum
    checksum = (10 - (total_sum % 10)) % 10
    
    # Return the checksum if requested
    if return_check:
        return str(checksum)

    # If ISMN is 9 digits, validate checksum
    return checksum == int(upc[8]) if len(upc) == 9 else str(checksum)


def get_ismn10_checksum(upc):
    upc = str(upc)
    upc = upc.replace("M", "")
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    return validate_ismn10_checksum(upc, True)


def fix_ismn10_checksum(upc):
    upc = str(upc)
    upc = upc.replace("M", "")
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(len(upc) > 9):
        fix_matches = re.findall("^(\\d{9})", upc)
        upc = fix_matches[1]
    return upc+str(get_ismn10_checksum(upc))


def validate_ismn13_checksum(upc, return_check=False):
    upc = str(upc)
    if(not re.findall("^9790(\\d{8})", upc)):
        return False
    if(re.findall("^9790(\\d{8})", upc)):
        return validate_ean13_checksum(upc, return_check)


def get_ismn13_checksum(upc):
    upc = str(upc)
    return validate_ismn13_checksum(upc, True)


def fix_ismn13_checksum(upc):
    upc = str(upc)
    if(not re.findall("^9790(\\d{8})", upc)):
        return False
    if(re.findall("^9790(\\d{8})", upc)):
        return fix_ean13_checksum(upc)


'''
// Get variable weight price checksum
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
// Source: http://barcodes.gs1us.org/GS1%20US%20BarCodes%20and%20eCom%20-%20The%20Global%20Language%20of%20Business.htm
'''


# Predefined number replacement tables
NUM_REP1 = [0, 2, 4, 6, 8, 9, 1, 3, 5, 7]
NUM_REP2 = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
NUM_REP3 = [0, 5, 9, 4, 8, 3, 7, 2, 6, 1]

def validate_vw_price_checksum(price, return_check=False):
    # Zero-pad the price to ensure it is at least 4 digits
    price = price.zfill(4)
    
    # Validate and extract 4 or 5 digits
    if len(price) > 5:
        price = re.match("^\\d{5}", price).group(0)
    elif len(price) not in {4, 5}:
        return False
    
    # Convert to list of integers
    price_digits = [int(digit) for digit in price]

    # Calculate the checksum using predefined tables
    if len(price) == 4:
        price_digits[0] = NUM_REP1[price_digits[0]]
        price_digits[1] = NUM_REP1[price_digits[1]]
        price_digits[2] = NUM_REP2[price_digits[2]]
        price_digits[3] = NUM_REP3[price_digits[3]]
        price_sum = sum(price_digits) * 3
    elif len(price) == 5:
        price_digits[1] = NUM_REP1[price_digits[1]]
        price_digits[2] = NUM_REP1[price_digits[2]]
        price_digits[3] = NUM_REP2[price_digits[3]]
        price_digits[4] = NUM_REP3[price_digits[4]]
        price_sum = sum(price_digits[1:]) * 3

    # Calculate the checksum digit
    checksum = price_sum % 10
    
    # Return the checksum if requested
    if return_check:
        return str(checksum)
    
    # Validate checksum for a 5-digit price
    return checksum == price_digits[0] if len(price) == 5 else str(checksum)

def get_vw_price_checksum(price):
    # Calculate the checksum for a given price
    return validate_vw_price_checksum(price.zfill(4), return_check=True)

def fix_vw_price_checksum(price):
    # Zero-pad and validate the price length
    price = price.zfill(4)
    if len(price) > 4:
        price = re.match("^\\d{4}", price).group(0)
    # Return the correct price with checksum prepended
    return str(get_vw_price_checksum(price)) + price

# Define a list of allowed prefixes for varying weight codes
VARYING_WEIGHT_PREFIXES = ["02"] + ["2{}".format(i) for i in range(1, 10)]

def validate_ean13_varying_weight_checksum(ean_code, return_check=False):
    # Remove any non-digit characters
    ean_code = re.sub("\\D", "", str(ean_code))
    
    # Check if the length is 13 and starts with a valid varying weight prefix
    if len(ean_code) != 13 or ean_code[:2] not in VARYING_WEIGHT_PREFIXES:
        return False

    # Convert code to a list of integers
    digits = [int(d) for d in ean_code[:12]]  # Exclude the checksum digit for calculation
    
    # Calculate the weighted sum for checksum (odd positions * 1, even positions * 3)
    total_sum = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits))
    checksum = (10 - (total_sum % 10)) % 10  # Calculate checksum digit
    
    # Return the checksum if requested
    if return_check:
        return str(checksum)
    
    # Validate the checksum digit
    return checksum == int(ean_code[-1])

def get_ean13_varying_weight_checksum(ean_code):
    # Returns the calculated checksum for an EAN-13 code with varying weight prefix
    return validate_ean13_varying_weight_checksum(ean_code, return_check=True)

def fix_ean13_varying_weight_checksum(ean_code):
    # Remove non-digit characters and ensure it is a 12-digit code
    ean_code = re.sub("\\D", "", str(ean_code)).zfill(12)
    
    # Return the complete code with the correct checksum appended
    return ean_code + get_ean13_varying_weight_checksum(ean_code)
