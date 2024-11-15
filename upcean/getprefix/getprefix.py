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

    $FileInfo: getprefix.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import upcean.validate
import upcean.convert


def get_upca_barcode_info(upc, infotype=None):
    # Convert to UPC-A if input is UPC-E
    upc = upcean.convert.convert_barcode_from_upce_to_upca(str(upc)) if len(upc) == 8 else str(upc)
    
    # Remove leading zeroes from 13-digit EAN if present
    upc = re.sub("^0(\\d{12})", "\\1", upc)
    
    # Verify format and extract components
    match = re.match("^(\\d)(\\d{5})(\\d{5})(\\d)$", upc)
    if not match:
        return False
    
    # Map components to dictionary
    upc_type = {
        'packagecode': None,
        'numbersystem': match.group(1),
        'manufacturer': match.group(2),
        'product': match.group(3),
        'checkdigit': match.group(4)
    }
    
    # Return specific infotype if provided
    return upc_type.get(infotype, upc_type)

def get_upca_barcode_numbersystem(upc):
    # Retrieve and return the numbersystem
    return get_upca_barcode_info(upc).get("numbersystem", False)

def get_upca_barcode_manufacturer(upc):
    # Retrieve and return the manufacturer
    return get_upca_barcode_info(upc).get("manufacturer", False)

def get_upca_barcode_product(upc):
    # Retrieve and return the product
    return get_upca_barcode_info(upc).get("product", False)

def get_upca_barcode_checkdigit(upc):
    # Retrieve and return the checkdigit
    return get_upca_barcode_info(upc).get("checkdigit", False)

def get_upca_barcode_info_from_upce(upc):
    # Retrieve UPC-A information for a UPC-E input
    return get_upca_barcode_info(upcean.convert.convert_barcode_from_upce_to_upca(upc))


def get_upce_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Remove leading zero for 13-digit EAN if present
    upc = re.sub(r"^0(\d{12})", "\\1", upc)
    
    # Convert UPC-A to UPC-E if 12 digits long
    upc = upcean.convert.convert_barcode_from_upca_to_upce(upc) if len(upc) == 12 else upc
    
    # Validate UPC-E format
    if not re.match(r"^\d{8}$", upc):
        return False

    # Define regex patterns for matching each format in UPC-E
    patterns = [
        "(0|1)(\\d{2})(\\d{3})([0-2])(\\d)",
        "(0|1)(\\d{3})(\\d{2})(3)(\\d)",
        "(0|1)(\\d{4})(\\d)(4)(\\d)",
        "(0|1)(\\d{5})([5-9])(\\d)"
    ]

    # Initialize barcode info variables
    get_ns, get_manufac, get_product, get_checksum = None, None, None, None

    # Match patterns to extract numbersystem, manufacturer, product, and checksum
    for pattern in patterns:
        match = re.match(pattern, upc)
        if match:
            get_ns = match.group(1)
            get_manufac = match.group(2)
            get_product = match.group(3) + (match.group(4) if match.group(4).isdigit() else "")
            get_checksum = match.group(5)
            break

    # Construct UPC-E information dictionary
    upc_type = {
        'packagecode': None,
        'numbersystem': get_ns,
        'manufacturer': get_manufac,
        'product': get_product,
        'checkdigit': get_checksum
    }

    # Return the requested infotype or the full dictionary if infotype is None
    return upc_type.get(infotype, upc_type)

def get_upce_barcode_numbersystem(upc):
    # Retrieve and return the numbersystem
    return get_upce_barcode_info(upc).get("numbersystem", False)

def get_upce_barcode_manufacturer(upc):
    # Retrieve and return the manufacturer
    return get_upce_barcode_info(upc).get("manufacturer", False)

def get_upce_barcode_product(upc):
    # Retrieve and return the product
    return get_upce_barcode_info(upc).get("product", False)

def get_upce_barcode_checkdigit(upc):
    # Retrieve and return the checkdigit
    return get_upce_barcode_info(upc).get("checkdigit", False)


def get_ean8_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Validate EAN-8 format
    match = re.match("^(\\d{2})(\\d{5})(\\d)$", upc)
    if not match:
        return False

    # Extract EAN-8 components
    upc_type = {
        'packagecode': None,
        'numbersystem': match.group(1),
        'manufacturer': None,
        'product': match.group(2),
        'checkdigit': match.group(3)
    }

    # Return specific infotype if provided, otherwise full dictionary
    return upc_type.get(infotype, upc_type)

