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

    $FileInfo: convert.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import upcean.validate


def make_upca_barcode(numbersystem, manufacturer, product):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    product = str(product)
    if(len(numbersystem) < 1 or len(manufacturer) < 5 or len(product) < 5):
        return False
    if(len(numbersystem) > 1):
        fix_matches = re.findall(r"^(\d{1})", numbersystem)
        numbersystem = fix_matches[0]
    if(len(manufacturer) > 5):
        fix_matches = re.findall(r"^(\d{5})", manufacturer)
        manufacturer = fix_matches[0]
    if(len(product) > 5):
        fix_matches = re.findall(r"^(\d{5})", product)
        product = fix_matches[0]
    upc = numbersystem+manufacturer+product
    upc = upc+str(upcean.validate.validate_upca_checksum(upc, True))
    return upc


def make_ean13_barcode(numbersystem, manufacturer, product):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    product = str(product)
    if(len(numbersystem) < 2 or len(manufacturer) < 5 or len(product) < 5):
        return False
    if(len(numbersystem) > 2):
        fix_matches = re.findall(r"^(\d{2})", numbersystem)
        numbersystem = fix_matches[0]
    if(len(manufacturer) > 5):
        fix_matches = re.findall(r"^(\d{5})", manufacturer)
        manufacturer = fix_matches[0]
    if(len(product) > 5):
        fix_matches = re.findall(r"^(\d{5})", product)
        product = fix_matches[0]
    upc = numbersystem+manufacturer+product
    upc = upc+str(upcean.validate.validate_ean13_checksum(upc, True))
    return upc


def make_itf14_barcode(numbersystem, manufacturer, product):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    product = str(product)
    if(len(numbersystem) < 3 or len(manufacturer) < 5 or len(product) < 5):
        return False
    if(len(numbersystem) > 3):
        fix_matches = re.findall(r"^(\d{3})", numbersystem)
        numbersystem = fix_matches[0]
    if(len(manufacturer) > 5):
        fix_matches = re.findall(r"^(\d{5})", manufacturer)
        manufacturer = fix_matches[0]
    if(len(product) > 5):
        fix_matches = re.findall(r"^(\d{5})", product)
        product = fix_matches[0]
    upc = numbersystem+manufacturer+product
    upc = upc+str(upcean.validate.validate_itf14_checksum(upc, True))
    return upc


def make_ean8_barcode(numbersystem, manufacturer, product):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    product = str(product)
    if(len(numbersystem) < 1 or len(manufacturer) < 3 or len(product) < 3):
        return False
    if(len(numbersystem) > 1):
        fix_matches = re.findall(r"^(\d{1})", numbersystem)
        numbersystem = fix_matches[0]
    if(len(manufacturer) > 3):
        fix_matches = re.findall(r"^(\d{3})", manufacturer)
        manufacturer = fix_matches[0]
    if(len(product) > 3):
        fix_matches = re.findall(r"^(\d{3})", product)
        product = fix_matches[0]
    upc = numbersystem+manufacturer+product
    upc = upc+str(upcean.validate.validate_ean8_checksum(upc, True))
    return upc


def make_upce_barcode(numbersystem, manufacturer, product):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    product = str(product)
    if(len(numbersystem) < 1 or len(manufacturer) < 3 or len(product) < 3):
        return False
    if(len(numbersystem) > 1):
        fix_matches = re.findall(r"^(\d{1})", numbersystem)
        numbersystem = fix_matches[0]
    if(len(manufacturer) > 3):
        fix_matches = re.findall(r"^(\d{3})", manufacturer)
        manufacturer = fix_matches[0]
    if(len(product) > 3):
        fix_matches = re.findall(r"^(\d{3})", product)
        product = fix_matches[0]
    upc = numbersystem+manufacturer+product
    upc = upc+str(upcean.validate.validate_upce_checksum(upc, True))
    return upc


