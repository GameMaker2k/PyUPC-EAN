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

    $FileInfo: files.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import sys
import re
import platform
import upcean.validate
import upcean.support
try:
    import simplejson as json
except ImportError:
    import json
try:
    import xml.etree.cElementTree as cElementTree
except ImportError:
    import xml.etree.ElementTree as cElementTree
try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO
if(sys.version[0] == "2"):
    import urllib2
    import urlparse
if(sys.version[0] >= "3"):
    import urllib.request as urllib2
    import urllib.parse as urlparse
from xml.sax.saxutils import XMLGenerator
from upcean.versioninfo import __author__, __copyright__, __credits__, __email__, __license__, __maintainer__, __project__, __project_url__, __revision__, __status__, __version__, __version_alt__, __version_date__, __version_date_alt__, __version_date_info__, __version_info__, version_date, version_info
import upcean.encode.barcode
import upcean.encode.shortcuts

''' // User-Agent string for http/https requests '''
useragent_string = "Mozilla/5.0 (compatible; {proname}/{prover}; +{prourl})".format(
    proname=__project__, prover=__version_alt__, prourl=__project_url__)
if(platform.python_implementation() != ""):
    useragent_string_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system()+" "+platform.release(
    ), archtype=platform.machine(), prourl=__project_url__, pyimp=platform.python_implementation(), pyver=platform.python_version(), proname=__project__, prover=__version_alt__)
if(platform.python_implementation() == ""):
    useragent_string_alt = "Mozilla/5.0 ({osver}; {archtype}; +{prourl}) {pyimp}/{pyver} (KHTML, like Gecko) {proname}/{prover}".format(osver=platform.system(
    )+" "+platform.release(), archtype=platform.machine(), prourl=__project_url__, pyimp="Python", pyver=platform.python_version(), proname=__project__, prover=__version_alt__)


def check_if_string(strtext):
    if(sys.version[0] == "2"):
        if(isinstance(strtext, basestring)):
            return True
    if(sys.version[0] >= "3"):
        if(isinstance(strtext, str)):
            return True
    return False


''' // Create barcodes from XML file '''


