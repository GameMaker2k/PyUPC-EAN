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

    $FileInfo: convert.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import upcean.validate


def make_barcode_by_type(bctype, numbersystem=None, manufacturer=None, product=None):
    bctype = bctype.lower()
    
    # Define lengths and specific checksum rules per barcode type
    barcode_specs = {
        "upca": {"ns_len": 1, "man_len": 5, "prod_len": 5, "upclen": 12, "checksum_func": upcean.validate.validate_luhn_checksum},
        "upce": {"ns_len": 1, "man_len": 2, "prod_len": 3, "upclen": 8, "checksum_func": upcean.validate.validate_luhn_checksum},
        "ean8": {"ns_len": 2, "man_len": 0, "prod_len": 5, "upclen": 8, "checksum_func": upcean.validate.validate_luhn_checksum},
        "ean13": {"ns_len": 1, "man_len": 5, "prod_len": 5, "upclen": 13, "checksum_func": upcean.validate.validate_luhn_checksum},
        "itf6": {"ns_len": 0, "man_len": 0, "prod_len": 5, "upclen": 6, "checksum_func": upcean.validate.validate_luhn_checksum},
        "itf14": {"ns_len": 1, "man_len": 5, "prod_len": 6, "upclen": 14, "checksum_func": upcean.validate.validate_luhn_checksum}
    }
    
    # Check if the specified barcode type is valid
    if bctype not in barcode_specs:
        return False
    
    # Retrieve the barcode specification for the given type
    spec = barcode_specs[bctype]
    
    # Format each part of the barcode to the required length, padding with zeros if necessary
    ns_len, man_len, prod_len, upclen = spec["ns_len"], spec["man_len"], spec["prod_len"], spec["upclen"]
    numbersystem = re.match("\\d{{{}}}".format(ns_len), str(numbersystem).zfill(ns_len)).group(0) if ns_len > 0 else ""
    manufacturer = re.match("\\d{{{}}}".format(man_len), str(manufacturer).zfill(man_len)).group(0) if man_len > 0 else ""
    product = re.match("\\d{{{}}}".format(prod_len), str(product).zfill(prod_len)).group(0)
    
    # Concatenate to form the partial barcode without the checksum
    upc = numbersystem + manufacturer + product
    
    # Calculate and append the checksum using the specified function
    checksum = spec["checksum_func"](upc, upclen, return_check=True)
    return upc + str(checksum)

def make_upca_barcode(numbersystem, manufacturer, product):
    # Ensure inputs are strings and properly padded/truncated
    numbersystem = re.match("\\d{1}", str(numbersystem).zfill(1)).group(0)
    manufacturer = re.match("\\d{5}", str(manufacturer).zfill(5)).group(0)
    product = re.match("\\d{5}", str(product).zfill(5)).group(0)
    
    # Concatenate to form the UPC without the checksum
    upc = numbersystem + manufacturer + product
    
    # Append the checksum
    checksum = upcean.validate.validate_upca_checksum(upc, True)
    return upc + str(checksum)

def make_ean13_barcode(numbersystem, manufacturer, product):
    numbersystem = re.match("\\d{2}", str(numbersystem).zfill(2)).group(0)
    manufacturer = re.match("\\d{5}", str(manufacturer).zfill(5)).group(0)
    product = re.match("\\d{5}", str(product).zfill(5)).group(0)
    
    # Concatenate and calculate checksum
    upc = numbersystem + manufacturer + product
    checksum = upcean.validate.validate_ean13_checksum(upc, True)
    return upc + str(checksum)

def make_itf14_barcode(numbersystem, manufacturer, product):
    numbersystem = re.match("\\d{3}", str(numbersystem).zfill(3)).group(0)
    manufacturer = re.match("\\d{5}", str(manufacturer).zfill(5)).group(0)
    product = re.match("\\d{5}", str(product).zfill(5)).group(0)
    
    # Concatenate and calculate checksum
    upc = numbersystem + manufacturer + product
    checksum = upcean.validate.validate_itf14_checksum(upc, True)
    return upc + str(checksum)

def make_ean8_barcode(numbersystem, manufacturer, product):
    numbersystem = re.match("\\d{1}", str(numbersystem).zfill(1)).group(0)
    manufacturer = re.match("\\d{3}", str(manufacturer).zfill(3)).group(0)
    product = re.match("\\d{3}", str(product).zfill(3)).group(0)
    
    # Concatenate and calculate checksum
    upc = numbersystem + manufacturer + product
    checksum = upcean.validate.validate_ean8_checksum(upc, True)
    return upc + str(checksum)

def make_upce_barcode(numbersystem, manufacturer, product):
    numbersystem = re.match("\\d{1}", str(numbersystem).zfill(1)).group(0)
    manufacturer = re.match("\\d{3}", str(manufacturer).zfill(3)).group(0)
    product = re.match("\\d{3}", str(product).zfill(3)).group(0)
    
    # Concatenate and calculate checksum
    upc = numbersystem + manufacturer + product
    checksum = upcean.validate.validate_upce_checksum(upc, True)
    return upc + str(checksum)


def convert_barcode_from_upce_to_upca(upc):
    upc = str(upc).zfill(8)  # Zero-pad to 8 digits if needed
    if len(upc) != 8 or not re.match(r"^[01]", upc):
        return False
    if not upcean.validate.validate_upce_checksum(upc):
        return False
    
    upc_matches = re.match("(0|1)(\\d{1})(\\d{1})(\\d{1})(\\d{1})(\\d{1})(\\d)(\\d)", upc).groups()
    base = upc_matches[0] + upc_matches[1] + upc_matches[2]
    
    if upc_matches[6] in "012":
        upca = "{}0000{}{}".format(base, upc_matches[3], upc_matches[4])
    elif upc_matches[6] == "3":
        upca = "{}00000{}".format(base, upc_matches[4])
    else:
        upca = "{}0000{}".format(upc_matches[0] + upc_matches[1] + upc_matches[2] + upc_matches[3] + upc_matches[4], upc_matches[6])
    
    return upca + upc_matches[7]

def convert_barcode_from_upca_to_ean13(upc):
    upc = str(upc).zfill(12)
    if len(upc) not in {12, 13} or not upcean.validate.validate_upca_checksum(upc):
        return False
    return "0" + upc if len(upc) == 12 else upc

def convert_barcode_from_ean13_to_itf14(upc):
    upc = str(upc).zfill(13)
    if len(upc) not in {13, 14} or not upcean.validate.validate_ean13_checksum(upc):
        return False
    return "0" + upc if len(upc) == 13 else upc

def convert_barcode_from_upce_to_ean13(upc):
    return convert_barcode_from_upca_to_ean13(convert_barcode_from_upce_to_upca(upc))

def convert_barcode_from_upce_to_itf14(upc):
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upce_to_ean13(upc))

def convert_barcode_from_upca_to_itf14(upc):
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upca_to_ean13(upc))

def convert_barcode_from_ean13_to_upca(upc):
    upc = str(upc).zfill(13)
    if len(upc) != 13 or not upcean.validate.validate_ean13_checksum(upc):
        return False
    match = re.match(r"^0(\d{12})$", upc)
    return match.group(1) if match else False

def convert_barcode_from_itf14_to_ean13(upc):
    upc = str(upc).zfill(14)
    if len(upc) != 14 or not upcean.validate.validate_itf14_checksum(upc):
        return False
    return upc[1:-1] + str(upcean.validate.validate_ean13_checksum(upc[1:-1], True))

def convert_barcode_from_upca_to_upce(upc):
    upc = str(upc).zfill(12)
    if len(upc) != 12 or not upcean.validate.validate_upca_checksum(upc):
        return False

    patterns = [
        ("(0|1)(\\d{2})00000(\\d{3})(\\d{1})", "{}{}{}0{}"),
        ("(0|1)(\\d{3})00000(\\d{2})(\\d{1})", "{}{}{}3{}"),
        ("(0|1)(\\d{4})00000(\\d{1})(\\d{1})", "{}{}{}4{}"),
        ("(0|1)(\\d{5})00005(\\d{1})", "{}{}5{}"),
    ]
    
    for pattern, fmt in patterns:
        match = re.match(pattern, upc)
        if match:
            return fmt.format(*match.groups())
    
    return False

def convert_barcode_from_ean13_to_upce(upc):
    return convert_barcode_from_upca_to_upce(convert_barcode_from_ean13_to_upca(upc))

def convert_barcode_from_itf14_to_upca(upc):
    return convert_barcode_from_ean13_to_upca(convert_barcode_from_itf14_to_ean13(upc))

def convert_barcode_from_itf14_to_upce(upc):
    return convert_barcode_from_upca_to_upce(convert_barcode_from_itf14_to_upca(upc))


'''
// Changing a EAN-8 code to UPC-A and EAN-13 based on whats used at:
// Source: http://www.upcdatabase.com/
'''


def convert_barcode_from_ean8_to_upca(upc):
    # Pad and validate EAN-8 length and checksum
    upc = str(upc).zfill(8)
    if len(upc) != 8 or not upcean.validate.validate_ean8_checksum(upc):
        return False
    # Convert EAN-8 to UPC-A by adding leading zeros
    return "0000" + upc

def convert_barcode_from_ean8_to_ean13(upc):
    # Convert EAN-8 to UPC-A, then UPC-A to EAN-13
    upca = convert_barcode_from_ean8_to_upca(upc)
    return convert_barcode_from_upca_to_ean13(upca) if upca else False