def get_ean8_barcode_numbersystem(upc):
    # Retrieve and return the numbersystem
    return get_ean8_barcode_info(upc).get("numbersystem", False)

def get_ean8_barcode_manufacturer(upc):
    # Retrieve and return the manufacturer
    return get_ean8_barcode_info(upc).get("manufacturer", False)

def get_ean8_barcode_product(upc):
    # Retrieve and return the product
    return get_ean8_barcode_info(upc).get("product", False)

def get_ean8_barcode_checkdigit(upc):
    # Retrieve and return the checkdigit
    return get_ean8_barcode_info(upc).get("checkdigit", False)


def get_ean13_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Convert UPC-E or UPC-A to EAN-13 format if necessary
    if len(upc) == 8:
        upc = upcean.convert.convert_barcode_from_upce_to_upca(upc)
    if len(upc) == 12:
        upc = "0" + upc
    
    # Validate EAN-13 format and extract components
    match = re.match("^(\\d{2})(\\d{5})(\\d{5})(\\d)$", upc)
    if not match:
        return False

    # Map extracted components to dictionary
    upc_type = {
        'packagecode': None,
        'numbersystem': match.group(1),
        'manufacturer': match.group(2),
        'product': match.group(3),
        'checkdigit': match.group(4)
    }
    
    # Return the requested infotype if provided, otherwise the full dictionary
    return upc_type.get(infotype, upc_type)

def get_ean13_barcode_numbersystem(upc):
    # Retrieve and return the numbersystem
    return get_ean13_barcode_info(upc).get("numbersystem", False)

def get_ean13_barcode_manufacturer(upc):
    # Retrieve and return the manufacturer
    return get_ean13_barcode_info(upc).get("manufacturer", False)

def get_ean13_barcode_product(upc):
    # Retrieve and return the product
    return get_ean13_barcode_info(upc).get("product", False)

def get_ean13_barcode_checkdigit(upc):
    # Retrieve and return the checkdigit
    return get_ean13_barcode_info(upc).get("checkdigit", False)


def get_itf14_barcode_info(upc, infotype=None):
    upc = str(upc)

    # Pad ITF-14 to ensure it is 14 digits if provided in shorter forms
    if len(upc) == 12:
        upc = "00" + upc
    elif len(upc) == 13:
        upc = "0" + upc

    # Validate ITF-14 format and extract components
    match = re.match("^(\\d)(\\d{2})(\\d{5})(\\d{5})(\\d)$", upc)
    if not match:
        return False

    # Map extracted components to dictionary
    upc_type = {
        'packagecode': match.group(1),
        'numbersystem': match.group(2),
        'manufacturer': match.group(3),
        'product': match.group(4),
        'checkdigit': match.group(5)
    }

    # Return the requested infotype if provided, otherwise the full dictionary
    return upc_type.get(infotype, upc_type)

def get_itf14_barcode_packagecode(upc):
    # Retrieve and return the packagecode
    return get_itf14_barcode_info(upc).get("packagecode", False)

def get_itf14_barcode_numbersystem(upc):
    # Retrieve and return the numbersystem
    return get_itf14_barcode_info(upc).get("numbersystem", False)

def get_itf14_barcode_manufacturer(upc):
    # Retrieve and return the manufacturer
    return get_itf14_barcode_info(upc).get("manufacturer", False)

def get_itf14_barcode_product(upc):
    # Retrieve and return the product
    return get_itf14_barcode_info(upc).get("product", False)

def get_itf14_barcode_checkdigit(upc):
    # Retrieve and return the checkdigit
    return get_itf14_barcode_info(upc).get("checkdigit", False)


'''
// Get Number System Prefix for UPC-A barcodes
// Source: http://www.morovia.com/education/symbology/upc-a.asp
// Source: http://www.computalabel.com/aboutupc.htm
'''


def get_upca_barcode_ns(upc):
    upc = str(upc)
    
    # Remove leading zero if upc is in 13-digit EAN format
    match = re.match("^0(\\d{12})$", upc)
    if match:
        upc = match.group(1)
    
    # Validate format as 12-digit UPC-A
    if not re.match("^\\d{12}$", upc):
        return False

    # Determine the barcode type based on the first digit (number system)
    ns_types = {
        '0': "Regular UPC",
        '1': "Regular UPC",
        '2': "Variable Weight Items",
        '3': "DrugHealth Items",
        '4': "In-store use",
        '5': "Coupons",
        '6': "Regular UPC",
        '7': "Regular UPC",
        '8': "Regular UPC",
        '9': "Coupons"
    }
    
    return ns_types.get(upc[0], False)


