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

    $FileInfo: itf.py - Last Update: 10/30/2024 Ver. 2.10.8 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from upcean.encode.predraw import *
import re
import sys
import upcean.support
try:
    from io import StringIO, BytesIO
except ImportError:
    try:
        from cStringIO import StringIO
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO
        from StringIO import StringIO as BytesIO
pilsupport = upcean.support.check_for_pil()
pillowsupport = upcean.support.check_for_pillow()
cairosupport = upcean.support.check_for_cairo()
if(pilsupport or pillowsupport):
    import upcean.encode.prepil
if(cairosupport):
    import upcean.encode.precairo


def create_itf_barcode(upc, outfile="./itf.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    upc = str(upc)
    hidesn = hideinfo[0]
    hidecd = hideinfo[1]
    hidetext = hideinfo[2]
    threewidebar = True
    imageoutlib = imageoutlib.lower()
    barheightadd = barheight[1]
    if(barheight[0] >= barheight[1]):
        barheightadd = barheight[0] + 6
    else:
        barheightadd = barheight[1]
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
        oldoutfile = upcean.encode.predraw.get_save_filename(
            outfile, imageoutlib)
        if(isinstance(oldoutfile, tuple) or isinstance(oldoutfile, list)):
            del(outfile)
            outfile = oldoutfile[0]
            outfileext = oldoutfile[1]
            if(cairosupport and imageoutlib == "cairo" and outfileext == "SVG"):
                imageoutlib = "cairosvg"
            if(cairosupport and imageoutlib == "cairosvg" and outfileext != "SVG"):
                imageoutlib = "cairo"
    if(len(upc) % 2):
        return False
    if(len(upc) < 6):
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
        cairo_addon_fix = (8 * (int(resize)))
    else:
        pil_addon_fix = 0
        cairo_addon_fix = 0
    upc_matches = re.findall("([0-9]{2})", upc)
    if(threewidebar):
        upc_size_add = (len(upc_matches) * 18) * barwidth[0]
    else:
        upc_size_add = (len(upc_matches) * 14) * barwidth[0]
    if(len(upc_matches) <= 0):
        return False
    if(pilsupport and imageoutlib == "pillow"):
        upc_preimg = Image.new(
            "RGB", (((39 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[0])) * int(resize)))
        upc_img = ImageDraw.Draw(upc_preimg)
        upc_img.rectangle([(0, 0), (((39 * barwidth[0]) + upc_size_add) * int(resize),
                          (barheightadd + (15 * barwidth[0])) * int(resize))], fill=barcolor[2])
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
                imgoutfile, ((39 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[0])) * int(resize))
        elif(outfileext == "PDF"):
            upc_preimg = cairo.PDFSurface(
                None, ((39 * barwidth[0]) + upc_size_add) * int(resize), barheightadd + (15 * barwidth[1]))
        elif(outfileext == "PS" or outfileext == "EPS"):
            upc_preimg = cairo.PSSurface(
                None, ((39 * barwidth[0]) + upc_size_add) * int(resize), barheightadd + (15 * barwidth[1]))
            if(outfileext == "EPS"):
                upc_preimg.set_eps(True)
            else:
                upc_preimg.set_eps(False)
        else:
            upc_preimg = cairo.ImageSurface(
                cairo.FORMAT_RGB24, ((39 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[0])) * int(resize))
        upc_img = cairo.Context(upc_preimg)
        upc_img.set_antialias(cairo.ANTIALIAS_NONE)
        upc_img.rectangle(
            0, 0, ((39 * barwidth[0]) + upc_size_add) * int(resize), (barheightadd + (15 * barwidth[0])) * int(resize))
        upc_img.set_source_rgb(barcolor[2][0], barcolor[2][1], barcolor[2][2])
        upc_img.fill()
    upc_array = {'upc': upc, 'code': []}
    start_barcode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
    LineStart = 0
    BarNum = 0
    start_bc_num_end = len(start_barcode)
    LineSize = barheight[0] * int(resize)
    if(hidetext):
        LineSize = barheight[1] * int(resize)
    while(BarNum < start_bc_num_end):
        if(start_barcode[BarNum] == 1):
            drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(start_barcode[BarNum] == 0):
            drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    NumZero = 0
    while (NumZero < len(upc_matches)):
        ArrayDigit = list(upc_matches[NumZero])
        left_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[0]) == 0):
            left_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[0]) == 1):
            left_barcolor = [1, 0, 0, 0, 1]
        if(int(ArrayDigit[0]) == 2):
            left_barcolor = [0, 1, 0, 0, 1]
        if(int(ArrayDigit[0]) == 3):
            left_barcolor = [1, 1, 0, 0, 0]
        if(int(ArrayDigit[0]) == 4):
            left_barcolor = [0, 0, 1, 0, 1]
        if(int(ArrayDigit[0]) == 5):
            left_barcolor = [1, 0, 1, 0, 0]
        if(int(ArrayDigit[0]) == 6):
            left_barcolor = [0, 1, 1, 0, 0]
        if(int(ArrayDigit[0]) == 7):
            left_barcolor = [0, 0, 0, 1, 1]
        if(int(ArrayDigit[0]) == 8):
            left_barcolor = [1, 0, 0, 1, 0]
        if(int(ArrayDigit[0]) == 9):
            left_barcolor = [0, 1, 0, 1, 0]
        right_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[1]) == 0):
            right_barcolor = [0, 0, 1, 1, 0]
        if(int(ArrayDigit[1]) == 1):
            right_barcolor = [1, 0, 0, 0, 1]
        if(int(ArrayDigit[1]) == 2):
            right_barcolor = [0, 1, 0, 0, 1]
        if(int(ArrayDigit[1]) == 3):
            right_barcolor = [1, 1, 0, 0, 0]
        if(int(ArrayDigit[1]) == 4):
            right_barcolor = [0, 0, 1, 0, 1]
        if(int(ArrayDigit[1]) == 5):
            right_barcolor = [1, 0, 1, 0, 0]
        if(int(ArrayDigit[1]) == 6):
            right_barcolor = [0, 1, 1, 0, 0]
        if(int(ArrayDigit[1]) == 7):
            right_barcolor = [0, 0, 0, 1, 1]
        if(int(ArrayDigit[1]) == 8):
            right_barcolor = [1, 0, 0, 1, 0]
        if(int(ArrayDigit[1]) == 9):
            right_barcolor = [0, 1, 0, 1, 0]
        InnerUPCNum = 0
        while (InnerUPCNum < len(left_barcolor)):
            if(left_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
                if(threewidebar):
                    drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                                  LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                    LineStart += barwidth[0] * int(resize)
                    BarNum += 1
            if(left_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
            if(right_barcolor[InnerUPCNum] == 1):
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
                if(threewidebar):
                    drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                                  LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                    LineStart += barwidth[0] * int(resize)
                    BarNum += 1
            if(right_barcolor[InnerUPCNum] == 0):
                drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                              LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
                LineStart += barwidth[0] * int(resize)
                BarNum += 1
            InnerUPCNum += 1
        NumZero += 1
    if(threewidebar):
        end_barcode = [1, 1, 1, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        end_barcode = [1, 1, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    end_bc_num = 0
    end_bc_num_end = len(end_barcode)
    while(end_bc_num < end_bc_num_end):
        if(end_barcode[end_bc_num] == 1):
            drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[0], imageoutlib)
        if(end_barcode[end_bc_num] == 0):
            drawColorLine(upc_img, LineStart, 4 * int(resize), LineStart,
                          LineSize, barwidth[0] * int(resize), barcolor[2], imageoutlib)
        end_bc_num += 1
        LineStart += barwidth[0] * int(resize)
        BarNum += 1
    if(not hidetext):
        NumTxtZero = 0
        LineTxtStart = 20
        if(not threewidebar):
            LineTxtStart -= 2
        while (NumTxtZero < len(upc_matches)):
            ArrayDigit = list(upc_matches[NumTxtZero])
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (21 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
                barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[0], barcolor[1], "ocrb", imageoutlib)
            if(threewidebar):
                LineTxtStart += 9 * int(resize)
            else:
                LineTxtStart += 7 * int(resize)
            drawColorText(upc_img, 10 * int(resize * barwidth[1]), (LineTxtStart + (21 * (int(resize) - 1))) * barwidth[0], cairo_addon_fix + (
                barheight[0] + (barheight[0] * (int(resize) - 1)) + pil_addon_fix) + (textxy[1] * int(resize)), ArrayDigit[1], barcolor[1], "ocrb", imageoutlib)
            if(threewidebar):
                LineTxtStart += 9 * int(resize)
            else:
                LineTxtStart += 7 * int(resize)
            NumTxtZero += 1
    exargdict = {}
    if(oldoutfile is None or isinstance(oldoutfile, bool)):
        if(pilsupport and imageoutlib == "pillow"):
            return [upc_img, upc_preimg, {'upc': upc, 'outfile': outfile, 'resize': resize, 'hideinfo': hideinfo, 'barheight': barheight, 'barwidth': barwidth, 'textxy': textxy, 'barcolor': barcolor}, upc_array]
        if(cairosupport and (imageoutlib == "cairo" or imageoutlib == "cairosvg")):
            return [upc_img, upc_preimg, {'upc': upc, 'outfile': outfile, 'resize': resize, 'hideinfo': hideinfo, 'barheight': barheight, 'barwidth': barwidth, 'textxy': textxy, 'barcolor': barcolor}, upc_array]
    if(sys.version[0] == "2"):
        if(outfile == "-" or outfile == "" or outfile == " " or outfile is None):
            stdoutfile = StringIO()
            if(outfileext == "WEBP"):
                exargdict.update(
                    {'lossless': True, 'quality': 100, 'method': 6})
            elif(outfileext == "JPEG"):
                exargdict.update(
                    {'quality': 95, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {}
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
                    {'quality': 95, 'optimize': True, 'progressive': True})
            elif(outfileext == "PNG"):
                exargdict.update({'optimize': True, 'compress_level': 9})
            else:
                exargdict = {}
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
        elif(outfileext == "JPEG"):
            exargdict.update(
                {'quality': 95, 'optimize': True, 'progressive': True})
        elif(outfileext == "PNG"):
            exargdict.update({'optimize': True, 'compress_level': 9})
        else:
            exargdict = {}
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


def draw_itf_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_itf_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_itf_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_itf_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def create_code25_interleaved_barcode(upc, outfile="./code25.png", resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_itf_barcode(upc, outfile, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def draw_code25_interleaved_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_code25_interleaved_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)


def encode_code25_interleaved_barcode(upc, resize=1, hideinfo=(False, False, False), barheight=(48, 54), barwidth=(1, 1), textxy=(1, 1, 1), barcolor=((0, 0, 0), (0, 0, 0), (255, 255, 255)), imageoutlib="pillow"):
    return create_code25_interleaved_barcode(upc, None, resize, hideinfo, barheight, barwidth, textxy, barcolor, imageoutlib)