def create_barcode_from_xml_file(xmlfile, draw=False):
    if(check_if_string(xmlfile) and re.findall("^(http|https)\\:\\/\\/", xmlfile)):
        xmlheaders = {'User-Agent': useragent_string}
        try:
            tree = cElementTree.ElementTree(file=urllib2.urlopen(
                urllib2.Request(xmlfile, None, xmlheaders)))
        except cElementTree.ParseError:
            return False
    else:
        try:
            tree = cElementTree.ElementTree(file=xmlfile)
        except cElementTree.ParseError:
            return False
    root = tree.getroot()
    bcdrawlist = []
    for child in root:
        if(child.tag == "python"):
            exec(child.text)
        if(child.tag == "barcode"):
            if(draw):
                xmlbarcode = {
                    "bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": None}
            if(not draw):
                if('file' in child.attrib):
                    xmlbarcode = {
                        "bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": child.attrib['file']}
                if('file' not in child.attrib):
                    xmlbarcode = {
                        "bctype": child.attrib['type'], "upc": child.attrib['code'], "outfile": None}
            if('size' in child.attrib):
                xmlbarcode.update({"resize": int(child.attrib['size'])})
            if('hideinfo' in child.attrib):
                hidebcinfo = child.attrib['hideinfo'].split()
                hidebcinfoval = []
                if(hidebcinfo[0] == "0"):
                    hidebcinfoval.append(False)
                if(hidebcinfo[0] == "1"):
                    hidebcinfoval.append(True)
                if(hidebcinfo[1] == "0"):
                    hidebcinfoval.append(False)
                if(hidebcinfo[1] == "1"):
                    hidebcinfoval.append(True)
                if(hidebcinfo[2] == "0"):
                    hidebcinfoval.append(False)
                if(hidebcinfo[2] == "1"):
                    hidebcinfoval.append(True)
                xmlbarcode.update({"hideinfo": tuple(hidebcinfoval)})
            if('height' in child.attrib):
                xmlbarcode.update(
                    {"barheight": tuple(map(int, child.attrib['height'].split()))})
            if('width' in child.attrib):
                xmlbarcode.update(
                    {"barwidth": tuple(map(int, child.attrib['width'].split()))})
            if('textxy' in child.attrib):
                xmlbarcode.update(
                    {"textxy": tuple(map(int, child.attrib['textxy'].split()))})
            if('color' in child.attrib):
                colorsplit = child.attrib['color'].split()
                colorsplit[0] = re.sub("\\s+", "", colorsplit[0])
                if(re.findall("^\\#", colorsplit[0])):
                    colorsplit1 = re.findall(
                        "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0])
                if(re.findall("^rgb", colorsplit[0])):
                    colorsplit1 = re.findall(
                        "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[0])
                colorsplit1 = colorsplit1[0]
                colorlist1 = (int(colorsplit1[0], 16), int(
                    colorsplit1[1], 16), int(colorsplit1[2], 16))
                colorsplit[1] = re.sub("\\s+", "", colorsplit[1])
                if(re.findall("^\\#", colorsplit[1])):
                    colorsplit2 = re.findall(
                        "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1])
                if(re.findall("^rgb", colorsplit[1])):
                    colorsplit2 = re.findall(
                        "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[1])
                colorsplit2 = colorsplit2[0]
                colorlist2 = (int(colorsplit2[0], 16), int(
                    colorsplit2[1], 16), int(colorsplit2[2], 16))
                colorsplit[2] = re.sub("\\s+", "", colorsplit[2])
                if(re.findall("^\\#", colorsplit[2])):
                    colorsplit3 = re.findall(
                        "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2])
                if(re.findall("^rgb", colorsplit[2])):
                    colorsplit3 = re.findall(
                        "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[2])
                colorsplit3 = colorsplit3[0]
                colorlist3 = (int(colorsplit3[0], 16), int(
                    colorsplit3[1], 16), int(colorsplit3[2], 16))
                colorlist = (colorlist1, colorlist2, colorlist3)
                xmlbarcode.update({"barcolor": colorlist})
            if('imageoutlib' in child.attrib):
                xmlbarcode.update({"imageoutlib": tuple(
                    map(int, child.attrib['imgoutlib'].split()))})
            bcstatinfo = upcean.encode.shortcuts.validate_create_barcode(
                **xmlbarcode)
            if(draw or 'file' not in child.attrib):
                bcdrawlist.append(bcstatinfo)
            if(not bcstatinfo):
                return False
    if(draw or (not draw and len(bcdrawlist) > 0)):
        return bcdrawlist
    if(not draw and len(bcdrawlist) == 0):
        return True


def create_barcode_from_xml_string(xmlfile, draw=False):
    return create_barcode_from_xml_file(StringIO(xmlfile), draw)


def draw_barcode_from_xml_file(xmlfile):
    return create_barcode_from_xml_file(xmlfile, True)


def draw_barcode_from_xml_string(xmlfile):
    return create_barcode_from_xml_file(StringIO(xmlfile), True)


def convert_from_xml_to_json_file(xmlfile, jsonfile=None):
    if(check_if_string(jsonfile) and re.findall("^(http|https)\\:\\/\\/", jsonfile)):
        xmlheaders = {'User-Agent': useragent_string}
        try:
            tree = cElementTree.ElementTree(file=urllib2.urlopen(
                urllib2.Request(xmlfile, None, xmlheaders)))
        except cElementTree.ParseError:
            return False
    else:
        try:
            tree = cElementTree.ElementTree(file=xmlfile)
        except cElementTree.ParseError:
            return False
    bctree = tree.getroot()
    bctreeln = len(bctree)
    bctreect = 0
    jsonlist = {'barcodes': {'barcode': []}}
    for child in bctree:
        if(child.tag == "barcode"):
            jsontmpdict = {}
        if('type' in child.attrib):
            jsontmpdict.update({"type": child.attrib['type']})
        if('code' in child.attrib):
            jsontmpdict.update({"code": child.attrib['code']})
        if('file' in child.attrib):
            jsontmpdict.update({"file": child.attrib['file']})
        if('size' in child.attrib):
            jsontmpdict.update({"size": child.attrib['size']})
        if('hideinfo' in child.attrib):
            jsontmpdict.update({"hideinfo": child.attrib['hideinfo']})
        if('height' in child.attrib):
            jsontmpdict.update({"height": child.attrib['height']})
        if('width' in child.attrib):
            jsontmpdict.update({"width": child.attrib['width']})
        if('textxy' in child.attrib):
            jsontmpdict.update({"textxy": child.attrib['textxy']})
        if('color' in child.attrib):
            jsontmpdict.update({"color": child.attrib['color']})
        if('imageoutlib' in child.attrib):
            jsontmpdict.update({"imageoutlib": child.attrib['imageoutlib']})
        jsonlist['barcodes']['barcode'].append(jsontmpdict)
    if(jsonfile is not None):
        jsonofile = open(jsonfile, "w+")
        json.dump(jsonlist, jsonofile)
        jsonofile.close()
        return True
    if(jsonfile is None):
        return json.dumps(jsonlist)


def convert_from_xml_to_json_string(xmlfile, jsonfile=None):
    return convert_from_xml_to_json_file(StringIO(xmlfile), jsonfile)


def create_barcode_from_json_file(jsonfile, draw=False):
    if(check_if_string(jsonfile) and re.findall("^(http|https)\\:\\/\\/", jsonfile)):
        jsonheaders = {'User-Agent': useragent_string}
        tree = json.load(urllib2.urlopen(
            urllib2.Request(jsonfile, None, jsonheaders)))
    else:
        if(check_if_string(jsonfile)):
            jsonfile = open(jsonfile, "r")
        tree = json.load(jsonfile)
        jsonfile.close()
    try:
        bctree = tree['barcodes']['barcode']
    except:
        return False
    bctreeln = len(bctree)
    bctreect = 0
    bcdrawlist = []
    while(bctreect < bctreeln):
        if(draw):
            jsonbarcode = {"bctype": bctree[bctreect]['type'],
                           "upc": bctree[bctreect]['code'], "outfile": None}
        if(not draw):
            if('file' in bctree[bctreect]):
                jsonbarcode = {"bctype": bctree[bctreect]['type'],
                               "upc": bctree[bctreect]['code'], "outfile": bctree[bctreect]['file']}
            if('file' not in bctree[bctreect]):
                jsonbarcode = {
                    "bctype": bctree[bctreect]['type'], "upc": bctree[bctreect]['code'], "outfile": None}
        if('size' in bctree[bctreect]):
            jsonbarcode.update({"resize": int(bctree[bctreect]['size'])})
        if('hideinfo' in bctree[bctreect]):
            hidebcinfo = bctree[bctreect]['hideinfo'].split()
            hidebcinfoval = []
            if(hidebcinfo[0] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[0] == "1"):
                hidebcinfoval.append(True)
            if(hidebcinfo[1] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[1] == "1"):
                hidebcinfoval.append(True)
            if(hidebcinfo[2] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[2] == "1"):
                hidebcinfoval.append(True)
            jsonbarcode.update({"hideinfo": tuple(hidebcinfoval)})
        if('height' in bctree[bctreect]):
            jsonbarcode.update(
                {"barheight": tuple(map(int, bctree[bctreect]['height'].split()))})
        if('width' in bctree[bctreect]):
            jsonbarcode.update(
                {"barwidth": tuple(map(int, bctree[bctreect]['width'].split()))})
        if('textxy' in bctree[bctreect]):
            jsonbarcode.update(
                {"textxy": tuple(map(int, bctree[bctreect]['textxy'].split()))})
        if('color' in bctree[bctreect]):
            colorsplit = bctree[bctreect]['color'].split()
            colorsplit[0] = re.sub("\\s+", "", colorsplit[0])
            if(re.findall("^\\#", colorsplit[0])):
                colorsplit1 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0])
            if(re.findall("^rgb", colorsplit[0])):
                colorsplit1 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[0])
            colorsplit1 = colorsplit1[0]
            colorlist1 = (int(colorsplit1[0], 16), int(
                colorsplit1[1], 16), int(colorsplit1[2], 16))
            colorsplit[1] = re.sub("\\s+", "", colorsplit[1])
            if(re.findall("^\\#", colorsplit[1])):
                colorsplit2 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1])
            if(re.findall("^rgb", colorsplit[1])):
                colorsplit2 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[1])
            colorsplit2 = colorsplit2[0]
            colorlist2 = (int(colorsplit2[0], 16), int(
                colorsplit2[1], 16), int(colorsplit2[2], 16))
            colorsplit[2] = re.sub("\\s+", "", colorsplit[2])
            if(re.findall("^\\#", colorsplit[2])):
                colorsplit3 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2])
            if(re.findall("^rgb", colorsplit[2])):
                colorsplit3 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[2])
            colorsplit3 = colorsplit3[0]
            colorlist3 = (int(colorsplit3[0], 16), int(
                colorsplit3[1], 16), int(colorsplit3[2], 16))
            colorlist = (colorlist1, colorlist2, colorlist3)
            jsonbarcode.update({"barcolor": colorlist})
        if('imageoutlib' in bctree[bctreect]):
            jsonbarcode.update({"imageoutlib": tuple(
                map(int, bctree[bctreect]['imgoutlib'].split()))})
        bcstatinfo = upcean.encode.shortcuts.validate_create_barcode(
            **jsonbarcode)
        if(draw or 'file' not in bctree[bctreect]):
            bcdrawlist.append(bcstatinfo)
        if(not bcstatinfo):
            return False
        bctreect = bctreect + 1
    if(draw or (not draw and len(bcdrawlist) > 0)):
        return bcdrawlist
    if(not draw and len(bcdrawlist) == 0):
        return True