'''
// Get ITF-14 Packaging Indicator
// Source: http://www.mecsw.com/specs/itf_14.html
// Source: http://www.qed.org/RBTL/chapters/ch3.3.htm
'''


def get_itf14_barcode_type(upc):
    upc = str(upc)
    
    # Validate that the input is a 14-digit ITF-14 barcode
    if not re.match("^\\d{14}$", upc):
        return False

    # Determine ITF-14 type based on the first digit
    itf14_types = {
        '0': "UPC code of contents differs from case code",
        '1': "More than each and below inner packs",
        '2': "More than each and below inner packs",
        '3': "Inner packs",
        '4': "Inner packs",
        '5': "Shipping containers (cartons)",
        '6': "Shipping containers (cartons)",
        '7': "Pallet",
        '8': "Reserved",
        '9': "Variable quantity content"
    }
    
    return itf14_types.get(upc[0], False)


'''
// Get Goodwill UPC Info.
'''


def get_goodwill_upca_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Remove leading zero if upc is in 13-digit EAN format
    match = re.match("^0(\\d{12})$", upc)
    if match:
        upc = match.group(1)
    
    # Validate that it's a 12-digit UPC-A barcode starting with '4'
    if not re.match("^4\\d{11}$", upc):
        return False
    
    # Parse main components
    main_match = re.match("^4(\\d{5})(\\d{5})(\\d)$", upc)
    if not main_match:
        return False
    code, price, checkdigit = main_match.groups()
    
    # Determine item type
    type_patterns = {
        "4111": "Softlines",
        "4666": "Hardlines",
        "4555": "Shoes/Purses",
        "4190": "Target",
        "4230": "Jacobs",
        "4333330": "Furniture",
        "4120120": "Books",
        "412": "Books",
        "413": "Media",
        "4002000": "Mystery Dozen Deal",
        "4010000": "Bagged Hardlines"
    }
    gw_item_type = None
    for k, v in type_patterns.items():
        if re.match(r"^" + k, upc):
            gw_item_type = v
            break
    
    # Determine item color based on last two digits of the price
    color_patterns = {
        "22": "Pink",
        "33": "Yellow",
        "44": "Green",
        "55": "Blue",
        "77": "Orange"
    }
    gw_item_color = color_patterns.get(price[-2:], None)

    # Further refine item type based on price ranges
    price_adjustments = {
        ("399", "Mystery Dozen Deal"): "Mystery DVD Deal",
        ("699", "Mystery Dozen Deal"): "Mystery 1/2 Dozen Deal",
        ("999", "Mystery Dozen Deal"): "Mystery Dozen Deal",
        ("199", "Books"): "Softcover / Kids Books",
        ("299", "Books"): "Hard Cover Books",
        ("199", "Media"): "Albums / CDs / VHD",
        ("299", "Media"): "DVD / Disney VHS",
        ("399", "Media"): "Blu-Ray / New VHS",
        ("499", "Media"): "Season DVD"
    }
    gw_item_type = price_adjustments.get((price[:3], gw_item_type), gw_item_type)
    
    # Format prices
    price_alt = str(int(price[:3])) + price[3:]
    formatted_price = "{}.{}".format(price[:3], price[3:])
    formatted_price_alt = "{}.{}".format(int(price[:3]), price[3:])

    # Compile product details into a dictionary
    product = {
        'numbersystem': "4",
        'code': code,
        'price': price,
        'pricendnz': price_alt,
        'pricewdwz': formatted_price,
        'pricewdnz': formatted_price_alt,
        'type': gw_item_type,
        'tagcolor': gw_item_color,
        'checkdigit': checkdigit
    }
    
    # Return the requested info type if specified, otherwise full dictionary
    return product.get(infotype, product)

def get_goodwill_upca_barcode_numbersystem(upc):
    return get_goodwill_upca_barcode_info(upc, "numbersystem")

def get_goodwill_upca_barcode_code(upc):
    return get_goodwill_upca_barcode_info(upc, "code")

def get_goodwill_upca_barcode_price(upc):
    return get_goodwill_upca_barcode_info(upc, "price")

def get_goodwill_upca_barcode_type(upc):
    return get_goodwill_upca_barcode_info(upc, "type")

