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

    $FileInfo: prepyqt.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

from PyQt5.QtGui import QImage, QPainter, QColor, QFont, QFontDatabase
from PyQt5.QtCore import QRect, QBuffer, QIODevice
import os
import re

try:
    basestring
except NameError:
    basestring = str

try:
    file
except NameError:
    from io import IOBase
    file = IOBase
from io import StringIO, BytesIO

# Importing the font paths and upload function from upcean
from upcean.fonts import fontpathocra, fontpathocraalt, fontpathocrb, fontpathocrbalt, fontpath
from upcean.xml.downloader import upload_file_to_internet_file

def color_to_qcolor(color):
    if isinstance(color, tuple):
        if len(color) == 3:
            return QColor(*color)
        elif len(color) == 4:
            return QColor(*color)  # RGBA
        else:
            raise ValueError("Color tuple must be of length 3 or 4.")
    elif isinstance(color, str):
        return QColor(color)
    else:
        raise ValueError("Color must be a tuple or string.")

def drawColorRectangle(image, x1, y1, x2, y2, color):
    color_qcolor = color_to_qcolor(color)
    painter = QPainter(image)
    painter.setPen(color_qcolor)
    painter.setBrush(color_qcolor)
    rect = QRect(x1, y1, x2 - x1, y2 - y1)
    painter.drawRect(rect)
    painter.end()
    return True

def drawColorLine(image, x1, y1, x2, y2, width, color):
    width = max(1, int(width))
    color_qcolor = color_to_qcolor(color)
    painter = QPainter(image)
    pen = painter.pen()
    pen.setWidth(width)
    pen.setColor(color_qcolor)
    painter.setPen(pen)
    painter.drawLine(x1, y1, x2, y2)
    painter.end()
    return True

def drawColorText(image, size, x, y, text, color, ftype="ocrb"):
    text = str(text)
    color_qcolor = color_to_qcolor(color)
    painter = QPainter(image)
    painter.setPen(color_qcolor)

    # Load custom fonts
    font_db = QFontDatabase()

    font = None
    if ftype == "ocra":
        # Try loading the primary OCR A font
        font_id = font_db.addApplicationFont(fontpathocra)
        if font_id == -1:
            # If failed, try the alternate font
            font_id = font_db.addApplicationFont(fontpathocraalt)
    elif ftype == "ocrb":
        # Try loading the primary OCR B font
        font_id = font_db.addApplicationFont(fontpathocrb)
        if font_id == -1:
            # If failed, try the alternate font
            font_id = font_db.addApplicationFont(fontpathocrbalt)
    else:
        # Load the default font
        font_id = font_db.addApplicationFont(fontpath)

    if font_id != -1:
        # Get the family name and create the font
        font_family = font_db.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, size)
    else:
        # If custom font loading failed, use a default font
        font = QFont()
        font.setPointSize(size)

    painter.setFont(font)
    # Adjust the position to account for the text baseline
    painter.drawText(x, y + size, text)
    painter.end()
    return True

def drawColorRectangleAlt(image, x1, y1, x2, y2, color):
    color_qcolor = color_to_qcolor(color)
    painter = QPainter(image)
    painter.setPen(color_qcolor)
    rect = QRect(x1, y1, x2 - x1, y2 - y1)
    painter.drawRect(rect)
    painter.end()
    return True

def new_image_surface(sizex, sizey, bgcolor):
    bgcolor_qcolor = color_to_qcolor(bgcolor)
    image = QImage(sizex, sizey, QImage.Format_ARGB32)
    image.fill(bgcolor_qcolor)
    return image

def get_save_filename(outfile):
    valid_extensions = {"PNG", "JPEG", "JPG", "BMP", "GIF", "RAW"}
    if outfile is None or isinstance(outfile, bool):
        return outfile

    if hasattr(outfile, 'write') or outfile == "-":
        return (outfile, "PNG")  # Default to PNG

    if isinstance(outfile, str):
        outfile = outfile.strip()
        if outfile in ["-", ""]:
            return (outfile, "PNG")

        # Extract extension
        base, ext = os.path.splitext(outfile)
        if ext:
            ext = ext[1:].upper()
            if ext not in valid_extensions:
                ext = "PNG"
        else:
            # Check for custom format 'name:EXT'
            custom_match = re.match("^(?P<name>.+):(?P<ext>[A-Za-z]+)$", outfile)
            if custom_match:
                outfile = custom_match.group('name')
                ext = custom_match.group('ext').upper()
            else:
                ext = "PNG"

        return (outfile, ext)

    return False

def get_save_file(outfile):
    return get_save_filename(outfile)

def save_to_file(image, outfile, outfileext, imgcomment="barcode"):
    """
    Saves the QImage to a file, uploads it, or returns the image data.
    """
    if outfileext.upper() not in ["PNG", "JPEG", "JPG", "BMP", "GIF", "RAW"]:
        outfileext = "PNG"  # Default to PNG

    uploadfile = None
    outfiletovar = False

    if isinstance(outfile, str):
        if re.match("^(ftp|ftps|sftp):\\/\\/", outfile):
            uploadfile = outfile
            outfile = BytesIO()
        elif outfile == "-":
            outfiletovar = True
            outfile = BytesIO()
        else:
            # Save to file
            result = image.save(outfile, outfileext)
            if not result:
                raise IOError("Failed to save image to file.")
            return True
    elif outfile is None:
        # Return image data as bytes
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        image.save(buffer, outfileext)
        image_data = buffer.data().data()
        buffer.close()
        return image_data
    elif hasattr(outfile, 'write'):
        # outfile is a file-like object
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        image.save(buffer, outfileext)
        image_data = buffer.data().data()
        outfile.write(image_data)
        buffer.close()
        return True
    else:
        # Unsupported outfile type
        raise ValueError("Invalid outfile type")

    if uploadfile:
        # Upload the image data
        outfile.seek(0, 0)
        upload_file_to_internet_file(outfile, uploadfile)
        outfile.close()
        return True
    elif outfiletovar:
        # Return image data as bytes
        outfile.seek(0, 0)
        outbyte = outfile.read()
        outfile.close()
        return outbyte

    return True

def save_to_filename(image, outfile, imgcomment="barcode"):
    if outfile is None:
        outfile = None
        outfileext = None
    else:
        outfile_info = get_save_filename(outfile)
        if isinstance(outfile_info, tuple) or isinstance(outfile_info, list):
            outfile = outfile_info[0]
            outfileext = outfile_info[1]
        else:
            outfile = None
            outfileext = None
    if outfileext is None:
        outfileext = "PNG"  # Default to PNG
    result = save_to_file(image, outfile, outfileext, imgcomment)
    return result
