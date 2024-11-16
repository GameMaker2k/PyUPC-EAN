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

    $FileInfo: goodwill.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.predraw import *
import re
import sys
import upcean.support

import io
try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import IOBase

try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO

import upcean.encode.ean2
import upcean.encode.ean5
from upcean.encode.upca import *
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
qahirahsupport = upcean.support.check_for_qahirah()
cairosvgsupport = upcean.support.check_for_cairosvg()
svgwritesupport = upcean.support.check_for_svgwrite()
wandsupport = upcean.support.check_for_wand()
magicksupport = upcean.support.check_for_magick()
pgmagicksupport = upcean.support.check_for_pgmagick()
defaultdraw = upcean.support.defaultdraw
if(pilsupport or pillowsupport):
    import upcean.predraw.prepil

if(cairosupport):
    import upcean.predraw.precairo
if(svgwritesupport):
    import upcean.predraw.presvgwrite


def create_goodwill_barcode(upc, outfile="./goodwill.png", resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    imageoutlib = imageoutlib.lower()
    if(not pilsupport and imageoutlib == "pillow"):
        imageoutlib = "cairo"
    if(not cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        imageoutlib = "pillow"
    if(not cairosupport and imageoutlib == "cairosvg"):
        imageoutlib = "pillow"
    if(imageoutlib != "pillow" and imageoutlib != "cairo" and imageoutlib != "cairosvg"):
        imageoutlib = "pillow"
    if(not pilsupport and not cairosupport):
        return False
    if(outfile is None):
        if(imageoutlib == "cairosvg"):
            oldoutfile = None
            outfile = None
            outfileext = "SVG"
        else:
            oldoutfile = None
            outfile = None
            outfileext = None
    else:
        oldoutfile = upcean.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    upc_pieces = None
    supplement = None
    if(re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]{1})([0-9]{2})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)):
        upc_pieces = re.findall("([0-9]+)([ |\\|]){1}([0-9]{5})$", upc)
        upc_pieces = upc_pieces[0]
        upc = upc_pieces[0]
        supplement = upc_pieces[2]
    if(len(upc) > 12 or len(upc) < 12):
        return False
    if(not re.findall("^([0-9]*[\\.]?[0-9])", str(resize)) or int(resize) < 1):
        resize = 1
    if(pilsupport and imageoutlib == "pillow"):
        try:
            pil_ver = Image.PILLOW_VERSION
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
            pil_is_pillow = True
        except AttributeError:
            try:
                pil_ver = Image.VERSION
                pil_is_pillow = False
            except AttributeError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            except NameError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
        except NameError:
            try:
                pil_ver = Image.VERSION
                pil_is_pillow = False
            except AttributeError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            except NameError:
                pil_ver = Image.__version__
                pil_is_pillow = True
            pil_ver = pil_ver.split(".")
            pil_ver = [int(x) for x in pil_ver]
        pil_addon_fix = 0
        cairo_addon_fix = 0
        pil_prevercheck = [str(x) for x in pil_ver]
        pil_vercheck = int(
            pil_prevercheck[0]+pil_prevercheck[1]+pil_prevercheck[2])
        if(pil_is_pillow and pil_vercheck >= 210 and pil_vercheck < 220):
            pil_addon_fix = int(resize) * 2
            cairo_addon_fix = 0
    elif(pilsupport and imageoutlib == "pillow"):
        pil_addon_fix = 0
        cairo_addon_fix = 0
    elif(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        pil_addon_fix = 0
        cairo_addon_fix = (9 * (int(resize) * barwidth[1]))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    cairo_addon_fix += (shiftxy[1] * (int(resize) * barwidth[1]))
    upc_matches = re.findall("(\\d{1})(\\d{5})(\\d{5})(\\d{1})", upc)
    if(len(upc_matches) <= 0):
        return False
    goodwillinfo = upcean.getprefix.getprefix.get_goodwill_upca_barcode_info(
        upc)
    barcolor = ((0, 0, 0), (0, 0, 0), (255, 255, 255))
    if(goodwillinfo['tagcolor'] == "Pink"):
        barcolor = ((0, 0, 0), (0, 0, 0), (255, 192, 203))
    elif(goodwillinfo['tagcolor'] == "Yellow"):
        barcolor = ((0, 0, 0), (0, 0, 0), (255, 255, 0))
    elif(goodwillinfo['tagcolor'] == "Green"):
        barcolor = ((0, 0, 0), (0, 0, 0), (207, 240, 236))
    elif(goodwillinfo['tagcolor'] == "Blue"):
        barcolor = ((0, 0, 0), (0, 0, 0), (12, 191, 233))
    elif(goodwillinfo['tagcolor'] == "Orange"):
        barcolor = ((0, 0, 0), (0, 0, 0), (255, 162, 0))
    else:
        barcolor = ((0, 0, 0), (0, 0, 0), (255, 255, 255))
    if(not goodwillinfo):
        return False
    upc_matches = upc_matches[0]
    PrefixDigit = upc_matches[0]
    LeftDigit = list(str(upc_matches[0])+str(upc_matches[1]))
    RightDigit = list(str(upc_matches[2])+str(upc_matches[3]))
    CheckDigit = upc_matches[3]
    upc_size_add = 0
    if(supplement is not None and len(supplement) == 2):
        upc_size_add = 29
    if(supplement is not None and len(supplement) == 5):
        upc_size_add = 56
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (113 + upc_size_add, barheight[1] + (45 * barwidth[0])))
        upc_img = ImageDraw.Draw(upc_preimg)
        upc_img.rectangle(
            [(0, 0), (113 + upc_size_add, barheight[1] + (45 * barwidth[0]))], fill=barcolor[2])
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(outfileext == "SVG"):
            if(outfile is None):
                imgoutfile = None
            else:
                if(sys.version[0] == "2"):
                    imgoutfile = StringIO()
                if(sys.version[0] >= "3"):
                    imgoutfile = BytesIO()
            upc_preimg = cairo.SVGSurface(
                imgoutfile, (113 + upc_size_add, barheight[1] + (45 * barwidth[0])))
        elif(outfileext == "PDF"):
            upc_preimg = cairo.PDFSurface(
                None, ((113 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
        elif(outfileext == "PS" or outfileext == "EPS"):
            upc_preimg = cairo.PSSurface(
                None, ((113 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (9 * barwidth[1])) * int(resize))
            if(outfileext == "EPS"):
                upc_preimg.set_eps(True)
            else:
                upc_preimg.set_eps(False)
        else:
            upc_preimg = cairo.ImageSurface(
                cairo.FORMAT_RGB24, (113 + upc_size_add, barheight[1] + (45 * barwidth[0])))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
        upc_img.rectangle(0, 0, 113 + upc_size_add,
                          barheight[1] + (45 * barwidth[0]))
        upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2])
        upc_img.fill()
    drawColorText(upc_img, 12 * int(resize * barwidth[0]), 30 + (23 * (int(resize) - 1)) - (4 * (int(
        resize * barwidth[0]) - 1)), (4 * int(resize * barwidth[0])), "Goodwill", barcolor[1], "ocrb", imageoutlib)
    if(len(goodwillinfo['pricewdnz']) < 4):
        goodwillinfo['pricewdnz'] = "0"+goodwillinfo['pricewdnz']
    upc_size_add = 0
    if(len(goodwillinfo['pricewdnz']) == 5):
        upc_size_add = -14
    if(len(goodwillinfo['pricewdnz']) == 6):
        upc_size_add = -30
    drawColorText(upc_img, 16 * int(resize * barwidth[0]), 36 + upc_size_add + (23 * (int(resize) - 1)) - (4 * (int(
        resize * barwidth[0]) - 1)), (75 * int(resize * barwidth[0])), "$"+goodwillinfo['pricewdnz'], barcolor[1], "ocrb", imageoutlib)
    if(pilsupport and imageoutlib == "pillow"):
        if(supplement is not None and len(supplement) == 2):
            upc_sup_img = upcean.encode.ean2.draw_ean2sup_barcode(
                supplement, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
            if(upc_sup_img):
                new_upc_img.paste(upc_sup_img, (113 * int(resize), 0))
                del(upc_sup_img)
        if(supplement is not None and len(supplement) == 5):
            upc_sup_img = upcean.encode.ean5.draw_ean5sup_barcode(
                supplement, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
            if(upc_sup_img):
                new_upc_img.paste(upc_sup_img, (113 * int(resize), 0))
                del(upc_sup_img)
    if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
        if(supplement != None and len(supplement) == 2):
            upc_sup_img = draw_ean2sup_barcode(
                supplement, 1, hideinfo, barheight, barwidth, barcolor, imageoutlib)
            new_upc_img.set_source_surface(upc_sup_img, 113, 0)
            new_upc_img.paint()
            del(upc_sup_img)
        if(supplement != None and len(supplement) == 5):
            upc_sup_img = draw_ean5sup_barcode(
                supplement, 1, hideinfo, barheight, barwidth, barcolor, imageoutlib)
            new_upc_img.set_source_surface(upc_sup_img, 113, 0)
            new_upc_img.paint()
            del(upc_sup_img)
    exargdict = {'comment': "upca; goodwill; "+upc}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        if(pilsupport and imageoutlib == "pillow"):
            return [upc_img, upc_preimg, {'upc': upc, 'outfile': outfile, 'resize': resize, 'shiftxy': shiftxy, 'barheight': barheight, 'barwidth': barwidth, 'barcolor': barcolor, 'hideinfo': hideinfo, 'imageoutlib': imageoutlib}, upc_array]
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            return [upc_img, upc_preimg, {'upc': upc, 'outfile': outfile, 'resize': resize, 'shiftxy': shiftxy, 'barheight': barheight, 'barwidth': barwidth, 'barcolor': barcolor, 'hideinfo': hideinfo, 'imageoutlib': imageoutlib}, upc_array]
    if(sys.version[0] == "2"):
        if(outfile == "-" or outfile == "" or outfile == " " or outfile is None):
            stdoutfile = StringIO()
            if(outfileext == "WEBP"):
                exargdict.update(
                    {'lossless': True, 'quality': 100, 'method': 6})
            elif(outfileext == "JPEG"):
                exargdict.update(
                    {'quality': 100, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {'comment': "upca; goodwill; "+upc}
            try:
                if(pilsupport and imageoutlib == "pillow"):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            upc_preimg.convert(mode="1").tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        upc_preimg.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        upc_preimg.flush()
                        upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.write_to_png(stdoutfile)
                        stdoutfile.seek(0)
                        return stdoutfile
            except:
                return False
    if(sys.version[0] >= "3"):
        stdoutfile = BytesIO()
        if(outfile == "-" or outfile == "" or outfile == " " or outfile is None):
            if(outfileext == "WEBP"):
                exargdict.update(
                    {'lossless': True, 'quality': 100, 'method': 6})
            elif(outfileext == "JPEG"):
                exargdict.update(
                    {'quality': 100, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {'comment': upc}
            try:
                if(pilsupport and imageoutlib == "pillow"):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XBM"):
                        stdoutfile.write(
                            upc_preimg.convert(mode='1').tobitmap())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "XPM"):
                        upc_preimg.convert(mode="P").save(
                            stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.save(stdoutfile, outfileext, **exargdict)
                        stdoutfile.seek(0)
                        return stdoutfile
                if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                    if(outfileext == "BYTES"):
                        stdoutfile.write(upc_preimg.get_data().tobytes())
                        stdoutfile.seek(0)
                        return stdoutfile
                    elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                        upc_preimg.flush()
                        upc_preimg.finish()
                        imgoutfile.seek(0)
                        svgouttext = imgoutfile.read()
                        stdoutfile.write(svgouttext)
                        imgoutfile.close()
                        stdoutfile.seek(0)
                        return stdoutfile
                    else:
                        upc_preimg.write_to_png(stdoutfile)
                        stdoutfile.seek(0)
                        return stdoutfile
            except:
                return False
    if(outfile != "-" and outfile != "" and outfile != " "):
        if(outfileext == "WEBP"):
            exargdict.update({'lossless': True, 'quality': 100, 'method': 6})
        if(outfileext == "HEIC"):
            exargdict.update({'lossless': True, 'quality': 100})
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 100, 'optimize': True, 'progressive': True})
        elif(outfileext == "GIF"):
            exargdict.update(
                {'optimize': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9, 'quality': 100})
            if(pilsupport):
                # Add a comment to the image
                info = PngImagePlugin.PngInfo()
                info.add_text("Comment", upc)
                exargdict.update({'pnginfo': info})
        else:
            exargdict = {'comment': upc}
        try:
            if(pilsupport and imageoutlib == "pillow"):
                if(outfileext == "BYTES"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.tobytes())
                elif(outfileext == "XBM"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.get_data().tobytes())
                elif(outfileext == "XPM"):
                    upc_preimg.convert(mode="P").save(
                        outfile, outfileext, **exargdict)
                else:
                    upc_preimg.save(outfile, outfileext, **exargdict)
            if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
                if(outfileext == "BYTES"):
                    with open(outfile, 'wb+') as f:
                        f.write(upc_preimg.get_data().tobytes())
                    return True
                elif(outfileext == "SVG" or outfileext == "PDF" or outfileext == "PS" or outfileext == "EPS" or imageoutlib == "cairosvg"):
                    upc_preimg.flush()
                    upc_preimg.finish()
                    imgoutfile.seek(0)
                    svgouttext = imgoutfile.read()
                    with open(outfile, 'wb+') as f:
                        f.write(svgouttext)
                    return True
                else:
                    upc_preimg.write_to_png(outfile)
                    return True
        except Exception:
            return False
    return True


def draw_goodwill_barcode(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    return create_goodwill_barcode(upc, None, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)


def encode_goodwill_barcode(upc, resize=1, shiftxy=(0, 0), barheight=(48, 54), barwidth=(1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), hideinfo=(False, False, False), imageoutlib=defaultdraw):
    return create_goodwill_barcode(upc, None, resize, shiftxy, barheight, barwidth, barcolor, hideinfo, imageoutlib)