def get_goodwill_upca_barcode_tagcolor(upc):
    return get_goodwill_upca_barcode_info(upc, "tagcolor")

def get_goodwill_upca_barcode_checkdigit(upc):
    return get_goodwill_upca_barcode_info(upc, "checkdigit")


'''
// Get variable weight info from UPC-A
// Source: http://wiki.answers.com/Q/How_does_a_price_embedded_bar_code_work
// Source: http://en.wikipedia.org/wiki/Universal_Product_Code#Prefixes
'''


def get_upca_vw_barcode_info(upc, infotype=None):
    upc = str(upc)

    # Remove leading zero if upc is in 13-digit EAN format
    match = re.match("^0(\\d{12})$", upc)
    if match:
        upc = match.group(1)

    # Ensure it is a valid 12-digit UPC-A starting with '2'
    if not re.match("^2\\d{11}$", upc):
        return False

    # Parse main components
    match = re.match("^2(\\d{5})(\\d)(\\d{4})(\\d)$", upc)
    if not match:
        return False

    code, pricecs, price, checkdigit = match.groups()
    product = {
        'numbersystem': "2",
        'code': code,
        'pricecs': pricecs,
        'price': price,
        'checkdigit': checkdigit
    }

    # Return the requested info type if specified, otherwise full dictionary
    return product.get(infotype, product)

def get_vw_barcode_info(upc, infotype=None):
    return get_upca_vw_barcode_info(upc, infotype)

def get_upca_vw_barcode_numbersystem(upc):
    product = get_upca_vw_barcode_info(upc)
    return product.get("numbersystem", False) if product else False

def get_vw_barcode_numbersystem(upc):
    return get_upca_vw_barcode_numbersystem(upc)

def get_upca_vw_barcode_code(upc):
    product = get_upca_vw_barcode_info(upc)
    return product.get("code", False) if product else False

def get_vw_barcode_code(upc):
    return get_upca_vw_barcode_code(upc)

def get_upca_vw_barcode_price(upc):
    product = get_upca_vw_barcode_info(upc)
    return product.get("price", False) if product else False

def get_vw_barcode_price(upc):
    return get_upca_vw_barcode_price(upc)

def get_upca_vw_barcode_pricecs(upc):
    product = get_upca_vw_barcode_info(upc)
    return product.get("pricecs", False) if product else False

def get_vw_barcode_pricecs(upc):
    return get_upca_vw_barcode_pricecs(upc)

def get_upca_vw_barcode_checkdigit(upc):
    product = get_upca_vw_barcode_info(upc)
    return product.get("checkdigit", False) if product else False

def get_upca_vw_barcode_checksum(upc):
    return get_upca_vw_barcode_checkdigit(upc)

def get_vw_barcode_checkdigit(upc):
    return get_upca_vw_barcode_checkdigit(upc)

def get_vw_barcode_checksum(upc):
    return get_upca_vw_barcode_checkdigit(upc)


'''
// Get variable weight info from EAN-13
// Source: https://softmatic.com/barcode-ean-13.html#ean-country
'''

def get_ean13_vw_barcode_info(ean, infotype=None):
    ean = str(ean)
    
    # Ensure EAN-13 format and prefix
    if not re.match("^(02|20|2[1-9])\\d{11}$", ean):
        return False

    # Parse main components
    match = re.match("^(02|20|2[1-9])(\\d{5})(\\d{4})(\\d)$", ean)
    if not match:
        return False

    gs1_prefix, item_code, price, checkdigit = match.groups()
    product_info = {
        'gs1_prefix': gs1_prefix,
        'item_code': item_code,
        'price': price,
        'checkdigit': checkdigit
    }

    # Return specific information if infotype is provided
    return product_info.get(infotype, product_info)

def get_ean13_vw_barcode_gs1_prefix(ean):
    product = get_ean13_vw_barcode_info(ean)
    return product.get("gs1_prefix", False) if product else False

def get_ean13_vw_barcode_item_code(ean):
    product = get_ean13_vw_barcode_info(ean)
    return product.get("item_code", False) if product else False

def get_ean13_vw_barcode_price(ean):
    product = get_ean13_vw_barcode_info(ean)
    return product.get("price", False) if product else False

def get_ean13_vw_barcode_checkdigit(ean):
    product = get_ean13_vw_barcode_info(ean)
    return product.get("checkdigit", False) if product else False

def get_ean13_vw_barcode_checksum(ean):
    return get_ean13_vw_barcode_checkdigit(ean)

