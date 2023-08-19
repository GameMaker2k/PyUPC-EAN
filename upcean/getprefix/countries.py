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

    $FileInfo: countries.py - Last Update: 8/18/2023 Ver. 2.10.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.validate;

'''
// Get GS1 Prefix for EAN-13 EAN-9 barcodes
// Source: http://en.wikipedia.org/wiki/List_of_GS1_country_codes
'''
def get_gs1_prefix(upc):
 upc = str(upc);
 if(re.findall(r"^(\d{12})", upc)):
  upc = "0"+upc;
 if(re.findall(r"^(\d{1})$", upc)):
  upc = upc+"00000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall(r"^(\d{2})$", upc)):
  upc = upc+"0000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall(r"^(\d{3})$", upc)):
  upc = upc+"000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall(r"^0(\d{3}\d{10})", upc)):
  fix_ean = re.findall(r"^0(\d{3}\d{10})", upc);
  upc = fix_ean[0];
 if(not re.findall(r"^(\d{3}\d{5}|\d{3}\d{10})$", upc)):
  return False;
 if(re.findall(r"^(\d{3}\d{10})$", upc) and not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(re.findall(r"^(\d{3}\d{5})$", upc) and not upcean.validate.validate_ean8_checksum(upc)):
  return False;
 if(re.findall(r"^(0[0-1][0-9])", upc)):
  return "United States and Canada";
 if(re.findall(r"^(02[0-9])", upc)):
  return "Restricted distribution";
 if(re.findall(r"^(03[0-9])", upc)):
  return "United States drugs";
 if(re.findall(r"^(04[0-9])", upc)):
  return "Restricted distribution";
 if(re.findall(r"^(05[0-9])", upc)):
  return "Coupons";
 if(re.findall(r"^(0[6-9][0-9])", upc)):
  return "United States and Canada";
 if(re.findall(r"^(1[0-3][0-9])", upc)):
  return "United States";
 if(re.findall(r"^(2[0-9][0-9])", upc)):
  return "Restricted distribution";
 if(re.findall(r"^(3[0-7][0-9])", upc)):
  return "France and Monaco";
 if(re.findall(r"^(380)", upc)):
  return "Bulgaria";
 if(re.findall(r"^(383)", upc)):
  return "Slovenia";
 if(re.findall(r"^(385)", upc)):
  return "Croatia";
 if(re.findall(r"^(387)", upc)):
  return "Bosnia and Herzegovina";
 if(re.findall(r"^(389)", upc)):
  return "Montenegro";
 if(re.findall(r"^(390)", upc)):
  return "Kosovo";
 if(re.findall(r"^(4[0-3][0-9]|440)", upc)):
  return "Germany";
 if(re.findall(r"^(4[0-5][0-9])", upc)):
  return "Japan";
 if(re.findall(r"^(46[0-9])", upc)):
  return "Russia";
 if(re.findall(r"^(470)", upc)):
  return "Kyrgyzstan";
 if(re.findall(r"^(471)", upc)):
  return "Taiwan";
 if(re.findall(r"^(474)", upc)):
  return "Estonia";
 if(re.findall(r"^(475)", upc)):
  return "Latvia";
 if(re.findall(r"^(476)", upc)):
  return "Azerbaijan";
 if(re.findall(r"^(477)", upc)):
  return "Lithuania";
 if(re.findall(r"^(478)", upc)):
  return "Uzbekistan";
 if(re.findall(r"^(479)", upc)):
  return "Sri Lanka";
 if(re.findall(r"^(480)", upc)):
  return "Philippines";
 if(re.findall(r"^(481)", upc)):
  return "Belarus";
 if(re.findall(r"^(482)", upc)):
  return "Ukraine";
 if(re.findall(r"^(483)", upc)):
  return "Turkmenistan";
 if(re.findall(r"^(484)", upc)):
  return "Moldova";
 if(re.findall(r"^(485)", upc)):
  return "Armenia";
 if(re.findall(r"^(486)", upc)):
  return "Georgia";
 if(re.findall(r"^(487)", upc)):
  return "Kazakhstan";
 if(re.findall(r"^(488)", upc)):
  return "Tajikistan";
 if(re.findall(r"^(489)", upc)):
  return "Hong Kong SAR";
 if(re.findall(r"^(49[0-9])", upc)):
  return "Japan";
 if(re.findall(r"^(50[0-9])", upc)):
  return "United Kingdom";
 if(re.findall(r"^(52[0-1])", upc)):
  return "Greece";
 if(re.findall(r"^(528)", upc)):
  return "Lebanon";
 if(re.findall(r"^(529)", upc)):
  return "Cyprus";
 if(re.findall(r"^(530)", upc)):
  return "Albania";
 if(re.findall(r"^(531)", upc)):
  return "North Macedonia";
 if(re.findall(r"^(535)", upc)):
  return "Malta";
 if(re.findall(r"^(539)", upc)):
  return "Ireland";
 if(re.findall(r"^(54[0-9])", upc)):
  return "Belgium and Luxembourg";
 if(re.findall(r"^(560)", upc)):
  return "Portugal";
 if(re.findall(r"^(569)", upc)):
  return "Iceland";
 if(re.findall(r"^(57[0-9])", upc)):
  return "Denmark, Faroe Islands and Greenland";
 if(re.findall(r"^(590)", upc)):
  return "Poland";
 if(re.findall(r"^(594)", upc)):
  return "Romania";
 if(re.findall(r"^(599)", upc)):
  return "Hungary";
 if(re.findall(r"^(60[0-1])", upc)):
  return "South Africa";
 if(re.findall(r"^(603)", upc)):
  return "Ghana";
 if(re.findall(r"^(604)", upc)):
  return "Senegal";
 if(re.findall(r"^(608)", upc)):
  return "Bahrain";
 if(re.findall(r"^(609)", upc)):
  return "Mauritius";
 if(re.findall(r"^(611)", upc)):
  return "Morocco";
 if(re.findall(r"^(613)", upc)):
  return "Algeria";
 if(re.findall(r"^(615)", upc)):
  return "Nigeria";
 if(re.findall(r"^(616)", upc)):
  return "Kenya";
 if(re.findall(r"^(618)", upc)):
  return "Côte d'Ivoire";
 if(re.findall(r"^(619)", upc)):
  return "Tunisia";
 if(re.findall(r"^(620)", upc)):
  return "Tanzania";
 if(re.findall(r"^(621)", upc)):
  return "Syria";
 if(re.findall(r"^(622)", upc)):
  return "Egypt";
 if(re.findall(r"^(623)", upc)):
  return "Brunei";
 if(re.findall(r"^(624)", upc)):
  return "Libya";
 if(re.findall(r"^(625)", upc)):
  return "Jordan";
 if(re.findall(r"^(626)", upc)):
  return "Iran";
 if(re.findall(r"^(627)", upc)):
  return "Kuwait";
 if(re.findall(r"^(628)", upc)):
  return "Saudi Arabia";
 if(re.findall(r"^(629)", upc)):
  return "United Arab Emirates";
 if(re.findall(r"^(630)", upc)):
  return "Qatar";
 if(re.findall(r"^(631)", upc)):
  return "Namibia";
 if(re.findall(r"^(64[0-9])", upc)):
  return "Finland";
 if(re.findall(r"^(69[0-5])", upc)):
  return "China";
 if(re.findall(r"^(70[0-9])", upc)):
  return "Norway";
 if(re.findall(r"^(729)", upc)):
  return "Israel";
 if(re.findall(r"^(73[0-9])", upc)):
  return "Sweden";
 if(re.findall(r"^(740)", upc)):
  return "Guatemala";
 if(re.findall(r"^(741)", upc)):
  return "El Salvador";
 if(re.findall(r"^(742)", upc)):
  return "Honduras";
 if(re.findall(r"^(743)", upc)):
  return "Nicaragua";
 if(re.findall(r"^(744)", upc)):
  return "Costa Rica";
 if(re.findall(r"^(745)", upc)):
  return "Panama";
 if(re.findall(r"^(746)", upc)):
  return "Dominican Republic";
 if(re.findall(r"^(750)", upc)):
  return "Mexico";
 if(re.findall(r"^(75[4-5])", upc)):
  return "Canada";
 if(re.findall(r"^(759)", upc)):
  return "Venezuela";
 if(re.findall(r"^(76[0-9])", upc)):
  return "Switzerland and Liechtenstein";
 if(re.findall(r"^(77[0-1])", upc)):
  return "Colombia";
 if(re.findall(r"^(773)", upc)):
  return "Uruguay";
 if(re.findall(r"^(775)", upc)):
  return "Peru";
 if(re.findall(r"^(777)", upc)):
  return "Bolivia";
 if(re.findall(r"^(77[8-9])", upc)):
  return "Argentina";
 if(re.findall(r"^(780)", upc)):
  return "Chile";
 if(re.findall(r"^(784)", upc)):
  return "Paraguay";
 if(re.findall(r"^(786)", upc)):
  return "Ecuador";
 if(re.findall(r"^(789|790)", upc)):
  return "Brazil";
 if(re.findall(r"^(8[0-3][0-9])", upc)):
  return "Italy, San Marino and Vatican City";
 if(re.findall(r"^(84[0-9])", upc)):
  return "Spain and Andorra";
 if(re.findall(r"^(850)", upc)):
  return "Cuba";
 if(re.findall(r"^(858)", upc)):
  return "Slovakia";
 if(re.findall(r"^(859)", upc)):
  return "Czechia";
 if(re.findall(r"^(860)", upc)):
  return "Serbia";
 if(re.findall(r"^(865)", upc)):
  return "Mongolia";
 if(re.findall(r"^(867)", upc)):
  return "North Korea";
 if(re.findall(r"^(86[8-9])", upc)):
  return "Türkiye";
 if(re.findall(r"^(87[0-9])", upc)):
  return "Netherlands";
 if(re.findall(r"^(880)", upc)):
  return "South Korea";
 if(re.findall(r"^(883)", upc)):
  return "Myanmar";
 if(re.findall(r"^(884)", upc)):
  return "Cambodia";
 if(re.findall(r"^(885)", upc)):
  return "Thailand";
 if(re.findall(r"^(888)", upc)):
  return "Singapore";
 if(re.findall(r"^(890)", upc)):
  return "India";
 if(re.findall(r"^(893)", upc)):
  return "Vietnam";
 if(re.findall(r"^(894)", upc)):
  return "Bangladesh";
 if(re.findall(r"^(896)", upc)):
  return "Pakistan";
 if(re.findall(r"^(899)", upc)):
  return "Indonesia";
 if(re.findall(r"^(9[0-1][0-9])", upc)):
  return "Austria";
 if(re.findall(r"^(93[0-9])", upc)):
  return "Australia";
 if(re.findall(r"^(94[0-9])", upc)):
  return "New Zealand";
 if(re.findall(r"^(950)", upc)):
  return "GS1 Global Office: Special applications";
 if(re.findall(r"^(951)", upc)):
  return "EPCglobal: Special applications";
 if(re.findall(r"^(955)", upc)):
  return "Malaysia";
 if(re.findall(r"^(958)", upc)):
  return "Macau";
 if(re.findall(r"^(960)", upc)):
  return "GS1 UK: GTIN-8 allocations";
 if(re.findall(r"^(96[1-9])", upc)):
  return "GS1 Global Office: GTIN-8 allocations";
 if(re.findall(r"^(977)", upc)):
  return "Serial publications (ISSN)";
 if(re.findall(r"^(97[8-9])", upc)):
  return "Bookland (ISBN)";
 if(re.findall(r"^(980)", upc)):
  return "Refund receipts";
 if(re.findall(r"^(98[1-3])", upc)):
  return "Common Currency Coupons";
 if(re.findall(r"^(99[0-9])", upc)):
  return "Coupons";
 '''
 // Reserved for future use
 '''
 if(re.findall(r"^(1[4-9][0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(381|382|384|386|388)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(39[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(44[1-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(472|473|483)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(51[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(52[1-7])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(53[2-4])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(53[6-8])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(55[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(56[1-8])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(58[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(59[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(59[5-8])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(602)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(60[5-7])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(610|612|614|617|620|623)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(63[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(6[5-8][0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(69[6-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(71[0-9]|72[0-8])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(74[7-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(75[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(75[6-8])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(772|774|776|778)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(78[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(785|787|788)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(79[1-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(85[1-7])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(86[1-4])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(866)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(88[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(886|887|889|891|892|895|897|898)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(92[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(95[2-4])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(956|957|959)", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(96[0-9]|97[0-6])", upc)):
  return "Reserved for future use";
 if(re.findall(r"^(98[4-9])", upc)):
  return "Reserved for future use";
 return False;

'''
// Get ISBN identifier groups
// Source: http://en.wikipedia.org/wiki/List_of_ISBN_identifier_groups
'''
def get_isbn_identifier(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(len(upc)>10):
  fix_matches = re.findall(r"^(\d{9})(\d{1}|X{1})", upc);
  fix_matches = fix_matches[0]
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>10 or len(upc)<10):
  return False;
 if(re.findall(r"^99972", upc)):
  return "Faroe Islands";
 if(re.findall(r"^99971", upc)):
  return "Myanmar";
 if(re.findall(r"^99970", upc)):
  return "Haiti";
 if(re.findall(r"^99969", upc)):
  return "Oman";
 if(re.findall(r"^99968", upc)):
  return "Botswana";
 if(re.findall(r"^99967", upc)):
  return "Paraguay";
 if(re.findall(r"^99966", upc)):
  return "Kuwait";
 if(re.findall(r"^99965", upc)):
  return "Macau";
 if(re.findall(r"^99964", upc)):
  return "Nicaragua";
 if(re.findall(r"^99963", upc)):
  return "Cambodia";
 if(re.findall(r"^99962", upc)):
  return "Mongolia";
 if(re.findall(r"^99961", upc)):
  return "El Salvador";
 if(re.findall(r"^99960", upc)):
  return "Malawi";
 if(re.findall(r"^99959", upc)):
  return "Luxembourg";
 if(re.findall(r"^99958", upc)):
  return "Bahrain";
 if(re.findall(r"^99957", upc)):
  return "Malta";
 if(re.findall(r"^99956", upc)):
  return "Albania";
 if(re.findall(r"^99955", upc)):
  return "Republika Srpska";
 if(re.findall(r"^99954", upc)):
  return "Bolivia";
 if(re.findall(r"^99953", upc)):
  return "Paraguay";
 if(re.findall(r"^99952", upc)):
  return "Mali";
 if(re.findall(r"^99951", upc)):
  return "Democratic Republic of Congo";
 if(re.findall(r"^99950", upc)):
  return "Cambodia";
 if(re.findall(r"^99949", upc)):
  return "Mauritius";
 if(re.findall(r"^99948", upc)):
  return "Eritrea";
 if(re.findall(r"^99947", upc)):
  return "Tajikistan";
 if(re.findall(r"^99946", upc)):
  return "Nepal";
 if(re.findall(r"^99945", upc)):
  return "Namibia";
 if(re.findall(r"^99944", upc)):
  return "Ethiopia";
 if(re.findall(r"^99943", upc)):
  return "Albania";
 if(re.findall(r"^99942", upc)):
  return "Sudan";
 if(re.findall(r"^99941", upc)):
  return "Armenia";
 if(re.findall(r"^99939", upc)):
  return "Guatemala";
 if(re.findall(r"^99938", upc)):
  return "Republika Srpska";
 if(re.findall(r"^99937", upc)):
  return "Macau";
 if(re.findall(r"^99936", upc)):
  return "Bhutan";
 if(re.findall(r"^99935", upc)):
  return "Haiti";
 if(re.findall(r"^99934", upc)):
  return "Dominican republic";
 if(re.findall(r"^99933", upc)):
  return "Nepal";
 if(re.findall(r"^99932", upc)):
  return "Malta";
 if(re.findall(r"^99931", upc)):
  return "Seychelles";
 if(re.findall(r"^99930", upc)):
  return "Armenia";
 if(re.findall(r"^99929", upc)):
  return "Mongolia";
 if(re.findall(r"^99928", upc)):
  return "Georgia";
 if(re.findall(r"^99927", upc)):
  return "Albania";
 if(re.findall(r"^99926", upc)):
  return "Honduras";
 if(re.findall(r"^99925", upc)):
  return "Paraguay";
 if(re.findall(r"^99924", upc)):
  return "Nicaragua";
 if(re.findall(r"^99923", upc)):
  return "El Salvador";
 if(re.findall(r"^99922", upc)):
  return "Guatemala";
 if(re.findall(r"^99921", upc)):
  return "Qatar";
 if(re.findall(r"^99920", upc)):
  return "Andorra";
 if(re.findall(r"^99919", upc)):
  return "Benin";
 if(re.findall(r"^99918", upc)):
  return "Faroe Islands";
 if(re.findall(r"^99917", upc)):
  return "Brunei Darussalam";
 if(re.findall(r"^99916", upc)):
  return "Namibia";
 if(re.findall(r"^99915", upc)):
  return "Maldives";
 if(re.findall(r"^99914", upc)):
  return "Suriname";
 if(re.findall(r"^99913", upc)):
  return "Andorra";
 if(re.findall(r"^99912", upc)):
  return "Botsana";
 if(re.findall(r"^99911", upc)):
  return "Lesotho";
 if(re.findall(r"^99910", upc)):
  return "Sierra Leone";
 if(re.findall(r"^99909", upc)):
  return "Malta";
 if(re.findall(r"^99908", upc)):
  return "Malawi";
 if(re.findall(r"^99906", upc)):
  return "Kuwait";
 if(re.findall(r"^99905", upc)):
  return "Bolivia";
 if(re.findall(r"^99904", upc)):
  return "Netherland Antilles, and Aruba";
 if(re.findall(r"^99903", upc)):
  return "Mauritius";
 if(re.findall(r"^99902", upc)):
  return "Gabon";
 if(re.findall(r"^99901", upc)):
  return "Bahrain";
 if(re.findall(r"^9989", upc)):
  return "Macedonia";
 if(re.findall(r"^9988", upc)):
  return "Ghana";
 if(re.findall(r"^9987", upc)):
  return "Tanzania";
 if(re.findall(r"^9986", upc)):
  return "Lithuania";
 if(re.findall(r"^9985", upc)):
  return "Estonia";
 if(re.findall(r"^9984", upc)):
  return "Latvia";
 if(re.findall(r"^9983", upc)):
  return "Gambia";
 if(re.findall(r"^9982", upc)):
  return "Zambia";
 if(re.findall(r"^9981", upc)):
  return "Morocco";
 if(re.findall(r"^9980", upc)):
  return "Papua New Guinea";
 if(re.findall(r"^9979", upc)):
  return "Iceland";
 if(re.findall(r"^9978", upc)):
  return "Ecuador";
 if(re.findall(r"^9977", upc)):
  return "Costa Rica";
 if(re.findall(r"^9976", upc)):
  return "Tanzania";
 if(re.findall(r"^9975", upc)):
  return "Moldova";
 if(re.findall(r"^9974", upc)):
  return "Uruguay";
 if(re.findall(r"^9973", upc)):
  return "Tunisia";
 if(re.findall(r"^9972", upc)):
  return "Peru";
 if(re.findall(r"^9971", upc)):
  return "Singapore";
 if(re.findall(r"^9970", upc)):
  return "Uganda";
 if(re.findall(r"^9968", upc)):
  return "Costa Rica";
 if(re.findall(r"^9967", upc)):
  return "Kyrgyzstan";
 if(re.findall(r"^9966", upc)):
  return "Kenya";
 if(re.findall(r"^9965", upc)):
  return "Kazakhstan";
 if(re.findall(r"^9964", upc)):
  return "Ghana";
 if(re.findall(r"^9963", upc)):
  return "Cyprus";
 if(re.findall(r"^9962", upc)):
  return "Panama";
 if(re.findall(r"^9961", upc)):
  return "Algeria";
 if(re.findall(r"^9960", upc)):
  return "Saudi Arabia";
 if(re.findall(r"^9959", upc)):
  return "Libya";
 if(re.findall(r"^9958", upc)):
  return "Bosnia and Herzegovina";
 if(re.findall(r"^9957", upc)):
  return "Jordan";
 if(re.findall(r"^9956", upc)):
  return "Cameroon";
 if(re.findall(r"^9955", upc)):
  return "Lithuania";
 if(re.findall(r"^9954", upc)):
  return "Morocco";
 if(re.findall(r"^9953", upc)):
  return "Lebanon";
 if(re.findall(r"^9952", upc)):
  return "Azerbaijan";
 if(re.findall(r"^9951", upc)):
  return "Kosovo";
 if(re.findall(r"^9950", upc)):
  return "Palestine";
 if(re.findall(r"^9949", upc)):
  return "Estonia";
 if(re.findall(r"^9948", upc)):
  return "United Arab Emirates";
 if(re.findall(r"^9947", upc)):
  return "Algeria";
 if(re.findall(r"^9946", upc)):
  return "North Korea";
 if(re.findall(r"^9945", upc)):
  return "Dominican Republic";
 if(re.findall(r"^9944", upc)):
  return "Turkey";
 if(re.findall(r"^9943", upc)):
  return "Uzbekistan";
 if(re.findall(r"^9942", upc)):
  return "Ecuador";
 if(re.findall(r"^9941", upc)):
  return "Georgia";
 if(re.findall(r"^9940", upc)):
  return "Montenegro";
 if(re.findall(r"^9939", upc)):
  return "Armenia";
 if(re.findall(r"^9937", upc)):
  return "Nepal";
 if(re.findall(r"^9936", upc)):
  return "Afghanistan";
 if(re.findall(r"^9935", upc)):
  return "Iceland";
 if(re.findall(r"^9934", upc)):
  return "Latvia";
 if(re.findall(r"^9933", upc)):
  return "Syria";
 if(re.findall(r"^9932", upc)):
  return "Laos";
 if(re.findall(r"^9931", upc)):
  return "Algeria";
 if(re.findall(r"^9930", upc)):
  return "Costa Rica";
 if(re.findall(r"^9929", upc)):
  return "Guatemala";
 if(re.findall(r"^9928", upc)):
  return "Albania";
 if(re.findall(r"^9927", upc)):
  return "Qatar";
 if(re.findall(r"^989", upc)):
  return "Portugal";
 if(re.findall(r"^988", upc)):
  return "Hong Kong";
 if(re.findall(r"^987", upc)):
  return "Argentina";
 if(re.findall(r"^986", upc)):
  return "Taiwan";
 if(re.findall(r"^985", upc)):
  return "Belarus";
 if(re.findall(r"^984", upc)):
  return "Bangladesh";
 if(re.findall(r"^983", upc)):
  return "Malaysia";
 if(re.findall(r"^982", upc)):
  return "South Pacific";
 if(re.findall(r"^981", upc)):
  return "Singapore";
 if(re.findall(r"^980", upc)):
  return "Venezuela";
 if(re.findall(r"^979", upc)):
  return "Indonesia";
 if(re.findall(r"^978", upc)):
  return "Nigeria";
 if(re.findall(r"^977", upc)):
  return "Egypt";
 if(re.findall(r"^976", upc)):
  return "CARICOM";
 if(re.findall(r"^975", upc)):
  return "Turkey";
 if(re.findall(r"^974", upc)):
  return "Thailand";
 if(re.findall(r"^973", upc)):
  return "Romania";
 if(re.findall(r"^972", upc)):
  return "Portugal";
 if(re.findall(r"^971", upc)):
  return "Philippines";
 if(re.findall(r"^970", upc)):
  return "Mexico";
 if(re.findall(r"^969", upc)):
  return "Pakistan";
 if(re.findall(r"^968", upc)):
  return "Mexico";
 if(re.findall(r"^967", upc)):
  return "Malaysia";
 if(re.findall(r"^966", upc)):
  return "Ukraine";
 if(re.findall(r"^965", upc)):
  return "Israel";
 if(re.findall(r"^964", upc)):
  return "Iran";
 if(re.findall(r"^963", upc)):
  return "Hungary";
 if(re.findall(r"^962", upc)):
  return "Hong Kong";
 if(re.findall(r"^961", upc)):
  return "Slovenia";
 if(re.findall(r"^960", upc)):
  return "Greece";
 if(re.findall(r"^959", upc)):
  return "Cuba";
 if(re.findall(r"^958", upc)):
  return "Colombia";
 if(re.findall(r"^957", upc)):
  return "Taiwan";
 if(re.findall(r"^956", upc)):
  return "Chile";
 if(re.findall(r"^955", upc)):
  return "Sri Lanka";
 if(re.findall(r"^954", upc)):
  return "Bulgaria";
 if(re.findall(r"^953", upc)):
  return "Croatia";
 if(re.findall(r"^952", upc)):
  return "Finland";
 if(re.findall(r"^951", upc)):
  return "Finland";
 if(re.findall(r"^950", upc)):
  return "Argentina";
 if(re.findall(r"^621", upc)):
  return "Philippines";
 if(re.findall(r"^620", upc)):
  return "Mauritius";
 if(re.findall(r"^619", upc)):
  return "Bulgaria";
 if(re.findall(r"^618", upc)):
  return "Greece";
 if(re.findall(r"^617", upc)):
  return "Ukraine";
 if(re.findall(r"^616", upc)):
  return "Thailand";
 if(re.findall(r"^615", upc)):
  return "Hungary";
 if(re.findall(r"^614", upc)):
  return "Lebanon";
 if(re.findall(r"^613", upc)):
  return "Mauritius";
 if(re.findall(r"^612", upc)):
  return "Peru";
 if(re.findall(r"^611", upc)):
  return "Thailand";
 if(re.findall(r"^609", upc)):
  return "Lithuania";
 if(re.findall(r"^608", upc)):
  return "Macedonia";
 if(re.findall(r"^607", upc)):
  return "Mexico";
 if(re.findall(r"^606", upc)):
  return "Romania";
 if(re.findall(r"^605", upc)):
  return "Turkey";
 if(re.findall(r"^604", upc)):
  return "Vietnam";
 if(re.findall(r"^603", upc)):
  return "Saudi Arabia";
 if(re.findall(r"^602", upc)):
  return "Indonesia";
 if(re.findall(r"^601", upc)):
  return "Kazakhstan";
 if(re.findall(r"^600", upc)):
  return "Iran";
 if(re.findall(r"^94", upc)):
  return "Netherlands";
 if(re.findall(r"^93", upc)):
  return "India";
 if(re.findall(r"^92", upc)):
  return "International NGO Publishers and EC Organizations";
 if(re.findall(r"^91", upc)):
  return "Sweden";
 if(re.findall(r"^90", upc)):
  return "Netherlands";
 if(re.findall(r"^89", upc)):
  return "Republic of Korea";
 if(re.findall(r"^88", upc)):
  return "Italy";
 if(re.findall(r"^87", upc)):
  return "Denmark";
 if(re.findall(r"^86", upc)):
  return "Serbia (shared)";
 if(re.findall(r"^85", upc)):
  return "Brazil";
 if(re.findall(r"^84", upc)):
  return "Spain";
 if(re.findall(r"^83", upc)):
  return "Poland";
 if(re.findall(r"^82", upc)):
  return "Norway";
 if(re.findall(r"^81", upc)):
  return "India";
 if(re.findall(r"^80", upc)):
  return "Czech Republic and Slovakia";
 if(re.findall(r"^7", upc)):
  return "China";
 if(re.findall(r"^5", upc)):
  return "Russia and former USSR";
 if(re.findall(r"^4", upc)):
  return "Japan";
 if(re.findall(r"^3", upc)):
  return "German";
 if(re.findall(r"^2", upc)):
  return "French";
 if(re.findall(r"^1", upc)):
  return "English";
 if(re.findall(r"^0", upc)):
  return "English";
 return False;