def convert_barcode_from_upce_to_upca(upc):
    upc = str(upc)
    if(len(upc) == 7):
        upc = upc+str(upcean.validate.validate_upce_checksum(upc, True))
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not re.findall(r"^(0|1)", upc)):
        return False
    if(not upcean.validate.validate_upce_checksum(upc)):
        return False
    if(re.findall(r"(0|1)(\d{5})([0-3])(\d{1})", upc)):
        upc_matches = re.findall(
            r"(0|1)(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc)
        upc_matches = upc_matches[0]
        if(int(upc_matches[6]) == 0):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6] + \
                "0000"+upc_matches[3]+upc_matches[4] + \
                upc_matches[5]+upc_matches[7]
        if(int(upc_matches[6]) == 1):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6] + \
                "0000"+upc_matches[3]+upc_matches[4] + \
                upc_matches[5]+upc_matches[7]
        if(int(upc_matches[6]) == 2):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[6] + \
                "0000"+upc_matches[3]+upc_matches[4] + \
                upc_matches[5]+upc_matches[7]
        if(int(upc_matches[6]) == 3):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2] + \
                upc_matches[3]+"00000"+upc_matches[4] + \
                upc_matches[5]+upc_matches[7]
    if(re.findall(r"(0|1)(\d{5})([4-9])(\d{1})", upc)):
        upc_matches = re.findall(
            r"(0|1)(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})(\d{1})", upc)
        upc_matches = upc_matches[0]
        if(int(upc_matches[6]) == 4):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2] + \
                upc_matches[3]+upc_matches[4]+"00000" + \
                upc_matches[5]+upc_matches[7]
        if(int(upc_matches[6]) == 5):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3] + \
                upc_matches[4]+upc_matches[5]+"0000" + \
                upc_matches[6]+upc_matches[7]
        if(int(upc_matches[6]) == 6):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3] + \
                upc_matches[4]+upc_matches[5]+"0000" + \
                upc_matches[6]+upc_matches[7]
        if(int(upc_matches[6]) == 7):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3] + \
                upc_matches[4]+upc_matches[5]+"0000" + \
                upc_matches[6]+upc_matches[7]
        if(int(upc_matches[6]) == 8):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3] + \
                upc_matches[4]+upc_matches[5]+"0000" + \
                upc_matches[6]+upc_matches[7]
        if(int(upc_matches[6]) == 9):
            upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+upc_matches[3] + \
                upc_matches[4]+upc_matches[5]+"0000" + \
                upc_matches[6]+upc_matches[7]
    return upce


def convert_barcode_from_upca_to_ean13(upc):
    upc = str(upc)
    if(len(upc) == 11):
        upc = upc+str(upcean.validate.validate_upca_checksum(upc, True))
    if(len(upc) > 13 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    if(len(upc) == 12):
        ean13 = "0"+upc
    if(len(upc) == 13):
        ean13 = upc
    return ean13


def convert_barcode_from_ean13_to_itf14(upc):
    upc = str(upc)
    if(len(upc) == 11):
        upc = upc+str(upcean.validate.validate_upca_checksum(upc, True))
    if(len(upc) == 12):
        upc = "0"+upc
    if(len(upc) > 14 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    if(len(upc) == 13):
        itf14 = "0"+upc
    if(len(upc) == 14):
        itf14 = upc
    return itf14


def convert_barcode_from_upce_to_ean13(upc):
    upc = str(upc)
    return convert_barcode_from_upca_to_ean13(convert_barcode_from_upce_to_upca(upc))


def convert_barcode_from_upce_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upce_to_ean13(upc))


def convert_barcode_from_upca_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_upca_to_ean13(upc))


def convert_barcode_from_ean13_to_upca(upc):
    upc = str(upc)
    if(len(upc) == 12):
        upc = "0"+upc
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not upcean.validate.validate_ean13_checksum(upc)):
        return False
    if(not re.findall(r"^0(\d{12})", upc)):
        return False
    if(re.findall(r"^0(\d{12})", upc)):
        upc_matches = re.findall(r"^0(\d{12})", upc)
        upca = upc_matches[0]
    return upca