def get_ean13_vw_from_ean13_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Ensure EAN-13 format and prefix
    if not re.match("^2\\d{12}$", upc):
        return False

    # Parse main components
    match = re.match("^2(\\d)(\\d{5})(\\d{5})(\\d)$", upc)
    if not match:
        return False

    numbersystem, subnumbersystem, code, price, checkdigit = match.groups()
    product_info = {
        'numbersystem': numbersystem,
        'subnumbersystem': subnumbersystem,
        'code': code,
        'price': price,
        'checkdigit': checkdigit
    }

    # Return specific information if infotype is provided
    return product_info.get(infotype, product_info)

def get_ean13_vw_from_ean13_barcode_numbersystem(upc):
    product = get_ean13_vw_from_ean13_barcode_info(upc)
    return product.get("numbersystem", False) if product else False

def get_ean13_vw_from_ean13_barcode_subnumbersystem(upc):
    product = get_ean13_vw_from_ean13_barcode_info(upc)
    return product.get("subnumbersystem", False) if product else False

def get_ean13_vw_from_ean13_barcode_code(upc):
    product = get_ean13_vw_from_ean13_barcode_info(upc)
    return product.get("code", False) if product else False

def get_ean13_vw_from_ean13_barcode_price(upc):
    product = get_ean13_vw_from_ean13_barcode_info(upc)
    return product.get("price", False) if product else False

def get_ean13_vw_from_ean13_barcode_checkdigit(upc):
    product = get_ean13_vw_from_ean13_barcode_info(upc)
    return product.get("checkdigit", False) if product else False

def get_ean13_vw_from_ean13_barcode_checksum(upc):
    return get_ean13_vw_from_ean13_barcode_checkdigit(upc)


'''
// Get coupon info
// Source: http://divagirlusa-ivil.tripod.com/austinitecouponers/id29.html
'''


def get_upca_coupon_barcode_info(upc, infotype=None):
    upc = str(upc)
    
    # Ensure UPC-A format and prefix validity
    if not re.match("^(5|9)\\d{11}$", upc):
        return False

    # Parse the components
    match = re.match("^(5|9)(\\d{5})(\\d{3})(\\d{2})(\\d)$", upc)
    if not match:
        return False

    numbersystem, manufacturer, family, value, checkdigit = match.groups()
    product_info = {
        'numbersystem': numbersystem,
        'manufacturer': manufacturer,
        'family': family,
        'value': value,
        'checkdigit': checkdigit
    }

    # Return specific information if infotype is provided
    return product_info.get(infotype, product_info)


def get_upca_coupon_barcode_numbersystem(upc):
    product = get_upca_coupon_barcode_info(upc)
    return product.get("numbersystem", False) if product else False


def get_upca_coupon_barcode_manufacturer(upc):
    product = get_upca_coupon_barcode_info(upc)
    return product.get("manufacturer", False) if product else False


def get_upca_coupon_barcode_family(upc):
    product = get_upca_coupon_barcode_info(upc)
    return product.get("family", False) if product else False


def get_upca_coupon_barcode_value(upc):
    product = get_upca_coupon_barcode_info(upc)
    return product.get("value", False) if product else False


def get_upca_coupon_barcode_checkdigit(upc):
    product = get_upca_coupon_barcode_info(upc)
    return product.get("checkdigit", False) if product else False


