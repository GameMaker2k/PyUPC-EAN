# -*- coding: utf-8 -*- 

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2014 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2014 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2014 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: getprefix.py - Last Update: 11/02/2014 Ver. 2.7.3 RC 1  - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import sys, re, upcean.validate, upcean.convert;

'''
// Get GS1 Prefix for EAN-13 EAN-9 barcodes
// Source: http://en.wikipedia.org/wiki/List_of_GS1_country_codes
'''
def get_gs1_prefix(upc):
 upc = str(upc);
 if(re.findall("^(\d{12})", upc)):
  upc = "0"+upc;
 if(re.findall("^0(\d{3}\d{10})", upc)):
  fix_ean = re.findall("^0(\d{3}\d{10})", upc);
  upc = fix_ean[0];
 if(not re.findall("^(\d{3}\d{5}|\d{3}\d{10})$", upc)):
  return False;
 if(re.findall("^(\d{3}\d{10})$", upc) and upcean.validate.validate_ean13_checksum(upc)==False):
  return False;
 if(re.findall("^(\d{3}\d{5})$", upc) and upcean.validate.validate_ean8_checksum(upc)==False):
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
  return "F.Y.R.O. Macedonia";
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
  if(sys.version[0]=="2"):
   return u"Côte d'Ivoire";
  if(sys.version[0]=="3"):
   return "Côte d'Ivoire";
 if(re.findall("^(619)", upc)):
  return "Tunisia";
 if(re.findall("^(621)", upc)):
  return "Syria";
 if(re.findall("^(622)", upc)):
  return "Egypt";
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
  return "Czech Republic";
 if(re.findall("^(860)", upc)):
  return "Serbia";
 if(re.findall("^(865)", upc)):
  return "Mongolia";
 if(re.findall("^(867)", upc)):
  return "North Korea";
 if(re.findall("^(86[8-9])", upc)):
  return "Turkey";
 if(re.findall("^(87[0-9])", upc)):
  return "Netherlands";
 if(re.findall("^(880)", upc)):
  return "South Korea";
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
 if(re.findall("^(96[0-9])", upc)):
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
  return "Serbia ";(shared)
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

