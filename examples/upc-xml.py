#!/usr/bin/env python
'''
     Code From: https://github.com/fizyk20/python-barcode
     Code From: https://github.com/fizyk20/python-barcode/blob/master/example.py
         $FileInfo: upc-example.py - Last Update: 12/3/2019 Ver. 2.7.19 RC 1  - Author: fizyk20 $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import upcean;

upcean.barcodes.create_barcode_from_xml_file("./xml/barcodes.xml");