def get_upca_coupon_barcode_value_code(vcode):
    # Define a dictionary for value codes
    value_codes = {
        "00": "Manual Input Required", "01": "Free Item", "02": "Buy 4 Get 1 Free",
        "03": "$1.10", "04": "$1.35", "05": "$1.40", "06": "$1.60",
        "07": "Buy 3 For $1.50", "08": "Buy 2 For $3.00", "09": "Buy 3 For $2.00",
        "10": "$0.10", "11": "$1.85", "12": "$0.12", "13": "Buy 4 For $1.00",
        "14": "Buy 1 Get 1 Free", "15": "$0.15", "16": "Buy 2 Get 1 Free",
        "17": "Reserved for future use", "18": "$2.60", "19": "Buy 3 Get 1 Free",
        "20": "$0.20", "21": "Buy 2 For $0.35", "22": "Buy 2 For $0.40",
        "23": "Buy 2 For $0.45", "24": "Buy 2 For $0.50", "25": "$0.25",
        "26": "$2.85", "27": "Reserved for future use", "28": "Buy 2 For $0.55",
        "29": "$0.29", "30": "$0.30", "31": "Buy 2 For $0.60", "32": "Buy 2 For $0.75",
        "33": "Buy 2 For $1.00", "34": "Buy 2 For $1.25", "35": "$0.35",
        "36": "Buy 2 For $1.50", "37": "Buy 3 For $0.25", "38": "Buy 3 For $0.30",
        "39": "$0.39", "40": "$0.40", "41": "Buy 3 For $0.50", "42": "Buy 3 For $1.00",
        "43": "Buy 2 For $1.10", "44": "Buy 2 For $1.35", "45": "$0.45",
        "46": "Buy 2 For $1.60", "47": "Buy 2 For $1.75", "48": "Buy 2 For $1.85",
        "49": "$0.49", "50": "$0.50", "51": "Buy 2 For $2.00", "52": "Buy 3 For $0.55",
        "53": "Buy 2 For $0.10", "54": "Buy 2 For $0.15", "55": "$0.55",
        "56": "Buy 2 For $0.20", "57": "Buy 2 For $0.25", "58": "Buy 2 For $0.30",
        "59": "$0.59", "60": "$0.60", "61": "$10.00", "62": "$9.50",
        "63": "$9.00", "64": "$8.50", "65": "$0.65", "66": "$8.00",
        "67": "$7.50", "68": "$7.00", "69": "$0.69", "70": "$0.70",
        "71": "$6.50", "72": "$6.00", "73": "$5.50", "74": "$5.00",
        "75": "$0.75", "76": "$1.00", "77": "$1.25", "78": "$1.50",
        "79": "$0.79", "80": "$0.80", "81": "$1.75", "82": "$2.00",
        "83": "$2.25", "84": "$2.50", "85": "$0.85", "86": "$2.75",
        "87": "$3.00", "88": "$3.25", "89": "$0.89", "90": "$0.90",
        "91": "$3.50", "92": "$3.75", "93": "$4.00", "94": "Reserved for future use",
        "95": "$0.95", "96": "$4.50", "97": "Reserved for future use",
        "98": "Buy 2 For $0.65", "99": "$0.99"
    }
    return value_codes.get(vcode, False)


'''
// Get Major Industry Identifier for Bank Card Number
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''


def get_bcn_mii_prefix(upc):
    # Clean input and validate format
    upc = str(upc).replace("-", "").replace(" ", "")
    if not re.match("^\\d{16}$", upc):
        return False

    # Define MII prefix categories
    mii_prefix_map = {
        "0": "ISO/TC 68",
        "1": "Airlines",
        "2": "Airlines",
        "3": "Travel and Entertainment and Banking/Financial",
        "4": "Banking and Financial",
        "5": "Banking and Financial",
        "6": "Merchandising and Banking/Financial",
        "7": "Petroleum",
        "8": "Healthcare and Telecommunications",
        "9": "National Assignment"
    }

    # Extract the first digit and return the corresponding category
    mii_prefix = upc[0]
    return mii_prefix_map.get(mii_prefix, False)


'''
// Get UPS Checkdigit and Info by stebo0728 and HolidayBows
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit
// Source: http://www.codeproject.com/Articles/21224/Calculating-the-UPS-Tracking-Number-Check-Digit?msg=2961884#xx2961884xx
'''


def get_ups_barcode_info(upc, infotype=None):
    # Convert input to uppercase and validate it starts with '1Z'
    upc = str(upc).upper()
    if not upc.startswith("1Z"):
        return False
    
    # Remove '1Z' prefix and restrict length to 16 alphanumeric characters
    upc = re.sub("^1Z", "", upc)
    upc = upc[:16]

    # Extract components of the barcode using regex pattern matching
    upc_matches = re.match("^(\\w{6})(\\w{2})(\\w{5})(\\w{2})(\\w{1})$", upc)
    if not upc_matches:
        return False
    
    # Map extracted values to a dictionary
    upc_type = {
        'accountnumber': upc_matches.group(1),
        'servicetype': upc_matches.group(2),
        'invoicenumber': upc_matches.group(3),
        'packagenumber': upc_matches.group(4),
        'checkdigit': upc_matches.group(5)
    }
    
    # Return the full dictionary or the specific info type requested
    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_ups_barcode_accountnumber(upc):
    product = get_ups_barcode_info(upc)
    return product.get("accountnumber", False) if product else False

def get_ups_barcode_servicetype(upc):
    product = get_ups_barcode_info(upc)
    return product.get("servicetype", False) if product else False

def get_ups_barcode_servicetype_info(upc):
    servicetype = get_ups_barcode_servicetype(upc)
    if servicetype == "01":
        return "Next Day Air Shipment"
    elif servicetype == "02":
        return "Second Day Air Shipment"
    elif servicetype == "03":
        return "Ground Shipment"
    return False

def get_ups_barcode_invoicenumber(upc):
    product = get_ups_barcode_info(upc)
    return product.get("invoicenumber", False) if product else False

def get_ups_barcode_packagenumber(upc):
    product = get_ups_barcode_info(upc)
    return product.get("packagenumber", False) if product else False

def get_ups_barcode_checkdigit(upc):
    product = get_ups_barcode_info(upc)
    return product.get("checkdigit", False) if product else False



'''
// Get IMEI (International Mobile Station Equipment Identity) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''


