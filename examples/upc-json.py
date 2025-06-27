#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     Code From: https://github.com/fizyk20/python-barcode
     Code From: https://github.com/fizyk20/python-barcode/blob/master/example.py
         $FileInfo: upc-example.py - Last Update: 6/27/2025 Ver. 2.20.0 RC 1  - Author: fizyk20 $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean

upcean.encode.create_barcode_from_json_file("./xml/barcodes.json")