def get_upca_barcode_info(upc):
 upc = str(upc);
 if(len(upc)==8):
  upc = upcean.convert.convert_barcode_from_upce_to_upca(upc);
 if(re.findall("^0(\d{13})", upc)):
  upc_matches = re.findall("^0(\d{13})", upc);
  upc = upc_matches[0];
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 upc_matches = re.findall("^(\d{1})(\d{5})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': None, 'numbersystem': pre_upc_type[0], 'manufacturer': pre_upc_type[1], 'product': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 return upc_type;
def get_upca_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_upca_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_upca_barcode_product(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['product'];
def get_upca_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_upca_barcode_info_from_upce(upc):
 return get_upca_barcode_info(convert_upce_to_upca(upc));
def get_upce_barcode_info(upc):
 upc = str(upc);
 if(re.findall("^0(\d{13})", upc)):
  upc_matches = re.findall("^0(\d{13})", upc);
  upc = upc_matches[0];
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(len(upc)==12):
  upc = convert_upca_to_upce(upc);
 if(not re.findall("^(\d{8})", upc)):
  return False;
 get_ns = None;
 get_manufac = None;
 get_product = None;
 get_checksum = None;
 if(re.findall("(0|1)(\d{2})(\d{3})(0)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})(\d{3})(0)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2]+upc_matches[3];
  get_checksum = upc_matches[4];
 if(re.findall("(0|1)(\d{2})(\d{3})(1)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})(\d{3})(1)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2]+upc_matches[3];
  get_checksum = upc_matches[4];
 if(re.findall("(0|1)(\d{2})(\d{3})(2)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{2})(\d{3})(2)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2]+upc_matches[3];
  get_checksum = upc_matches[4];
 if(re.findall("(0|1)(\d{3})(\d{2})(3)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{3})(\d{2})(3)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2]+upc_matches[3];
  get_checksum = upc_matches[4];
 if(re.findall("(0|1)(\d{4})(\d{1})(4)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{4})(\d{1})(4)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2]+upc_matches[3];
  get_checksum = upc_matches[4];
 if(re.findall("(0|1)(\d{5})(5)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})(5)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2];
  get_checksum = upc_matches[3];
 if(re.findall("(0|1)(\d{5})(6)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})(6)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2];
  get_checksum = upc_matches[3];
 if(re.findall("(0|1)(\d{5})(7)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})(7)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2];
  get_checksum = upc_matches[3];
 if(re.findall("(0|1)(\d{5})(8)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})(8)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2];
  get_checksum = upc_matches[3];
 if(re.findall("(0|1)(\d{5})(9)(\d{1})", upc)):
  upc_matches = re.findall("(0|1)(\d{5})(9)(\d{1})", upc);
  upc_matches = upc_matches[0];
  get_ns = upc_matches[0];
  get_manufac = upc_matches[1];
  get_product = upc_matches[2];
  get_checksum = upc_matches[3];
 upc_type = {'packagecode': None, 'numbersystem': get_ns, 'manufacturer': get_manufac, 'product': get_product, 'checkdigit': get_checksum};
 return upc_type;
def get_upce_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_upce_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_upce_barcode_product(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(product==False):
  return False;
 return product['product'];
def get_upce_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_ean8_barcode_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{8})", upc)):
  return False;
 upc_matches = re.findall("^(\d{2})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': None, 'numbersystem': pre_upc_type[0], 'manufacturer': None, 'product': pre_upc_type[1], 'checkdigit': pre_upc_type[2]};
 return upc_type;
def get_ean8_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_ean8_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_ean8_barcode_product(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(product==False):
  return False;
 return product['product'];
def get_ean8_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_ean13_barcode_info(upc):
 upc = str(upc);
 if(len(upc)==8):
  upc = convert_upce_to_upca(upc);
 if(len(upc)==12):
  upc = "0"+upc;
 if(not re.findall("^(\d{13})", upc)):
  return False;
 upc_matches = re.findall("^(\d{2})(\d{5})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': None, 'numbersystem': pre_upc_type[0], 'manufacturer': pre_upc_type[1], 'product': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 return upc_type;
def get_ean13_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_ean13_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_ean13_barcode_product(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(product==False):
  return False;
 return product['product'];
def get_ean13_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_itf14_barcode_info(upc):
 upc = str(upc);
 if(len(upc)==12):
  upc = "00"+upc;
 if(len(upc)==13):
  upc = "0"+upc;
 if(not re.findall("^(\d{14})", upc)):
  return False;
 upc_matches = re.findall("^(\d{1})(\d{2})(\d{5})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': pre_upc_type[0], 'numbersystem': pre_upc_type[1], 'manufacturer': pre_upc_type[2], 'product': pre_upc_type[3], 'checkdigit': pre_upc_type[4]};
 return upc_type;
def get_itf14_barcode_packagecode(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(product==False):
  return False;
 return product['packagecode'];
def get_itf14_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_itf14_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_itf14_barcode_product(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(product==False):
  return False;
 return product['product'];
def get_itf14_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
'''
// Get Number System Prefix for UPC-A barcodes
// Source: http://www.morovia.com/education/symbology/upc-a.asp
// Source: http://www.computalabel.com/aboutupc.htm
'''
def get_upca_barcode_ns(upc):
 upc = str(upc);
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 if(re.findall("^(0)", upc)):
  return "Regular UPC";
 if(re.findall("^(1)", upc)):
  return "Regular UPC";
 if(re.findall("^(2)", upc)):
  return "Variable Weight Items";
 if(re.findall("^(3)", upc)):
  return "DrugHealth Items";
 if(re.findall("^(4)", upc)):
  return "In-store use";
 if(re.findall("^(5)", upc)):
  return "Coupons";
 if(re.findall("^(6)", upc)):
  return "Regular UPC";
 if(re.findall("^(7)", upc)):
  return "Regular UPC";
 if(re.findall("^(8)", upc)):
  return "Regular UPC";
 if(re.findall("^(9)", upc)):
  return "Coupons";
 return False;

'''
// Get ITF-14 Packaging Indicator
// Source: http://www.mecsw.com/specs/itf_14.html
// Source: http://www.qed.org/RBTL/chapters/ch3.3.htm
'''
def get_itf14_barcode_type(upc):
 upc = str(upc);
 if(not re.findall("^(\d{14})", upc)):
  return False;
 if(re.findall("^(0)", upc)):
  return "UPC code of contents differs from case code";
 if(re.findall("^(1)", upc)):
  return "More than each and below inner packs";
 if(re.findall("^(2)", upc)):
  return "More than each and below inner packs";
 if(re.findall("^(3)", upc)):
  return "Inner packs";
 if(re.findall("^(4)", upc)):
  return "Inner packs";
 if(re.findall("^(5)", upc)):
  return "Shipping containers (cartons)";
 if(re.findall("^(6)", upc)):
  return "Shipping containers (cartons)";
 if(re.findall("^(7)", upc)):
  return "Pallet";
 if(re.findall("^(8)", upc)):
  return "Reserved";
 if(re.findall("^(9)", upc)):
  return "Variable quantity content";
 return False;

'''
// Get Goodwill UPC Info.
'''
def get_goodwill_upca_barcode_info(upc):
 upc = str(upc);
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 if(not re.findall("^4(\d{11})", upc)):
  return False;
 upc_matches = re.findall("^4(\d{5})(\d{5})(\d{1})", upc);
 upc_matches = upc_matches[0];
 product = {'numbersystem': str(4), 'code': upc_matches[0], 'price': upc_matches[1], 'checkdigit': upc_matches[2]};
 return product;
def get_goodwill_upca_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_goodwill_upca_barcode_code(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['code'];
def get_goodwill_upca_barcode_price(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['price'];
def get_goodwill_upca_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];

'''
// Get variable weight info
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
'''
def get_upca_vw_barcode_info(upc):
 upc = str(upc);
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 if(not re.findall("^2(\d{11})", upc)):
  return False;
 upc_matches = re.findall("^2(\d{5})(\d{1})(\d{4})(\d{1})", upc);
 upc_matches = upc_matches[0];
 product = {'numbersystem': str(2), 'code': upc_matches[0], 'pricecs': upc_matches[1], 'price': upc_matches[2], 'checkdigit': upc_matches[3]};
 return product;
def get_upca_vw_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_upca_vw_barcode_code(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(product==False):
  return False;
 return product['code'];
def get_upca_vw_barcode_price(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(product==False):
  return False;
 return product['price'];
def get_upca_vw_barcode_pricecs(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(product==False):
  return False;
 return product['pricecs'];
def get_upca_vw_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];

'''
// Get coupon info
// Source: http://divagirlusa-ivil.tripod.com/austinitecouponers/id29.html
'''
def get_upca_coupon_barcode_info(upc):
 upc = str(upc);
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 if(not re.findall("^(5|9)(\d{11})", upc)):
  return False;
 upc_matches = re.findall("^(5|9)(\d{5})(\d{3})(\d{2})(\d{1})", upc);
 upc_matches = upc_matches[0];
 product = {'numbersystem': upc_matches[0], 'manufacturer': upc_matches[1], 'family': upc_matches[2], 'value': upc_matches[3], 'checkdigit': upc_matches[4]};
 return product;
def get_upca_coupon_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(product==False):
  return False;
 return product['numbersystem'];
def get_upca_coupon_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(product==False):
  return False;
 return product['manufacturer'];
def get_upca_coupon_barcode_family(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(product==False):
  return False;
 return product['family'];
def get_upca_coupon_barcode_value(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(product==False):
  return False;
 return product['value'];
def get_upca_coupon_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_upca_coupon_barcode_value_code(vcode):
 vcode = str(vcode);
 if(re.findall("^(00)", vcode)):
  return "Manual Input Required";
 if(re.findall("^(01)", vcode)):
  return "Free Item";
 if(re.findall("^(02)", vcode)):
  return "Buy 4 Get 1 Free";
 if(re.findall("^(03)", vcode)):
  return "$1.10";
 if(re.findall("^(04)", vcode)):
  return "$1.35";
 if(re.findall("^(05)", vcode)):
  return "$1.40";
 if(re.findall("^(06)", vcode)):
  return "$1.60";
 if(re.findall("^(07)", vcode)):
  return "Buy 3 For $1.50";
 if(re.findall("^(08)", vcode)):
  return "Buy 2 For $3.00";
 if(re.findall("^(09)", vcode)):
  return "Buy 3 For $2.00";
 if(re.findall("^(10)", vcode)):
  return "$0.10";
 if(re.findall("^(11)", vcode)):
  return "$1.85";
 if(re.findall("^(12)", vcode)):
  return "$0.12";
 if(re.findall("^(13)", vcode)):
  return "Buy 4 For $1.00";
 if(re.findall("^(14)", vcode)):
  return "Buy 1 Get 1 Free";
 if(re.findall("^(15)", vcode)):
  return "$0.15";
 if(re.findall("^(16)", vcode)):
  return "Buy 2 Get 1 Free";
 if(re.findall("^(17)", vcode)):
  return "Reserved for future use";
 if(re.findall("^(18)", vcode)):
  return "$2.60";
 if(re.findall("^(19)", vcode)):
  return "Buy 3 Get 1 Free";
 if(re.findall("^(20)", vcode)):
  return "$0.20";
 if(re.findall("^(21)", vcode)):
  return "Buy 2 For $0.35";
 if(re.findall("^(22)", vcode)):
  return "Buy 2 For $0.40";
 if(re.findall("^(23)", vcode)):
  return "Buy 2 For $0.45";
 if(re.findall("^(24)", vcode)):
  return "Buy 2 For $0.50";
 if(re.findall("^(25)", vcode)):
  return "$0.25";
 if(re.findall("^(26)", vcode)):
  return "$2.85";
 if(re.findall("^(27)", vcode)):
  return "Reserved for future use";
 if(re.findall("^(28)", vcode)):
  return "Buy 2 For $0.55";
 if(re.findall("^(29)", vcode)):
  return "$0.29";
 if(re.findall("^(30)", vcode)):
  return "$0.30";
 if(re.findall("^(31)", vcode)):
  return "Buy 2 For $0.60";
 if(re.findall("^(32)", vcode)):
  return "Buy 2 For $0.75";
 if(re.findall("^(33)", vcode)):
  return "Buy 2 For $1.00";
 if(re.findall("^(34)", vcode)):
  return "Buy 2 For $1.25";
 if(re.findall("^(35)", vcode)):
  return "$0.35";
 if(re.findall("^(36)", vcode)):
  return "Buy 2 For $1.50";
 if(re.findall("^(37)", vcode)):
  return "Buy 3 For $0.25";
 if(re.findall("^(38)", vcode)):
  return "Buy 3 For $0.30";
 if(re.findall("^(39)", vcode)):
  return "$0.39";
 if(re.findall("^(40)", vcode)):
  return "$0.40";
 if(re.findall("^(41)", vcode)):
  return "Buy 3 For $0.50";
 if(re.findall("^(42)", vcode)):
  return "Buy 3 For $1.00";
 if(re.findall("^(43)", vcode)):
  return "Buy 2 For $1.10";
 if(re.findall("^(44)", vcode)):
  return "Buy 2 For $1.35";
 if(re.findall("^(45)", vcode)):
  return "$0.45";
 if(re.findall("^(46)", vcode)):
  return "Buy 2 For $1.60";
 if(re.findall("^(47)", vcode)):
  return "Buy 2 For $1.75";
 if(re.findall("^(48)", vcode)):
  return "Buy 2 For $1.85";
 if(re.findall("^(49)", vcode)):
  return "$0.49";
 if(re.findall("^(50)", vcode)):
  return "$0.50";
 if(re.findall("^(51)", vcode)):
  return "Buy 2 For $2.00";
 if(re.findall("^(52)", vcode)):
  return "Buy 3 For $0.55";
 if(re.findall("^(53)", vcode)):
  return "Buy 2 For $0.10";
 if(re.findall("^(54)", vcode)):
  return "Buy 2 For $0.15";
 if(re.findall("^(55)", vcode)):
  return "$0.55";
 if(re.findall("^(56)", vcode)):
  return "Buy 2 For $0.20";
 if(re.findall("^(57)", vcode)):
  return "Buy 2 For $0.25";
 if(re.findall("^(58)", vcode)):
  return "Buy 2 For $0.30";
 if(re.findall("^(59)", vcode)):
  return "$0.59";
 if(re.findall("^(60)", vcode)):
  return "$0.60";
 if(re.findall("^(61)", vcode)):
  return "$10.00";
 if(re.findall("^(62)", vcode)):
  return "$9.50";
 if(re.findall("^(63)", vcode)):
  return "$9.00";
 if(re.findall("^(64)", vcode)):
  return "$8.50";
 if(re.findall("^(65)", vcode)):
  return "$0.65";
 if(re.findall("^(66)", vcode)):
  return "$8.00";
 if(re.findall("^(67)", vcode)):
  return "$7.50";
 if(re.findall("^(68)", vcode)):
  return "$7.00";
 if(re.findall("^(69)", vcode)):
  return "$0.69";
 if(re.findall("^(70)", vcode)):
  return "$0.70";
 if(re.findall("^(71)", vcode)):
  return "$6.50";
 if(re.findall("^(72)", vcode)):
  return "$6.00";
 if(re.findall("^(73)", vcode)):
  return "$5.50";
 if(re.findall("^(74)", vcode)):
  return "$5.00";
 if(re.findall("^(75)", vcode)):
  return "$0.75";
 if(re.findall("^(76)", vcode)):
  return "$1.00";
 if(re.findall("^(77)", vcode)):
  return "$1.25";
 if(re.findall("^(78)", vcode)):
  return "$1.50";
 if(re.findall("^(79)", vcode)):
  return "$0.79";
 if(re.findall("^(80)", vcode)):
  return "$0.80";
 if(re.findall("^(81)", vcode)):
  return "$1.75";
 if(re.findall("^(82)", vcode)):
  return "$2.00";
 if(re.findall("^(83)", vcode)):
  return "$2.25";
 if(re.findall("^(84)", vcode)):
  return "$2.50";
 if(re.findall("^(85)", vcode)):
  return "$0.85";
 if(re.findall("^(86)", vcode)):
  return "$2.75";
 if(re.findall("^(87)", vcode)):
  return "$3.00";
 if(re.findall("^(88)", vcode)):
  return "$3.25";
 if(re.findall("^(89)", vcode)):
  return "$0.89";
 if(re.findall("^(90)", vcode)):
  return "$0.90";
 if(re.findall("^(91)", vcode)):
  return "$3.50";
 if(re.findall("^(92)", vcode)):
  return "$3.75";
 if(re.findall("^(93)", vcode)):
  return "$4.00";
 if(re.findall("^(94)", vcode)):
  return "Reserved for future use";
 if(re.findall("^(95)", vcode)):
  return "$0.95";
 if(re.findall("^(96)", vcode)):
  return "$4.50";
 if(re.findall("^(97)", vcode)):
  return "Reserved for future use";
 if(re.findall("^(98)", vcode)):
  return "Buy 2 For $0.65";
 if(re.findall("^(99)", vcode)):
  return "$0.99";
 return False;

'''
// Get Major Industry Identifier for Bank Card Number
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_bcn_mii_prefix(upc):
 upc = str(upc);
 upc = upc.replace("-", "");
 upc = upc.replace(" ", "");
 if(not re.findall("^(\d{16})", upc)):
  return False;
 if(re.findall("^(0)", upc)):
  return "ISO/TC 68";
 if(re.findall("^(1)", upc)):
  return "Airlines";
 if(re.findall("^(2)", upc)):
  return "Airlines";
 if(re.findall("^(3)", upc)):
  return "Travel and Entertainment and Banking/Financial";
 if(re.findall("^(4)", upc)):
  return "Banking and Financial";
 if(re.findall("^(5)", upc)):
  return "Banking and Financial";
 if(re.findall("^(6)", upc)):
  return "Merchandising and Banking/Financial";
 if(re.findall("^(7)", upc)):
  return "Petroleum";
 if(re.findall("^(8)", upc)):
  return "Healthcare and Telecommunications";
 if(re.findall("^(9)", upc)):
  return "National Assignment";
 return False;

'''
// Get UPS Checkdigit and Info by stebo0728 and HolidayBows
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit?msg=2961884#xx2961884xx
'''
def get_ups_barcode_info(upc):
 upc = str(upc).upper();
 if(not re.findall("^1Z", upc)):
  return False;
 if(re.findall("^1Z", upc)):
  fix_matches = re.findall("^1Z(\w*)", upc);
  upc = fix_matches[0];
 if(len(upc)>16):
  fix_matches = re.findall("^(\w{16})", upc);
  upc = fix_matches[0];
 upc_matches = re.findall("^(\w{6})(\w{2})(\w{5})(\w{2})(\w{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'accountnumber': pre_upc_type[0], 'servicetype': pre_upc_type[1], 'invoicenumber': pre_upc_type[2], 'packagenumber': pre_upc_type[3], 'checkdigit': pre_upc_type[4]};
 return upc_type;
def get_ups_barcode_accountnumber(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(product==False):
  return False;
 return product['accountnumber'];
def get_ups_barcode_servicetype(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(product==False):
  return False;
 return product['servicetype'];
def get_ups_barcode_servicetype_info(upc):
 upc = str(upc);
 upc = get_ups_barcode_servicetype(upc);
 if(re.findall("^(01)", upc)):
  return "Next Day Air Shipment";
 if(re.findall("^(02)", upc)):
  return "Second Day Air Shipment";
 if(re.findall("^(03)", upc)):
  return "Ground Shipment";
 return False;
def get_ups_barcode_invoicenumber(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(product==False):
  return False;
 return product['invoicenumber'];
def get_ups_barcode_packagenumber(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(product==False):
  return False;
 return product['packagenumber'];
def get_ups_barcode_checkdigit(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];

'''
// Get IMEI (International Mobile Station Equipment Identity) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_new_imei_barcode_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{8})(\d{6})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'serialnumber': pre_upc_type[1], 'checkdigit': pre_upc_type[2]};
 return upc_type;
def get_new_imei_barcode_tac(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['tac'];
def get_new_imei_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['serialnumber'];
def get_new_imei_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];
def get_old_imei_barcode_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{6})(\d{2})(\d{6})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'fac': pre_upc_type[1], 'serialnumber': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 return upc_type;
def get_old_imei_barcode_tac(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['tac'];
def get_old_imei_barcode_fac(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['fac'];
def get_old_imei_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['serialnumber'];
def get_old_imei_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];

'''
// Get IMEISV (International Mobile Station Equipment Identity Software Version) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_new_imeisv_barcode_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{8})(\d{6})(\d{2})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'serialnumber': pre_upc_type[1], 'svn': pre_upc_type[2]};
 return upc_type;
def get_new_imeisv_barcode_tac(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['tac'];
def get_new_imeisv_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['serialnumber'];
def get_new_imeisv_barcode_svn(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['svn'];
def get_old_imeisv_barcode_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{6})(\d{2})(\d{6})(\d{2})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'fac': pre_upc_type[1], 'serialnumber': pre_upc_type[2], 'svn': pre_upc_type[3]};
 return upc_type;
def get_old_imeisv_barcode_tac(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['tac'];
def get_old_imeisv_barcode_fac(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['fac'];
def get_old_imeisv_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['serialnumber'];
def get_old_imeisv_barcode_svn(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(product==False):
  return False;
 return product['svn'];

'''
// Get Bank Card Number Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_bcn_info(upc):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{1})(\d{5})(\d{12})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'mii': pre_upc_type[0], 'iin': pre_upc_type[0]+pre_upc_type[1], 'account': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 return upc_type;
def get_bcn_mii(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(product==False):
  return False;
 return product['mii'];
def get_bcn_iin(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(product==False):
  return False;
 return product['iin'];
def get_bcn_account(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(product==False):
  return False;
 return product['account'];
def get_bcn_checkdigit(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(product==False):
  return False;
 return product['checkdigit'];

'''
// Shortcut Codes by Kazuki Przyborowski
// getprefix
'''
def get_barcode_info(bctype, upc, infotype=None):
 if(infotype==None):
  if(hasattr(upcean, "get_"+bctype+"_barcode_info") and callable(getattr(upcean, "get_"+bctype+"_barcode_info"))):
   return getattr(upcean, "get_"+bctype+"_barcode_info")(upc);
  if(not hasattr(upcean, "get_"+bctype+"_barcode_info") or not callable(getattr(upcean, "get_"+bctype+"_barcode_info"))):
   return False;
 if(infotype!=None):
  if(hasattr(upcean, "get_"+bctype+"_barcode_"+infotype) and callable(getattr(upcean, "get_"+bctype+"_barcode_"+infotype))):
   return getattr(upcean, "get_"+bctype+"_barcode_"+infotype)(upc);
  if(not hasattr(upcean, "get_"+bctype+"_barcode_"+infotype) or not callable(getattr(upcean, "get_"+bctype+"_barcode_"+infotype))):
   return False;
 return False;
def get_barcode_packagecode(bctype, upc):
 if(hasattr(upcean, "get_"+bctype+"_barcode_packagecode") and callable(getattr(upcean, "get_"+bctype+"_barcode_packagecode"))):
  return getattr(upcean, "get_"+bctype+"_barcode_packagecode")(upc);
 if(not hasattr(upcean, "get_"+bctype+"_barcode_packagecode") or not callable(getattr(upcean, "get_"+bctype+"_barcode_packagecode"))):
  return False;
 return False;
def get_barcode_numbersystem(bctype, upc):
 if(hasattr(upcean, "get_"+bctype+"_barcode_numbersystem") and callable(getattr(upcean, "get_"+bctype+"_barcode_numbersystem"))):
  return getattr(upcean, "get_"+bctype+"_barcode_numbersystem")(upc);
 if(not hasattr(upcean, "get_"+bctype+"_barcode_numbersystem") or not callable(getattr(upcean, "get_"+bctype+"_barcode_numbersystem"))):
  return False;
 return False;
def get_barcode_manufacturer(bctype, upc):
 if(hasattr(upcean, "get_"+bctype+"_barcode_manufacturer") and callable(getattr(upcean, "get_"+bctype+"_barcode_manufacturer"))):
  return getattr(upcean, "get_"+bctype+"_barcode_manufacturer")(upc);
 if(not hasattr(upcean, "get_"+bctype+"_barcode_manufacturer") or not callable(getattr(upcean, "get_"+bctype+"_barcode_manufacturer"))):
  return False;
 return False;
def get_barcode_product(bctype, upc):
 if(hasattr(upcean, "get_"+bctype+"_barcode_product") and callable(getattr(upcean, "get_"+bctype+"_barcode_product"))):
  return getattr(upcean, "get_"+bctype+"_barcode_product")(upc);
 if(not hasattr(upcean, "get_"+bctype+"_barcode_product") or not callable(getattr(upcean, "get_"+bctype+"_barcode_product"))):
  return False;
 return False;
def get_barcode_checkdigit(bctype, upc):
 if(hasattr(upcean, "get_"+bctype+"_barcode_checkdigit") and callable(getattr(upcean, "get_"+bctype+"_barcode_checkdigit"))):
  return getattr(upcean, "get_"+bctype+"_barcode_checkdigit")(upc);
 if(not hasattr(upcean, "get_"+bctype+"_barcode_checkdigit") or not callable(getattr(upcean, "get_"+bctype+"_barcode_checkdigit"))):
  return False;
 return False;