def get_new_imei_barcode_info(upc, infotype=None):
    upc = str(upc)
    if not re.match("^\\d{16}$", upc):
        return False

    upc_matches = re.match("^(\\d{8})(\\d{6})(\\d{1})$", upc)
    if not upc_matches:
        return False

    upc_type = {
        'tac': upc_matches.group(1),
        'serialnumber': upc_matches.group(2),
        'checkdigit': upc_matches.group(3)
    }

    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_new_imei_barcode_tac(upc):
    product = get_new_imei_barcode_info(upc)
    return product.get("tac", False) if product else False

def get_new_imei_barcode_serialnumber(upc):
    product = get_new_imei_barcode_info(upc)
    return product.get("serialnumber", False) if product else False

def get_new_imei_barcode_checkdigit(upc):
    product = get_new_imei_barcode_info(upc)
    return product.get("checkdigit", False) if product else False


def get_old_imei_barcode_info(upc, infotype=None):
    upc = str(upc)
    if not re.match("^\\d{16}$", upc):
        return False

    upc_matches = re.match("^(\\d{6})(\\d{2})(\\d{6})(\\d{1})$", upc)
    if not upc_matches:
        return False

    upc_type = {
        'tac': upc_matches.group(1),
        'fac': upc_matches.group(2),
        'serialnumber': upc_matches.group(3),
        'checkdigit': upc_matches.group(4)
    }

    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_old_imei_barcode_tac(upc):
    product = get_old_imei_barcode_info(upc)
    return product.get("tac", False) if product else False

def get_old_imei_barcode_fac(upc):
    product = get_old_imei_barcode_info(upc)
    return product.get("fac", False) if product else False

def get_old_imei_barcode_serialnumber(upc):
    product = get_old_imei_barcode_info(upc)
    return product.get("serialnumber", False) if product else False

def get_old_imei_barcode_checkdigit(upc):
    product = get_old_imei_barcode_info(upc)
    return product.get("checkdigit", False) if product else False


