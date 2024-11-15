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

    $FileInfo: countries.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import upcean.validate

'''
// Get GS1 Prefix for EAN-13 EAN-9 barcodes
// Source: http://en.wikipedia.org/wiki/List_of_GS1_country_codes
'''


def get_gs1_prefix(upc):
    upc = str(upc)
    if re.match("^\\d{12}$", upc):
        upc = "0" + upc

    if re.match("^\\d{1}$", upc):
        upc += "00000000000" + str(upcean.validate.get_ean13_checksum(upc))
    elif re.match("^\\d{2}$", upc):
        upc += "0000000000" + str(upcean.validate.get_ean13_checksum(upc))
    elif re.match("^\\d{3}$", upc):
        upc += "000000000" + str(upcean.validate.get_ean13_checksum(upc))

    if re.match("^0(\\d{3}\\d{10})$", upc):
        upc = re.match("^0(\\d{3}\\d{10})$", upc).group(1)

    if not re.match("^\\d{3}\\d{5}$|^\\d{3}\\d{10}$", upc):
        return False

    if re.match("^\\d{3}\\d{10}$", upc) and not upcean.validate.validate_ean13_checksum(upc):
        return False
    if re.match("^\\d{3}\\d{5}$", upc) and not upcean.validate.validate_ean8_checksum(upc):
        return False

    # GS1 prefix rules
    gs1_mapping = {
        "^(0[0-1][0-9])": "United States and Canada",
        "^(02[0-9])": "Restricted distribution",
        "^(03[0-9])": "United States drugs",
        "^(04[0-9])": "Restricted distribution",
        "^(05[0-9])": "Coupons",
        "^(0[6-9][0-9])": "United States and Canada",
        "^(1[0-3][0-9])": "United States",
        "^(2[0-9][0-9])": "Restricted distribution",
        "^(3[0-7][0-9])": "France and Monaco",
        "^(380)": "Bulgaria",
        "^(383)": "Slovenia",
        "^(385)": "Croatia",
        "^(387)": "Bosnia and Herzegovina",
        "^(389)": "Montenegro",
        "^(390)": "Kosovo",
        "^(4[0-3][0-9]|440)": "Germany",
        "^(4[0-5][0-9])": "Japan",
        "^(46[0-9])": "Russia",
        "^(470)": "Kyrgyzstan",
        "^(471)": "Taiwan",
        "^(474)": "Estonia",
        "^(475)": "Latvia",
        "^(476)": "Azerbaijan",
        "^(477)": "Lithuania",
        "^(478)": "Uzbekistan",
        "^(479)": "Sri Lanka",
        "^(480)": "Philippines",
        "^(481)": "Belarus",
        "^(482)": "Ukraine",
        "^(483)": "Turkmenistan",
        "^(484)": "Moldova",
        "^(485)": "Armenia",
        "^(486)": "Georgia",
        "^(487)": "Kazakhstan",
        "^(488)": "Tajikistan",
        "^(489)": "Hong Kong SAR",
        "^(49[0-9])": "Japan",
        "^(50[0-9])": "United Kingdom",
        "^(52[0-1])": "Greece",
        "^(528)": "Lebanon",
        "^(529)": "Cyprus",
        "^(530)": "Albania",
        "^(531)": "North Macedonia",
        "^(535)": "Malta",
        "^(539)": "Ireland",
        "^(54[0-9])": "Belgium and Luxembourg",
        "^(560)": "Portugal",
        "^(569)": "Iceland",
        "^(57[0-9])": "Denmark, Faroe Islands and Greenland",
        "^(590)": "Poland",
        "^(594)": "Romania",
        "^(599)": "Hungary",
        "^(60[0-1])": "South Africa",
        "^(603)": "Ghana",
        "^(604)": "Senegal",
        "^(608)": "Bahrain",
        "^(609)": "Mauritius",
        "^(611)": "Morocco",
        "^(613)": "Algeria",
        "^(615)": "Nigeria",
        "^(616)": "Kenya",
        "^(618)": "Côte d'Ivoire",
        "^(619)": "Tunisia",
        "^(620)": "Tanzania",
        "^(621)": "Syria",
        "^(622)": "Egypt",
        "^(623)": "Brunei",
        "^(624)": "Libya",
        "^(625)": "Jordan",
        "^(626)": "Iran",
        "^(627)": "Kuwait",
        "^(628)": "Saudi Arabia",
        "^(629)": "United Arab Emirates",
        "^(630)": "Qatar",
        "^(631)": "Namibia",
        "^(64[0-9])": "Finland",
        "^(69[0-5])": "China",
        "^(70[0-9])": "Norway",
        "^(729)": "Israel",
        "^(73[0-9])": "Sweden",
        "^(740)": "Guatemala",
        "^(741)": "El Salvador",
        "^(742)": "Honduras",
        "^(743)": "Nicaragua",
        "^(744)": "Costa Rica",
        "^(745)": "Panama",
        "^(746)": "Dominican Republic",
        "^(750)": "Mexico",
        "^(75[4-5])": "Canada",
        "^(759)": "Venezuela",
        "^(76[0-9])": "Switzerland and Liechtenstein",
        "^(77[0-1])": "Colombia",
        "^(773)": "Uruguay",
        "^(775)": "Peru",
        "^(777)": "Bolivia",
        "^(77[8-9])": "Argentina",
        "^(780)": "Chile",
        "^(784)": "Paraguay",
        "^(786)": "Ecuador",
        "^(789|790)": "Brazil",
        "^(8[0-3][0-9])": "Italy, San Marino and Vatican City",
        "^(84[0-9])": "Spain and Andorra",
        "^(850)": "Cuba",
        "^(858)": "Slovakia",
        "^(859)": "Czechia",
        "^(860)": "Serbia",
        "^(865)": "Mongolia",
        "^(867)": "North Korea",
        "^(86[8-9])": "Türkiye",
        "^(87[0-9])": "Netherlands",
        "^(880)": "South Korea",
        "^(883)": "Myanmar",
        "^(884)": "Cambodia",
        "^(885)": "Thailand",
        "^(888)": "Singapore",
        "^(890)": "India",
        "^(893)": "Vietnam",
        "^(894)": "Bangladesh",
        "^(896)": "Pakistan",
        "^(899)": "Indonesia",
        "^(9[0-1][0-9])": "Austria",
        "^(93[0-9])": "Australia",
        "^(94[0-9])": "New Zealand",
        "^(950)": "GS1 Global Office: Special applications",
        "^(951)": "EPCglobal: Special applications",
        "^(955)": "Malaysia",
        "^(958)": "Macau",
        "^(960)": "GS1 UK: GTIN-8 allocations",
        "^(96[1-9])": "GS1 Global Office: GTIN-8 allocations",
        "^(977)": "Serial publications (ISSN)",
        "^(97[8-9])": "Bookland (ISBN)",
        "^(980)": "Refund receipts",
        "^(98[1-3])": "Common Currency Coupons",
        "^(99[0-9])": "Coupons"
    }

    for pattern, region in gs1_mapping.items():
        if re.match(pattern, upc):
            return region

    return "Reserved for future use" if re.match("^(1[4-9][0-9]|381|382|384|386|388|39[0-9]|44[1-9]|472|473|483|51[0-9]|52[1-7]|53[2-4]|53[6-8]|55[0-9]|56[1-8]|58[0-9]|59[1-3]|59[5-8]|60[5-7]|610|612|614|617|620|623|63[0-9]|6[5-8][0-9]|69[6-9]|71[0-9]|72[0-8]|74[7-9]|75[1-3]|75[6-8]|772|774|776|778|78[1-3]|785|787|788|79[1-9]|85[1-7]|86[1-4]|866|88[1-3]|886|887|889|891|892|895|897|898|92[0-9]|95[2-4]|956|957|959|96[0-9]|97[0-6]|98[4-9])", upc) else False