def create_barcode_from_json_string(jsonfile, draw=False):
    return create_barcode_from_json_file(StringIO(jsonfile), draw)


def draw_barcode_from_json_file(jsonfile):
    return create_barcode_from_json_file(jsonfile, True)


def draw_barcode_from_json_string(jsonfile):
    return create_barcode_from_json_file(StringIO(jsonfile), True)


def convert_from_json_to_xml_file(jsonfile, xmlfile=None):
    if(check_if_string(jsonfile) and re.findall("^(http|https)\\:\\/\\/", jsonfile)):
        jsonheaders = {'User-Agent': useragent_string}
        tree = json.load(urllib2.urlopen(
            urllib2.Request(jsonfile, None, jsonheaders)))
    else:
        if(check_if_string(jsonfile)):
            jsonfile = open(jsonfile, "r")
        tree = json.load(jsonfile)
        jsonfile.close()
    try:
        bctree = tree['barcodes']['barcode']
    except:
        return False
    bctreeln = len(bctree)
    bctreect = 0
    bcdrawlist = []
    xmlout = StringIO()
    upcxml = XMLGenerator(xmlout, "utf-8")
    upcxml.startDocument()
    upcxml.startElement("barcodes", {})
    upcxml.characters("\n")
    while(bctreect < bctreeln):
        upcxml.characters(" ")
        upcxml.startElement("barcode", bctree[bctreect])
        upcxml.endElement("barcode")
        upcxml.characters("\n")
        bctreect = bctreect + 1
    upcxml.endElement("barcodes")
    upcxml.endDocument()
    xmlout.seek(0)
    if(xmlfile is not None):
        xmlofile = open(xmlfile, "w+")
        xmlofile.write(xmlout.read())
        xmlofile.close()
        return True
    if(xmlfile is None):
        return xmlout.read()


