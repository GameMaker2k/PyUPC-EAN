#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     Code From: https://github.com/fizyk20/python-barcode
     Code From: https://github.com/fizyk20/python-barcode/blob/master/example.py
         $FileInfo: upc-example.py - Last Update: 3/9/2023 Ver. 2.7.27 RC 1  - Author: fizyk20 $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean

barcode = upcean.oopfuncs.barcode('ean13', '1234567890128')
print(barcode.validate_checksum())
barcode.validate_create_barcode("./1234567890128.png", 1)

debarcode = upcean.oopfuncs.decode('ean13', './1234567890128.png')
ean = decode.validate_decode_barcode()
print(ean)

barcode2 = upcean.oopfuncs.barcode('itf14', '30012345678906')
print(barcode2.validate_checksum())
barcode2.validate_create_barcode("./30012345678906.png", 1)

debarcode = upcean.oopfuncs.decode('itf14', './30012345678906.png')
itf = decode.validate_decode_barcode()
print(itf)