def convert_barcode_from_ean8_to_itf14(upc):
    # Convert EAN-8 to EAN-13, then EAN-13 to ITF-14
    ean13 = convert_barcode_from_ean8_to_ean13(upc)
    return convert_barcode_from_ean13_to_itf14(ean13) if ean13 else False

def convert_barcode_from_upca_to_ean8(upc):
    # Pad and validate UPC-A length and checksum
    upc = str(upc).zfill(12)
    if len(upc) != 12 or not upcean.validate.validate_upca_checksum(upc):
        return False
    
    # Check for and extract EAN-8 code pattern from UPC-A
    match = re.match("^0000(\\d{8})$", upc)
    return match.group(1) if match else False

def convert_barcode_from_ean13_to_ean8(upc):
    # Convert EAN-13 to UPC-A, then UPC-A to EAN-8
    upca = convert_barcode_from_ean13_to_upca(upc)
    return convert_barcode_from_upca_to_ean8(upca) if upca else False

def convert_barcode_from_itf14_to_ean8(upc):
    # Convert ITF-14 to EAN-13, then EAN-13 to EAN-8
    ean13 = convert_barcode_from_itf14_to_ean13(upc)
    return convert_barcode_from_ean13_to_ean8(ean13) if ean13 else False


'''
// Code 128
// Source: http://www.barcodeisland.com/code128.phtml
// Source: http://en.wikipedia.org/wiki/Code_128
'''

# Define the range for hex values from "00" to "6d" and create the mappings dynamically

# Initialize mappings
code128_hex_to_digit = {}
code128_digit_to_hex = {}

# Starting decimal value
current_decimal = 0

# Populate mappings dynamically
for i in range(int("00", 16), int("6d", 16) + 1):
    hex_value = format(i, '02x')  # Convert to two-digit hex string
    code128_hex_to_digit[hex_value] = current_decimal
    code128_digit_to_hex[current_decimal] = hex_value
    current_decimal += 1

def hex_to_decimal(hex_string):
    """
    Convert a hexadecimal string (two-digit hex) to a three-digit decimal string.
    """
    if hex_string in code128_hex_to_digit:
        return str(code128_hex_to_digit[hex_string]).zfill(3)
    else:
        raise ValueError("Hex '{}' not found in the mapping.".format(hex_string))

def decimal_to_hex(decimal_string):
    """
    Convert a decimal string (three-digit decimal) to a two-digit hex string.
    """
    decimal_value = int(decimal_string)
    if decimal_value in code128_digit_to_hex:
        return code128_digit_to_hex[decimal_value]
    else:
        raise ValueError("Decimal '{}' not found in the mapping.".format(decimal_string))

def convert_first_number_to_hex_and_append_one_if_odd_length(s):
    # Check if the last character is a digit and if it is odd
    if s and s[-1].isdigit() and int(s[-1]) % 2 == 1:
        # Separate the last odd digit and set it for appending '1' later
        last_digit = s[-1]
        remaining_string = s[:-1]
    else:
        # If the last digit is not odd, keep the original string and no last digit
        remaining_string, last_digit = s, None

    # Find the first sequence of digits at the beginning of the string
    match = re.match('^(\\d+)', remaining_string)
    if match:
        # Extract the numeric part
        num_str = match.group(0)
        # Convert to hexadecimal in pairs, ensuring each part is two characters long
        hex_value = ''.join(format(int(num_str[i:i+2]), '02x') for i in range(0, len(num_str), 2))
        
        # Preserve the original leading zeros
        leading_zeros = len(num_str) - len(num_str.lstrip('0'))
        hex_value_with_zeros = '0' * (leading_zeros * 2) + hex_value
        
        # If the length of the numeric part is odd, append '1' at the end
        if len(num_str) % 2 == 1:
            hex_value_with_zeros += '1'
        
        # Replace the original numeric part with the hex representation
        remaining_string = hex_value_with_zeros + remaining_string[len(num_str):]

    return remaining_string, last_digit

def convert_numbers_to_hex_code128(upc, reverse=False):
    upc = str(upc)
    if len(upc) < 4:
        return False
    if not upc.isdigit():
        return False
    if reverse:
        upc = upc[::-1]
    
    # Convert and format the string as per Code 128 requirements
    digchck = convert_first_number_to_hex_and_append_one_if_odd_length(upc)
    outstr = "69" + digchck[0]
    if digchck[1] is not None:
        # Directly add the last odd digit if needed
        outstr = outstr + "651" + digchck[1]
    
    return outstr

def convert_ascii_code128_to_hex_code128(upc, reverse=False):
    upc = str(upc)
    if(len(upc) < 4):
        return False
    if(reverse):
        upc = upc[::-1]
    hextoascii = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V",
                  '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36",
                  'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    barcodeout = ""
    for upcpart in upc:
        barcodeout = barcodeout + asciitohex.get(upcpart, '')
    return barcodeout


def convert_hex_code128_to_ascii_code128(upc, reverse=False):
    upc = str(upc)
    if(len(upc) < 8):
        return False
    if(reverse):
        upc = upc[::-1]
    hextoascii = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V",
                  '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36",
                  'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    barcodeout = ""
    for upcpart in upc:
        barcodeout = barcodeout + hextoascii.get(upcpart, '')
    return barcodeout

# Build the mapping dictionaries
char_to_code_set_a = {}
for i in range(0, 96):
    char = chr(i)
    char_to_code_set_a[char] = i

char_to_code_set_b = {}
for i in range(32, 128):
    char = chr(i)
    char_to_code_set_b[char] = i - 32

pair_to_code_set_c = {}
for i in range(0, 100):
    pair = '{:02d}'.format(i)
    pair_to_code_set_c[pair] = i

def can_use_code_b(text):
    for c in text:
        if c not in char_to_code_set_b:
            return False
    return True

def can_use_code_a(text):
    for c in text:
        if c not in char_to_code_set_a:
            return False
    return True

def should_use_code_c(segments, index):
    segment = segments[index]
    assert segment[0] == 'digits'
    digits = segment[1]
    length = len(digits)
    num_segments = len(segments)

    # Code set C requires even number of digits
    if length % 2 != 0:
        return False

    # Check if the entire data is digits
    if num_segments == 1 and segment[0] == 'digits':
        if length == 2 or length >= 4:
            return True
        else:
            return False

    # Beginning of data
    if index == 0:
        if length >= 4:
            return True
        else:
            return False

    # End of data
    if index == num_segments -1:
        if length >= 4:
            return True
        else:
            return False

    # Middle of data
    else:
        if length >=6:
            return True
        else:
            return False

def convert_text_to_hex_code128(upc, reverse=False):
    # Ensure upc is a string type (compatibility with Python 2 and 3)
    if not isinstance(upc, str):
        upc = str(upc)
    if(reverse):
        upc = upc[::-1]

    # Build the segments
    segments = []
    i = 0
    text_len = len(upc)
    while i < text_len:
        if upc[i].isdigit():
            start = i
            while i < text_len and upc[i].isdigit():
                i += 1
            digits = upc[start:i]
            segments.append(('digits', digits))
        else:
            start = i
            while i < text_len and not upc[i].isdigit():
                i += 1
            non_digits = upc[start:i]
            segments.append(('other', non_digits))

    # Initialize output sequence and current code set
    output_sequence = []
    current_code_set = None

    # Process segments
    for idx, segment in enumerate(segments):
        seg_type, data = segment
        if seg_type == 'digits':
            # Decide whether to use code set C
            use_code_c = should_use_code_c(segments, idx)
            if use_code_c:
                # Switch to code set C if necessary
                if current_code_set != 'C':
                    if not output_sequence:
                        # At the beginning, use Start Code C (105)
                        output_sequence.append(105)
                    else:
                        # Switch to Code Set C (99)
                        output_sequence.append(99)
                    current_code_set = 'C'
                # Encode digits in pairs
                for j in range(0, len(data), 2):
                    pair = data[j:j+2]
                    code_point = pair_to_code_set_c[pair]
                    output_sequence.append(code_point)
            else:
                # Process digits as individual characters in code set A or B
                # Handle as 'other' segment
                if can_use_code_b(data):
                    code_set_needed = 'B'
                else:
                    code_set_needed = 'A'
                if current_code_set != code_set_needed:
                    if not output_sequence:
                        # At the beginning, use Start Code
                        output_sequence.append(103 if code_set_needed == 'A' else 104)
                    else:
                        # Switch code set
                        output_sequence.append(101 if code_set_needed == 'A' else 100)
                    current_code_set = code_set_needed
                # Encode each digit
                for c in data:
                    if current_code_set == 'A':
                        code_point = char_to_code_set_a.get(c)
                    else:
                        code_point = char_to_code_set_b.get(c)
                    if code_point is None:
                        raise ValueError('Character {} not found in code set {}'.format(c, current_code_set))
                    output_sequence.append(code_point)
        elif seg_type == 'other':
            # Decide whether to use code set B or A
            if can_use_code_b(data):
                code_set_needed = 'B'
            else:
                code_set_needed = 'A'
            if current_code_set != code_set_needed:
                if not output_sequence:
                    # At the beginning, use Start Code
                    output_sequence.append(103 if code_set_needed == 'A' else 104)
                else:
                    # Switch code set
                    output_sequence.append(101 if code_set_needed == 'A' else 100)
                current_code_set = code_set_needed
            # Encode each character
            for c in data:
                if current_code_set == 'A':
                    code_point = char_to_code_set_a.get(c)
                else:
                    code_point = char_to_code_set_b.get(c)
                if code_point is None:
                    raise ValueError('Character {} not found in code set {}'.format(c, current_code_set))
                output_sequence.append(code_point)

    # Now, convert the code points to hex codes
    hex_codes = []
    for code_point in output_sequence:
        hex_code = '{:02x}'.format(code_point)
        hex_codes.append(hex_code)

    return ''.join(hex_codes)


