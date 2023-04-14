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

    $FileInfo: getprefix.py - Last Update: 4/14/2023 Ver. 2.9.4 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals;
import re, upcean.validate, upcean.convert;

def get_upca_barcode_info(upc, infotype=None):
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
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_upca_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_upca_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_upca_barcode_product(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("product", False);
def get_upca_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_upca_barcode_info_from_upce(upc):
 return get_upca_barcode_info(upcean.convert.convert_barcode_from_upce_to_upca(upc));
def get_upce_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(re.findall("^0(\d{13})", upc)):
  upc_matches = re.findall("^0(\d{13})", upc);
  upc = upc_matches[0];
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(len(upc)==12):
  upc = upcean.convert.convert_barcode_from_upca_to_upce(upc);
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
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_upce_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_upce_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_upce_barcode_product(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(not product):
  return False;
 return product.get("product", False);
def get_upce_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upce_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_ean8_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{8})", upc)):
  return False;
 upc_matches = re.findall("^(\d{2})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': None, 'numbersystem': pre_upc_type[0], 'manufacturer': None, 'product': pre_upc_type[1], 'checkdigit': pre_upc_type[2]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_ean8_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_ean8_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_ean8_barcode_product(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(not product):
  return False;
 return product.get("product", False);
def get_ean8_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_ean8_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_ean13_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(len(upc)==8):
  upc = upcean.convert.convert_barcode_from_upce_to_upca(upc);
 if(len(upc)==12):
  upc = "0"+upc;
 if(not re.findall("^(\d{13})", upc)):
  return False;
 upc_matches = re.findall("^(\d{2})(\d{5})(\d{5})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'packagecode': None, 'numbersystem': pre_upc_type[0], 'manufacturer': pre_upc_type[1], 'product': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_ean13_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_ean13_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_ean13_barcode_product(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(not product):
  return False;
 return product.get("product", False);
def get_ean13_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_ean13_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_itf14_barcode_info(upc, infotype=None):
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
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_itf14_barcode_packagecode(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(not product):
  return False;
 return product.get("packagecode", False);
def get_itf14_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_itf14_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_itf14_barcode_product(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(not product):
  return False;
 return product.get("product", False);
def get_itf14_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_itf14_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
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
def get_goodwill_upca_barcode_info(upc, infotype=None):
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
 gw_item_type = None;
 # 400310
 # 400321
 # 400322
 # 400323
 # 400324
 # 400325
 if(re.findall("^(4111)", upc)):
  gw_item_type = "Softlines";
 elif(re.findall("^(4666)", upc)):
  gw_item_type = "Hardlines";
 elif(re.findall("^(4555)", upc)):
  gw_item_type = "Shoes/Purses";
 elif(re.findall("^(4190)", upc)):
  gw_item_type = "Target";
 elif(re.findall("^(4230)", upc)):
  gw_item_type = "Jacobs";
 elif(re.findall("^(4333330)", upc)):
  gw_item_type = "Furniture";
 elif(re.findall("^(4120120)", upc)):
  gw_item_type = "Books";
 elif(re.findall("^(4002000)", upc)):
  gw_item_type = "Mystery Dozen Deal";
 elif(re.findall("^(4010000)", upc)):
  gw_item_type = "Bagged Hardlines";
 else:
  gw_item_type = None;
 gw_item_color = None;
 if(re.findall("^(4)(\d{3})(22)", upc)):
  gw_item_color = "Pink";
 elif(re.findall("^(4)(\d{3})(33)", upc)):
  gw_item_color = "Yellow";
 elif(re.findall("^(4)(\d{3})(44)", upc)):
  gw_item_color = "Green";
 elif(re.findall("^(4)(\d{3})(55)", upc)):
  gw_item_color = "Blue";
 elif(re.findall("^(4)(\d{3})(77)", upc)):
  gw_item_color = "Orange";
 else:
  gw_item_color = None;
 price_matches = re.findall("^(\d{3})(\d{2})", upc_matches[1]);
 price_matches = price_matches[0];
 if(price_matches[0]=="399" and gw_item_type=="Mystery Dozen Deal"):
  gw_item_type = "Mystery DVD Deal";
 elif(price_matches[0]=="699" and gw_item_type=="Mystery Dozen Deal"):
  gw_item_type = "Mystery 1/2 Dozen Deal";
 elif(price_matches[0]=="999" and gw_item_type=="Mystery Dozen Deal"):
  gw_item_type = "Mystery Dozen Deal";
 else:
  gw_item_type = gw_item_type;
 price_alt = str(price_matches[0].lstrip('0'))+price_matches[1];
 formated_price = price_matches[0]+"."+price_matches[1];
 formated_price_alt = str(price_matches[0].lstrip('0'))+"."+price_matches[1];
 product = {'numbersystem': str(4), 'code': upc_matches[0], 'price': upc_matches[1], 'pricendnz': price_alt, 'pricewdwz': formated_price, 'pricewdnz': formated_price_alt, 'type': gw_item_type, 'tagcolor': gw_item_color, 'checkdigit': upc_matches[2]};
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_goodwill_upca_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_goodwill_upca_barcode_code(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("code", False);
def get_goodwill_upca_barcode_price(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("price", False);
def get_goodwill_upca_barcode_type(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("type", False);
def get_goodwill_upca_barcode_tagcolor(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("tagcolor", False);
def get_goodwill_upca_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_goodwill_upca_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);

'''
// Get variable weight info from UPC-A
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
'''
def get_upca_vw_barcode_info(upc, infotype=None):
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
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_vw_barcode_info(upc, infotype=None):
 return get_upca_vw_barcode_info(upc, infotype);
def get_upca_vw_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_vw_barcode_numbersystem(upc):
 return get_upca_vw_barcode_numbersystem(upc);
def get_upca_vw_barcode_code(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("code", False);
def get_vw_barcode_code(upc):
 return get_upca_vw_barcode_code(upc);
def get_upca_vw_barcode_price(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("price", False);
def get_vw_barcode_price(upc):
 return get_upca_vw_barcode_price(upc);
def get_upca_vw_barcode_pricecs(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("pricecs", False);
def get_vw_barcode_pricecs(upc):
 return get_upca_vw_barcode_pricecs(upc);
def get_upca_vw_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_upca_vw_barcode_checksum(upc):
 return get_upca_vw_barcode_checkdigit(upc);
def get_vw_barcode_checkdigit(upc):
 return get_upca_vw_barcode_checkdigit(upc);
def get_vw_barcode_checksum(upc):
 return get_upca_vw_barcode_checkdigit(upc);

'''
// Get variable weight info from EAN-13
// Source: https://softmatic.com/barcode-ean-13.html#ean-country
'''
def get_ean13_vw_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(re.findall("^0(\d{13})", upc)):
  upc_matches = re.findall("^0(\d{13})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{13})", upc)):
  return False;
 if(not re.findall("^2(\d{12})", upc)):
  return False;
 upc_matches = re.findall("^2(\d{1})(\d{5})(\d{5})(\d{1})", upc);
 upc_matches = upc_matches[0];
 product = {'numbersystem': str(2), 'subnumbersystem': upc_matches[0], 'code': upc_matches[1], 'price': upc_matches[2], 'checkdigit': upc_matches[3]};
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_ean13_vw_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_ean13_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_ean13_vw_barcode_subnumbersystem(upc):
 upc = str(upc);
 product = get_ean13_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("subnumbersystem", False);
def get_ean13_vw_barcode_code(upc):
 upc = str(upc);
 product = get_ean13_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("code", False);
def get_ean13_vw_barcode_price(upc):
 upc = str(upc);
 product = get_ean13_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("price", False);
def get_ean13_vw_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_ean13_vw_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_ean13_vw_barcode_checksum(upc):
 return get_ean13_vw_barcode_checkdigit(upc);

'''
// Get coupon info
// Source: http://divagirlusa-ivil.tripod.com/austinitecouponers/id29.html
'''
def get_upca_coupon_barcode_info(upc, infotype=None):
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
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_upca_coupon_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_upca_coupon_barcode_manufacturer(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(not product):
  return False;
 return product.get("manufacturer", False);
def get_upca_coupon_barcode_family(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(not product):
  return False;
 return product.get("family", False);
def get_upca_coupon_barcode_value(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(not product):
  return False;
 return product.get("value", False);
def get_upca_coupon_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_coupon_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
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
def get_ups_barcode_info(upc, infotype=None):
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
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_ups_barcode_accountnumber(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(not product):
  return False;
 return product.get("accountnumber", False);
def get_ups_barcode_servicetype(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(not product):
  return False;
 return product.get("servicetype", False);
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
 if(not product):
  return False;
 return product.get("invoicenumber", False);
def get_ups_barcode_packagenumber(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(not product):
  return False;
 return product.get("packagenumber", False);
def get_ups_barcode_checkdigit(upc):
 upc = str(upc).upper();
 product = get_ups_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);

'''
// Get IMEI (International Mobile Station Equipment Identity) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_new_imei_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{8})(\d{6})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'serialnumber': pre_upc_type[1], 'checkdigit': pre_upc_type[2]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_new_imei_barcode_tac(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("tac", False);
def get_new_imei_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("serialnumber", False);
def get_new_imei_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_new_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);
def get_old_imei_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{6})(\d{2})(\d{6})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'fac': pre_upc_type[1], 'serialnumber': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_old_imei_barcode_tac(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("tac", False);
def get_old_imei_barcode_fac(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("fac", False);
def get_old_imei_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("serialnumber", False);
def get_old_imei_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_old_imei_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);

'''
// Get IMEISV (International Mobile Station Equipment Identity Software Version) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_new_imeisv_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{8})(\d{6})(\d{2})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'serialnumber': pre_upc_type[1], 'svn': pre_upc_type[2]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_new_imeisv_barcode_tac(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("tac", False);
def get_new_imeisv_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("serialnumber", False);
def get_new_imeisv_barcode_svn(upc):
 upc = str(upc);
 product = get_new_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("svn", False);
def get_old_imeisv_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{6})(\d{2})(\d{6})(\d{2})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'tac': pre_upc_type[0], 'fac': pre_upc_type[1], 'serialnumber': pre_upc_type[2], 'svn': pre_upc_type[3]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_old_imeisv_barcode_tac(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("tac", False);
def get_old_imeisv_barcode_fac(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("fac", False);
def get_old_imeisv_barcode_serialnumber(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("serialnumber", False);
def get_old_imeisv_barcode_svn(upc):
 upc = str(upc);
 product = get_old_imeisv_barcode_info(upc);
 if(not product):
  return False;
 return product.get("svn", False);

'''
// Get Bank Card Number Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''
def get_bcn_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{16})", upc)):
  return False;
 upc_matches = re.findall("^(\d{1})(\d{5})(\d{12})(\d{1})", upc);
 pre_upc_type = upc_matches[0];
 upc_type = {'mii': pre_upc_type[0], 'iin': pre_upc_type[0]+pre_upc_type[1], 'account': pre_upc_type[2], 'checkdigit': pre_upc_type[3]};
 if(infotype is None):
  return upc_type;
 if(infotype is not None):
  return upc_type.get(infotype, upc_type);
def get_bcn_mii(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(not product):
  return False;
 return product.get("mii", False);
def get_bcn_iin(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(not product):
  return False;
 return product.get("iin", False);
def get_bcn_account(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(not product):
  return False;
 return product.get("account", False);
def get_bcn_checkdigit(upc):
 upc = str(upc);
 product = get_bcn_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);

'''
// Get National Drug Codes UPC-A info
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''
def get_upca_ndc_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(re.findall("^0(\d{12})", upc)):
  upc_matches = re.findall("^0(\d{12})", upc);
  upc = upc_matches[0];
 if(not re.findall("^(\d{12})", upc)):
  return False;
 if(not re.findall("^3(\d{11})", upc)):
  return False;
 upc_matches = re.findall("^3(\d{4})(\d{4})(\d{2})(\d{1})", upc);
 upc_matches = upc_matches[0];
 product = {'numbersystem': str(3), 'labeler': upc_matches[0], 'productcode': upc_matches[1], 'packagecode': upc_matches[2], 'checkdigit': upc_matches[3]};
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_upca_ndc_barcode_numbersystem(upc):
 upc = str(upc);
 product = get_upca_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("numbersystem", False);
def get_upca_ndc_barcode_labeler(upc):
 upc = str(upc);
 product = get_upca_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("labeler", False);
def get_upca_ndc_barcode_productcode(upc):
 upc = str(upc);
 product = get_upca_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("productcode", False);
def get_upca_ndc_barcode_packagecode(upc):
 upc = str(upc);
 product = get_upca_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("packagecode", False);
def get_upca_ndc_barcode_checkdigit(upc):
 upc = str(upc);
 product = get_upca_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("checkdigit", False);

'''
// Get National Drug Codes info
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''
def get_ndc_barcode_info(upc, infotype=None):
 upc = str(upc);
 if(not re.findall("^(\d{10})", upc)):
  return False;
 if(not re.findall("^(\d{10})", upc)):
  return False;
 upc_matches = re.findall("(\d{4})(\d{4})(\d{2})", upc);
 upc_matches = upc_matches[0];
 product = {'labeler': upc_matches[0], 'productcode': upc_matches[1], 'packagecode': upc_matches[2]};
 if(infotype is None):
  return product;
 if(infotype is not None):
  return product.get(infotype, product);
def get_ndc_barcode_labeler(upc):
 upc = str(upc);
 product = get_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("labeler", False);
def get_ndc_barcode_productcode(upc):
 upc = str(upc);
 product = get_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("productcode", False);
def get_ndc_barcode_packagecode(upc):
 upc = str(upc);
 product = get_ndc_barcode_info(upc);
 if(not product):
  return False;
 return product.get("packagecode", False);