def convert_barcode_from_itf14_to_ean13(upc):
    upc = str(upc)
    if(len(upc) == 13):
        upc = "0"+upc
    if(len(upc) > 14 or len(upc) < 14):
        return False
    if(not upcean.validate.validate_itf14_checksum(upc)):
        return False
    if(not re.findall(r"^(\d{1})(\d{12})(\d{1})", upc)):
        return False
    if(re.findall(r"^(\d{1})(\d{12})(\d{1})", upc)):
        upc_matches = re.findall(r"^(\d{1})(\d{12})(\d{1})", upc)
        upc_matches = upc_matches[0]
        ean13 = upc_matches[1] + \
            str(upcean.validate.validate_ean13_checksum(upc_matches[1], True))
    return ean13


def convert_barcode_from_upca_to_upce(upc):
    upc = str(upc)
    if(len(upc) == 11):
        upc = upc+str(upcean.validate.validate_upca_checksum(upc, True))
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    if(not re.findall(r"(0|1)(\d{11})", upc)):
        return False
    upce = None
    if(re.findall(r"(0|1)(\d{2})00000(\d{3})(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{2})00000(\d{3})(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"0"
        upce = upce+upc_matches[3]
        return upce
    if(re.findall(r"(0|1)(\d{2})10000(\d{3})(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{2})10000(\d{3})(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"1"
        upce = upce+upc_matches[3]
        return upce
    if(re.findall(r"(0|1)(\d{2})20000(\d{3})(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{2})20000(\d{3})(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"2"
        upce = upce+upc_matches[3]
        return upce
    if(re.findall(r"(0|1)(\d{3})00000(\d{2})(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{3})00000(\d{2})(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"3"
        upce = upce+upc_matches[3]
        return upce
    if(re.findall(r"(0|1)(\d{4})00000(\d{1})(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{4})00000(\d{1})(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+upc_matches[2]+"4"
        upce = upce+upc_matches[3]
        return upce
    if(re.findall(r"(0|1)(\d{5})00005(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{5})00005(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+"5"
        upce = upce+upc_matches[2]
        return upce
    if(re.findall(r"(0|1)(\d{5})00006(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{5})00006(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+"6"
        upce = upce+upc_matches[2]
        return upce
    if(re.findall(r"(0|1)(\d{5})00007(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{5})00007(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+"7"
        upce = upce+upc_matches[2]
        return upce
    if(re.findall(r"(0|1)(\d{5})00008(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{5})00008(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+"8"
        upce = upce+upc_matches[2]
        return upce
    if(re.findall(r"(0|1)(\d{5})00009(\d{1})", upc)):
        upc_matches = re.findall(r"(0|1)(\d{5})00009(\d{1})", upc)
        upc_matches = upc_matches[0]
        upce = upc_matches[0]+upc_matches[1]+"9"
        upce = upce+upc_matches[2]
        return upce
    if(upce is None):
        return False
    return upce


def convert_barcode_from_ean13_to_upce(upc):
    upc = str(upc)
    return convert_barcode_from_upca_to_upce(convert_barcode_from_ean13_to_upca(upc))


def convert_barcode_from_itf14_to_upca(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_upca(convert_barcode_from_itf14_to_ean13(upc))


def convert_barcode_from_itf14_to_upce(upc):
    upc = str(upc)
    return convert_barcode_from_upca_to_upce(convert_barcode_from_itf14_to_upca(upc))


'''
// Changing a EAN-8 code to UPC-A and EAN-13 based on whats used at:
// Source: http://www.upcdatabase.com/
'''


def convert_barcode_from_ean8_to_upca(upc):
    upc = str(upc)
    if(len(upc) == 7):
        upc = upc+str(upcean.validate.validate_ean8_checksum(upc, True))
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not upcean.validate.validate_ean8_checksum(upc)):
        return False
    upca = "0000"+upc
    return upca


def convert_barcode_from_ean8_to_ean13(upc):
    upc = str(upc)
    return convert_barcode_from_upca_to_ean13(convert_barcode_from_ean8_to_upca(upc))


def convert_barcode_from_ean8_to_itf14(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_itf14(convert_barcode_from_ean8_to_ean13(upc))


def convert_barcode_from_upca_to_ean8(upc):
    upc = str(upc)
    if(len(upc) == 11):
        upc = upc+str(upcean.validate.validate_upca_checksum(upc, True))
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    if(not re.findall(r"^0000(\d{8})", upc)):
        return False
    if(re.findall(r"^0000(\d{8})", upc)):
        upc_matches = re.findall(r"^0000(\d{8})", upc)
        ean8 = upc_matches[0]
    return ean8


def convert_barcode_from_ean13_to_ean8(upc):
    upc = str(upc)
    return convert_barcode_from_upca_to_ean8(convert_barcode_from_ean13_to_upca(upc))


def convert_barcode_from_itf14_to_ean8(upc):
    upc = str(upc)
    return convert_barcode_from_ean13_to_ean8(convert_barcode_from_itf14_to_ean13(upc))


'''
// Code 128
// Source: http://www.barcodeisland.com/code128.phtml
// Source: http://en.wikipedia.org/wiki/Code_128
'''


def convert_ascii_code128_to_hex_code128(upc):
    upc = str(upc)
    if(len(upc) < 4):
        return False
    hextoascii = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V",
                  '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36",
                  'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    barcodeout = ""
    for upcpart in upc:
        barcodeout = barcodeout + asciitohex.get(upcpart, '')
    return barcodeout


def convert_hex_code128_to_ascii_code128(upc):
    upc = str(upc)
    if(len(upc) < 8):
        return False
    hextoascii = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V",
                  '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': "Ã", '60': "Ä", '61': "Å", '62': "Æ", '63': "Ç", '64': "È", '65': "É", '66': "Ê", '67': "Ë", '68': "Ì", '69': "Í", '6a': "Î", '6b': "Ï", '6c': "Ó", '6d': "Ò"}
    asciitohex = {' ': "00", '!': "01", '"': "02", '#': "03", '$': "04", '%': "05", '&': "06", '\'': "07", '(': "08", ')': "09", '*': "0a", '+': "0b", ',': "0c", '-': "0d", '.': "0e", '/': "0f", '0': "10", '1': "11", '2': "12", '3': "13", '4': "14", '5': "15", '6': "16", '7': "17", '8': "18", '9': "19", ':': "1a", ';': "1b", '<': "1c", '=': "1d", '>': "1e", '?': "1f", '@': "20", 'A': "21", 'B': "22", 'C': "23", 'D': "24", 'E': "25", 'F': "26", 'G': "27", 'H': "28", 'I': "29", 'J': "2a", 'K': "2b", 'L': "2c", 'M': "2d", 'N': "2e", 'O': "2f", 'P': "30", 'Q': "31", 'R': "32", 'S': "33", 'T': "34", 'U': "35", 'V': "36",
                  'W': "37", 'X': "38", 'Y': "39", 'Z': "3a", '[': "3b", '\\': "3c", ']': "3d", '^': "3e", '_': "3f", '`': "40", 'a': "41", 'b': "42", 'c': "43", 'd': "44", 'e': "45", 'f': "46", 'g': "47", 'h': "48", 'i': "49", 'j': "4a", 'k': "4b", 'l': "4c", 'm': "4d", 'n': "4e", 'o': "4f", 'p': "50", 'q': "51", 'r': "52", 's': "53", 't': "54", 'u': "55", 'v': "56", 'w': "57", 'x': "58", 'y': "59", 'z': "5a", '{': "5b", '|': "5c", '}': "5d", '~': "5e", 'Ã': "5f", 'Ä': "60", 'Å': "61", 'Æ': "62", 'Ç': "63", 'È': "64", 'É': "65", 'Ê': "66", 'Ë': "67", 'Ì': "68", 'Í': "69", 'Î': "6a", 'Ï': "6b", 'Ó': "6c", 'Ò': "6d"}
    barcodeout = ""
    for upcpart in upc:
        barcodeout = barcodeout + hextoascii.get(upcpart, '')
    return barcodeout


def convert_text_to_hex_code128(upc):
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


def convert_text_to_hex_code128_manual(upc):
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


def convert_text_to_hex_code128_with_checksum(upc):
    code128out = convert_text_to_hex_code128(upc)
    if(not code128out):
        return False
    return code128out+"6d"+upcean.validate.get_code128_checksum(code128out)+"6c"


def convert_text_to_hex_code128_manual_with_checksum(upc):
    code128out = convert_text_to_hex_code128_manual(upc)
    if(not code128out):
        return False
    return code128out+"6d"+upcean.validate.get_code128_checksum(code128out)+"6c"


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
        fix_matches = re.findall(r"^(\d{7})", upc)
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
    if(not re.findall(r"/^977(\d{7})/", upc)):
        return False
    if(re.findall(r"^977(\d{7})", upc)):
        upc_matches = re.findall(r"^977(\d{7})", upc)
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
        fix_matches = re.findall(r"^(\d{8})", upc)
        upc = fix_matches[1]
    if(len(upc) > 8 or len(upc) < 8):
        return False
    if(not re.findall(r"^(\d{4})(\d{4})", upc)):
        return False
    issn_matches = re.findall(r"^(\d{4})(\d{4})", upc)
    issn_matches = issn_matches[0]
    issn8 = issn_matches[0]+"-"+issn_matches[1]
    return issn8


def print_issn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall(r"^(\d{13})", upc)
        upc = fix_matches[1]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall(r"^(\d{3})(\d{4})(\d{4})(\d{2})", upc)):
        return False
    issn_matches = re.findall(r"^(\d{3})(\d{4})(\d{4})(\d{2})", upc)
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
        fix_matches = re.findall(r"^(\d{9})", upc)
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
    if(not re.findall(r"^978(\d{9})", upc)):
        return False
    if(re.findall(r"^978(\d{9})", upc)):
        upc_matches = re.findall(r"^978(\d{9})", upc)
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
        fix_matches = re.findall(r"^(\d{9})(\d{1}|X{1})", upc)
        fix_matches = fix_matches[0]
        upc = fix_matches[0]+fix_matches[1]
    if(len(upc) > 10 or len(upc) < 10):
        return False
    if(not re.findall(r"^(\d{1})(\d{3})(\d{5})(\d{1}|X{1})", upc)):
        return False
    isbn_matches = re.findall(r"^(\d{1})(\d{3})(\d{5})(\d{1}|X{1})", upc)
    isbn_matches = isbn_matches[0]
    isbn10 = isbn_matches[0]+"-"+isbn_matches[1] + \
        "-"+isbn_matches[2]+"-"+isbn_matches[3]
    return isbn10


def print_isbn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall(r"^(\d{13})", upc)
        upc = fix_matches[1]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall(r"^(\d{3})(\d{1})(\d{3})(\d{5})(\d{1})", upc)):
        return False
    isbn_matches = re.findall(r"^(\d{3})(\d{1})(\d{3})(\d{5})(\d{1})", upc)
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
        fix_matches = re.findall(r"^(\d{8})", upc)
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
    if(not re.findall(r"^9790(\d{8})", upc)):
        return False
    if(re.findall(r"^9790(\d{8})", upc)):
        upc_matches = re.findall(r"^9790(\d{8})", upc)
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
        fix_matches = re.findall(r"^(\d{9})", upc)
        upc = fix_matches[0]
    if(len(upc) > 9 or len(upc) < 9):
        return False
    if(not re.findall(r"^(\d{4})(\d{4})(\d{1})", upc)):
        return False
    ismn_matches = re.findall(r"^(\d{4})(\d{4})(\d{1})", upc)
    ismn_matches = ismn_matches[0]
    ismn10 = "M-"+ismn_matches[0]+"-"+ismn_matches[1]+"-"+ismn_matches[2]
    return ismn10


def print_ismn13_barcode(upc):
    upc = str(upc)
    if(len(upc) > 13):
        fix_matches = re.findall(r"^(\d{13})", upc)
        upc = fix_matches[0]
    if(len(upc) > 13 or len(upc) < 13):
        return False
    if(not re.findall(r"^(\d{3})(\d{1})(\d{4})(\d{4})(\d{1})", upc)):
        return False
    ismn_matches = re.findall(r"^(\d{3})(\d{1})(\d{4})(\d{4})(\d{1})", upc)
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
    code = str(code)
    price = str(price)
    if(len(code) > 5):
        if(re.findall(r"^(\d{5})", code)):
            code_matches = re.findall(r"^(\d{5})", code)
            code = code_matches[0]
    if(len(price) > 4):
        if(re.findall(r"^(\d{4})", price)):
            price_matches = re.findall(r"^(\d{4})", price)
            price = price_matches[0]
    pricecs = str(upcean.validate.get_vw_price_checksum(price))
    vwupc = "2"+code+pricecs+price.zfill(4)
    vwupc = vwupc+str(upcean.validate.validate_upca_checksum(vwupc, True))
    return vwupc


def make_vw_to_upca_barcode(code, price):
    return make_upca_vw_to_upca_barcode(code, price)


def make_upca_vw_to_ean13_barcode(code, price):
    code = str(code)
    price = str(price)
    vwean13 = convert_barcode_from_upca_to_ean13(
        make_upca_vw_to_upca_barcode(code, price))
    return vwean13


def make_vw_to_ean13_barcode(code, price):
    return make_upca_vw_to_ean13_barcode(code, price)


def make_upca_vw_to_itf14_barcode(code, price):
    code = str(code)
    price = str(price)
    vwitf14 = convert_barcode_from_upca_to_itf14(
        make_upca_vw_to_upca_barcode(code, price))
    return vwitf14


def make_vw_to_itf14_barcode(code, price):
    return make_upca_vw_to_itf14_barcode(code, price)


'''
// Get variable weight price checksum for EAN-13
// Source: https://softmatic.com/barcode-ean-13.html#ean-country
'''


def make_ean13_vw_to_ean13_barcode(numbersystem, code, price):
    code = str(code)
    price = str(price)
    numbersystem = str(numbersystem)
    if(len(numbersystem) > 1):
        if(re.findall(r"^(\d{1})", numbersystem)):
            ns_matches = re.findall(r"^(\d{1})", numbersystem)
            numbersystem = ns_matches[0]
    if(len(code) > 5):
        if(re.findall(r"^(\d{5})", code)):
            code_matches = re.findall(r"^(\d{5})", code)
            code = code_matches[0]
    if(len(price) > 5):
        if(re.findall(r"^(\d{5})", price)):
            price_matches = re.findall(r"^(\d{5})", price)
            price = price_matches[0]
    vwupc = "2"+numbersystem+code+price.zfill(5)
    vwupc = vwupc+str(upcean.validate.validate_ean13_checksum(vwupc, True))
    return vwupc


def make_ean13_vw_to_itf14_barcode(numbersystem, code, price):
    code = str(code)
    price = str(price)
    vwitf14 = convert_barcode_from_upca_to_itf14(
        make_ean13_vw_to_upca_barcode(numbersystem, code, price))
    return vwitf14


def make_goodwill_to_upca_barcode(code, price):
    code = str(code)
    price = str(price)
    if(len(code) > 5):
        if(re.findall(r"^(\d{5})", code)):
            code_matches = re.findall(r"^(\d{5})", code)
            code = code_matches[0]
    if(len(price) > 5):
        if(re.findall(r"^(\d{5})", price)):
            price_matches = re.findall(r"^(\d{5})", price)
            price = price_matches[0]
    vwupc = "4"+code+price.zfill(5)
    vwupc = vwupc+str(upcean.validate.validate_upca_checksum(vwupc, True))
    return vwupc


def make_goodwill_to_ean13_barcode(code, price):
    code = str(code)
    price = str(price)
    vwean13 = convert_barcode_from_upca_to_ean13(
        make_goodwill_to_upca_barcode(code, price))
    return vwean13


def make_goodwill_to_itf14_barcode(code, price):
    code = str(code)
    price = str(price)
    vwitf14 = convert_barcode_from_upca_to_itf14(
        make_goodwill_to_upca_barcode(code, price))
    return vwitf14


def make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    family = str(family)
    value = str(value)
    if(int(numbersystem) != 5 and int(numbersystem) != 9):
        numbersystem = "5"
    if(len(manufacturer) > 5):
        fix_matches = re.findall(r"^(\d{5})", manufacturer)
        upc = fix_matches[0]
    if(len(family) > 3):
        fix_matches = re.findall(r"^(\d{3})", family)
        upc = fix_matches[0]
    if(len(value) > 2):
        fix_matches = re.findall(r"^(\d{2})", value)
        upc = fix_matches[0]
    couponupca = numbersystem+manufacturer+family+value
    couponupca = couponupca + \
        str(upcean.validate.validate_upca_checksum(couponupca, True))
    return couponupca


def make_coupon_to_ean13_barcode(numbersystem, manufacturer, family, value):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    family = str(family)
    value = str(value)
    couponean13 = convert_barcode_from_upca_to_ean13(
        make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value))
    return couponean13


def make_coupon_to_itf14_barcode(numbersystem, manufacturer, family, value):
    numbersystem = str(numbersystem)
    manufacturer = str(manufacturer)
    family = str(family)
    value = str(value)
    couponitf14 = convert_barcode_from_upca_to_itf14(
        make_coupon_to_upca_barcode(numbersystem, manufacturer, family, value))
    return couponitf14


'''
// NDC (National Drug Codes)
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''


def make_ndc_to_upca_barcode(labeler, product, package):
    labeler = str(labeler)
    product = str(product)
    package = str(package)
    if(len(labeler) > 4):
        if(re.findall(r"^(\d{4})", labeler)):
            labeler_matches = re.findall(r"^(\d{4})", labeler)
            labeler = labeler_matches[0]
    if(len(product) > 4):
        if(re.findall(r"^(\d{4})", product)):
            product_matches = re.findall(r"^(\d{4})", product)
            product = product_matches[0]
    if(len(package) > 2):
        if(re.findall(r"^(\d{2})", package)):
            package_matches = re.findall(r"^(\d{2})", package)
            package = package_matches[0]
    ndcupc = "3"+labeler+product+package
    ndcupc = ndcupc+str(upcean.validate.validate_upca_checksum(ndcupc, True))
    return ndcupc


def make_ndc_to_ean13_barcode(labeler, product, package):
    labeler = str(labeler)
    product = str(product)
    package = str(package)
    ndcean13 = convert_barcode_from_upca_to_ean13(
        make_ndc_to_upca_barcode(labeler, product, package))
    return ndcean13


def make_ndc_to_itf14_barcode(labeler, product, package):
    labeler = str(labeler)
    product = str(product)
    package = str(package)
    ndcitf14 = convert_barcode_from_upca_to_itf14(
        make_ndc_to_upca_barcode(labeler, product, package))
    return ndcitf14


def convert_barcode_from_ndc_to_upca(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    if(len(upc) > 10):
        fix_matches = re.findall(r"^(\d{10})", upc)
        upc = fix_matches[0]
    ndcupca = "3"+upc + \
        str(upcean.validate.validate_upca_checksum("3"+upc, True))
    return ndcupca


def convert_barcode_from_upca_to_ndc(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    if(not upcean.validate.validate_upca_checksum(upc)):
        return False
    if(not re.findall(r"^3(\d{10})", upc)):
        return False
    if(re.findall(r"^3(\d{10})", upc)):
        upc_matches = re.findall(r"^3(\d{10})", upc)
        ndc = upc_matches[0]
    return ndc


def convert_barcode_from_ndc_to_ean13(upc):
    upc = str(upc)
    ndcean13 = convert_barcode_from_upca_to_ean13(
        convert_barcode_from_ndc_to_upca(upc))
    return ndcean13


def convert_barcode_from_ndc_to_itf14(upc):
    upc = str(upc)
    ndcitf14 = convert_barcode_from_upca_to_itf14(
        convert_barcode_from_ndc_to_upca(upc))
    return ndcitf14


def print_ndc_barcode(upc):
    upc = str(upc)
    upc = upc.replace("-", "")
    if(len(upc) > 10):
        fix_matches = re.findall(r"^(\d{10})", upc)
        upc = fix_matches[0]
    if(len(upc) > 10 or len(upc) < 10):
        return False
    if(not re.findall(r"^(\d{4})(\d{4})(\d{2})", upc)):
        return False
    ndc_matches = re.findall(r"^(\d{4})(\d{4})(\d{2})", upc)
    ndc_matches = ndc_matches[0]
    ndc = ndc_matches[0]+"-"+ndc_matches[1]+"-"+ndc_matches[2]
    return ndc


def print_convert_barcode_from_upca_to_ndc(upc):
    upc = str(upc)
    ndc = print_ndc_barcode(convert_barcode_from_upca_to_ndc(upc))
    return ndc
