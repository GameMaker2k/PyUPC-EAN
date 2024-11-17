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

    $FileInfo: code128.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.predraw import *
import re
import sys
import upcean.support

import io
try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or pillowsupport):
    import upcean.predraw.prepil
if(cairosupport):
    import upcean.predraw.precairo
if(qahirahsupport):
    import upcean.predraw.preqahirah
if(svgwritesupport):
    import upcean.predraw.presvgwrite
if(wandsupport):
    import upcean.predraw.prewand
if(magicksupport):
    import upcean.predraw.premagick


def get_code128_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) > 2 or len(upc) < 2):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc)
    if(len(upc_matches) <= 0):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    reswoshift = (((29 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((29 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code128_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(inimage is None):
        upc_img = None
        upc_preimg = None
    else:
        upc_img = inimage[0]
        upc_preimg = inimage[1]
    imageoutlib = None
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif qahirahsupport and isinstance(upc_img, qah.Context) and isinstance(upc_preimg, qah.Surface):
        imageoutlib = "qahirah"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif wandsupport and isinstance(upc_img, wImage):
        imageoutlib = "wand"
    elif magicksupport and isinstance(upc_img, PythonMagick.Image):
        imageoutlib = "magick"
    elif pgmagicksupport and isinstance(upc_img, pgmagick.Image):
        imageoutlib = "pgmagick"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and inimage != "none" and inimage is not None):
        imageoutlib = None
    elif(inimage == "none" or inimage is None):
        imageoutlib = None
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(len(upc) % 2):
        return False
    if(len(upc) < 8):
        return False
    if(not re.findall("([0-9a-f]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        vertical_text_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        vertical_text_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick") or (pgmagicksupport and imageoutlib == "pgmagick")):
        vertical_text_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and imageoutlib == "svgwrite"):
        vertical_text_fix = (8 * (int(resize) * barwidth[1]))
    else:
        vertical_text_fix = 0
    vertical_text_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc = upc.lower()
    if(not re.findall("[0-9a-f]{2}", upc)):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc)
    upc_to_dec = list([int(x, 16) for x in upc_matches])
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((29 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code128", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0] * 14
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    BarNum = 0
    # Draw the start barcode
    start_barcode = [0] * 14
    upc_array['code'].append(start_barcode)
    barsizeloop = []
    LineSizeType = 0
    for bar in start_barcode:
        if bar == 1:
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        else:
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    # Optimized Mappings
    hextocharsetone = {
        '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&",
        '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-",
        '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4",
        '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";",
        '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B",
        '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I",
        '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P",
        '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W",
        '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^",
        '3f': "_", '40': " ", '41': " ", '42': " ", '43': " ", '44': " ", '45': " ",
        '46': " ", '47': " ", '48': " ", '49': " ", '4a': " ", '4b': " ", '4c': " ",
        '4d': " ", '4e': " ", '4f': " ", '50': " ", '51': " ", '52': " ", '53': " ",
        '54': " ", '55': " ", '56': " ", '57': " ", '58': " ", '59': " ", '5a': " ",
        '5b': " ", '5c': " ", '5d': " ", '5e': " ", '5f': " ", '60': " ", '61': " ",
        '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ",
        '69': " ", '6a': " ", '6b': " ", '6c': " "
    }
    hextocharsettwo = {
        '00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&",
        '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-",
        '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4",
        '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";",
        '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B",
        '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I",
        '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P",
        '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U", '36': "V", '37': "W",
        '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^",
        '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e",
        '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l",
        '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s",
        '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z",
        '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': " ", '60': " ", '61': " ",
        '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ",
        '69': " ", '6a': " ", '6b': " ", '6c': " "
    }
    hextocharsetthree = {
        '00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05",
        '06': "06", '07': "07", '08': "08", '09': "09", '0a': "10", '0b': "11",
        '0c': "12", '0d': "13", '0e': "14", '0f': "15", '10': "16", '11': "17",
        '12': "18", '13': "19", '14': "20", '15': "21", '16': "22", '17': "23",
        '18': "24", '19': "25", '1a': "26", '1b': "27", '1c': "28", '1d': "29",
        '1e': "30", '1f': "31", '20': "32", '21': "33", '22': "34", '23': "35",
        '24': "36", '25': "37", '26': "38", '27': "39", '28': "40", '29': "41",
        '2a': "42", '2b': "43", '2c': "44", '2d': "45", '2e': "46", '2f': "47",
        '30': "48", '31': "49", '32': "50", '33': "51", '34': "52", '35': "53",
        '36': "54", '37': "55", '38': "56", '39': "57", '3a': "58", '3b': "59",
        '3c': "60", '3d': "61", '3e': "62", '3f': "63", '40': "64", '41': "65",
        '42': "66", '43': "67", '44': "68", '45': "69", '46': "70", '47': "71",
        '48': "72", '49': "73", '4a': "74", '4b': "75", '4c': "76", '4d': "77",
        '4e': "78", '4f': "79", '50': "80", '51': "81", '52': "82", '53': "83",
        '54': "84", '55': "85", '56': "86", '57': "87", '58': "88", '59': "89",
        '5a': "90", '5b': "91", '5c': "92", '5d': "93", '5e': "94", '5f': "95",
        '60': "96", '61': "97", '62': "98", '63': "99", '64': " ", '65': " ",
        '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ",
        '6c': " "
    }
    hextocharsetfour = {
        '00': "32", '01': "33", '02': "34", '03': "35", '04': "36", '05': "37",
        '06': "38", '07': "39", '08': "40", '09': "41", '0a': "42", '0b': "43",
        '0c': "44", '0d': "45", '0e': "46", '0f': "47", '10': "48", '11': "49",
        '12': "50", '13': "51", '14': "52", '15': "53", '16': "54", '17': "55",
        '18': "56", '19': "57", '1a': "58", '1b': "59", '1c': "60", '1d': "61",
        '1e': "62", '1f': "63", '20': "64", '21': "65", '22': "66", '23': "67",
        '24': "68", '25': "69", '26': "70", '27': "71", '28': "72", '29': "73",
        '2a': "74", '2b': "75", '2c': "76", '2d': "77", '2e': "78", '2f': "79",
        '30': "80", '31': "81", '32': "82", '33': "83", '34': "84", '35': "85",
        '36': "86", '37': "87", '38': "88", '39': "89", '3a': "90", '3b': "91",
        '3c': "92", '3d': "93", '3e': "94", '3f': "95", '40': "96", '41': "97",
        '42': "98", '43': "99", '44': "100", '45': "101", '46': "102", '47': "103",
        '48': "104", '49': "105", '4a': "106", '4b': "107", '4c': "108", '4d': "109",
        '4e': "110", '4f': "111", '50': "112", '51': "113", '52': "114", '53': "115",
        '54': "116", '55': "117", '56': "118", '57': "119", '58': "120", '59': "121",
        '5a': "122", '5b': "123", '5c': "124", '5d': "125", '5e': "126", '5f': "195",
        '60': "196", '61': "197", '62': "198", '63': "199", '64': "200", '65': "201",
        '66': "202", '67': "203", '68': "204", '69': "205", '6a': "127", '6b': "128",
        '6c': "129"
    }
    hextoaltdigit = {
        '00': 32, '01': 33, '02': 34, '03': 35, '04': 36, '05': 37, '06': 38,
        '07': 39, '08': 40, '09': 41, '0a': 42, '0b': 43, '0c': 44, '0d': 45,
        '0e': 46, '0f': 47, '10': 48, '11': 49, '12': 50, '13': 51, '14': 52,
        '15': 53, '16': 54, '17': 55, '18': 56, '19': 57, '1a': 58, '1b': 59,
        '1c': 60, '1d': 61, '1e': 62, '1f': 63, '20': 64, '21': 65, '22': 66,
        '23': 67, '24': 68, '25': 69, '26': 70, '27': 71, '28': 72, '29': 73,
        '2a': 74, '2b': 75, '2c': 76, '2d': 77, '2e': 78, '2f': 79, '30': 80,
        '31': 81, '32': 82, '33': 83, '34': 84, '35': 85, '36': 86, '37': 87,
        '38': 88, '39': 89, '3a': 90, '3b': 91, '3c': 92, '3d': 93, '3e': 94,
        '3f': 95, '40': 96, '41': 97, '42': 98, '43': 99, '44': 100, '45': 101,
        '46': 102, '47': 103, '48': 104, '49': 105, '4a': 106, '4b': 107,
        '4c': 108, '4d': 109, '4e': 110, '4f': 111, '50': 112, '51': 113,
        '52': 114, '53': 115, '54': 116, '55': 117, '56': 118, '57': 119,
        '58': 120, '59': 121, '5a': 122, '5b': 123, '5c': 124, '5d': 125,
        '5e': 126, '5f': 195, '60': 196, '61': 197, '62': 198, '63': 199,
        '64': 200, '65': 201, '66': 202, '67': 203, '68': 204, '69': 205,
        '6a': "127", '6b': "128", '6c': "129"
    }
    hextodecnum = {
        '00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7,
        '08': 8, '09': 9, '0a': 10, '0b': 11, '0c': 12, '0d': 13, '0e': 14,
        '0f': 15, '10': 16, '11': 17, '12': 18, '13': 19, '14': 20, '15': 21,
        '16': 22, '17': 23, '18': 24, '19': 25, '1a': 26, '1b': 27, '1c': 28,
        '1d': 29, '1e': 30, '1f': 31, '20': 32, '21': 33, '22': 34, '23': 35,
        '24': 36, '25': 37, '26': 38, '27': 39, '28': 40, '29': 41, '2a': 42,
        '2b': 43, '2c': 44, '2d': 45, '2e': 46, '2f': 47, '30': 48, '31': 49,
        '32': 50, '33': 51, '34': 52, '35': 53, '36': 54, '37': 55, '38': 56,
        '39': 57, '3a': 58, '3b': 59, '3c': 60, '3d': 61, '3e': 62, '3f': 63,
        '40': 64, '41': 65, '42': 66, '43': 67, '44': 68, '45': 69, '46': 70,
        '47': 71, '48': 72, '49': 73, '4a': 74, '4b': 75, '4c': 76, '4d': 77,
        '4e': 78, '4f': 79, '50': 80, '51': 81, '52': 82, '53': 83, '54': 84,
        '55': 85, '56': 86, '57': 87, '58': 88, '59': 89, '5a': 90, '5b': 91,
        '5c': 92, '5d': 93, '5e': 94, '5f': 95, '60': 96, '61': 97, '62': 98,
        '63': 99, '64': " ", '65': " ", '66': " ", '67': " ", '68': " ",
        '69': " ", '6a': " ", '6b': " ", '6c': " "
    }
    decnumtohex = {
        0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07',
        8: '08', 9: '09', 10: '0a', 11: '0b', 12: '0c', 13: '0d', 14: '0e',
        15: '0f', 16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15',
        22: '16', 23: '17', 24: '18', 25: '19', 26: '1a', 27: '1b', 28: '1c',
        29: '1d', 30: '1e', 31: '1f', 32: '20', 33: '21', 34: '22', 35: '23',
        36: '24', 37: '25', 38: '26', 39: '27', 40: '28', 41: '29', 42: '2a',
        43: '2b', 44: '2c', 45: '2d', 46: '2e', 47: '2f', 48: '30', 49: '31',
        50: '32', 51: '33', 52: '34', 53: '35', 54: '36', 55: '37', 56: '38',
        57: '39', 58: '3a', 59: '3b', 60: '3c', 61: '3d', 62: '3e', 63: '3f',
        64: '40', 65: '41', 66: '42', 67: '43', 68: '44', 69: '45', 70: '46',
        71: '47', 72: '48', 73: '49', 74: '4a', 75: '4b', 76: '4c', 77: '4d',
        78: '4e', 79: '4f', 80: '50', 81: '51', 82: '52', 83: '53', 84: '54',
        85: '55', 86: '56', 87: '57', 88: '58', 89: '59', 90: '5a', 91: '5b',
        92: '5c', 93: '5d', 94: '5e', 95: '5f', 96: '60', 97: '61', 98: '62',
        99: '63'
    }
    decnumalttohex = {
        32: '00', 194: '00', 207: '00', 212: '00', 252: '00', 33: '01', 34: '02',
        35: '03', 36: '04', 37: '05', 38: '06', 39: '07', 40: '08', 41: '09',
        42: '0a', 43: '0b', 44: '0c', 45: '0d', 46: '0e', 47: '0f', 48: '10',
        49: '11', 50: '12', 51: '13', 52: '14', 53: '15', 54: '16', 55: '17',
        56: '18', 57: '19', 58: '1a', 59: '1b', 60: '1c', 61: '1d', 62: '1e',
        63: '1f', 64: '20', 65: '21', 66: '22', 67: '23', 68: '24', 69: '25',
        70: '26', 71: '27', 72: '28', 73: '29', 74: '2a', 75: '2b', 76: '2c',
        77: '2d', 78: '2e', 79: '2f', 80: '30', 81: '31', 82: '32', 83: '33',
        84: '34', 85: '35', 86: '36', 87: '37', 88: '38', 89: '39', 90: '3a',
        91: '3b', 92: '3c', 93: '3d', 94: '3e', 95: '3f', 96: '40', 97: '41',
        98: '42', 99: '43', 100: '44', 101: '45', 102: '46', 103: '47',
        104: '48', 105: '49', 106: '4a', 107: '4b', 108: '4c', 109: '4d',
        110: '4e', 111: '4f', 112: '50', 113: '51', 114: '52', 115: '53',
        116: '54', 117: '55', 118: '56', 119: '57', 120: '58', 121: '59',
        122: '5a', 123: '5b', 124: '5c', 125: '5d', 126: '5e', 195: '5f',
        200: '5f', 240: '5f', 196: '60', 201: '60', 241: '60', 197: '61',
        202: '61', 242: '61', 198: '62', 203: '62', 243: '62', 199: '63',
        204: '63', 244: '63', 200: '64', 205: '64', 245: '64', 201: '65',
        206: '65', 246: '65', 202: '66', 207: '66', 247: '66', 203: '67',
        208: '67', 248: '67', 204: '68', 209: '68', 249: '68', 205: '69',
        210: '69', 250: '69', '6a': "127", '6b': "128", '6c': "129"
    }
    codecharset = [hextocharsetone, hextocharsettwo, hextocharsetthree, hextocharsetfour]
    upc_print = []
    shift_cur_set = False
    start_shift = 0
    NumZero = 0
    cur_set = 0
    BarNum = 0
    left_barcolor_map = {
        "00": [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        "01": [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
        "02": [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
        "03": [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
        "04": [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
        "05": [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
        "06": [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
        "07": [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
        "08": [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
        "09": [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        "0a": [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        "0b": [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        "0c": [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        "0d": [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        "0e": [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0],
        "0f": [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
        "10": [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0],
        "11": [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
        "12": [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
        "13": [1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0],
        "14": [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        "15": [1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
        "16": [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        "17": [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        "18": [1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0],
        "19": [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0],
        "1a": [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        "1b": [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
        "1c": [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        "1d": [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0],
        "1e": [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
        "1f": [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        "20": [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0],
        "21": [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
        "22": [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        "23": [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0],
        "24": [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
        "25": [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
        "26": [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
        "27": [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        "28": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        "29": [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        "2a": [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
        "2b": [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        "2c": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
        "2d": [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0],
        "2e": [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0],
        "2f": [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
        "30": [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        "31": [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0],
        "32": [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
        "33": [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
        "34": [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        "35": [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        "36": [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0],
        "37": [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
        "38": [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
        "39": [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
        "3a": [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0],
        "3b": [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0],
        "3c": [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        "3d": [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        "3e": [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0],
        "3f": [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        "40": [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
        "41": [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        "42": [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
        "43": [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        "44": [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
        "45": [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
        "46": [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
        "47": [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
        "48": [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
        "49": [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
        "4a": [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0],
        "4b": [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        "4c": [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        "4d": [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        "4e": [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        "4f": [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
        "50": [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
        "51": [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
        "52": [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0],
        "53": [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
        "54": [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        "55": [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
        "56": [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
        "57": [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        "58": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0],
        "59": [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
        "5a": [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
        "5b": [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        "5c": [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0],
        "5d": [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
        "5e": [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        "5f": [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0],
        "60": [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0],
        "61": [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
        "62": [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
        "63": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        "64": [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        "65": [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        "66": [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
        "67": [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        "68": [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        "69": [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0],
        "6a": [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0],
        "6b": [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
        "6c": [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        "6d": []  # Assuming an empty list as per original code
    }
    cur_set_change_map = {
        "62": "toggle",
        "63": "set_to_2_if_0_or_1",
        "64": "set_to_1_if_0_or_2",
        "65": "set_to_0_if_1_or_2",
        "67": "set_to_0",
        "68": "set_to_1",
        "69": "set_to_2",
        "6d": "set_to_3"
    }
    barcode_is_rev = False;
    while NumZero < len(upc_matches):
        old_cur_set = cur_set
        if start_shift:
            cur_set = shift_cur_set
        upc_value = upc_matches[NumZero]
        left_barcolor = left_barcolor_map.get(upc_value, [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0])
        # Handle cur_set changes
        if upc_value in cur_set_change_map:
            change = cur_set_change_map[upc_value]
            if change == "toggle":
                cur_set = 1 - cur_set
            elif change == "set_to_2_if_0_or_1" and cur_set in [0, 1]:
                cur_set = 2
            elif change == "set_to_1_if_0_or_2" and cur_set in [0, 2]:
                cur_set = 1
            elif change == "set_to_0_if_1_or_2" and cur_set in [1, 2]:
                cur_set = 0
            elif change == "set_to_0":
                cur_set = 0
            elif change == "set_to_1":
                cur_set = 1
            elif change == "set_to_2":
                cur_set = 2
            elif change == "set_to_3":
                cur_set = 3
            # Specific handling for "62" as per original code
            if upc_value == "62":
                shift_cur_set = cur_set
                start_shift = 1
                cur_set = old_cur_set
        # Append to upc_print based on cur_set and upc_to_dec
        dec_num = upc_to_dec[NumZero]
        if cur_set < len(codecharset):
            charset = codecharset[cur_set]
            if upc_value in charset:
                if (cur_set == 0 and dec_num < 64) or \
                   (cur_set == 1 and dec_num < 95) or \
                   (cur_set == 2 and dec_num < 100):
                    upc_print.append(charset[upc_value])
                else:
                    upc_print.append(" ")
            else:
                upc_print.append(" ")
        else:
            upc_print.append(" ")
        # Handle post-processing cur_set changes
        if upc_value in ["63", "64", "65", "66", "67", "68", "69", "6a", "6b", "6c", "6d"]:
            if upc_value == "63":
                left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0]
                if cur_set in [0, 1]:
                    cur_set = 2
            elif upc_value == "64":
                left_barcolor = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0]
                if cur_set in [0, 2]:
                    cur_set = 1
            elif upc_value == "65":
                left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
                if cur_set in [1, 2]:
                    cur_set = 0
            elif upc_value == "66":
                left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
            elif upc_value == "67":
                left_barcolor = [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
                cur_set = 0
            elif upc_value == "68":
                left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
                cur_set = 1
            elif upc_value == "69":
                left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0]
                cur_set = 2
            elif upc_value == "6a":
                barcode_is_rev = False;
                left_barcolor = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]
            elif upc_value == "6b":
                barcode_is_rev = True;
                left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0]
            elif upc_value == "6c":
                barcode_is_rev = False;
                left_barcolor = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1]
            elif upc_value == "6d":
                left_barcolor = []
                cur_set = 3
        # Draw the bar colors
        if(len(left_barcolor)>0):
            upc_array['code'].append(left_barcolor)
        barsizeloop = []
        for color in left_barcolor:
            if color == 1:
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            else:
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            barsizeloop.append(LineSizeType)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
        # Reset cur_set if shift was applied
        if start_shift:
            cur_set = old_cur_set
            start_shift = 0
        NumZero += 1
        if(len(left_barcolor)>0):
            upc_array['barsize'].append(barsizeloop)
    # Define the mappings for left_barcolor and cur_set changes
    # (Already defined above)
    # Draw the end barcode
    end_barcode = [0] * 15
    upc_array['code'].append(end_barcode)
    barsizeloop = []
    for bar in end_barcode:
        if bar == 1:
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        else:
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart, LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)

    NumTxtZero = 0
    LineTxtStart = ((shiftxy[0] + 16) * int(resize))
    LineTxtStartNorm = 16
    if(barcode_is_rev):
        upc_print.reverse()
    while (NumTxtZero < len(upc_print)):
        texthidden = False
        if hidetext:
            texthidden = True
        if(len(upc_print[NumTxtZero]) == 1):
            if(not texthidden):
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
        barheight[0] * int(resize)),  upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
            upc_array['text']['location'].append(LineTxtStartNorm)
            upc_array['text']['text'].append(upc_print[NumTxtZero])
            upc_array['text']['type'].append("txt")
            LineTxtStart += 11 * int(resize)
            LineTxtStartNorm += 11
        if(len(upc_print[NumTxtZero]) == 2):
            if(not texthidden):
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
        barheight[0] * int(resize)),  upc_print[NumTxtZero][0], barcolor[1], "ocrb", imageoutlib)
            LineTxtStart += 6 * int(resize)
            upc_array['text']['location'].append(LineTxtStartNorm)
            upc_array['text']['text'].append(upc_print[NumTxtZero][0])
            upc_array['text']['type'].append("txt")
            LineTxtStart += 11 * int(resize)
            LineTxtStartNorm += 6
            if(not texthidden):
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
        barheight[0] * int(resize)),  upc_print[NumTxtZero][1], barcolor[1], "ocrb", imageoutlib)
            LineTxtStart += 5 * int(resize)
            upc_array['text']['location'].append(LineTxtStartNorm)
            upc_array['text']['text'].append(upc_print[NumTxtZero][1])
            upc_array['text']['type'].append("txt")
            LineTxtStart += 11 * int(resize)
            LineTxtStartNorm += 5
        NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_code128_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    upc_low = upc.lower()
    if(not re.findall("[0-9a-f]{2}", upc_low)):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc_low)
    upc_to_dec = list([int(x, 16) for x in upc_matches])
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((29 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code128_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib]

def create_code128_barcode(upc, outfile="./code128.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "svgwrite"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "svgwrite"
    if(not qahirahsupport and imageoutlib == "qahirah"):
        imageoutlib = "svgwrite"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "svgwrite"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "svgwrite"
    if(not wandsupport and imageoutlib == "wand"):
        imageoutlib = "svgwrite"
    if(not magicksupport and imageoutlib == "magick"):
        imageoutlib = "svgwrite"
    if(not pgmagicksupport and imageoutlib == "pgmagick"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and imageoutlib != "svgwrite"):
        imageoutlib = "svgwrite"
    if(not pilsupport and not cairosupport):
        imageoutlib = "svgwrite"
    if(outfile is None):
        if(imageoutlib == "cairosvg"):
            oldoutfile = None
            outfile = None
            outfileext = "SVG"
        else:
            oldoutfile = None
            outfile = None
            outfileext = None
    else:
        oldoutfile = upcean.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    imgout = draw_code128_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, "code128; "+upc, imageoutlib)
    return True


def get_code128old_barcode_size(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1)):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(len(upc) > 2 or len(upc) < 2):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc)
    if(len(upc_matches) <= 0):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    reswoshift = (((29 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
    reswshift = ((((29 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize))
    return {'without_shift': reswoshift, 'with_shift': reswshift}


def encode_code128old_barcode(inimage, upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False)):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(inimage is None):
        upc_img = None
        upc_preimg = None
    else:
        upc_img = inimage[0]
        upc_preimg = inimage[1]
    imageoutlib = None
    if pilsupport and isinstance(upc_img, ImageDraw.ImageDraw) and isinstance(upc_preimg, Image.Image):
        imageoutlib = "pillow"
    elif cairosupport and isinstance(upc_img, cairo.Context) and isinstance(upc_preimg, cairo.Surface):
        imageoutlib = "cairo"
    elif qahirahsupport and isinstance(upc_img, qah.Context) and isinstance(upc_preimg, qah.Surface):
        imageoutlib = "qahirah"
    elif svgwritesupport and isinstance(upc_img, svgwrite.Drawing):
        imageoutlib = "svgwrite"
    elif wandsupport and isinstance(upc_img, wImage):
        imageoutlib = "wand"
    elif magicksupport and isinstance(upc_img, PythonMagick.Image):
        imageoutlib = "magick"
    elif pgmagicksupport and isinstance(upc_img, pgmagick.Image):
        imageoutlib = "pgmagick"
    elif(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and inimage != "none" and inimage is not None):
        imageoutlib = None
    elif(inimage == "none" or inimage is None):
        imageoutlib = None
    elif(not pilsupport and not cairosupport and not svgwritesupport):
        return False
    else:
        return False
    if(len(upc) % 2):
        return False
    if(len(upc) < 8):
        return False
    if(not re.findall("([0-9a-f]+)", upc)):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        vertical_text_fix = 0
    elif((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")) or (svgwritesupport and cairosvgsupport and imageoutlib == "svgwrite") or (qahirahsupport and imageoutlib == "qahirah")):
        vertical_text_fix = (9 * (int(resize) * barwidth[1]))
    elif((wandsupport and imageoutlib == "wand") or (magicksupport and imageoutlib == "magick") or (pgmagicksupport and imageoutlib == "pgmagick")):
        vertical_text_fix = (10 * (int(resize) * barwidth[1]))
    elif(svgwritesupport and imageoutlib == "svgwrite"):
        vertical_text_fix = (8 * (int(resize) * barwidth[1]))
    else:
        vertical_text_fix = 0
    vertical_text_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc = upc.lower()
    if(not re.findall("[0-9a-f]{2}", upc)):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc)
    upc_to_dec = list([int(x, 16) for x in upc_matches])
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    if(inimage is not None):
        drawColorRectangle(upc_img, 0 + (shiftxy[0] * barwidth[0]) * int(resize), 0 + (shiftxy[1] * barwidth[1]) * int(resize), (((29 + shiftxy[0]) * barwidth[0]) + upc_size_add) * int(resize), ((barheightadd + shiftxy[1]) + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    upc_array = {'upc': upc, 'heightadd': 9, 'type': "code128", 'barsize': [], 'code': [], 'text': {'location': [], 'text': [], 'type': []}}
    LineSize = (barheight[0] + shiftxy[1]) * int(resize)
    if(hidetext):
        LineSize = (barheight[1] + shiftxy[1]) * int(resize)
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(start_barcode)
    LineStart = (shiftxy[0] * barwidth[0]) * int(resize)
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    barsizeloop = []
    LineSizeType = 0
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    NumZero = 0
    cur_set = 0
    hextocharsetone = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U",
                       '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': " ", '41': " ", '42': " ", '43': " ", '44': " ", '45': " ", '46': " ", '47': " ", '48': " ", '49': " ", '4a': " ", '4b': " ", '4c': " ", '4d': " ", '4e': " ", '4f': " ", '50': " ", '51': " ", '52': " ", '53': " ", '54': " ", '55': " ", '56': " ", '57': " ", '58': " ", '59': " ", '5a': " ", '5b': " ", '5c': " ", '5d': " ", '5e': " ", '5f': " ", '60': " ", '61': " ", '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " "}
    hextocharsettwo = {'00': " ", '01': "!", '02': "\"", '03': "#", '04': "$", '05': "%", '06': "&", '07': "'", '08': "(", '09': ")", '0a': "*", '0b': "+", '0c': ",", '0d': "-", '0e': ".", '0f': "/", '10': "0", '11': "1", '12': "2", '13': "3", '14': "4", '15': "5", '16': "6", '17': "7", '18': "8", '19': "9", '1a': ":", '1b': ";", '1c': "<", '1d': "=", '1e': ">", '1f': "?", '20': "@", '21': "A", '22': "B", '23': "C", '24': "D", '25': "E", '26': "F", '27': "G", '28': "H", '29': "I", '2a': "J", '2b': "K", '2c': "L", '2d': "M", '2e': "N", '2f': "O", '30': "P", '31': "Q", '32': "R", '33': "S", '34': "T", '35': "U",
                       '36': "V", '37': "W", '38': "X", '39': "Y", '3a': "Z", '3b': "[", '3c': "\\", '3d': "]", '3e': "^", '3f': "_", '40': "`", '41': "a", '42': "b", '43': "c", '44': "d", '45': "e", '46': "f", '47': "g", '48': "h", '49': "i", '4a': "j", '4b': "k", '4c': "l", '4d': "m", '4e': "n", '4f': "o", '50': "p", '51': "q", '52': "r", '53': "s", '54': "t", '55': "u", '56': "v", '57': "w", '58': "x", '59': "y", '5a': "z", '5b': "{", '5c': "|", '5d': "}", '5e': "~", '5f': " ", '60': " ", '61': " ", '62': " ", '63': " ", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " "}
    hextocharsetthree = {'00': "00", '01': "01", '02': "02", '03': "03", '04': "04", '05': "05", '06': "06", '07': "07", '08': "08", '09': "09", '0a': "10", '0b': "11", '0c': "12", '0d': "13", '0e': "14", '0f': "15", '10': "16", '11': "17", '12': "18", '13': "19", '14': "20", '15': "21", '16': "22", '17': "23", '18': "24", '19': "25", '1a': "26", '1b': "27", '1c': "28", '1d': "29", '1e': "30", '1f': "31", '20': "32", '21': "33", '22': "34", '23': "35", '24': "36", '25': "37", '26': "38", '27': "39", '28': "40", '29': "41", '2a': "42", '2b': "43", '2c': "44", '2d': "45", '2e': "46", '2f': "47", '30': "48", '31': "49", '32': "50", '33': "51", '34': "52",
                         '35': "53", '36': "54", '37': "55", '38': "56", '39': "57", '3a': "58", '3b': "59", '3c': "60", '3d': "61", '3e': "62", '3f': "63", '40': "64", '41': "65", '42': "66", '43': "67", '44': "68", '45': "69", '46': "70", '47': "71", '48': "72", '49': "73", '4a': "74", '4b': "75", '4c': "76", '4d': "77", '4e': "78", '4f': "79", '50': "80", '51': "81", '52': "82", '53': "83", '54': "84", '55': "85", '56': "86", '57': "87", '58': "88", '59': "89", '5a': "90", '5b': "91", '5c': "92", '5d': "93", '5e': "94", '5f': "95", '60': "96", '61': "97", '62': "98", '63': "99", '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " "}
    hextocharsetfour = {'00': "32", '00': "194", '00': "207", '00': "212", '00': "252", '01': "33", '02': "34", '03': "35", '04': "36", '05': "37", '06': "38", '07': "39", '08': "40", '09': "41", '0a': "42", '0b': "43", '0c': "44", '0d': "45", '0e': "46", '0f': "47", '10': "48", '11': "49", '12': "50", '13': "51", '14': "52", '15': "53", '16': "54", '17': "55", '18': "56", '19': "57", '1a': "58", '1b': "59", '1c': "60", '1d': "61", '1e': "62", '1f': "63", '20': "64", '21': "65", '22': "66", '23': "67", '24': "68", '25': "69", '26': "70", '27': "71", '28': "72", '29': "73", '2a': "74", '2b': "75", '2c': "76", '2d': "77", '2e': "78", '2f': "79", '30': "80", '31': "81", '32': "82", '33': "83", '34': "84", '35': "85", '36': "86", '37': "87", '38': "88", '39': "89", '3a': "90", '3b': "91", '3c': "92", '3d': "93", '3e': "94", '3f': "95", '40': "96",
                        '41': "97", '42': "98", '43': "99", '44': "100", '45': "101", '46': "102", '47': "103", '48': "104", '49': "105", '4a': "106", '4b': "107", '4c': "108", '4d': "109", '4e': "110", '4f': "111", '50': "112", '51': "113", '52': "114", '53': "115", '54': "116", '55': "117", '56': "118", '57': "119", '58': "120", '59': "121", '5a': "122", '5b': "123", '5c': "124", '5d': "125", '5e': "126", '5f': "195", '5f': "200", '5f': "240", '60': "196", '60': "201", '60': "241", '61': "197", '61': "202", '61': "242", '62': "198", '62': "203", '62': "243", '63': "199", '63': "204", '63': "244", '64': "200", '64': "205", '64': "245", '65': "201", '65': "206", '65': "246", '66': "202", '66': "207", '66': "247", '67': "203", '67': "208", '67': "248", '68': "204", '68': "209", '68': "249", '69': "205", '69': "210", '69': "250", '6a': "127", '6b': "128", '6c': "129"}
    hextoaltdigit = {'00': 32, '00': 194, '00': 207, '00': 212, '00': 252, '01': 33, '02': 34, '03': 35, '04': 36, '05': 37, '06': 38, '07': 39, '08': 40, '09': 41, '0a': 42, '0b': 43, '0c': 44, '0d': 45, '0e': 46, '0f': 47, '10': 48, '11': 49, '12': 50, '13': 51, '14': 52, '15': 53, '16': 54, '17': 55, '18': 56, '19': 57, '1a': 58, '1b': 59, '1c': 60, '1d': 61, '1e': 62, '1f': 63, '20': 64, '21': 65, '22': 66, '23': 67, '24': 68, '25': 69, '26': 70, '27': 71, '28': 72, '29': 73, '2a': 74, '2b': 75, '2c': 76, '2d': 77, '2e': 78, '2f': 79, '30': 80, '31': 81, '32': 82, '33': 83, '34': 84, '35': 85, '36': 86, '37': 87, '38': 88, '39': 89, '3a': 90, '3b': 91, '3c': 92, '3d': 93, '3e': 94, '3f': 95, '40': 96, '41': 97,
                     '42': 98, '43': 99, '44': 100, '45': 101, '46': 102, '47': 103, '48': 104, '49': 105, '4a': 106, '4b': 107, '4c': 108, '4d': 109, '4e': 110, '4f': 111, '50': 112, '51': 113, '52': 114, '53': 115, '54': 116, '55': 117, '56': 118, '57': 119, '58': 120, '59': 121, '5a': 122, '5b': 123, '5c': 124, '5d': 125, '5e': 126, '5f': 195, '5f': 200, '5f': 240, '60': 196, '60': 201, '60': 241, '61': 197, '61': 202, '61': 242, '62': 198, '62': 203, '62': 243, '63': 199, '63': 204, '63': 244, '64': 200, '64': 205, '64': 245, '65': 201, '65': 206, '65': 246, '66': 202, '66': 207, '66': 247, '67': 203, '67': 208, '67': 248, '68': 204, '68': 209, '68': 249, '69': 205, '69': 210, '69': 250, '6a': "127", '6b': "128", '6c': "129"}
    hextodecnum = {'00': 0, '01': 1, '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9, '0a': 10, '0b': 11, '0c': 12, '0d': 13, '0e': 14, '0f': 15, '10': 16, '11': 17, '12': 18, '13': 19, '14': 20, '15': 21, '16': 22, '17': 23, '18': 24, '19': 25, '1a': 26, '1b': 27, '1c': 28, '1d': 29, '1e': 30, '1f': 31, '20': 32, '21': 33, '22': 34, '23': 35, '24': 36, '25': 37, '26': 38, '27': 39, '28': 40, '29': 41, '2a': 42, '2b': 43, '2c': 44, '2d': 45, '2e': 46, '2f': 47, '30': 48, '31': 49, '32': 50, '33': 51, '34': 52, '35': 53, '36': 54,
                   '37': 55, '38': 56, '39': 57, '3a': 58, '3b': 59, '3c': 60, '3d': 61, '3e': 62, '3f': 63, '40': 64, '41': 65, '42': 66, '43': 67, '44': 68, '45': 69, '46': 70, '47': 71, '48': 72, '49': 73, '4a': 74, '4b': 75, '4c': 76, '4d': 77, '4e': 78, '4f': 79, '50': 80, '51': 81, '52': 82, '53': 83, '54': 84, '55': 85, '56': 86, '57': 87, '58': 88, '59': 89, '5a': 90, '5b': 91, '5c': 92, '5d': 93, '5e': 94, '5f': 95, '60': 96, '61': 97, '62': 98, '63': 99, '64': " ", '65': " ", '66': " ", '67': " ", '68': " ", '69': " ", '6a': " ", '6b': " ", '6c': " "}
    decnumtohex = {0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '0a', 11: '0b', 12: '0c', 13: '0d', 14: '0e', 15: '0f', 16: '10', 17: '11', 18: '12', 19: '13', 20: '14', 21: '15', 22: '16', 23: '17', 24: '18', 25: '19', 26: '1a', 27: '1b', 28: '1c', 29: '1d', 30: '1e', 31: '1f', 32: '20', 33: '21', 34: '22', 35: '23', 36: '24', 37: '25', 38: '26', 39: '27', 40: '28', 41: '29', 42: '2a', 43: '2b', 44: '2c', 45: '2d', 46: '2e', 47: '2f', 48: '30', 49: '31', 50: '32', 51: '33', 52: '34', 53: '35', 54: '36',
                   55: '37', 56: '38', 57: '39', 58: '3a', 59: '3b', 60: '3c', 61: '3d', 62: '3e', 63: '3f', 64: '40', 65: '41', 66: '42', 67: '43', 68: '44', 69: '45', 70: '46', 71: '47', 72: '48', 73: '49', 74: '4a', 75: '4b', 76: '4c', 77: '4d', 78: '4e', 79: '4f', 80: '50', 81: '51', 82: '52', 83: '53', 84: '54', 85: '55', 86: '56', 87: '57', 88: '58', 89: '59', 90: '5a', 91: '5b', 92: '5c', 93: '5d', 94: '5e', 95: '5f', 95: '5f', 95: '5f', 96: '60', 96: '60', 96: '60', 97: '61', 97: '61', 97: '61', 98: '62', 98: '62', 98: '62', 99: '63', 99: '63', 99: '63'}
    decnumalttohex = {32: '00', 194: '00', 207: '00', 212: '00', 252: '00', 33: '01', 34: '02', 35: '03', 36: '04', 37: '05', 38: '06', 39: '07', 40: '08', 41: '09', 42: '0a', 43: '0b', 44: '0c', 45: '0d', 46: '0e', 47: '0f', 48: '10', 49: '11', 50: '12', 51: '13', 52: '14', 53: '15', 54: '16', 55: '17', 56: '18', 57: '19', 58: '1a', 59: '1b', 60: '1c', 61: '1d', 62: '1e', 63: '1f', 64: '20', 65: '21', 66: '22', 67: '23', 68: '24', 69: '25', 70: '26', 71: '27', 72: '28', 73: '29', 74: '2a', 75: '2b', 76: '2c', 77: '2d', 78: '2e', 79: '2f', 80: '30', 81: '31', 82: '32', 83: '33', 84: '34', 85: '35', 86: '36', 87: '37', 88: '38', 89: '39', 90: '3a', 91: '3b', 92: '3c', 93: '3d', 94: '3e', 95: '3f',
                      96: '40', 97: '41', 98: '42', 99: '43', 100: '44', 101: '45', 102: '46', 103: '47', 104: '48', 105: '49', 106: '4a', 107: '4b', 108: '4c', 109: '4d', 110: '4e', 111: '4f', 112: '50', 113: '51', 114: '52', 115: '53', 116: '54', 117: '55', 118: '56', 119: '57', 120: '58', 121: '59', 122: '5a', 123: '5b', 124: '5c', 125: '5d', 126: '5e', 195: '5f', 200: '5f', 240: '5f', 196: '60', 201: '60', 241: '60', 197: '61', 202: '61', 242: '61', 198: '62', 203: '62', 243: '62', 199: '63', 204: '63', 244: '63', 200: '64', 205: '64', 245: '64', 201: '65', 206: '65', 246: '65', 202: '66', 207: '66', 247: '66', 203: '67', 208: '67', 248: '67', 204: '68', 209: '68', 249: '68', 205: '69', 210: '69', 250: '69'}
    codecharset = [hextocharsetone, hextocharsettwo,
                   hextocharsetthree,  hextocharsetfour]
    upc_print = []
    shift_cur_set = False
    start_shift = 0
    barcode_is_rev = False;
    while (NumZero < len(upc_matches)):
        old_cur_set = cur_set
        if(start_shift == 1):
            cur_set = shift_cur_set
        left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "00"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "01"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "02"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "03"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "04"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "05"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "06"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "07"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "08"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "09"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "0a"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "0b"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "0c"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "0d"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "0e"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "0f"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "10"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "11"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "12"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "13"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "14"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "15"):
            left_barcolor = [1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "16"):
            left_barcolor = [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "17"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "18"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "19"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "1a"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "1b"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "1c"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "1d"):
            left_barcolor = [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "1e"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "1f"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "20"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "21"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "22"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "23"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "24"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "25"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "26"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "27"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "28"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "29"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "2a"):
            left_barcolor = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "2b"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "2c"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "2d"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "2e"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "2f"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "30"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "31"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "32"):
            left_barcolor = [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "33"):
            left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "34"):
            left_barcolor = [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "35"):
            left_barcolor = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "36"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "37"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "38"):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "39"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "3a"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "3b"):
            left_barcolor = [1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "3c"):
            left_barcolor = [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "3d"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "3e"):
            left_barcolor = [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "3f"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "40"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "41"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "42"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "43"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "44"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "45"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "46"):
            left_barcolor = [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "47"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "48"):
            left_barcolor = [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "49"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "4a"):
            left_barcolor = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "4b"):
            left_barcolor = [1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "4c"):
            left_barcolor = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        if(upc_matches[NumZero] == "4d"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "4e"):
            left_barcolor = [1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "4f"):
            left_barcolor = [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "50"):
            left_barcolor = [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "51"):
            left_barcolor = [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
        if(upc_matches[NumZero] == "52"):
            left_barcolor = [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "53"):
            left_barcolor = [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "54"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "55"):
            left_barcolor = [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "56"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "57"):
            left_barcolor = [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0]
        if(upc_matches[NumZero] == "58"):
            left_barcolor = [1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "59"):
            left_barcolor = [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "5a"):
            left_barcolor = [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "5b"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0]
        if(upc_matches[NumZero] == "5c"):
            left_barcolor = [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "5d"):
            left_barcolor = [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "5e"):
            left_barcolor = [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "5f"):
            left_barcolor = [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "60"):
            left_barcolor = [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0]
        if(upc_matches[NumZero] == "61"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "62"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0]
            old_cur_set = cur_set
            if(cur_set == 0):
                cur_set = 1
            if(cur_set == 1):
                cur_set = 0
            shift_cur_set = cur_set
            start_shift = 1
            cur_set = old_cur_set
        if(cur_set == 0 and upc_to_dec[NumZero] < 64):
            upc_print.append(codecharset[cur_set][upc_matches[NumZero]])
        elif(cur_set == 1 and upc_to_dec[NumZero] < 95):
            upc_print.append(codecharset[cur_set][upc_matches[NumZero]])
        elif(cur_set == 2 and upc_to_dec[NumZero] < 100):
            upc_print.append(codecharset[cur_set][upc_matches[NumZero]])
        else:
            upc_print.append(" ")
        if(upc_matches[NumZero] == "63"):
            left_barcolor = [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0]
            if(cur_set == 0 or cur_set == 1):
                cur_set = 2
        if(upc_matches[NumZero] == "64"):
            left_barcolor = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0]
            if(cur_set == 0 or cur_set == 2):
                cur_set = 1
        if(upc_matches[NumZero] == "65"):
            left_barcolor = [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0]
            if(cur_set == 1 or cur_set == 2):
                cur_set = 0
        if(upc_matches[NumZero] == "66"):
            left_barcolor = [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
        if(upc_matches[NumZero] == "67"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]
            cur_set = 0
        if(upc_matches[NumZero] == "68"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
            cur_set = 1
        if(upc_matches[NumZero] == "69"):
            left_barcolor = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0]
            cur_set = 2
        if(upc_matches[NumZero] == "6a"):
            barcode_is_rev = False;
            left_barcolor = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0]
        if(upc_matches[NumZero] == "6b"):
            barcode_is_rev = True;
            left_barcolor = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0]
        if(upc_matches[NumZero] == "6c"):
            barcode_is_rev = False;
            left_barcolor = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1]
        if(upc_matches[NumZero] == "6d"):
            left_barcolor = []
            cur_set = 3
        if(start_shift == 1):
            cur_set = old_cur_set
            start_shift = 0
        if(len(left_barcolor)>0):
            upc_array['code'].append(left_barcolor)
        InnerUPCNum = 0
        barsizeloop = []
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
            barsizeloop.append(LineSizeType)
            LineStart += barwidth[0] * int(resize)
            BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    if(len(left_barcolor)>0):
        upc_array['barsize'].append(barsizeloop)
    end_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    upc_array['code'].append(end_barcode)
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    barsizeloop = []
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, (4 + shiftxy[1]) * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        barsizeloop.append(LineSizeType)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    upc_array['barsize'].append(barsizeloop)
    if(not hidetext):
        if(svgwritesupport and imageoutlib == "svgwrite"):
            try:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrb, "OCRB")
            except OSError:
                upcean.predraw.presvgwrite.embed_font(upc_img, fontpathocrbalt, "OCRB")
        if(barcode_is_rev):
            upc_print.reverse()
        NumTxtZero = 0
        LineTxtStart = 16 * int(resize)
        LineTxtStartNorm = 16
        if(barcode_is_rev):
            upc_print.reverse()
        while (NumTxtZero < len(upc_print)):
            if(len(upc_print[NumTxtZero]) == 1):
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  upc_print[NumTxtZero], barcolor[1], "ocrb", imageoutlib)
                upc_array['text']['location'].append(LineTxtStartNorm)
                upc_array['text']['text'].append(upc_print[NumTxtZero])
                upc_array['text']['type'].append("txt")
                LineTxtStart += 11 * int(resize)
                LineTxtStartNorm += 11
            if(len(upc_print[NumTxtZero]) == 2):
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  upc_print[NumTxtZero][0], barcolor[1], "ocrb", imageoutlib)
                LineTxtStart += 6 * int(resize)
                upc_array['text']['location'].append(LineTxtStartNorm)
                upc_array['text']['text'].append(upc_print[NumTxtZero][0])
                upc_array['text']['type'].append("txt")
                LineTxtStart += 11 * int(resize)
                LineTxtStartNorm += 6
                drawColorText(upc_img, 10 * int(resize * barwidth[1]), LineTxtStart * barwidth[0], vertical_text_fix + (
            barheight[0] * int(resize)),  upc_print[NumTxtZero][1], barcolor[1], "ocrb", imageoutlib)
                LineTxtStart += 5 * int(resize)
                upc_array['text']['location'].append(LineTxtStartNorm)
                upc_array['text']['text'].append(upc_print[NumTxtZero][1])
                upc_array['text']['type'].append("txt")
                LineTxtStart += 11 * int(resize)
                LineTxtStartNorm += 5
            NumTxtZero += 1
    if((cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg"))):
        upc_preimg.flush()
    if(imageoutlib is None):
        return upc_array
    else:
        return [upc_img, upc_preimg, imageoutlib]


def draw_code128old_barcode(upc, resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "svgwrite"):
        imageoutlib = "pillow"
    upc_low = upc.lower()
    if(not re.findall("[0-9a-f]{2}", upc_low)):
        return False
    upc_matches = re.findall("[0-9a-f]{2}", upc_low)
    upc_to_dec = list([int(x, 16) for x in upc_matches])
    subfromlist = upc_matches.count("6d")
    upc_size_add = (((len(upc_matches) - subfromlist) * 11) +
                    (len(re.findall("6c", upc)) * 2)) * barwidth[0]
    upc_img, upc_preimg = upcean.predraw.new_image_surface(((29 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize), barcolor[2], imageoutlib)
    imgout = encode_code128old_barcode([upc_img, upc_preimg], upc, resize, (0, 0), barheight, barwidth, barcolor, hideinfo)
    return [upc_img, upc_preimg, imageoutlib]

def create_code128old_barcode(upc, outfile="./code128.png", resize=1, barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "svgwrite"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "svgwrite"
    if(not qahirahsupport and imageoutlib == "qahirah"):
        imageoutlib = "svgwrite"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "svgwrite"
    if(not svgwritesupport and imageoutlib == "svgwrite"):
        imageoutlib = "svgwrite"
    if(not wandsupport and imageoutlib == "wand"):
        imageoutlib = "svgwrite"
    if(not magicksupport and imageoutlib == "magick"):
        imageoutlib = "svgwrite"
    if(not pgmagicksupport and imageoutlib == "pgmagick"):
        imageoutlib = "svgwrite"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "qahirah" and imageoutlib != "cairosvg" and imageoutlib != "wand" and imageoutlib != "magick" and imageoutlib != "pgmagick" and imageoutlib != "svgwrite"):
        imageoutlib = "svgwrite"
    if(not pilsupport and not cairosupport):
        imageoutlib = "svgwrite"
    if(outfile is None):
        if(imageoutlib == "cairosvg"):
            oldoutfile = None
            outfile = None
            outfileext = "SVG"
        else:
            oldoutfile = None
            outfile = None
            outfileext = None
    else:
        oldoutfile = upcean.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    imgout = draw_code128old_barcode(upc, resize, barheight, barwidth, barcolor, hideinfo, imageoutlib)
    upc_img = imgout[0]
    upc_preimg = imgout[1]
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        return [upc_img, upc_preimg, imageoutlib]
    else:
        return upcean.predraw.save_to_file([upc_img, upc_preimg], outfile, outfileext, "code128; "+upc, imageoutlib)
    return True