'''
// Get IMEISV (International Mobile Station Equipment Identity Software Version) Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''


def get_new_imeisv_barcode_info(upc, infotype=None):
    upc = str(upc)
    if not re.match("^\\d{16}$", upc):
        return False

    upc_matches = re.match("^(\\d{8})(\\d{6})(\\d{2})$", upc)
    if not upc_matches:
        return False

    upc_type = {
        'tac': upc_matches.group(1),
        'serialnumber': upc_matches.group(2),
        'svn': upc_matches.group(3)
    }

    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_new_imeisv_barcode_tac(upc):
    product = get_new_imeisv_barcode_info(upc)
    return product.get("tac", False) if product else False

def get_new_imeisv_barcode_serialnumber(upc):
    product = get_new_imeisv_barcode_info(upc)
    return product.get("serialnumber", False) if product else False

def get_new_imeisv_barcode_svn(upc):
    product = get_new_imeisv_barcode_info(upc)
    return product.get("svn", False) if product else False


def get_old_imeisv_barcode_info(upc, infotype=None):
    upc = str(upc)
    if not re.match("^\\d{16}$", upc):
        return False

    upc_matches = re.match("^(\\d{6})(\\d{2})(\\d{6})(\\d{2})$", upc)
    if not upc_matches:
        return False

    upc_type = {
        'tac': upc_matches.group(1),
        'fac': upc_matches.group(2),
        'serialnumber': upc_matches.group(3),
        'svn': upc_matches.group(4)
    }

    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_old_imeisv_barcode_tac(upc):
    product = get_old_imeisv_barcode_info(upc)
    return product.get("tac", False) if product else False

def get_old_imeisv_barcode_fac(upc):
    product = get_old_imeisv_barcode_info(upc)
    return product.get("fac", False) if product else False

def get_old_imeisv_barcode_serialnumber(upc):
    product = get_old_imeisv_barcode_info(upc)
    return product.get("serialnumber", False) if product else False

def get_old_imeisv_barcode_svn(upc):
    product = get_old_imeisv_barcode_info(upc)
    return product.get("svn", False) if product else False


'''
// Get Bank Card Number Info
// Source: https://en.wikipedia.org/wiki/Credit_card_number#Major_Industry_Identifier_.28MII.29
'''


def get_bcn_info(upc, infotype=None):
    upc = str(upc)
    if not re.match("^\\d{16}$", upc):
        return False

    upc_matches = re.match("^(\\d{1})(\\d{5})(\\d{9})(\\d{1})$", upc)
    if not upc_matches:
        return False

    upc_type = {
        'mii': upc_matches.group(1),
        'iin': upc_matches.group(1) + upc_matches.group(2),
        'account': upc_matches.group(3),
        'checkdigit': upc_matches.group(4)
    }

    return upc_type if infotype is None else upc_type.get(infotype, upc_type)

def get_bcn_mii(upc):
    product = get_bcn_info(upc)
    return product.get("mii", False) if product else False

def get_bcn_iin(upc):
    product = get_bcn_info(upc)
    return product.get("iin", False) if product else False

def get_bcn_account(upc):
    product = get_bcn_info(upc)
    return product.get("account", False) if product else False

def get_bcn_checkdigit(upc):
    product = get_bcn_info(upc)
    return product.get("checkdigit", False) if product else False


'''
// Get National Drug Codes UPC-A info
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''

def get_upca_ndc_barcode_info(upc, infotype=None):
    upc = str(upc)
    # Ensure proper 12-digit length and format for NDC
    if re.match("^0(\\d{12})$", upc):
        upc = upc[1:]  # Remove leading zero
    if not re.match("^3\\d{11}$", upc):
        return False

    upc_matches = re.match("^3(\\d{4})(\\d{4})(\\d{2})(\\d{1})$", upc)
    if not upc_matches:
        return False

    product = {
        'numbersystem': '3',
        'labeler': upc_matches.group(1),
        'productcode': upc_matches.group(2),
        'packagecode': upc_matches.group(3),
        'checkdigit': upc_matches.group(4)
    }
    return product if infotype is None else product.get(infotype, product)

def get_upca_ndc_barcode_numbersystem(upc):
    product = get_upca_ndc_barcode_info(upc)
    return product.get("numbersystem", False) if product else False

def get_upca_ndc_barcode_labeler(upc):
    product = get_upca_ndc_barcode_info(upc)
    return product.get("labeler", False) if product else False

def get_upca_ndc_barcode_productcode(upc):
    product = get_upca_ndc_barcode_info(upc)
    return product.get("productcode", False) if product else False

def get_upca_ndc_barcode_packagecode(upc):
    product = get_upca_ndc_barcode_info(upc)
    return product.get("packagecode", False) if product else False

def get_upca_ndc_barcode_checkdigit(upc):
    product = get_upca_ndc_barcode_info(upc)
    return product.get("checkdigit", False) if product else False


'''
// Get National Drug Codes info
// Source: http://www.drugs.com/ndc.html
// Source: http://www.wikihow.com/Read-12-Digit-UPC-Barcodes
'''


def get_ndc_barcode_info(upc, infotype=None):
    upc = str(upc)
    # Ensure the UPC is exactly 10 digits
    if not re.match("^\\d{10}$", upc):
        return False

    upc_matches = re.match("(\\d{4})(\\d{4})(\\d{2})", upc)
    if not upc_matches:
        return False

    product = {
        'labeler': upc_matches.group(1),
        'productcode': upc_matches.group(2),
        'packagecode': upc_matches.group(3)
    }
    return product if infotype is None else product.get(infotype, product)

def get_ndc_barcode_labeler(upc):
    product = get_ndc_barcode_info(upc)
    return product.get("labeler", False) if product else False

def get_ndc_barcode_productcode(upc):
    product = get_ndc_barcode_info(upc)
    return product.get("productcode", False) if product else False

def get_ndc_barcode_packagecode(upc):
    product = get_ndc_barcode_info(upc)
    return product.get("packagecode", False) if product else False

