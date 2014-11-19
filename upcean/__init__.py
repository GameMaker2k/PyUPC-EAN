'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: __init__.py - Last Update: 11/18/2014 Ver. 2.7.7 RC 2 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import imp;
from upcean.versioninfo import __author__, __copyright__, __credits__, __email__, __license__, __maintainer__, __project__, __project_url__, __revision__, __status__, __version__, __version_alt__, __version_date__, __version_date_alt__, __version_date_info__, __version_info__, version_date, version_info;

# PIL Support Check
pilsupport = True;
try:
 imp.find_module('PIL');
 pilsupport = True;
except ImportError:
 try:
  imp.find_module('Image');
  pilsupport = True;
 except ImportError:
  pilsupport = False;

'''
// UPC Resources and Info
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code
// Source: http://en.wikipedia.org/wiki/Global_Trade_Item_Number
// Source: http://en.wikipedia.org/wiki/Barcode
// Source: http://www.ucancode.net/CPP_Library_Control_Tool/Draw-Print-encode-UPCA-barcode-UPCE-barcode-EAN13-barcode-VC-Code.htm
// Source: http://en.wikipedia.org/wiki/International_Article_Number
// Source: http://www.upcdatabase.com/docs/
// Source: http://www.accipiter.org/projects/cat.php
// Source: http://www.accipiter.org/download/kittycode.js
// Source: http://uscan.sourceforge.net/upc.txt
// Source: http://www.adams1.com/upccode.html
// Source: http://www.documentmedia.com/Media/PublicationsArticles/QuietZone.pdf
// Source: http://zxing.org/w/decode.jspx
// Source: http://code.google.com/p/zxing/
// Source: http://www.terryburton.co.uk/barcodewriter/generator/
// Source: http://en.wikipedia.org/wiki/Interleaved_2_of_5
// Source: http://www.gs1au.org/assets/documents/info/user_manuals/barcode_technical_details/ITF_14_Barcode_Structure.pdf
// Source: http://www.barcodeisland.com/
'''

import upcean.validate, upcean.convert, upcean.support, upcean.getprefix, upcean.oopfuncs;
if(pilsupport==True):
 import upcean.fonts, upcean.xml, upcean.barcodes, upcean.getsfname;