def convert_from_json_to_xml_string(jsonfile, xmlfile=None):
    return convert_from_json_to_xml_file(StringIO(jsonfile), xmlfile)


def create_barcode_from_qs_file(qsfile, draw=False):
    if(check_if_string(qsfile) and re.findall("^(http|https)\\:\\/\\/", qsfile)):
        qsheaders = {'User-Agent': useragent_string}
        tree = urlparse.parse_qs(urllib2.urlopen(
            urllib2.Request(qsfile, None, qsheaders)).read())
    else:
        if(check_if_string(qsfile)):
            qsfile = open(qsfile, "r")
        qsfile.seek(0)
        tree = urlparse.parse_qs(qsfile.read())
        qsfile.close()
    bctree = tree
    if(len(bctree['type']) < len(bctree['code']) or len(bctree['type']) == len(bctree['code'])):
        bctreeln = len(bctree['type'])
    if(len(bctree['code']) < len(bctree['type'])):
        bctreeln = len(bctree['code'])
    bctreect = 0
    bcdrawlist = []
    while(bctreect < bctreeln):
        qsbarcode = {}
        nofilesave = False
        if(draw):
            nofilesave = True
            qsbarcode.update(
                {"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None})
        if(not draw):
            try:
                nofilesave = False
                qsbarcode.update(
                    {"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": bctree['file'][bctreect]})
            except KeyError:
                nofilesave = True
                qsbarcode.update(
                    {"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None})
            except IndexError:
                nofilesave = True
                qsbarcode.update(
                    {"bctype": bctree['type'][bctreect], "upc": bctree['code'][bctreect], "outfile": None})
        try:
            qsbarcode.update({"resize": int(bctree['size'][bctreect])})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            hidebcinfo = bctree['hideinfo'][bctreect].split()
            hidebcinfoval = []
            if(hidebcinfo[0] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[0] == "1"):
                hidebcinfoval.append(True)
            if(hidebcinfo[1] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[1] == "1"):
                hidebcinfoval.append(True)
            if(hidebcinfo[2] == "0"):
                hidebcinfoval.append(False)
            if(hidebcinfo[2] == "1"):
                hidebcinfoval.append(True)
            qsbarcode.update({"hideinfo": tuple(hidebcinfoval)})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barheight": int(bctree['height'][bctreect])})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barwidth": int(bctree['width'][bctreect])})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"textxy": int(bctree['textxy'][bctreect])})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            colorsplit = bctree['color'][bctreect].split()
            colorsplit[0] = re.sub("\\s+", "", colorsplit[0])
            if(re.findall("^\\#", colorsplit[0])):
                colorsplit1 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[0])
            if(re.findall("^rgb", colorsplit[0])):
                colorsplit1 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[0])
            colorsplit1 = colorsplit1[0]
            colorlist1 = (int(colorsplit1[0], 16), int(
                colorsplit1[1], 16), int(colorsplit1[2], 16))
            colorsplit[1] = re.sub("\\s+", "", colorsplit[1])
            if(re.findall("^\\#", colorsplit[1])):
                colorsplit2 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[1])
            if(re.findall("^rgb", colorsplit[1])):
                colorsplit2 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[1])
            colorsplit2 = colorsplit2[0]
            colorlist2 = (int(colorsplit2[0], 16), int(
                colorsplit2[1], 16), int(colorsplit2[2], 16))
            colorsplit[2] = re.sub("\\s+", "", colorsplit[2])
            if(re.findall("^\\#", colorsplit[2])):
                colorsplit3 = re.findall(
                    "^\\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", colorsplit[2])
            if(re.findall("^rgb", colorsplit[2])):
                colorsplit3 = re.findall(
                    "^rgb\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\)", colorsplit[2])
            colorsplit3 = colorsplit3[0]
            colorlist3 = (int(colorsplit3[0], 16), int(
                colorsplit3[1], 16), int(colorsplit3[2], 16))
            colorlist = (colorlist1, colorlist2, colorlist3)
            qsbarcode.update({"barcolor": colorlist})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update(
                {"imageoutlib": int(bctree['imgoutlib'][bctreect])})
        except KeyError:
            pass
        except IndexError:
            pass
        bcstatinfo = upcean.encode.shortcuts.validate_create_barcode(
            **qsbarcode)
        if(draw or nofilesave):
            bcdrawlist.append(bcstatinfo)
        if(not bcstatinfo):
            return False
        bctreect = bctreect + 1
    if(draw or (not draw and len(bcdrawlist) > 0)):
        return bcdrawlist
    if(not draw and len(bcdrawlist) == 0):
        return True


