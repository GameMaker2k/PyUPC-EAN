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

    $FileInfo: validate.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
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


'''
// Luhn Algorithm ( Luhn Formula )
// http://en.wikipedia.org/wiki/Luhn_algorithm#Implementation_of_standard_Mod_10
'''

def validate_luhn_checksum(upc, upclen, return_check=False):
    upc = str(upc)
    upclen = int(upclen)
    upclendwn = upclen - 1

    # Trim the UPC to the specified length if it's too long
    if len(upc) > upclen:
        upc = re.findall("^\\d{" + str(upclen) + "}", upc)[0]

    # If UPC length is incorrect after trimming, return False
    if len(upc) > upclen or len(upc) < upclendwn:
        return False

    # Convert UPC to a list of integers
    upc_digits = [int(digit) for digit in upc]

    # Separate into odd and even positioned sums based on length
    odd_sum = sum(upc_digits[0::2])
    even_sum = sum(upc_digits[1::2])

    # Adjust sums based on parity of upclen
    if upclen % 2 == 0:
        total_sum = (odd_sum * 3) + even_sum
    else:
        total_sum = odd_sum + (even_sum * 3)

    # Calculate checksum digit
    checksum = (10 - (total_sum % 10)) % 10

    # Validate checksum or return it based on the `return_check` flag
    if return_check:
        return str(checksum)

    # If the provided UPC length matches upclen, validate the checksum
    return checksum == upc_digits[-1] if len(upc) == upclen else str(checksum)


def get_luhn_checksum(upc, upclen):
    upc = str(upc)
    upclen = int(upclen)
    return validate_luhn_checksum(upc, upclen, True)


def fix_luhn_checksum(upc, upclen):
    upc = str(upc)
    upclen = int(upclen)
    if(len(upc) > upclen):
        fix_matches = re.findall("^(\\d{"+str(upclen)+"})", upc)
        upc = fix_matches[0]
    return upc+str(get_luhn_checksum(upc, upclen))


# Define a custom character set for mod N (e.g., alphanumeric)
# Here we use base 36 (0-9, A-Z) as an example.
CHARSET = string.digits + string.ascii_uppercase
BASE = len(CHARSET)

# Mapping character to index for quick lookup
CHAR_TO_INDEX = {ch: idx for idx, ch in enumerate(CHARSET)}

def validate_luhn_mod_n_checksum(code, length, return_check=False):
    code = str(code).upper()  # Convert to uppercase to match CHARSET
    length = int(length)
    len_minus_one = length - 1

    # Trim the code to the specified length if it's too long
    if len(code) > length:
        code = re.findall("^[" + CHARSET + "]{" + str(length) + "}", code)[0]

    # If code length is incorrect after trimming, return False
    if len(code) > length or len(code) < len_minus_one:
        return False

    # Convert code to a list of indices in CHARSET
    code_indices = [CHAR_TO_INDEX[char] for char in code]

    # Separate into odd and even positioned sums based on length
    odd_sum = sum(code_indices[0::2])
    even_sum = sum(code_indices[1::2])

    # Adjust sums based on parity of length
    if length % 2 == 0:
        total_sum = (odd_sum * 2) + even_sum
    else:
        total_sum = odd_sum + (even_sum * 2)

    # Calculate checksum index
    checksum_index = (BASE - (total_sum % BASE)) % BASE
    checksum_char = CHARSET[checksum_index]

    # Validate checksum or return it based on the `return_check` flag
    if return_check:
        return checksum_char

    # If the provided code length matches length, validate the checksum
    return checksum_char == code[-1] if len(code) == length else checksum_char


def get_luhn_mod_n_checksum(code, length):
    return validate_luhn_mod_n_checksum(code, length, True)


def fix_luhn_mod_n_checksum(code, length):
    code = str(code).upper()  # Ensure uppercase to match CHARSET
    length = int(length)

    # Trim or pad the code to be one less than the specified length
    if len(code) >= length:
        code = code[:length - 1]
    elif len(code) < length - 1:
        code = code.zfill(length - 1)

    # Calculate and append the correct checksum character
    return code + get_luhn_mod_n_checksum(code, length)



