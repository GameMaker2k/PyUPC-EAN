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

    $FileInfo: __init__.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import upcean.support
import upcean.oopfuncs
import upcean.getprefix
import upcean.convert
import upcean.validate
from upcean.versioninfo import getcuryear, __author__, __copyright__, __credits__, __copyright_year__, __license__, __license_string__, __maintainer__, __email__, __status__, __project__, __project_url__, __version_info__, __build_time__, __build_time_utc__, __build_python_info__, get_build_python_info, __revision__, __revision_id__, __version__, __version_alt__, version_info, __version_date_info__, __version_date__, __version_date_alt__, version_date

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

pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or pillowsupport or cairosupport or qahirahsupport or svgwritesupport):
    import upcean.fonts
    import upcean.xml
    import upcean.encode
    import upcean.predraw.getsfname
    import upcean.encode as barcodes
if(pilsupport or pillowsupport):
    import upcean.decode