def create_barcode_from_qs_string(qsfile, draw=False):
    return create_barcode_from_qs_file(StringIO(qsfile), draw)


def draw_barcode_from_qs_file(qsfile):
    return create_barcode_from_qs_file(qsfile, True)


def draw_barcode_from_qs_string(qsfile):
    return create_barcode_from_qs_file(StringIO(qsfile), True)


def convert_from_qs_to_xml_file(qsfile, xmlfile=None):
    if(check_if_string(qsfile) and re.findall("^(http|https)\\:\\/\\/", qsfile)):
        qsheaders = {'User-Agent': useragent_string}
        tree = urlparse.parse_qs(urllib2.urlopen(
            urllib2.Request(qsfile, None, qsheaders)).read())
    else:
        if(check_if_string(qsfile)):
            qsfile = open(qsfile, "r")
        qsfile.seek(0)
        tree = urlparse.parse_qs(qsfile.read())
        qsfile.close()
    bctree = tree
    bctreeln = len(bctree)
    if(len(bctree['type']) < len(bctree['code']) or len(bctree['type']) == len(bctree['code'])):
        bctreeln = len(bctree['type'])
    if(len(bctree['code']) < len(bctree['type'])):
        bctreeln = len(bctree['code'])
    bctreect = 0
    bcdrawlist = []
    xmlout = StringIO()
    upcxml = XMLGenerator(xmlout, "utf-8")
    upcxml.startDocument()
    upcxml.startElement("barcodes", {})
    upcxml.characters("\n")
    while(bctreect < bctreeln):
        qsbarcode = {}
        qsbarcode.update(
            {"type": bctree['type'][bctreect], "code": bctree['code'][bctreect]})
        try:
            qsbarcode.update({"file": bctree['file'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"size": bctree['size'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"hideinfo": bctree['hideinfo'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barheight": bctree['barheight'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barwidth": bctree['barwidth'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"textxy": bctree['textxy'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"color": bctree['color'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"imageoutlib": bctree['imageoutlib'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        upcxml.characters(" ")
        upcxml.startElement("barcode", qsbarcode)
        upcxml.endElement("barcode")
        upcxml.characters("\n")
        bctreect = bctreect + 1
    upcxml.endElement("barcodes")
    upcxml.endDocument()
    xmlout.seek(0)
    if(xmlfile is not None):
        xmlofile = open(xmlfile, "w+")
        xmlofile.write(xmlout.read())
        xmlofile.close()
        return True
    if(xmlfile is None):
        return xmlout.read()


def convert_from_qs_to_xml_string(qsfile, xmlfile=None):
    return convert_from_qs_to_xml_file(StringIO(qsfile), xmlfile)


def convert_from_qs_to_json_file(qsfile, jsonfile=None):
    if(check_if_string(qsfile) and re.findall("^(http|https)\\:\\/\\/", qsfile)):
        qsheaders = {'User-Agent': useragent_string}
        tree = urlparse.parse_qs(urllib2.urlopen(
            urllib2.Request(qsfile, None, qsheaders)).read())
    else:
        if(check_if_string(qsfile)):
            qsfile = open(qsfile, "r")
        qsfile.seek(0)
        tree = urlparse.parse_qs(qsfile.read())
        qsfile.close()
    bctree = tree
    bctreeln = len(bctree)
    if(len(bctree['type']) < len(bctree['code']) or len(bctree['type']) == len(bctree['code'])):
        bctreeln = len(bctree['type'])
    if(len(bctree['code']) < len(bctree['type'])):
        bctreeln = len(bctree['code'])
    bctreect = 0
    bcdrawlist = []
    jsonlist = {'barcodes': {'barcode': []}}
    while(bctreect < bctreeln):
        qsbarcode = {}
        qsbarcode.update(
            {"type": bctree['type'][bctreect], "code": bctree['code'][bctreect]})
        try:
            qsbarcode.update({"file": bctree['file'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"size": bctree['size'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"hideinfo": bctree['hideinfo'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barheight": bctree['barheight'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"barwidth": bctree['barwidth'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"textxy": bctree['textxy'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"color": bctree['color'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        try:
            qsbarcode.update({"imageoutlib": bctree['imageoutlib'][bctreect]})
        except KeyError:
            pass
        except IndexError:
            pass
        jsonlist['barcodes']['barcode'].append(qsbarcode)
        bctreect = bctreect + 1
    if(jsonfile is not None):
        jsonofile = open(jsonfile, "w+")
        json.dump(jsonlist, jsonofile)
        jsonofile.close()
        return True
    if(jsonfile is None):
        return json.dumps(jsonlist)


def convert_from_qs_to_json_string(qsfile, jsonfile=None):
    return convert_from_qs_to_json_file(StringIO(qsfile), jsonfile)
