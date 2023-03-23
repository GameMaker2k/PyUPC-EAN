#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     Code From: http://code.activestate.com/lists/python-list/376068/
     Code From: https://mail.python.org/pipermail/python-list/2004-January/239664.html
     Code From: http://compgroups.net/comp.lang.python/upc-ean-barcode-script/1631450
         $FileInfo: upc-test.py - Last Update: 3/23/2023 Ver. 2.8.4 RC 1  - Author: alisonken11 $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean

# Below codes taken from http://www.barcodeisland.com examples
# UPC-E codes to expand/verify
e = { 0: '01278907',
      1: '01278916',
      2: '01278925',
      3: '01238935',
      4: '01248934',
      5: '01258933',
      6: '01268932',
      7: '01278931',
      8: '01288930',
      9: '01298939',
      10: '01291944',
      11: '01291155',
      12: '01291162',
      13: '01291179',
      14: '01291186' }

# UPC-A codes to verify/compress
a = { 0: '012000007897',
      1: '012100007896',
      2: '012200007895',
      3: '012300000895',
      4: '012400000894',
      5: '012500000893',
      6: '012600000892',
      7: '012700000891',
      8: '012800000890',
      9: '012900000899',
      10: '012910000094',
      11: '012911000055',
      12: '012911000062',
      13: '012911000079',
      14: '012911000086' }

print('checking upca2e ...')
for i in a.keys():
      t1=a[i]
      t2=upcean.convert.convert_barcode("upca", "upce", t1)
      ip=str(i).zfill(2)
      print('key ', ip, ':', t1+" ", upcean.validate.validate_checksum("upca", t1))
      print('upce', ip, ':', t2+"     ", upcean.validate.validate_checksum("upce", t2))

print
print('Checking upce2a ...')
for i in e.keys():
      t1=e[i]
      t2=upcean.convert.convert_barcode("upce", "upca", t1)
      ip=str(i).zfill(2)
      print('key ', ip, ':', t1+"     ", upcean.validate.validate_checksum("upce", t1))
      print('upca', ip, ':', t2+" ", upcean.validate.validate_checksum("upca", t2))
