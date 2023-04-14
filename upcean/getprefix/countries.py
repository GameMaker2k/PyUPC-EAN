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

    $FileInfo: countries.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.validate;

'''
// Get GS1 Prefix for EAN-13 EAN-9 barcodes
// Source: http://en.wikipedia.org/wiki/List_of_GS1_country_codes
'''
def get_gs1_prefix(upc):
 upc = str(upc);
 if(re.findall("^(\d{12})", upc)):
  upc = "0"+upc;
 if(re.findall("^(\d{1})$", upc)):
  upc = upc+"00000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall("^(\d{2})$", upc)):
  upc = upc+"0000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall("^(\d{3})$", upc)):
  upc = upc+"000000000";
  upc = upc+str(upcean.validate.get_ean13_checksum(upc));
 if(re.findall("^0(\d{3}\d{10})", upc)):
  fix_ean = re.findall("^0(\d{3}\d{10})", upc);
  upc = fix_ean[0];
 if(not re.findall("^(\d{3}\d{5}|\d{3}\d{10})$", upc)):
  return False;
 if(re.findall("^(\d{3}\d{10})$", upc) and not upcean.validate.validate_ean13_checksum(upc)):
  return False;
 if(re.findall("^(\d{3}\d{5})$", upc) and not upcean.validate.validate_ean8_checksum(upc)):
  return False;
 if(re.findall("^(0[0-1][0-9])", upc)):
  return "United States and Canada";
 if(re.findall("^(02[0-9])", upc)):
  return "Restricted distribution";
 if(re.findall("^(03[0-9])", upc)):
  return "United States drugs";
 if(re.findall("^(04[0-9])", upc)):
  return "Restricted distribution";
 if(re.findall("^(05[0-9])", upc)):
  return "Coupons";
 if(re.findall("^(0[6-9][0-9])", upc)):
  return "United States and Canada";
 if(re.findall("^(1[0-3][0-9])", upc)):
  return "United States";
 if(re.findall("^(2[0-9][0-9])", upc)):
  return "Restricted distribution";
 if(re.findall("^(3[0-7][0-9])", upc)):
  return "France and Monaco";
 if(re.findall("^(380)", upc)):
  return "Bulgaria";
 if(re.findall("^(383)", upc)):
  return "Slovenia";
 if(re.findall("^(385)", upc)):
  return "Croatia";
 if(re.findall("^(387)", upc)):
  return "Bosnia and Herzegovina";
 if(re.findall("^(389)", upc)):
  return "Montenegro";
 if(re.findall("^(390)", upc)):
  return "Kosovo";
 if(re.findall("^(4[0-3][0-9]|440)", upc)):
  return "Germany";
 if(re.findall("^(4[0-5][0-9])", upc)):
  return "Japan";
 if(re.findall("^(46[0-9])", upc)):
  return "Russia";
 if(re.findall("^(470)", upc)):
  return "Kyrgyzstan";
 if(re.findall("^(471)", upc)):
  return "Taiwan";
 if(re.findall("^(474)", upc)):
  return "Estonia";
 if(re.findall("^(475)", upc)):
  return "Latvia";
 if(re.findall("^(476)", upc)):
  return "Azerbaijan";
 if(re.findall("^(477)", upc)):
  return "Lithuania";
 if(re.findall("^(478)", upc)):
  return "Uzbekistan";
 if(re.findall("^(479)", upc)):
  return "Sri Lanka";
 if(re.findall("^(480)", upc)):
  return "Philippines";
 if(re.findall("^(481)", upc)):
  return "Belarus";
 if(re.findall("^(482)", upc)):
  return "Ukraine";
 if(re.findall("^(483)", upc)):
  return "Turkmenistan";
 if(re.findall("^(484)", upc)):
  return "Moldova";
 if(re.findall("^(485)", upc)):
  return "Armenia";
 if(re.findall("^(486)", upc)):
  return "Georgia";
 if(re.findall("^(487)", upc)):
  return "Kazakhstan";
 if(re.findall("^(488)", upc)):
  return "Tajikistan";
 if(re.findall("^(489)", upc)):
  return "Hong Kong SAR";
 if(re.findall("^(49[0-9])", upc)):
  return "Japan";
 if(re.findall("^(50[0-9])", upc)):
  return "United Kingdom";
 if(re.findall("^(52[0-1])", upc)):
  return "Greece";
 if(re.findall("^(528)", upc)):
  return "Lebanon";
 if(re.findall("^(529)", upc)):
  return "Cyprus";
 if(re.findall("^(530)", upc)):
  return "Albania";
 if(re.findall("^(531)", upc)):
  return "North Macedonia";
 if(re.findall("^(535)", upc)):
  return "Malta";
 if(re.findall("^(539)", upc)):
  return "Ireland";
 if(re.findall("^(54[0-9])", upc)):
  return "Belgium and Luxembourg";
 if(re.findall("^(560)", upc)):
  return "Portugal";
 if(re.findall("^(569)", upc)):
  return "Iceland";
 if(re.findall("^(57[0-9])", upc)):
  return "Denmark, Faroe Islands and Greenland";
 if(re.findall("^(590)", upc)):
  return "Poland";
 if(re.findall("^(594)", upc)):
  return "Romania";
 if(re.findall("^(599)", upc)):
  return "Hungary";
 if(re.findall("^(60[0-1])", upc)):
  return "South Africa";
 if(re.findall("^(603)", upc)):
  return "Ghana";
 if(re.findall("^(604)", upc)):
  return "Senegal";
 if(re.findall("^(608)", upc)):
  return "Bahrain";
 if(re.findall("^(609)", upc)):
  return "Mauritius";
 if(re.findall("^(611)", upc)):
  return "Morocco";
 if(re.findall("^(613)", upc)):
  return "Algeria";
 if(re.findall("^(615)", upc)):
  return "Nigeria";
 if(re.findall("^(616)", upc)):
  return "Kenya";
 if(re.findall("^(618)", upc)):
  return "Côte d'Ivoire";
 if(re.findall("^(619)", upc)):
  return "Tunisia";
 if(re.findall("^(620)", upc)):
  return "Tanzania";
 if(re.findall("^(621)", upc)):
  return "Syria";
 if(re.findall("^(622)", upc)):
  return "Egypt";
 if(re.findall("^(623)", upc)):
  return "Brunei";
 if(re.findall("^(624)", upc)):
  return "Libya";
 if(re.findall("^(625)", upc)):
  return "Jordan";
 if(re.findall("^(626)", upc)):
  return "Iran";
 if(re.findall("^(627)", upc)):
  return "Kuwait";
 if(re.findall("^(628)", upc)):
  return "Saudi Arabia";
 if(re.findall("^(629)", upc)):
  return "United Arab Emirates";
 if(re.findall("^(630)", upc)):
  return "Qatar";
 if(re.findall("^(631)", upc)):
  return "Namibia";
 if(re.findall("^(64[0-9])", upc)):
  return "Finland";
 if(re.findall("^(69[0-5])", upc)):
  return "China";
 if(re.findall("^(70[0-9])", upc)):
  return "Norway";
 if(re.findall("^(729)", upc)):
  return "Israel";
 if(re.findall("^(73[0-9])", upc)):
  return "Sweden";
 if(re.findall("^(740)", upc)):
  return "Guatemala";
 if(re.findall("^(741)", upc)):
  return "El Salvador";
 if(re.findall("^(742)", upc)):
  return "Honduras";
 if(re.findall("^(743)", upc)):
  return "Nicaragua";
 if(re.findall("^(744)", upc)):
  return "Costa Rica";
 if(re.findall("^(745)", upc)):
  return "Panama";
 if(re.findall("^(746)", upc)):
  return "Dominican Republic";
 if(re.findall("^(750)", upc)):
  return "Mexico";
 if(re.findall("^(75[4-5])", upc)):
  return "Canada";
 if(re.findall("^(759)", upc)):
  return "Venezuela";
 if(re.findall("^(76[0-9])", upc)):
  return "Switzerland and Liechtenstein";
 if(re.findall("^(77[0-1])", upc)):
  return "Colombia";
 if(re.findall("^(773)", upc)):
  return "Uruguay";
 if(re.findall("^(775)", upc)):
  return "Peru";
 if(re.findall("^(777)", upc)):
  return "Bolivia";
 if(re.findall("^(77[8-9])", upc)):
  return "Argentina";
 if(re.findall("^(780)", upc)):
  return "Chile";
 if(re.findall("^(784)", upc)):
  return "Paraguay";
 if(re.findall("^(786)", upc)):
  return "Ecuador";
 if(re.findall("^(789|790)", upc)):
  return "Brazil";
 if(re.findall("^(8[0-3][0-9])", upc)):
  return "Italy, San Marino and Vatican City";
 if(re.findall("^(84[0-9])", upc)):
  return "Spain and Andorra";
 if(re.findall("^(850)", upc)):
  return "Cuba";
 if(re.findall("^(858)", upc)):
  return "Slovakia";
 if(re.findall("^(859)", upc)):
  return "Czechia";
 if(re.findall("^(860)", upc)):
  return "Serbia";
 if(re.findall("^(865)", upc)):
  return "Mongolia";
 if(re.findall("^(867)", upc)):
  return "North Korea";
 if(re.findall("^(86[8-9])", upc)):
  return "Türkiye";
 if(re.findall("^(87[0-9])", upc)):
  return "Netherlands";
 if(re.findall("^(880)", upc)):
  return "South Korea";
 if(re.findall("^(883)", upc)):
  return "Myanmar";
 if(re.findall("^(884)", upc)):
  return "Cambodia";
 if(re.findall("^(885)", upc)):
  return "Thailand";
 if(re.findall("^(888)", upc)):
  return "Singapore";
 if(re.findall("^(890)", upc)):
  return "India";
 if(re.findall("^(893)", upc)):
  return "Vietnam";
 if(re.findall("^(894)", upc)):
  return "Bangladesh";
 if(re.findall("^(896)", upc)):
  return "Pakistan";
 if(re.findall("^(899)", upc)):
  return "Indonesia";
 if(re.findall("^(9[0-1][0-9])", upc)):
  return "Austria";
 if(re.findall("^(93[0-9])", upc)):
  return "Australia";
 if(re.findall("^(94[0-9])", upc)):
  return "New Zealand";
 if(re.findall("^(950)", upc)):
  return "GS1 Global Office: Special applications";
 if(re.findall("^(951)", upc)):
  return "EPCglobal: Special applications";
 if(re.findall("^(955)", upc)):
  return "Malaysia";
 if(re.findall("^(958)", upc)):
  return "Macau";
 if(re.findall("^(960)", upc)):
  return "GS1 UK: GTIN-8 allocations";
 if(re.findall("^(96[1-9])", upc)):
  return "GS1 Global Office: GTIN-8 allocations";
 if(re.findall("^(977)", upc)):
  return "Serial publications (ISSN)";
 if(re.findall("^(97[8-9])", upc)):
  return "Bookland (ISBN)";
 if(re.findall("^(980)", upc)):
  return "Refund receipts";
 if(re.findall("^(98[1-3])", upc)):
  return "Common Currency Coupons";
 if(re.findall("^(99[0-9])", upc)):
  return "Coupons";
 '''
 // Reserved for future use
 '''
 if(re.findall("^(1[4-9][0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(381|382|384|386|388)", upc)):
  return "Reserved for future use";
 if(re.findall("^(39[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(44[1-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(472|473|483)", upc)):
  return "Reserved for future use";
 if(re.findall("^(51[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(52[1-7])", upc)):
  return "Reserved for future use";
 if(re.findall("^(53[2-4])", upc)):
  return "Reserved for future use";
 if(re.findall("^(53[6-8])", upc)):
  return "Reserved for future use";
 if(re.findall("^(55[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(56[1-8])", upc)):
  return "Reserved for future use";
 if(re.findall("^(58[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(59[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall("^(59[5-8])", upc)):
  return "Reserved for future use";
 if(re.findall("^(602)", upc)):
  return "Reserved for future use";
 if(re.findall("^(60[5-7])", upc)):
  return "Reserved for future use";
 if(re.findall("^(610|612|614|617|620|623)", upc)):
  return "Reserved for future use";
 if(re.findall("^(63[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(6[5-8][0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(69[6-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(71[0-9]|72[0-8])", upc)):
  return "Reserved for future use";
 if(re.findall("^(74[7-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(75[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall("^(75[6-8])", upc)):
  return "Reserved for future use";
 if(re.findall("^(772|774|776|778)", upc)):
  return "Reserved for future use";
 if(re.findall("^(78[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall("^(785|787|788)", upc)):
  return "Reserved for future use";
 if(re.findall("^(79[1-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(85[1-7])", upc)):
  return "Reserved for future use";
 if(re.findall("^(86[1-4])", upc)):
  return "Reserved for future use";
 if(re.findall("^(866)", upc)):
  return "Reserved for future use";
 if(re.findall("^(88[1-3])", upc)):
  return "Reserved for future use";
 if(re.findall("^(886|887|889|891|892|895|897|898)", upc)):
  return "Reserved for future use";
 if(re.findall("^(92[0-9])", upc)):
  return "Reserved for future use";
 if(re.findall("^(95[2-4])", upc)):
  return "Reserved for future use";
 if(re.findall("^(956|957|959)", upc)):
  return "Reserved for future use";
 if(re.findall("^(96[0-9]|97[0-6])", upc)):
  return "Reserved for future use";
 if(re.findall("^(98[4-9])", upc)):
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
  fix_matches = re.findall("^(\d{9})(\d{1}|X{1})", upc);
  fix_matches = fix_matches[0]
  upc = fix_matches[0]+fix_matches[1];
 if(len(upc)>10 or len(upc)<10):
  return False;
 if(re.findall("^99972", upc)):
  return "Faroe Islands";
 if(re.findall("^99971", upc)):
  return "Myanmar";
 if(re.findall("^99970", upc)):
  return "Haiti";
 if(re.findall("^99969", upc)):
  return "Oman";
 if(re.findall("^99968", upc)):
  return "Botswana";
 if(re.findall("^99967", upc)):
  return "Paraguay";
 if(re.findall("^99966", upc)):
  return "Kuwait";
 if(re.findall("^99965", upc)):
  return "Macau";
 if(re.findall("^99964", upc)):
  return "Nicaragua";
 if(re.findall("^99963", upc)):
  return "Cambodia";
 if(re.findall("^99962", upc)):
  return "Mongolia";
 if(re.findall("^99961", upc)):
  return "El Salvador";
 if(re.findall("^99960", upc)):
  return "Malawi";
 if(re.findall("^99959", upc)):
  return "Luxembourg";
 if(re.findall("^99958", upc)):
  return "Bahrain";
 if(re.findall("^99957", upc)):
  return "Malta";
 if(re.findall("^99956", upc)):
  return "Albania";
 if(re.findall("^99955", upc)):
  return "Republika Srpska";
 if(re.findall("^99954", upc)):
  return "Bolivia";
 if(re.findall("^99953", upc)):
  return "Paraguay";
 if(re.findall("^99952", upc)):
  return "Mali";
 if(re.findall("^99951", upc)):
  return "Democratic Republic of Congo";
 if(re.findall("^99950", upc)):
  return "Cambodia";
 if(re.findall("^99949", upc)):
  return "Mauritius";
 if(re.findall("^99948", upc)):
  return "Eritrea";
 if(re.findall("^99947", upc)):
  return "Tajikistan";
 if(re.findall("^99946", upc)):
  return "Nepal";
 if(re.findall("^99945", upc)):
  return "Namibia";
 if(re.findall("^99944", upc)):
  return "Ethiopia";
 if(re.findall("^99943", upc)):
  return "Albania";
 if(re.findall("^99942", upc)):
  return "Sudan";
 if(re.findall("^99941", upc)):
  return "Armenia";
 if(re.findall("^99939", upc)):
  return "Guatemala";
 if(re.findall("^99938", upc)):
  return "Republika Srpska";
 if(re.findall("^99937", upc)):
  return "Macau";
 if(re.findall("^99936", upc)):
  return "Bhutan";
 if(re.findall("^99935", upc)):
  return "Haiti";
 if(re.findall("^99934", upc)):
  return "Dominican republic";
 if(re.findall("^99933", upc)):
  return "Nepal";
 if(re.findall("^99932", upc)):
  return "Malta";
 if(re.findall("^99931", upc)):
  return "Seychelles";
 if(re.findall("^99930", upc)):
  return "Armenia";
 if(re.findall("^99929", upc)):
  return "Mongolia";
 if(re.findall("^99928", upc)):
  return "Georgia";
 if(re.findall("^99927", upc)):
  return "Albania";
 if(re.findall("^99926", upc)):
  return "Honduras";
 if(re.findall("^99925", upc)):
  return "Paraguay";
 if(re.findall("^99924", upc)):
  return "Nicaragua";
 if(re.findall("^99923", upc)):
  return "El Salvador";
 if(re.findall("^99922", upc)):
  return "Guatemala";
 if(re.findall("^99921", upc)):
  return "Qatar";
 if(re.findall("^99920", upc)):
  return "Andorra";
 if(re.findall("^99919", upc)):
  return "Benin";
 if(re.findall("^99918", upc)):
  return "Faroe Islands";
 if(re.findall("^99917", upc)):
  return "Brunei Darussalam";
 if(re.findall("^99916", upc)):
  return "Namibia";
 if(re.findall("^99915", upc)):
  return "Maldives";
 if(re.findall("^99914", upc)):
  return "Suriname";
 if(re.findall("^99913", upc)):
  return "Andorra";
 if(re.findall("^99912", upc)):
  return "Botsana";
 if(re.findall("^99911", upc)):
  return "Lesotho";
 if(re.findall("^99910", upc)):
  return "Sierra Leone";
 if(re.findall("^99909", upc)):
  return "Malta";
 if(re.findall("^99908", upc)):
  return "Malawi";
 if(re.findall("^99906", upc)):
  return "Kuwait";
 if(re.findall("^99905", upc)):
  return "Bolivia";
 if(re.findall("^99904", upc)):
  return "Netherland Antilles, and Aruba";
 if(re.findall("^99903", upc)):
  return "Mauritius";
 if(re.findall("^99902", upc)):
  return "Gabon";
 if(re.findall("^99901", upc)):
  return "Bahrain";
 if(re.findall("^9989", upc)):
  return "Macedonia";
 if(re.findall("^9988", upc)):
  return "Ghana";
 if(re.findall("^9987", upc)):
  return "Tanzania";
 if(re.findall("^9986", upc)):
  return "Lithuania";
 if(re.findall("^9985", upc)):
  return "Estonia";
 if(re.findall("^9984", upc)):
  return "Latvia";
 if(re.findall("^9983", upc)):
  return "Gambia";
 if(re.findall("^9982", upc)):
  return "Zambia";
 if(re.findall("^9981", upc)):
  return "Morocco";
 if(re.findall("^9980", upc)):
  return "Papua New Guinea";
 if(re.findall("^9979", upc)):
  return "Iceland";
 if(re.findall("^9978", upc)):
  return "Ecuador";
 if(re.findall("^9977", upc)):
  return "Costa Rica";
 if(re.findall("^9976", upc)):
  return "Tanzania";
 if(re.findall("^9975", upc)):
  return "Moldova";
 if(re.findall("^9974", upc)):
  return "Uruguay";
 if(re.findall("^9973", upc)):
  return "Tunisia";
 if(re.findall("^9972", upc)):
  return "Peru";
 if(re.findall("^9971", upc)):
  return "Singapore";
 if(re.findall("^9970", upc)):
  return "Uganda";
 if(re.findall("^9968", upc)):
  return "Costa Rica";
 if(re.findall("^9967", upc)):
  return "Kyrgyzstan";
 if(re.findall("^9966", upc)):
  return "Kenya";
 if(re.findall("^9965", upc)):
  return "Kazakhstan";
 if(re.findall("^9964", upc)):
  return "Ghana";
 if(re.findall("^9963", upc)):
  return "Cyprus";
 if(re.findall("^9962", upc)):
  return "Panama";
 if(re.findall("^9961", upc)):
  return "Algeria";
 if(re.findall("^9960", upc)):
  return "Saudi Arabia";
 if(re.findall("^9959", upc)):
  return "Libya";
 if(re.findall("^9958", upc)):
  return "Bosnia and Herzegovina";
 if(re.findall("^9957", upc)):
  return "Jordan";
 if(re.findall("^9956", upc)):
  return "Cameroon";
 if(re.findall("^9955", upc)):
  return "Lithuania";
 if(re.findall("^9954", upc)):
  return "Morocco";
 if(re.findall("^9953", upc)):
  return "Lebanon";
 if(re.findall("^9952", upc)):
  return "Azerbaijan";
 if(re.findall("^9951", upc)):
  return "Kosovo";
 if(re.findall("^9950", upc)):
  return "Palestine";
 if(re.findall("^9949", upc)):
  return "Estonia";
 if(re.findall("^9948", upc)):
  return "United Arab Emirates";
 if(re.findall("^9947", upc)):
  return "Algeria";
 if(re.findall("^9946", upc)):
  return "North Korea";
 if(re.findall("^9945", upc)):
  return "Dominican Republic";
 if(re.findall("^9944", upc)):
  return "Turkey";
 if(re.findall("^9943", upc)):
  return "Uzbekistan";
 if(re.findall("^9942", upc)):
  return "Ecuador";
 if(re.findall("^9941", upc)):
  return "Georgia";
 if(re.findall("^9940", upc)):
  return "Montenegro";
 if(re.findall("^9939", upc)):
  return "Armenia";
 if(re.findall("^9937", upc)):
  return "Nepal";
 if(re.findall("^9936", upc)):
  return "Afghanistan";
 if(re.findall("^9935", upc)):
  return "Iceland";
 if(re.findall("^9934", upc)):
  return "Latvia";
 if(re.findall("^9933", upc)):
  return "Syria";
 if(re.findall("^9932", upc)):
  return "Laos";
 if(re.findall("^9931", upc)):
  return "Algeria";
 if(re.findall("^9930", upc)):
  return "Costa Rica";
 if(re.findall("^9929", upc)):
  return "Guatemala";
 if(re.findall("^9928", upc)):
  return "Albania";
 if(re.findall("^9927", upc)):
  return "Qatar";
 if(re.findall("^989", upc)):
  return "Portugal";
 if(re.findall("^988", upc)):
  return "Hong Kong";
 if(re.findall("^987", upc)):
  return "Argentina";
 if(re.findall("^986", upc)):
  return "Taiwan";
 if(re.findall("^985", upc)):
  return "Belarus";
 if(re.findall("^984", upc)):
  return "Bangladesh";
 if(re.findall("^983", upc)):
  return "Malaysia";
 if(re.findall("^982", upc)):
  return "South Pacific";
 if(re.findall("^981", upc)):
  return "Singapore";
 if(re.findall("^980", upc)):
  return "Venezuela";
 if(re.findall("^979", upc)):
  return "Indonesia";
 if(re.findall("^978", upc)):
  return "Nigeria";
 if(re.findall("^977", upc)):
  return "Egypt";
 if(re.findall("^976", upc)):
  return "CARICOM";
 if(re.findall("^975", upc)):
  return "Turkey";
 if(re.findall("^974", upc)):
  return "Thailand";
 if(re.findall("^973", upc)):
  return "Romania";
 if(re.findall("^972", upc)):
  return "Portugal";
 if(re.findall("^971", upc)):
  return "Philippines";
 if(re.findall("^970", upc)):
  return "Mexico";
 if(re.findall("^969", upc)):
  return "Pakistan";
 if(re.findall("^968", upc)):
  return "Mexico";
 if(re.findall("^967", upc)):
  return "Malaysia";
 if(re.findall("^966", upc)):
  return "Ukraine";
 if(re.findall("^965", upc)):
  return "Israel";
 if(re.findall("^964", upc)):
  return "Iran";
 if(re.findall("^963", upc)):
  return "Hungary";
 if(re.findall("^962", upc)):
  return "Hong Kong";
 if(re.findall("^961", upc)):
  return "Slovenia";
 if(re.findall("^960", upc)):
  return "Greece";
 if(re.findall("^959", upc)):
  return "Cuba";
 if(re.findall("^958", upc)):
  return "Colombia";
 if(re.findall("^957", upc)):
  return "Taiwan";
 if(re.findall("^956", upc)):
  return "Chile";
 if(re.findall("^955", upc)):
  return "Sri Lanka";
 if(re.findall("^954", upc)):
  return "Bulgaria";
 if(re.findall("^953", upc)):
  return "Croatia";
 if(re.findall("^952", upc)):
  return "Finland";
 if(re.findall("^951", upc)):
  return "Finland";
 if(re.findall("^950", upc)):
  return "Argentina";
 if(re.findall("^621", upc)):
  return "Philippines";
 if(re.findall("^620", upc)):
  return "Mauritius";
 if(re.findall("^619", upc)):
  return "Bulgaria";
 if(re.findall("^618", upc)):
  return "Greece";
 if(re.findall("^617", upc)):
  return "Ukraine";
 if(re.findall("^616", upc)):
  return "Thailand";
 if(re.findall("^615", upc)):
  return "Hungary";
 if(re.findall("^614", upc)):
  return "Lebanon";
 if(re.findall("^613", upc)):
  return "Mauritius";
 if(re.findall("^612", upc)):
  return "Peru";
 if(re.findall("^611", upc)):
  return "Thailand";
 if(re.findall("^609", upc)):
  return "Lithuania";
 if(re.findall("^608", upc)):
  return "Macedonia";
 if(re.findall("^607", upc)):
  return "Mexico";
 if(re.findall("^606", upc)):
  return "Romania";
 if(re.findall("^605", upc)):
  return "Turkey";
 if(re.findall("^604", upc)):
  return "Vietnam";
 if(re.findall("^603", upc)):
  return "Saudi Arabia";
 if(re.findall("^602", upc)):
  return "Indonesia";
 if(re.findall("^601", upc)):
  return "Kazakhstan";
 if(re.findall("^600", upc)):
  return "Iran";
 if(re.findall("^94", upc)):
  return "Netherlands";
 if(re.findall("^93", upc)):
  return "India";
 if(re.findall("^92", upc)):
  return "International NGO Publishers and EC Organizations";
 if(re.findall("^91", upc)):
  return "Sweden";
 if(re.findall("^90", upc)):
  return "Netherlands";
 if(re.findall("^89", upc)):
  return "Republic of Korea";
 if(re.findall("^88", upc)):
  return "Italy";
 if(re.findall("^87", upc)):
  return "Denmark";
 if(re.findall("^86", upc)):
  return "Serbia (shared)";
 if(re.findall("^85", upc)):
  return "Brazil";
 if(re.findall("^84", upc)):
  return "Spain";
 if(re.findall("^83", upc)):
  return "Poland";
 if(re.findall("^82", upc)):
  return "Norway";
 if(re.findall("^81", upc)):
  return "India";
 if(re.findall("^80", upc)):
  return "Czech Republic and Slovakia";
 if(re.findall("^7", upc)):
  return "China";
 if(re.findall("^5", upc)):
  return "Russia and former USSR";
 if(re.findall("^4", upc)):
  return "Japan";
 if(re.findall("^3", upc)):
  return "German";
 if(re.findall("^2", upc)):
  return "French";
 if(re.findall("^1", upc)):
  return "English";
 if(re.findall("^0", upc)):
  return "English";
 return False;
