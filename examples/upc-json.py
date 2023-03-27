#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
     Code From: https://github.com/fizyk20/python-barcode
     Code From: https://github.com/fizyk20/python-barcode/blob/master/example.py
         $FileInfo: upc-example.py - Last Update: 3/26/2023 Ver. 2.8.11 RC 1  - Author: fizyk20 $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean;

upcean.encode.create_barcode_from_json_file("./xml/barcodes.json");