def convert_text_to_hex_code128_auto(upc, reverse=False):
    if(reverse):
        upc = upc[::-1]
    hextocharsetone = {' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33",
                       'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '\x00': "40", '\x01': "41", '\x02': "42", '\x03': "43", '\x04': "44", '\x05': "45", '\x06': "46", '\x07': "47", '\x08': "48", '\x09': "49", '\x0a': "4a", '\x0b': "4b", '\x0c': "4c", '\x0d': "4d", '\x0e': "4e", '\x0f': "4f", '\x10': "50", '\x11': "51", '\x12': "52", '\x13': "53", '\x14': "54", '\x15': "55", '\x16': "56", '\x17': "57", '\x18': "58", '\x19': "59", '\x1a': "5a", '\x1b': "5b", '\x1c': "5c", '\x1d': "5d", '\x1e': "5e", '\x1f': "5f"}
    hextocharsettwo = {' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e",
                       'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", '\x7f': "5f"}
    hextocharsetthree = {'00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '10': "0a", '11': "0b", '12': "0c", '13': "0d", '14': "0e", '15': "0f", '16': "10", '17': "11", '18': "12", '19': "13", '20': "14", '21': "15", '22': "16", '23': "17", '24': "18", '25': "19", '26': "1a", '27': "1b", '28': "1c", '29': "1d", '30': "1e", '31': "1f", '32': "20", '33': "21", '34': "22", '35': "23", '36': "24", '37': "25", '38': "26", '39': "27", '40': "28", '41': "29", '42': "2a", '43': "2b", '44': "2c", '45': "2d", '46': "2e", '47': "2f", '48': "30", '49': "31", '50': "32", '51': "33", '52': "34",
                         '53': "35", '54': "36", '55': "37", '56': "38", '57': "39", '58': "3a", '59': "3b", '60': "3c", '61': "3d", '62': "3e", '63': "3f", '64': "40", '65': "41", '66': "42", '67': "43", '68': "44", '69': "45", '70': "46", '71': "47", '72': "48", '73': "49", '74': "4a", '75': "4b", '76': "4c", '77': "4d", '78': "4e", '79': "4f", '80': "50", '81': "51", '82': "52", '83': "53", '84': "54", '85': "55", '86': "56", '87': "57", '88': "58", '89': "59", '90': "5a", '91': "5b", '92': "5c", '93': "5d", '94': "5e", '95': "5f", '96': "60", '97': "61", '98': "62", '99': "63", ' ': "64", ' ': "65", ' ': "66", ' ': "67", ' ': "68", ' ': "69", ' ': "6a", ' ': "6b", ' ': "6c"}
    hextocharsetfour = {'32': "00", '194': "00", '207': "00", '212': "00", '252': "00", '33': "01", '34': "02", '35': "03", '36': "04", '37': "05", '38': "06", '39': "07", '40': "08", '41': "09", '42': "0a", '43': "0b", '44': "0c", '45': "0d", '46': "0e", '47': "0f", '48': "10", '49': "11", '50': "12", '51': "13", '52': "14", '53': "15", '54': "16", '55': "17", '56': "18", '57': "19", '58': "1a", '59': "1b", '60': "1c", '61': "1d", '62': "1e", '63': "1f", '64': "20", '65': "21", '66': "22", '67': "23", '68': "24", '69': "25", '70': "26", '71': "27", '72': "28", '73': "29", '74': "2a", '75': "2b", '76': "2c", '77': "2d", '78': "2e", '79': "2f", '80': "30", '81': "31", '82': "32", '83': "33", '84': "34", '85': "35", '86': "36", '87': "37", '88': "38", '89': "39", '90': "3a", '91': "3b", '92': "3c", '93': "3d", '94': "3e", '95': "3f", '96': "40",
                        '97': "41", '98': "42", '99': "43", '100': "44", '101': "45", '102': "46", '103': "47", '104': "48", '105': "49", '106': "4a", '107': "4b", '108': "4c", '109': "4d", '110': "4e", '111': "4f", '112': "50", '113': "51", '114': "52", '115': "53", '116': "54", '117': "55", '118': "56", '119': "57", '120': "58", '121': "59", '122': "5a", '123': "5b", '124': "5c", '125': "5d", '126': "5e", '195': "5f", '200': "5f", '240': "5f", '196': "60", '201': "60", '241': "60", '197': "61", '202': "61", '242': "61", '198': "62", '203': "62", '243': "62", '199': "63", '204': "63", '244': "63", '200': "64", '205': "64", '245': "64", '201': "65", '206': "65", '246': "65", '202': "66", '207': "66", '247': "66", '203': "67", '208': "67", '248': "67", '204': "68", '209': "68", '249': "68", '205': "69", '210': "69", '250': "69", '127': "6a", '128': "6b", '129': "6c"}
    hextoascii = {'60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É",
                  '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65",
                  'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    textlen = len(upc)
    textc = 0
    incharset = None
    shiftcharset = None
    textlist = []
    while(textc < textlen):
        skipcheck = False
        if(asciitohex.get(upc[textc], False)):
            if((upc[textc] == "Ä" and (incharset == 1 or incharset == 2 or incharset is None)) or (upc[textc] == "Å" and (incharset == 1 or incharset == 2 or incharset is None)) or (upc[textc] == "È" and (incharset == 2 or incharset is None)) or (upc[textc] == "É" and (incharset == 1 or incharset is None)) or upc[textc] == "Ê"):
                if(textc == 0):
                    textlist.append("67")
                    incharset = 2
                textlist.append(asciitohex.get(upc[textc], False))
        elif((incharset == 1 and upc[textc] == " ") or (incharset == 2 and upc[textc] == " ")):
            textlist.append(hextocharsetone.get(upc[textc], False))
        elif((upc[textc].isnumeric() and ((textc+1) < textlen) and upc[textc+1].isnumeric()) and not skipcheck):
            if(hextocharsetthree.get(upc[textc]+upc[textc+1], False)):
                if(incharset == 3):
                    textlist.append(hextocharsetthree.get(
                        upc[textc]+upc[textc+1], False))
                else:
                    if(textc == 0):
                        textlist.append("69")
                    else:
                        textlist.append("63")
                    textlist.append(hextocharsetthree.get(
                        upc[textc]+upc[textc+1], False))
                incharset = 3
                skipcheck = True
                textc += 1
        elif(hextocharsettwo.get(upc[textc], False) and not (incharset == 1 and shiftcharset is None and hextocharsetone.get(upc[textc], False)) and not skipcheck):
            if(incharset == 2):
                textlist.append(hextocharsettwo.get(upc[textc], False))
            else:
                if(textc == 0):
                    textlist.append("68")
                else:
                    if(((textc+1) < textlen) and hextocharsettwo.get(upc[textc+1], False) or incharset == 3):
                        textlist.append("64")
                    else:
                        textlist.append("62")
                        shiftcharset = True
                textlist.append(hextocharsettwo.get(upc[textc], False))
            skipcheck = True
            if(shiftcharset is None):
                incharset = 2
            else:
                shiftcharset = None
        elif(hextocharsetone.get(upc[textc], False) and not skipcheck):
            if(incharset == 1):
                textlist.append(hextocharsetone.get(upc[textc], False))
            else:
                if(textc == 0):
                    textlist.append("67")
                else:
                    if(((textc+1) < textlen) and hextocharsetone.get(upc[textc+1], False) or incharset == 3):
                        textlist.append("65")
                    else:
                        textlist.append("62")
                        shiftcharset = True
                textlist.append(hextocharsetone.get(upc[textc], False))
            skipcheck = True
            if(shiftcharset is None):
                incharset = 1
            else:
                shiftcharset = None
        textc += 1
    if(not any(textlist)):
        return False
    return str(''.join(textlist))


def convert_text_to_hex_code128_manual(upc, reverse=False):
    if(reverse):
        upc = upc[::-1]
    hextocharsetone = {' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33",
                       'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '\x00': "40", '\x01': "41", '\x02': "42", '\x03': "43", '\x04': "44", '\x05': "45", '\x06': "46", '\x07': "47", '\x08': "48", '\x09': "49", '\x0a': "4a", '\x0b': "4b", '\x0c': "4c", '\x0d': "4d", '\x0e': "4e", '\x0f': "4f", '\x10': "50", '\x11': "51", '\x12': "52", '\x13': "53", '\x14': "54", '\x15': "55", '\x16': "56", '\x17': "57", '\x18': "58", '\x19': "59", '\x1a': "5a", '\x1b': "5b", '\x1c': "5c", '\x1d': "5d", '\x1e': "5e", '\x1f': "5f"}
    hextocharsettwo = {' ': "00", '!': "01", '\\': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e",
                       'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36", 'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", '\x7f': "5f"}
    hextocharsetthree = {'00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '10': "0a", '11': "0b", '12': "0c", '13': "0d", '14': "0e", '15': "0f", '16': "10", '17': "11", '18': "12", '19': "13", '20': "14", '21': "15", '22': "16", '23': "17", '24': "18", '25': "19", '26': "1a", '27': "1b", '28': "1c", '29': "1d", '30': "1e", '31': "1f", '32': "20", '33': "21", '34': "22", '35': "23", '36': "24", '37': "25", '38': "26", '39': "27", '40': "28", '41': "29", '42': "2a", '43': "2b", '44': "2c", '45': "2d", '46': "2e", '47': "2f", '48': "30",
                         '49': "31", '50': "32", '51': "33", '52': "34", '53': "35", '54': "36", '55': "37", '56': "38", '57': "39", '58': "3a", '59': "3b", '60': "3c", '61': "3d", '62': "3e", '63': "3f", '64': "40", '65': "41", '66': "42", '67': "43", '68': "44", '69': "45", '70': "46", '71': "47", '72': "48", '73': "49", '74': "4a", '75': "4b", '76': "4c", '77': "4d", '78': "4e", '79': "4f", '80': "50", '81': "51", '82': "52", '83': "53", '84': "54", '85': "55", '86': "56", '87': "57", '88': "58", '89': "59", '90': "5a", '91': "5b", '92': "5c", '93': "5d", '94': "5e", '95': "5f", '96': "60", '97': "61", '98': "62", '99': "63"}
    hextocharsetfour = {'32': "00", '194': "00", '207': "00", '212': "00", '252': "00", '33': "01", '34': "02", '35': "03", '36': "04", '37': "05", '38': "06", '39': "07", '40': "08", '41': "09", '42': "0a", '43': "0b", '44': "0c", '45': "0d", '46': "0e", '47': "0f", '48': "10", '49': "11", '50': "12", '51': "13", '52': "14", '53': "15", '54': "16", '55': "17", '56': "18", '57': "19", '58': "1a", '59': "1b", '60': "1c", '61': "1d", '62': "1e", '63': "1f", '64': "20", '65': "21", '66': "22", '67': "23", '68': "24", '69': "25", '70': "26", '71': "27", '72': "28", '73': "29", '74': "2a", '75': "2b", '76': "2c", '77': "2d", '78': "2e", '79': "2f", '80': "30", '81': "31", '82': "32", '83': "33", '84': "34", '85': "35", '86': "36", '87': "37", '88': "38", '89': "39", '90': "3a", '91': "3b", '92': "3c", '93': "3d", '94': "3e", '95': "3f", '96': "40",
                        '97': "41", '98': "42", '99': "43", '100': "44", '101': "45", '102': "46", '103': "47", '104': "48", '105': "49", '106': "4a", '107': "4b", '108': "4c", '109': "4d", '110': "4e", '111': "4f", '112': "50", '113': "51", '114': "52", '115': "53", '116': "54", '117': "55", '118': "56", '119': "57", '120': "58", '121': "59", '122': "5a", '123': "5b", '124': "5c", '125': "5d", '126': "5e", '195': "5f", '200': "5f", '240': "5f", '196': "60", '201': "60", '241': "60", '197': "61", '202': "61", '242': "61", '198': "62", '203': "62", '243': "62", '199': "63", '204': "63", '244': "63", '200': "64", '205': "64", '245': "64", '201': "65", '206': "65", '246': "65", '202': "66", '207': "66", '247': "66", '203': "67", '208': "67", '248': "67", '204': "68", '209': "68", '249': "68", '205': "69", '210': "69", '250': "69", '127': "6a", '128': "6b", '129': "6c"}
    hextoascii = {'60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É",
                  '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65",
                  'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    textlen = len(upc)
    textc = 0
    incharset = None
    shiftcharset = None
    textlist = []
    while(textc < textlen):
        skipcheck = False
        if(asciitohex.get(upc[textc], False)):
            if(upc[textc] == "Ë" and textc == 0):
                incharset = 1
            elif(upc[textc] == "Ì" and textc == 0):
                incharset = 2
            elif(upc[textc] == "Í" and textc == 0):
                incharset = 3
            elif(upc[textc] == "Æ"):
                if(incharset == 1):
                    shiftcharset = 2
                elif(incharset == 2):
                    shiftcharset = 1
            elif(upc[textc] == "Ç" and (incharset == 1 or incharset == 2)):
                incharset = 3
            elif(upc[textc] == "È" and (incharset == 1 or incharset == 3)):
                incharset = 2
            elif(upc[textc] == "É" and (incharset == 2 or incharset == 3)):
                incharset = 1
            textlist.append(asciitohex.get(upc[textc], False))
        elif(incharset == 3):
            textlist.append(hextocharsetthree.get(
                upc[textc]+upc[textc+1], False))
            skipcheck = True
            textc += 1
        elif((incharset == 2 and shiftcharset is None) or (shiftcharset == 2 and incharset == 1)):
            textlist.append(hextocharsettwo.get(upc[textc], False))
            if(shiftcharset == 2 and incharset == 1):
                shiftcharset = None
            skipcheck = True
        elif((incharset == 1 and shiftcharset is None) or (shiftcharset == 1 and incharset == 2)):
            textlist.append(hextocharsetone.get(upc[textc], False))
            if(shiftcharset == 1 and incharset == 2):
                shiftcharset = None
            skipcheck = True
        textc += 1
    if(not any(textlist)):
        return False
    return str(''.join(textlist))


# Define the code set mappings
CODE_SET_A = {chr(i): i for i in range(128)}
CODE_SET_B = {chr(i): i - 32 for i in range(32, 128)}
CODE_SET_C = {'{:02d}'.format(i): i for i in range(100)}

# Start codes
START_CODES = {'A': 103, 'B': 104, 'C': 105}

# Code set switch codes
SWITCH_CODES = {'A': 101, 'B': 100, 'C': 99}

def optimize_encoding_code128(upc, reverse=False):
    if(reverse):
        input_string = upc[::-1]
    else:
        input_string = str(upc)
    """
    Optimize the input string to produce the smallest EAN-128 encoding.
    """
    # Ensure input_string is a unicode string (for Python 2 compatibility)
    if not isinstance(input_string, str):
        input_string = str(input_string)

    length = len(input_string)
    # Dynamic programming table to store the minimal cost and action
    cost = [{} for _ in range(length + 1)]  # cost[i][code_set] = (total_cost, action)
    cost[length] = {'A': (0, None), 'B': (0, None), 'C': (0, None)}  # Base case

    # Precompute which code sets can encode each character
    can_encode = [{} for _ in range(length)]
    for i in range(length):
        c = input_string[i]
        can_encode[i]['A'] = c in CODE_SET_A and ord(c) < 96  # Code Set A can encode ASCII 0-95
        can_encode[i]['B'] = c in CODE_SET_B  # Code Set B can encode ASCII 32-127
        if i + 1 < length and c.isdigit() and input_string[i+1].isdigit():
            can_encode[i]['C'] = True  # Code Set C can encode pairs of digits
        else:
            can_encode[i]['C'] = False

    # Dynamic programming to find the minimal cost encoding
    for i in range(length -1, -1, -1):
        for cs in ['A', 'B', 'C']:
            min_total_cost = float('inf')
            best_action = None

            # Try to encode starting with code set cs
            if cs == 'C' and can_encode[i]['C']:
                # Try to encode as many digit pairs as possible
                j = i
                while j + 1 < length and input_string[j].isdigit() and input_string[j+1].isdigit():
                    j += 2
                num_pairs = (j - i) // 2
                for next_cs in ['A', 'B', 'C']:
                    switch_cost = 0 if cs == next_cs else 1  # Cost of switching code sets
                    total_cost = num_pairs + switch_cost + cost[j][next_cs][0]
                    if total_cost < min_total_cost:
                        min_total_cost = total_cost
                        best_action = ('encode_c', j, next_cs)
                cost[i][cs] = (min_total_cost, best_action)
            elif cs in ['A', 'B'] and can_encode[i][cs]:
                # Encode one character
                for next_cs in ['A', 'B', 'C']:
                    switch_cost = 0 if cs == next_cs else 1  # Cost of switching code sets
                    total_cost = 1 + switch_cost + cost[i+1][next_cs][0]
                    if total_cost < min_total_cost:
                        min_total_cost = total_cost
                        best_action = ('encode_one', i+1, next_cs)
                cost[i][cs] = (min_total_cost, best_action)
            else:
                # Cannot encode with this code set
                cost[i][cs] = (float('inf'), None)

    # Find the minimal total cost at position 0
    min_total_cost = float('inf')
    start_cs = None
    for cs in ['A', 'B', 'C']:
        total_cost = cost[0][cs][0]
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            start_cs = cs

    # Reconstruct the path to get the encoding
    i = 0
    encoding = []
    current_code_set = start_cs

    # Add the start code
    encoding.append(START_CODES[current_code_set])

    while i < length:
        action = cost[i][current_code_set][1]
        if action is None:
            raise ValueError("Cannot encode character at position {}".format(i))

        if action[0] == 'encode_c':
            # Encode pairs of digits
            j = action[1]
            while i < j:
                pair = input_string[i:i+2]
                code_point = CODE_SET_C[pair]
                encoding.append(code_point)
                i += 2
            next_cs = action[2]
            if next_cs != current_code_set:
                # Switch code sets
                encoding.append(SWITCH_CODES[next_cs])
                current_code_set = next_cs
        elif action[0] == 'encode_one':
            # Encode single character
            c = input_string[i]
            if current_code_set == 'A':
                code_point = ord(c)
            elif current_code_set == 'B':
                code_point = ord(c) - 32
            encoding.append(code_point)
            i += 1
            next_cs = action[2]
            if next_cs != current_code_set:
                # Switch code sets
                encoding.append(SWITCH_CODES[next_cs])
                current_code_set = next_cs
        else:
            # Unknown action
            raise ValueError("Unknown action '{}' at position {}".format(action[0], i))

    # Convert code points to hex representation
    hex_codes = ['{:02x}'.format(code_point) for code_point in encoding]

    return ''.join(hex_codes)

# Define the reverse mappings for Code Sets A, B, and C
CODE_SET_A_REV = {i: chr(i) for i in range(128)}
CODE_SET_B_REV = {i: chr(i + 32) for i in range(96)}
CODE_SET_C_REV = {'{:02d}'.format(i): i for i in range(100)}

# Reverse mapping of start codes and switch codes
START_CODES_REV = {103: 'A', 104: 'B', 105: 'C'}
SWITCH_CODES_REV = {101: 'A', 100: 'B', 99: 'C'}

def hex_to_code128(hex_string):
    # Check for the reversed end code "6b" at the end
    is_reversed = hex_string.endswith("6b")
    
    # Remove the reversed end code if present
    if is_reversed:
        hex_string = hex_string[:-2]

    # Convert the hex string to a list of integers representing code points
    code_points = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    
    # Determine initial code set from the start code
    if code_points[0] not in START_CODES_REV:
        raise ValueError("Invalid start code")
    current_code_set = START_CODES_REV[code_points.pop(0)]

    # Decode the sequence of code points
    decoded_output = ""
    
    i = 0
    while i < len(code_points):
        code_point = code_points[i]
        
        # Check if it's a switch code
        if code_point in SWITCH_CODES_REV:
            current_code_set = SWITCH_CODES_REV[code_point]
            i += 1
            continue
        
        # Decode based on the current code set
        if current_code_set == 'A':
            decoded_output += CODE_SET_A_REV.get(code_point, '')
        elif current_code_set == 'B':
            decoded_output += CODE_SET_B_REV.get(code_point, '')
        elif current_code_set == 'C' and i + 1 < len(code_points):
            # Code set C uses pairs of digits (2 code points per character)
            decoded_output += '{:02d}'.format(code_point)
            i += 1  # Move an extra step since it encodes two digits
        
        i += 1
    
    # Reverse the output if the reverse end code "6b" was detected
    if is_reversed:
        decoded_output = decoded_output[::-1]
    
    return decoded_output


def optimize_encoding_code128_alt(upc, reverse=False):
    if reverse:
        input_string = upc[::-1]
    else:
        input_string = str(upc)
    """
    Optimize the input string to produce the smallest EAN-128 encoding.
    """
    # Ensure input_string is a string
    if not isinstance(input_string, str):
        input_string = str(input_string)

    length = len(input_string)
    # Dynamic programming table to store the minimal cost and action
    cost = [{} for _ in range(length + 1)]  # cost[i][code_set] = (total_cost, action)
    cost[length] = {'A': (0, None), 'B': (0, None), 'C': (0, None)}  # Base case

    # Precompute which code sets can encode each character
    can_encode = [{} for _ in range(length)]
    for i in range(length):
        c = input_string[i]
        can_encode[i]['A'] = c in CODE_SET_A and ord(c) < 96  # Code Set A can encode ASCII 0-95
        can_encode[i]['B'] = c in CODE_SET_B  # Code Set B can encode ASCII 32-127
        if i + 1 < length and c.isdigit() and input_string[i+1].isdigit():
            can_encode[i]['C'] = True  # Code Set C can encode pairs of digits
        else:
            can_encode[i]['C'] = False

    # Dynamic programming to find the minimal cost encoding
    for i in range(length -1, -1, -1):
        for cs in ['A', 'B', 'C']:
            min_total_cost = float('inf')
            best_action = None

            if cs == 'C' and can_encode[i]['C']:
                # Try to encode as many digit pairs as possible
                j = i
                while j + 1 < length and input_string[j].isdigit() and input_string[j+1].isdigit():
                    j += 2
                num_pairs = (j - i) // 2
                for next_cs in ['A', 'B', 'C']:
                    switch_cost = 0 if cs == next_cs else 1  # Cost of switching code sets
                    total_cost = num_pairs + switch_cost + cost[j][next_cs][0]
                    if total_cost < min_total_cost:
                        min_total_cost = total_cost
                        best_action = ('encode_c', j, next_cs)
                cost[i][cs] = (min_total_cost, best_action)
            elif cs in ['A', 'B']:
                c = input_string[i]
                other_cs = 'B' if cs == 'A' else 'A'
                options = []
                # Option 1: Encode in current code set if possible
                if can_encode[i][cs]:
                    for next_cs in ['A', 'B', 'C']:
                        switch_cost = 0 if cs == next_cs else 1  # Cost of switching code sets
                        total_cost = 1 + switch_cost + cost[i+1][next_cs][0]
                        action = ('encode_one', i+1, next_cs)
                        options.append((total_cost, action))
                # Option 2: Use Shift code if possible
                if can_encode[i][other_cs]:
                    # Shift code can be used
                    total_cost = 2 + cost[i+1][cs][0]  # Shift code + encode char + continue in current cs
                    action = ('shift', i+1)
                    options.append((total_cost, action))
                # Option 3: Switch to other code set
                if can_encode[i][other_cs]:
                    switch_cost = 1  # Cost of switching code sets
                    total_cost = switch_cost + 1 + cost[i+1][other_cs][0]
                    action = ('switch_and_encode', i+1, other_cs)
                    options.append((total_cost, action))
                # Choose the option with minimal total cost
                if options:
                    min_total_cost, best_action = min(options, key=lambda x: x[0])
                    cost[i][cs] = (min_total_cost, best_action)
                else:
                    # Cannot encode character at position i
                    cost[i][cs] = (float('inf'), None)
            else:
                # Cannot encode with this code set
                cost[i][cs] = (float('inf'), None)

    # Find the minimal total cost at position 0
    min_total_cost = float('inf')
    start_cs = None
    for cs in ['A', 'B', 'C']:
        total_cost = cost[0][cs][0]
        if total_cost < min_total_cost:
            min_total_cost = total_cost
            start_cs = cs

    # Reconstruct the path to get the encoding
    i = 0
    encoding = []
    current_code_set = start_cs

    # Add the start code
    encoding.append(START_CODES[current_code_set])

    while i < length:
        action = cost[i][current_code_set][1]
        if action is None:
            raise ValueError("Cannot encode character at position {}".format(i))

        if action[0] == 'encode_c':
            # Encode pairs of digits
            j = action[1]
            while i < j:
                pair = input_string[i:i+2]
                code_point = CODE_SET_C[pair]
                encoding.append(code_point)
                i += 2
            next_cs = action[2]
            if next_cs != current_code_set:
                # Switch code sets
                encoding.append(SWITCH_CODES[next_cs])
                current_code_set = next_cs
        elif action[0] == 'encode_one':
            # Encode single character
            c = input_string[i]
            if current_code_set == 'A':
                code_point = ord(c)
            elif current_code_set == 'B':
                code_point = ord(c) - 32
            encoding.append(code_point)
            i += 1
            next_cs = action[2]
            if next_cs != current_code_set:
                # Switch code sets
                encoding.append(SWITCH_CODES[next_cs])
                current_code_set = next_cs
        elif action[0] == 'shift':
            # Use shift code to encode one character in other code set
            encoding.append(98)  # Shift code
            c = input_string[i]
            if current_code_set == 'A':
                # Shift to B for one character
                code_point = ord(c) - 32
            elif current_code_set == 'B':
                # Shift to A for one character
                code_point = ord(c)
            encoding.append(code_point)
            i += 1
            # Continue in current_code_set
        elif action[0] == 'switch_and_encode':
            # Switch code sets and encode character
            next_cs = action[2]
            encoding.append(SWITCH_CODES[next_cs])
            current_code_set = next_cs
            c = input_string[i]
            if current_code_set == 'A':
                code_point = ord(c)
            elif current_code_set == 'B':
                code_point = ord(c) - 32
            encoding.append(code_point)
            i += 1
        else:
            # Unknown action
            raise ValueError("Unknown action '{}' at position {}".format(action[0], i))

    # Convert code points to hex representation
    hex_codes = ['{:02x}'.format(code_point) for code_point in encoding]

    return ''.join(hex_codes)


# Define the code point to hex mapping at the module level
code_point_to_hex = {
    0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07',
    8: '08', 9: '09', 10: '0a', 11: '0b', 12: '0c', 13: '0d', 14: '0e', 15: '0f',
    16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16', 23: '17',
    24: '18', 25: '19', 26: '1a', 27: '1b', 28: '1c', 29: '1d', 30: '1e', 31: '1f',
    32: '20', 33: '21', 34: '22', 35: '23', 36: '24', 37: '25', 38: '26', 39: '27',
    40: '28', 41: '29', 42: '2a', 43: '2b', 44: '2c', 45: '2d', 46: '2e', 47: '2f',
    48: '30', 49: '31', 50: '32', 51: '33', 52: '34', 53: '35', 54: '36', 55: '37',
    56: '38', 57: '39', 58: '3a', 59: '3b', 60: '3c', 61: '3d', 62: '3e', 63: '3f',
    64: '40', 65: '41', 66: '42', 67: '43', 68: '44', 69: '45', 70: '46', 71: '47',
    72: '48', 73: '49', 74: '4a', 75: '4b', 76: '4c', 77: '4d', 78: '4e', 79: '4f',
    80: '50', 81: '51', 82: '52', 83: '53', 84: '54', 85: '55', 86: '56', 87: '57',
    88: '58', 89: '59', 90: '5a', 91: '5b', 92: '5c', 93: '5d', 94: '5e', 95: '5f',
    96: '60', 97: '61', 98: '62', 99: '63', 100: '64', 101: '65', 102: '66',
    103: '67', 104: '68', 105: '69', 106: '6a', 107: '6b', 108: '6c', 109: '6d'
}

# Also define the inverse mapping for hex to code point
hex_to_code_point = {v: k for k, v in code_point_to_hex.items()}

def convert_text_to_hex_gs1_128(data, reverse=False):
    # Ensure data is a string
    if not isinstance(data, str):
        data = str(data)
    if reverse:
        data = data[::-1]

    # Build the segments (digits and non-digits)
    segments = []
    i = 0
    text_len = len(data)
    while i < text_len:
        if data[i].isdigit():
            start = i
            while i < text_len and data[i].isdigit():
                i += 1
            digits = data[start:i]
            segments.append(('digits', digits))
        else:
            start = i
            while i < text_len and not data[i].isdigit():
                i += 1
            non_digits = data[start:i]
            segments.append(('other', non_digits))

    # Initialize output sequence and current code set
    output_sequence = []
    current_code_set = None

    # Include FNC1
    fnc1_code_point = 102  # FNC1

    # Process segments
    for idx, segment in enumerate(segments):
        seg_type, segment_data = segment
        if seg_type == 'digits':
            # Decide whether to use Code Set C (digits, even length)
            use_code_c = len(segment_data) >= 4 and len(segment_data) % 2 == 0
            if use_code_c:
                # Switch to Code Set C if necessary
                if current_code_set != 'C':
                    if not output_sequence:
                        # At the beginning, use Start Code C
                        output_sequence.append(105)
                        # Append FNC1 for GS1-128
                        output_sequence.append(fnc1_code_point)
                    else:
                        # Switch to Code Set C (99)
                        output_sequence.append(99)
                    current_code_set = 'C'
                # Encode digits in pairs
                for j in range(0, len(segment_data), 2):
                    pair = segment_data[j:j+2]
                    code_point = int(pair)
                    output_sequence.append(code_point)
            else:
                # Process digits as individual characters in Code Set B
                seg_type = 'other'
                segment_data = segment_data
        if seg_type == 'other':
            # Use Code Set B for other characters
            code_set_needed = 'B'
            # Switch code set if necessary
            if current_code_set != code_set_needed:
                if not output_sequence:
                    # At the beginning, use Start Code B
                    output_sequence.append(104)
                    # Append FNC1 for GS1-128
                    output_sequence.append(fnc1_code_point)
                else:
                    # Switch to Code Set B (100)
                    output_sequence.append(100)
                current_code_set = code_set_needed
            # Encode each character
            for c in segment_data:
                code_point = ord(c) - 32
                if 0 <= code_point <= 95:
                    output_sequence.append(code_point)
                else:
                    raise ValueError("Character '{}' not valid in Code Set B.".format(c))

    # Convert the code points to hex codes using the mapping
    hex_codes = []
    for code_point in output_sequence:
        hex_code = code_point_to_hex.get(code_point)
        if hex_code is None:
            raise ValueError("No hex code mapping for code point {}".format(code_point))
        hex_codes.append(hex_code)

    # Return the hex code sequence as a string
    return ''.join(hex_codes)


def convert_text_to_hex_gs1_128_with_checksum(data, hidecs=True, reverse=False, stopcode='6c'):
    if reverse:
        stopcode = '6b'
    code128_hex = convert_text_to_hex_gs1_128(data, reverse)
    if not code128_hex:
        return False

    # Reconstruct the code point sequence from the hex codes to compute checksum
    code_points = []
    hex_codes = [code128_hex[i:i+2] for i in range(0, len(code128_hex), 2)]
    i = 0
    while i < len(hex_codes):
        hex_code = hex_codes[i]
        if hex_code == '6d':
            # Skip hide checksum indicator
            i += 1
            continue
        code_point = hex_to_code_point.get(hex_code)
        if code_point is None:
            raise ValueError("No code point mapping for hex code {}".format(hex_code))
        code_points.append(code_point)
        i += 1

    # Calculate the checksum
    checksum = code_points[0]  # Start code
    for idx, code_point in enumerate(code_points[1:], start=1):
        checksum += code_point * idx
    checksum %= 103

    # Convert checksum code point to hex code using the mapping
    checksum_hex = code_point_to_hex.get(checksum)
    if checksum_hex is None:
        raise ValueError("No hex code mapping for checksum code point {}".format(checksum))

    # Include hide checksum indicator if required
    hidecschar = ''
    if hidecs:
        hidecschar = '6d'

    # Return the full hex code sequence with checksum and stop code
    return code128_hex + hidecschar + checksum_hex + stopcode


def convert_text_to_hex_code128_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = convert_text_to_hex_code128(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode


def convert_text_to_hex_code128_auto_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = convert_text_to_hex_code128_auto(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode


def convert_text_to_hex_code128_optimize_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = optimize_encoding_code128(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode


def convert_text_to_hex_code128_optimize_alt_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = optimize_encoding_code128_alt(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode

def convert_numbers_to_hex_code128_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = convert_numbers_to_hex_code128(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode

def convert_text_to_hex_code128_manual_with_checksum(upc, hidecs=True, reverse=False, stopcode="6c"):
    if(reverse):
        stopcode = "6b"
    code128out = convert_text_to_hex_code128_manual(upc, reverse)
    if(not code128out):
        return False
    hidecschar = ""
    if(hidecs):
        hidecschar = "6d"
    return code128out+hidecschar+upcean.validate.get_code128_checksum(code128out)+stopcode


def convert_text_to_code39ext(upc):
    code39_char_to_encoding = {
        # Digits
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        # Uppercase letters
        'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E',
        'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J',
        'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O',
        'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T',
        'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'Z': 'Z', '-': '-', '.': '.', ' ': ' ', '$': '$',
        '/': '/', '+': '+', '%': '%'
    }

    # Map punctuation and special characters
    code39_char_to_encoding.update({
        '!': '/A', '"': '/B', '#': '/C', '$': '/D', '%': '/E',
        '&': '/F', "'": '/G', '(': '/H', ')': '/I', '*': '/J',
        '+': '/K', ',': '/L', '-': '-', '.': '.', '/': '/O',
        ':': '/Z', ';': '%F', '<': '%G', '=': '%H', '>': '%I',
        '?': '%J', '@': '%V', '[': '%K', '\\': '%L', ']': '%M',
        '^': '%N', '_': '%O', '`': '%W', '{': '%P', '|': '%Q',
        '}': '%R', '~': '%S'
    })

    # Map lowercase letters
    for c in range(ord('a'), ord('z') + 1):
        code39_char_to_encoding[chr(c)] = '+' + chr(c - 32)  # '+A' to '+Z'

    # Map non-printable ASCII characters (0-31)
    for i in range(0, 32):
        if i < 27:
            code39_char_to_encoding[chr(i)] = '$' + chr(i + 64)  # $A - $Z
        else:
            code39_char_to_encoding[chr(i)] = '%' + chr(i + 38)  # %A - %F

    # Map DEL character (ASCII 127) to '%T'
    code39_char_to_encoding[chr(127)] = '%T'

    encoded = ''
    for char in upc:
        if char in code39_char_to_encoding:
            encoded += code39_char_to_encoding[char]
        else:
            # Characters not in encoding map are replaced with space
            encoded += ' '
    return encoded

def convert_text_to_code93ext(upc):
    code93_char_to_encoding = {}

    # Map non-printable ASCII characters (0-26)
    for i in range(0, 27):
        code93_char_to_encoding[chr(i)] = '$' + chr(i + 64)  # $A - $Z

    # Map ASCII 27-31
    special_chars = {27: '%A', 28: '%B', 29: '%C', 30: '%D', 31: '%E'}
    for i in range(27, 32):
        code93_char_to_encoding[chr(i)] = special_chars[i]

    # Map printable ASCII characters
    for i in range(32, 127):
        char = chr(i)
        if char.isalnum() or char in '-. $/+%':
            code93_char_to_encoding[char] = char
        elif 33 <= i <= 44:
            code93_char_to_encoding[char] = '/' + chr(i + 32)  # /A - /O
        elif 45 <= i <= 57:
            code93_char_to_encoding[char] = char  # 0-9, -, .
        elif 58 <= i <= 63:
            code93_char_to_encoding[char] = '%' + chr(i + 11)  # %F - %J
        elif 64 == i:
            code93_char_to_encoding[char] = '%V'  # @
        elif 91 <= i <= 95:
            code93_char_to_encoding[char] = '%' + chr(i - 27)  # %K - %O
        elif 96 == i:
            code93_char_to_encoding[char] = '%W'  # `
        elif 97 <= i <= 122:
            code93_char_to_encoding[char] = '+' + chr(i - 32)  # +A - +Z
        elif 123 <= i <= 126:
            code93_char_to_encoding[char] = '%' + chr(i - 80)  # %P - %S
        else:
            # Characters not in encoding map are replaced with space
            code93_char_to_encoding[char] = ' '

    # Map DEL character (ASCII 127) to '%T'
    code93_char_to_encoding[chr(127)] = '%T'

    encoded = ''
    for char in upc:
        if char in code93_char_to_encoding:
            encoded += code93_char_to_encoding[char]
        else:
            # Characters not in encoding map are replaced with space
            encoded += ' '
    return encoded


'''
// ISSN (International Standard Serial Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Serial_Number
'''


def convert_barcode_from_issn8_to_issn13(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    upc = upc.replace("X", "")
    if(not upcean.validate.validate_issn8_checksum(upc)):
        return False
    if(len(upc) > 7):
        fix_matches = re.findall("^(\\d{7})", upc)
        upc = fix_matches[0]
    issn13 = "977"+upc+"00" + \
        str(upcean.validate.validate_ean13_checksum("977"+upc+"00", True))
    return issn13


def convert_barcode_from_issn13_to_issn8(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    upc = upc.replace("X", "")
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    if(not re.findall("/^977(\\d{7})/", upc)):
        return False
    if(re.findall("^977(\\d{7})", upc)):
        upc_matches = re.findall("^977(\\d{7})", upc)
        issn8 = upc_matches[1] + \
            upcean.validate.validate_issn8_checksum(upc_matches[1], True)
    return issn8


def convert_barcode_from_issn8_to_ean13(upc):
    upc = str(upc)
    return convert_barcode_from_issn8_to_issn13(upc)


def convert_barcode_from_ean13_to_issn8(upc):
    upc = str(upc)
    return convert_barcode_from_issn13_to_issn8(upc)


def convert_barcode_from_issn8_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_issn8_to_issn13(upc))


def convert_barcode_from_itf14_to_issn8(upc):
    upc = str(upc)
    return convert_barcode_from_itf14_to_ean13(convert_barcode_from_issn13_to_issn8(upc))


def print_issn8_barcode(upc):
    upc = str(upc)
    if(len(upc) > 8):
        fix_matches = re.findall("^(\\d{8})", upc)
        upc = fix_matches[1]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not re.findall("^(\\d{4})(\\d{4})", upc)):
        return False
    issn_matches = re.findall("^(\\d{4})(\\d{4})", upc)
    issn_matches = issn_matches[0]
    issn8 = issn_matches[0]+"-"+issn_matches[1]
    return issn8


def print_issn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[1]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall("^(\\d{3})(\\d{4})(\\d{4})(\\d{2})", upc)):
        return False
    issn_matches = re.findall("^(\\d{3})(\\d{4})(\\d{4})(\\d{2})", upc)
    issn_matches = issn_matches[0]
    issn13 = issn_matches[0]+"-"+issn_matches[1] + \
        "-"+issn_matches[2]+"-"+issn_matches[3]
    return issn13


def print_convert_barcode_from_issn8_to_issn13(upc):
    upc = str(upc)
    issn13 = print_issn13_barcode(convert_barcode_from_issn8_to_issn13(upc))
    return issn13


def print_convert_barcode_from_issn13_to_issn8(upc):
    upc = str(upc)
    issn8 = print_issn8_barcode(convert_barcode_from_issn13_to_issn8(upc))
    return issn8


'''
// ISBN (International Standard Book Number)
// Source: http://en.wikipedia.org/wiki/ISBN
'''


def convert_barcode_from_isbn10_to_isbn13(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(not upcean.validate.validate_isbn10_checksum(upc)):
        return False
    if(len(upc) > 9):
        fix_matches = re.findall("^(\\d{9})", upc)
        upc = fix_matches[0]
        isbn13 = "978"+upc + \
            str(upcean.validate.validate_ean13_checksum("978"+upc, True))
    return isbn13


def convert_barcode_from_isbn13_to_isbn10(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    if(not re.findall("^978(\\d{9})", upc)):
        return False
    if(re.findall("^978(\\d{9})", upc)):
        upc_matches = re.findall("^978(\\d{9})", upc)
        isbn10 = upc_matches[0] + \
            str(upcean.validate.validate_isbn10_checksum(upc_matches[0], True))
    return isbn10


def convert_barcode_from_isbn10_to_ean13(upc):
    upc = str(upc)
    return convert_barcode_from_isbn10_to_isbn13(upc)


def convert_barcode_from_ean13_to_isbn10(upc):
    upc = str(upc)
    return convert_barcode_from_isbn13_to_isbn10(upc)


def convert_barcode_from_isbn10_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_isbn10_to_isbn13(upc))


def convert_barcode_from_itf14_to_isbn10(upc):
    upc = str(upc)
    return convert_barcode_from_itf14_to_ean13(convert_barcode_from_isbn13_to_isbn10(upc))


def print_isbn10_barcode(upc):
    upc = str(upc)
    if(len(upc) > 10):
        fix_matches = re.findall("^(\\d{9})(\\d{1}|X{1})", upc)
        fix_matches = fix_matches[0]
        upc = fix_matches[0]+fix_matches[1]
    if(len(upc) > 10 or len(upc) < 10):
        return False
    if(not re.findall("^(\\d{1})(\\d{3})(\\d{5})(\\d{1}|X{1})", upc)):
        return False
    isbn_matches = re.findall("^(\\d{1})(\\d{3})(\\d{5})(\\d{1}|X{1})", upc)
    isbn_matches = isbn_matches[0]
    isbn10 = isbn_matches[0]+"-"+isbn_matches[1] + \
        "-"+isbn_matches[2]+"-"+isbn_matches[3]
    return isbn10


def print_isbn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[1]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall("^(\\d{3})(\\d{1})(\\d{3})(\\d{5})(\\d{1})", upc)):
        return False
    isbn_matches = re.findall("^(\\d{3})(\\d{1})(\\d{3})(\\d{5})(\\d{1})", upc)
    isbn_matches = isbn_matches[0]
    isbn13 = isbn_matches[0]+"-"+isbn_matches[1]+"-" + \
        isbn_matches[2]+"-"+isbn_matches[3]+"-"+isbn_matches[4]
    return isbn13


def print_convert_barcode_from_isbn10_to_isbn13(upc):
    upc = str(upc)
    isbn13 = print_isbn13_barcode(convert_barcode_from_isbn10_to_isbn13(upc))
    return isbn13


def print_convert_barcode_from_isbn13_to_isbn10(upc):
    upc = str(upc)
    isbn10 = print_isbn10_barcode(convert_barcode_from_isbn13_to_isbn10(upc))
    return isbn10


'''
// ISMN (International Standard Music Number)
// Source: http://en.wikipedia.org/wiki/International_Standard_Music_Number
// Source: http://www.ismn-international.org/whatis.html
// Source: http://www.ismn-international.org/manual_1998/chapter2.html
'''


def convert_barcode_from_ismn10_to_ismn13(upc):
    upc = str(upc)
    upc = upc.replace("M", "")
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(not upcean.validate.validate_ismn10_checksum(upc)):
        return False
    if(len(upc) > 8):
        fix_matches = re.findall("^(\\d{8})", upc)
        upc = fix_matches[0]
    ismn13 = "9790"+upc + \
        str(upcean.validate.validate_ean13_checksum("9790"+upc, True))
    return ismn13


def convert_barcode_from_ismn13_to_ismn10(upc):
    upc = str(upc)
    upc = upc.replace("M", "")
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    if(not re.findall("^9790(\\d{8})", upc)):
        return False
    if(re.findall("^9790(\\d{8})", upc)):
        upc_matches = re.findall("^9790(\\d{8})", upc)
        ismn10 = upc_matches[0] + \
            str(upcean.validate.validate_ismn10_checksum(upc_matches[0], True))
    return ismn10


def convert_barcode_from_ismn10_to_ean13(upc):
    upc = str(upc)
    return convert_barcode_from_ismn10_to_ismn13(upc)


def convert_barcode_from_ean13_to_ismn10(upc):
    upc = str(upc)
    return convert_barcode_from_ismn13_to_ismn10(upc)


def convert_barcode_from_ismn10_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_ismn10_to_ismn13(upc))


def convert_barcode_from_itf14_to_ismn10(upc):
    upc = str(upc)
    return convert_barcode_from_itf14_to_ean13(convert_barcode_from_ismn13_to_ismn10(upc))


def print_ismn10_barcode(upc):
    upc = str(upc)
    upc = upc.replace("M", "")
    upc = upc.replace("-", "")
    upc = upc.replace(" ", "")
    if(len(upc) > 9):
        fix_matches = re.findall("^(\\d{9})", upc)
        upc = fix_matches[0]
    if(len(upc) > 9 or len(upc) < 9):
        return False
    if(not re.findall("^(\\d{4})(\\d{4})(\\d{1})", upc)):
        return False
    ismn_matches = re.findall("^(\\d{4})(\\d{4})(\\d{1})", upc)
    ismn_matches = ismn_matches[0]
    ismn10 = "M-"+ismn_matches[0]+"-"+ismn_matches[1]+"-"+ismn_matches[2]
    return ismn10


def print_ismn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall("^(\\d{13})", upc)
        upc = fix_matches[0]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall("^(\\d{3})(\\d{1})(\\d{4})(\\d{4})(\\d{1})", upc)):
        return False
    ismn_matches = re.findall("^(\\d{3})(\\d{1})(\\d{4})(\\d{4})(\\d{1})", upc)
    ismn_matches = ismn_matches[0]
    ismn13 = ismn_matches[0]+"-"+ismn_matches[1]+"-" + \
        ismn_matches[2]+"-"+ismn_matches[3]+"-"+ismn_matches[4]
    return ismn13


def print_convert_barcode_from_ismn10_to_ismn13(upc):
    upc = str(upc)
    ismn13 = print_ismn13_barcode(convert_barcode_from_ismn10_to_ismn13(upc))
    return ismn13


def print_convert_barcode_from_ismn13_to_ismn10(upc):
    upc = str(upc)
    ismn10 = print_ismn10_barcode(convert_barcode_from_ismn13_to_ismn10(upc))
    return ismn10


'''
// Get variable weight price checksum for UPC-A
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
// Source: http://barcodes.gs1us.org/GS1%20US%20BarCodes%20and%20eCom%20-%20The%20Global%20Language%20of%20Business.htm
'''


def make_upca_vw_to_upca_barcode(code, price):
    # Trim and pad code and price to required lengths
    code = re.match("\\d{5}", code.zfill(5)).group(0)
    price = re.match("\\d{4}", price.zfill(4)).group(0)
    
    # Calculate price checksum and create the base variable-weight UPC-A barcode
    price_checksum = str(upcean.validate.get_vw_price_checksum(price))
    vwupc = "2{}{}{}".format(code, price_checksum, price)
    
    # Append the UPC-A checksum
    return vwupc + str(upcean.validate.validate_upca_checksum(vwupc, True))

def make_vw_to_upca_barcode(code, price):
    # Alias for make_upca_vw_to_upca_barcode
    return make_upca_vw_to_upca_barcode(code, price)

def make_upca_vw_to_ean13_barcode(code, price):
    # Convert UPC-A variable-weight barcode to EAN-13
    upca_barcode = make_upca_vw_to_upca_barcode(code, price)
    return convert_barcode_from_upca_to_ean13(upca_barcode)

def make_vw_to_ean13_barcode(code, price):
    # Alias for make_upca_vw_to_ean13_barcode
    return make_upca_vw_to_ean13_barcode(code, price)

def make_upca_vw_to_itf14_barcode(code, price):
    # Convert UPC-A variable-weight barcode to ITF-14
    upca_barcode = make_upca_vw_to_upca_barcode(code, price)
    return convert_barcode_from_upca_to_itf14(upca_barcode)

def make_vw_to_itf14_barcode(code, price):
    # Alias for make_upca_vw_to_itf14_barcode
    return make_upca_vw_to_itf14_barcode(code, price)


'''
// Get variable weight price checksum for EAN-13
// Source: https://softmatic.com/barcode-ean-13.html#ean-country
'''

# List of valid GS1 prefixes for variable-weight products
VARYING_WEIGHT_PREFIXES = ["02", "20"] + ["2{}".format(i) for i in range(1, 10)]

def make_ean13_vw_barcode(prefix, code, price):
    # Ensure prefix is valid and padded to 2 digits
    prefix = str(prefix).zfill(2)
    if prefix not in VARYING_WEIGHT_PREFIXES:
        return False  # Invalid GS1 prefix for variable-weight goods

    # Pad and trim the code and price to required lengths
    code = re.match("\\d{5}", str(code).zfill(5)).group(0)
    price = re.match("\\d{4}", str(price).zfill(4)).group(0)
    
    # Calculate price checksum and create the base variable-weight EAN-13 barcode
    price_checksum = str(upcean.validate.get_vw_price_checksum(price))
    vw_ean13 = "{}{}{}{}".format(prefix, code, price_checksum, price)
    
    # Append the EAN-13 checksum
    return vw_ean13 + str(upcean.validate.validate_ean13_checksum(vw_ean13, True))

# Helper function to pad and trim code and price
def pad_and_trim(value, length):
    return re.match("\\d{{{}}}".format(length), str(value).zfill(length)).group(0)

def make_vw_to_itf14_from_ean13(prefix, code, price):
    # Convert EAN-13 variable-weight barcode to ITF-14
    ean13_barcode = make_ean13_vw_barcode(prefix, code, price)
    return convert_barcode_from_ean13_to_itf14(ean13_barcode) if ean13_barcode else False

def make_ean13_vw_to_ean13_barcode(numbersystem, code, price):
    # Ensure inputs are strings and trimmed/padded as necessary
    numbersystem = pad_and_trim(numbersystem, 1)
    code = pad_and_trim(code, 5)
    price = pad_and_trim(price, 5)

    # Construct base EAN-13 variable-weight barcode
    vwupc = "2{}{}{}".format(numbersystem, code, price)
    
    # Append the EAN-13 checksum
    return vwupc + str(upcean.validate.validate_ean13_checksum(vwupc, True))


def make_ean13_vw_to_itf14_barcode(numbersystem, code, price):
    # Generate the EAN-13 barcode with variable weight
    ean13_barcode = make_ean13_vw_to_ean13_barcode(numbersystem, code, price)
    
    # Convert EAN-13 variable-weight barcode to ITF-14
    return convert_barcode_from_ean13_to_itf14(ean13_barcode) if ean13_barcode else False


def make_goodwill_to_upca_barcode(code, price):
    # Pad and trim code and price to required lengths
    code = pad_and_trim(code, 5)
    price = pad_and_trim(price, 5)

    # Construct the UPC-A barcode for Goodwill with a "4" prefix
    vwupc = "4{}{}".format(code, price)
    
    # Append the UPC-A checksum
    return vwupc + str(upcean.validate.validate_upca_checksum(vwupc, True))

def make_goodwill_to_ean13_barcode(code, price):
    # Generate UPC-A barcode and convert it to EAN-13
    upca_barcode = make_goodwill_to_upca_barcode(code, price)
    return convert_barcode_from_upca_to_ean13(upca_barcode)

def make_goodwill_to_itf14_barcode(code, price):
    # Generate UPC-A barcode and convert it to ITF-14
    upca_barcode = make_goodwill_to_upca_barcode(code, price)
    return convert_barcode_from_upca_to_itf14(upca_barcode)


def make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value):
    # Ensure numbersystem is either "5" or "9"
    numbersystem = "5" if str(numbersystem) not in {"5", "9"} else str(numbersystem)
    
    # Pad and trim manufacturer, family, and value fields
    manufacturer = pad_and_trim(manufacturer, 5)
    family = pad_and_trim(family, 3)
    value = pad_and_trim(value, 2)
    
    # Construct UPC-A coupon barcode with the calculated checksum
    coupon_upca = "{}{}{}{}".format(numbersystem, manufacturer, family, value)
    return coupon_upca + str(upcean.validate.validate_upca_checksum(coupon_upca, True))

def make_coupon_to_ean13_barcode(numbersystem, manufacturer, family, value):
    # Convert UPC-A coupon barcode to EAN-13
    upca_barcode = make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value)
    return convert_barcode_from_upca_to_ean13(upca_barcode)

def make_coupon_to_itf14_barcode(numbersystem, manufacturer, family, value):
    # Convert UPC-A coupon barcode to ITF-14
    upca_barcode = make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value)
    return convert_barcode_from_upca_to_itf14(upca_barcode)


'''
// NDC (National Drug Codes)
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''


def make_ndc_to_upca_barcode(labeler, product, package):
    # Pad and trim labeler, product, and package to required lengths
    labeler = pad_and_trim(labeler, 4)
    product = pad_and_trim(product, 4)
    package = pad_and_trim(package, 2)
    
    # Construct UPC-A NDC barcode with the calculated checksum
    ndc_upca = "3{}{}{}".format(labeler, product, package)
    return ndc_upca + str(upcean.validate.validate_upca_checksum(ndc_upca, True))

def make_ndc_to_ean13_barcode(labeler, product, package):
    # Generate UPC-A NDC barcode and convert it to EAN-13
    upca_barcode = make_ndc_to_upca_barcode(labeler, product, package)
    return convert_barcode_from_upca_to_ean13(upca_barcode)

def make_ndc_to_itf14_barcode(labeler, product, package):
    # Generate UPC-A NDC barcode and convert it to ITF-14
    upca_barcode = make_ndc_to_upca_barcode(labeler, product, package)
    return convert_barcode_from_upca_to_itf14(upca_barcode)

def convert_barcode_from_ndc_to_upca(upc):
    # Strip non-numeric characters and pad/trim to 10 digits
    upc = re.sub("\\D", "", str(upc))
    upc = pad_and_trim(upc, 10)

    # Construct UPC-A NDC barcode with "3" prefix and calculate checksum
    ndc_upca = "3" + upc
    return ndc_upca + str(upcean.validate.validate_upca_checksum(ndc_upca, True))

def convert_barcode_from_upca_to_ndc(upc):
    # Ensure upc is a valid UPC-A with an "NDC" prefix (starts with "3")
    upc = re.sub("\\D", "", str(upc))
    if not upcean.validate.validate_upca_checksum(upc) or not re.match("^3\\d{10}$", upc):
        return False

    # Extract NDC from the UPC-A
    return upc[1:11]  # Skip the "3" prefix

def convert_barcode_from_ndc_to_ean13(upc):
    # Convert NDC to UPC-A and then to EAN-13
    upca_barcode = convert_barcode_from_ndc_to_upca(upc)
    return convert_barcode_from_upca_to_ean13(upca_barcode)

def convert_barcode_from_ndc_to_itf14(upc):
    # Convert NDC to UPC-A and then to ITF-14
    upca_barcode = convert_barcode_from_ndc_to_upca(upc)
    return convert_barcode_from_upca_to_itf14(upca_barcode)
