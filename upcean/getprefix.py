#!/usr/bin/python
# -*- coding: utf-8 -*- 

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2012 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2012 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2012 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: getprefix.py - Last Update: 02/13/2012 Ver. 2.2.5 RC 1 - Author: cooldude2k $
'''

import sys, re, upcean.validate;
from upcean.validate import *;

'''
// Get GS1 Prefix for EAN-13 EAN-9 barcodes
// Source: http://en.wikipedia.org/wiki/List_of_GS1_country_codes
'''
def get_gs1_prefix(upc):
	if(re.findall("^(\d{12})", upc)):
		upc = "0"+upc;
	if(re.findall("^0(\d{3}\d{10})", upc)):
		fix_ean = re.findall("^0(\d{3}\d{10})", upc);
		upc = fix_ean[0];
	if(not re.findall("^(\d{3}\d{5}|\d{3}\d{10})$", upc)):
		return False;
	if(re.findall("^(\d{3}\d{10})$", upc) and validate_ean13(upc)==False):
		return False;
	if(re.findall("^(\d{3}\d{5})$", upc) and validate_ean8(upc)==False):
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
	Reserved for future use
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
// Get Number System Prefix for UPC-A barcodes
// Source: http://www.morovia.com/education/symbology/upc-a.asp
// Source: http://www.computalabel.com/aboutupc.htm
'''
def get_upca_ns(upc):
	if(re.findall("^0(\d{12})", upc, upc_matches)):
		upc = upc_matches[1];
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
def get_itf14_type(upc):
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
// Get variable weight info
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
'''
def get_upca_vw_info(upc):
	if(re.findall("^0(\d{12})", upc, upc_matches)):
		upc = upc_matches[1];
	if(not re.findall("^(\d{12})", upc)):
		return False;
	if(not re.findall("^2(\d{11})", upc)):
		return False;
	upc_matches = re.findall("^2(\d{5})(\d{1})(\d{4})(\d{1})", upc);
	upc_matches = upc_matches[0];
	product = {'code': upc_matches[0], 'pricecs': upc_matches[1], 'price': upc_matches[2]}
	return product;
def get_upca_vw_code(upc):
	product = get_upca_vw_info(upc);
	if(product==False):
		return False;
	return product['code'];
def get_upca_vw_price(upc):
	product = get_upca_vw_info(upc);
	if(product==False):
		return False;
	return product['price'];
def get_upca_vw_pricecs(upc):
	product = get_upca_vw_info(upc);
	if(product==False):
		return False;
	return product['pricecs'];
'''
// Get coupon info
// Source: http://divagirlusa-ivil.tripod.com/austinitecouponers/id29.html
'''
def get_upca_coupon_info(upc):
	if(re.findall("^0(\d{12})", upc, upc_matches)):
		upc = upc_matches[1];
	if(not re.findall("^(\d{12})", upc)):
		return False;
	if(not re.findall("^(5|9)(\d{11})", upc)):
		return False;
	upc_matches = re.findall("^(5|9)(\d{5})(\d{3})(\d{2})(\d{1})", upc);
	upc_matches = upc_matches[0];
	product = {'manufacturer': upc_matches[1], 'family': upc_matches[2], 'value': upc_matches[3]}
	return product;
def get_upca_coupon_manufacturer(upc):
	product = get_upca_coupon_info(upc);
	if(product==False):
		return False;
	return product['manufacturer'];
def get_upca_coupon_family(upc):
	product = get_upca_coupon_info(upc);
	if(product==False):
		return False;
	return product['family'];
def get_upca_coupon_value(upc):
	product = get_upca_coupon_info(upc);
	if(product==False):
		return False;
	return product['value'];
def get_upca_coupon_value_code(vcode):
	if(re.findall("^(00)", vcode)):
		return "Manual Input Required";
	if(re.findall("^(01)", vcode)):
		return "Free Item";
	if(re.findall("^(02)", vcode)):
		return "Buy 4 Get 1 Free";
	if(re.findall("^(03)", vcode)):
		return "\$1.10";
	if(re.findall("^(04)", vcode)):
		return "\$1.35";
	if(re.findall("^(05)", vcode)):
		return "\$1.40";
	if(re.findall("^(06)", vcode)):
		return "\$1.60";
	if(re.findall("^(07)", vcode)):
		return "Buy 3 For $1.50";
	if(re.findall("^(08)", vcode)):
		return "Buy 2 For $3.00";
	if(re.findall("^(09)", vcode)):
		return "Buy 3 For $2.00";
	if(re.findall("^(10)", vcode)):
		return "\$0.10";
	if(re.findall("^(11)", vcode)):
		return "\$1.85";
	if(re.findall("^(12)", vcode)):
		return "\$0.12";
	if(re.findall("^(13)", vcode)):
		return "Buy 4 For $1.00";
	if(re.findall("^(14)", vcode)):
		return "Buy 1 Get 1 Free";
	if(re.findall("^(15)", vcode)):
		return "\$0.15";
	if(re.findall("^(16)", vcode)):
		return "Buy 2 Get 1 Free";
	if(re.findall("^(17)", vcode)):
		return "Reserved for future use";
	if(re.findall("^(18)", vcode)):
		return "\$2.60";
	if(re.findall("^(19)", vcode)):
		return "Buy 3 Get 1 Free";
	if(re.findall("^(20)", vcode)):
		return "\$0.20";
	if(re.findall("^(21)", vcode)):
		return "Buy 2 For $0.35";
	if(re.findall("^(22)", vcode)):
		return "Buy 2 For $0.40";
	if(re.findall("^(23)", vcode)):
		return "Buy 2 For $0.45";
	if(re.findall("^(24)", vcode)):
		return "Buy 2 For $0.50";
	if(re.findall("^(25)", vcode)):
		return "\$0.25";
	if(re.findall("^(26)", vcode)):
		return "\$2.85";
	if(re.findall("^(27)", vcode)):
		return "Reserved for future use";
	if(re.findall("^(28)", vcode)):
		return "Buy 2 For $0.55";
	if(re.findall("^(29)", vcode)):
		return "\$0.29";
	if(re.findall("^(30)", vcode)):
		return "\$0.30";
	if(re.findall("^(31)", vcode)):
		return "Buy 2 For $0.60";
	if(re.findall("^(32)", vcode)):
		return "Buy 2 For $0.75";
	if(re.findall("^(33)", vcode)):
		return "Buy 2 For $1.00";
	if(re.findall("^(34)", vcode)):
		return "Buy 2 For $1.25";
	if(re.findall("^(35)", vcode)):
		return "\$0.35";
	if(re.findall("^(36)", vcode)):
		return "Buy 2 For $1.50";
	if(re.findall("^(37)", vcode)):
		return "Buy 3 For $0.25";
	if(re.findall("^(38)", vcode)):
		return "Buy 3 For $0.30";
	if(re.findall("^(39)", vcode)):
		return "\$0.39";
	if(re.findall("^(40)", vcode)):
		return "\$0.40";
	if(re.findall("^(41)", vcode)):
		return "Buy 3 For $0.50";
	if(re.findall("^(42)", vcode)):
		return "Buy 3 For $1.00";
	if(re.findall("^(43)", vcode)):
		return "Buy 2 For $1.10";
	if(re.findall("^(44)", vcode)):
		return "Buy 2 For $1.35";
	if(re.findall("^(45)", vcode)):
		return "\$0.45";
	if(re.findall("^(46)", vcode)):
		return "Buy 2 For $1.60";
	if(re.findall("^(47)", vcode)):
		return "Buy 2 For $1.75";
	if(re.findall("^(48)", vcode)):
		return "Buy 2 For $1.85";
	if(re.findall("^(49)", vcode)):
		return "\$0.49";
	if(re.findall("^(50)", vcode)):
		return "\$0.50";
	if(re.findall("^(51)", vcode)):
		return "Buy 2 For $2.00";
	if(re.findall("^(52)", vcode)):
		return "Buy 3 For $0.55";
	if(re.findall("^(53)", vcode)):
		return "Buy 2 For $0.10";
	if(re.findall("^(54)", vcode)):
		return "Buy 2 For $0.15";
	if(re.findall("^(55)", vcode)):
		return "\$0.55";
	if(re.findall("^(56)", vcode)):
		return "Buy 2 For $0.20";
	if(re.findall("^(57)", vcode)):
		return "Buy 2 For $0.25";
	if(re.findall("^(58)", vcode)):
		return "Buy 2 For $0.30";
	if(re.findall("^(59)", vcode)):
		return "\$0.59";
	if(re.findall("^(60)", vcode)):
		return "\$0.60";
	if(re.findall("^(61)", vcode)):
		return "\$10.00";
	if(re.findall("^(62)", vcode)):
		return "\$9.50";
	if(re.findall("^(63)", vcode)):
		return "\$9.00";
	if(re.findall("^(64)", vcode)):
		return "\$8.50";
	if(re.findall("^(65)", vcode)):
		return "\$0.65";
	if(re.findall("^(66)", vcode)):
		return "\$8.00";
	if(re.findall("^(67)", vcode)):
		return "\$7.50";
	if(re.findall("^(68)", vcode)):
		return "\$7.00";
	if(re.findall("^(69)", vcode)):
		return "\$0.69";
	if(re.findall("^(70)", vcode)):
		return "\$0.70";
	if(re.findall("^(71)", vcode)):
		return "\$6.50";
	if(re.findall("^(72)", vcode)):
		return "\$6.00";
	if(re.findall("^(73)", vcode)):
		return "\$5.50";
	if(re.findall("^(74)", vcode)):
		return "\$5.00";
	if(re.findall("^(75)", vcode)):
		return "\$0.75";
	if(re.findall("^(76)", vcode)):
		return "\$1.00";
	if(re.findall("^(77)", vcode)):
		return "\$1.25";
	if(re.findall("^(78)", vcode)):
		return "\$1.50";
	if(re.findall("^(79)", vcode)):
		return "\$0.79";
	if(re.findall("^(80)", vcode)):
		return "\$0.80";
	if(re.findall("^(81)", vcode)):
		return "\$1.75";
	if(re.findall("^(82)", vcode)):
		return "\$2.00";
	if(re.findall("^(83)", vcode)):
		return "\$2.25";
	if(re.findall("^(84)", vcode)):
		return "\$2.50";
	if(re.findall("^(85)", vcode)):
		return "\$0.85";
	if(re.findall("^(86)", vcode)):
		return "\$2.75";
	if(re.findall("^(87)", vcode)):
		return "\$3.00";
	if(re.findall("^(88)", vcode)):
		return "\$3.25";
	if(re.findall("^(89)", vcode)):
		return "\$0.89";
	if(re.findall("^(90)", vcode)):
		return "\$0.90";
	if(re.findall("^(91)", vcode)):
		return "\$3.50";
	if(re.findall("^(92)", vcode)):
		return "\$3.75";
	if(re.findall("^(93)", vcode)):
		return "\$4.00";
	if(re.findall("^(94)", vcode)):
		return "Reserved for future use";
	if(re.findall("^(95)", vcode)):
		return "\$0.95";
	if(re.findall("^(96)", vcode)):
		return "\$4.50";
	if(re.findall("^(97)", vcode)):
		return "Reserved for future use";
	if(re.findall("^(98)", vcode)):
		return "Buy 2 For $0.65";
	if(re.findall("^(99)", vcode)):
		return "\$0.99";
	return False;