# Tables needed for Verhoeff algorithm
d_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
]

p_table = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
]

inv_table = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# https://en.wikipedia.org/wiki/Verhoeff_algorithm

def validate_verhoeff_checksum(number, length, return_check=False):
    number = str(number)
    length = int(length)

    # Trim the number to the specified length if it's too long
    if len(number) > length:
        number = re.findall("^\\d{" + str(length) + "}", number)[0]

    # If number length is incorrect after trimming, return False
    if len(number) != length:
        return False

    # Calculate Verhoeff checksum
    c = 0
    for i, digit in enumerate(reversed(number)):
        c = d_table[c][p_table[i % 8][int(digit)]]

    checksum = inv_table[c]

    if return_check:
        return str(checksum)

    # Validate checksum by checking if last digit matches
    return checksum == int(number[-1])

def get_verhoeff_checksum(number, length):
    return validate_verhoeff_checksum(number, length, True)

def fix_verhoeff_checksum(number, length):
    number = str(number)
    length = int(length)

    # Ensure number is of length-1 and get checksum to append
    if len(number) >= length:
        number = number[:length - 1]
    elif len(number) < length - 1:
        number = number.zfill(length - 1)

    return number + get_verhoeff_checksum(number, length)

# https://en.wikipedia.org/wiki/Damm_algorithm

# Damm algorithm table (quasigroup)
damm_table = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
]

def validate_damm_checksum(number, length, return_check=False):
    number = str(number)
    length = int(length)

    # Trim the number to the specified length if it's too long
    if len(number) > length:
        number = re.findall("^\\d{" + str(length) + "}", number)[0]

    # If number length is incorrect after trimming, return False
    if len(number) != length:
        return False

    # Calculate Damm checksum
    interim = 0
    for digit in number[:-1]:
        interim = damm_table[interim][int(digit)]

    checksum = damm_table[interim][int(number[-1])]

    if return_check:
        return str(interim)

    # Validate by checking if the checksum result is 0
    return checksum == 0

def get_damm_checksum(number, length):
    return validate_damm_checksum(number, length, True)

def fix_damm_checksum(number, length):
    number = str(number)
    length = int(length)

    # Ensure number is of length-1 and get checksum to append
    if len(number) >= length:
        number = number[:length - 1]
    elif len(number) < length - 1:
        number = number.zfill(length - 1)

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
    return validate_luhn_checksum(upc, 12, return_check)


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
    return validate_luhn_checksum(upc, 13, return_check)


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
    return validate_luhn_checksum(upc, 6, return_check)


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
    return validate_luhn_checksum(upc, 14, return_check)


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
    return validate_luhn_checksum(upc, 14, return_check)


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

def get_code93_alt_checksum(upc):
    # Validate input
    if len(upc) < 1 or not re.match("^[0-9A-Z\\-\\.\\$\\/\\+% ]+$", upc, re.IGNORECASE):
        return False

    # Helper function to calculate weighted sum with specified max weight
    def calculate_weighted_sum(upc_reversed, max_weight):
        return sum(((i % max_weight) + 1) * CODE93_VALUES[char] for i, char in enumerate(upc_reversed))

    # Calculate first checksum with max weight of 20
    upc_reversed = upc[::-1].upper()
    checksum1 = CODE93_ARRAY[calculate_weighted_sum(upc_reversed, 20) % 47]

    # Calculate second checksum with max weight of 15
    checksum2 = CODE93_ARRAY[calculate_weighted_sum(upc_reversed, 15) % 47]

    # Return concatenated checksums
    return checksum1 + checksum2


'''
// Code 93
// Source: http://www.barcodeisland.com/code93.phtml
// Source: http://en.wikipedia.org/wiki/Code_93
'''


def get_code93_checksum(upc):
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
