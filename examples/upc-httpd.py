#!/usr/bin/env python
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
    $FileInfo: upc-httpd.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1  - Author: cooldude2k $
'''

from __future__ import print_function, unicode_literals
import tempfile
import uuid
import os
import sys
import cherrypy
import upcean
import argparse
from PIL import Image

# Handle StringIO for Python 2 and 3
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

# Dynamically gather supported image types
supported_image_formats = [
    ext.lstrip('.') for ext, fmt in Image.registered_extensions().items()
]

parser = argparse.ArgumentParser(
    description="A web server that draws barcodes with PyUPC-EAN powered by CherryPy web server."
)
parser.add_argument("--port", default=8080, help="Port number to use for the server.")
parser.add_argument("--host", default="127.0.0.1", help="Host name to use for the server.")
parser.add_argument("--verbose", help="Show log on terminal screen.", action="store_true")
parser.add_argument("--gzip", help="Enable gzip HTTP requests.", action="store_true")
parser.add_argument("--accesslog", help="Location to store access log file.")
parser.add_argument("--errorlog", help="Location to store error log file.")
parser.add_argument("--timeout", default=6000, help="Response timeout in seconds.")
parser.add_argument("--environment", default="production", help="Server environment (production/development).")

getargs = parser.parse_args()

# Set server configurations
port = int(getargs.port)
host = getargs.host
timeout = int(getargs.timeout)
accesslog = getargs.accesslog or "./access.log"
errorlog = getargs.errorlog or "./errors.log"
serv_environ = getargs.environment

# Generate dynamic options for the form
image_type_options = "".join(
    '<option value="{0}">{1}</option>'.format(fmt, fmt.upper()) for fmt in supported_image_formats
)
size_options = "".join(
    '<option value="{0}">{0}x</option>'.format(i) for i in range(1, 6)
)

IndexHTMLCode = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Barcode Generator</title>
    <meta charset="UTF-8">
    <meta name="author" content="Game Maker 2k">
    <meta name="keywords" content="barcode,upc,ean,stf,itf,itf14,upca,upce,ean2,ean5,ean8,ean13,code11,code39,code93,codabar,msi">
    <meta name="description" content="Barcode Generator with PyUPC-EAN">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 50px auto;
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            color: #343a40;
        }}
        form {{
            margin-top: 20px;
        }}
        label {{
            font-weight: bold;
            margin-top: 10px;
            display: block;
        }}
        input, select, button {{
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        button {{
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 18px;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
    </style>
    <script>
        function redirectToBarcode(event) {{
            event.preventDefault();
            var form = document.forms['upcean'];
            var url = '/generate/' + form.bctype.value + '/' + form.size.value + '/' + form.rotate.value + '/' + form.upc.value + '.' + form.imgtype.value;
            window.location.href = url;
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>Barcode Generator</h1>
        <form name="upcean" id="upcean" method="get" onsubmit="redirectToBarcode(event);">
            <label for="upc">Enter UPC/EAN:</label>
            <input type="text" id="upc" name="upc" placeholder="Enter barcode value" required>
            <label for="bctype">Select Barcode Type:</label>
            <select id="bctype" name="bctype">
                <option value="upca" selected>UPC-A</option>
                <option value="upce">UPC-E</option>
                <option value="ean13">EAN-13</option>
                <option value="ean8">EAN-8</option>
            </select>
            <label for="size">Select Size:</label>
            <select id="size" name="size">
                {0}
            </select>
            <label for="rotate">Rotate (degrees):</label>
            <input type="number" id="rotate" name="rotate" value="0">
            <label for="imgtype">Select Image Type:</label>
            <select id="imgtype" name="imgtype">
                {1}
            </select>
            <button type="submit">Generate Barcode</button>
        </form>
    </div>
</body>
</html>
""".format(size_options, image_type_options)

class GenerateIndexPage(object):
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        return IndexHTMLCode
    index.exposed = True

    def generate(self, bctype, bcsize, bcrotate, upc_imgtype):
        imgdata = BytesIO()

        # Split UPC and image type
        if '.' in upc_imgtype:
            upc, imgtype = upc_imgtype.rsplit('.', 1)
        else:
            raise ValueError("Invalid format: UPC and image type must be separated by a dot.")

        # Default values and validations
        bcsize = int(bcsize) if bcsize.isdigit() else 1
        bcrotate = int(bcrotate) if bcrotate.isdigit() else 0

        # Check if barcode type is supported
        if bctype not in upcean.support.supported_barcodes("tuple"):
            raise ValueError("Unsupported barcode type: {}".format(bctype))

        # Check if image format is supported
        if imgtype.lower() not in supported_image_formats:
            raise ValueError("Unsupported image format: {}".format(imgtype))

        # Generate the barcode
        imgdraw = upcean.encode.validate_draw_barcode(bctype, upc, bcsize)

        # Apply rotation if required
        if bcrotate != 0:
            imgdraw[1].rotate(bcrotate, Image.BICUBIC, expand=True).save(imgdata, imgtype.lower())
        else:
            imgdraw[1].save(imgdata, imgtype.lower())

        # Set content type based on file extension
        cherrypy.response.headers['Content-Type'] = Image.MIME.get(imgtype.lower(), 'image/png')
        imgdata.seek(0)
        return imgdata.read()
    generate.exposed = True


# CherryPy configuration
cherrypy.config.update({
    "environment": serv_environ,
    "log.error_file": errorlog,
    "log.access_file": accesslog,
    "log.screen": getargs.verbose,
    "tools.gzip.on": getargs.gzip,
    "server.socket_host": host,
    "server.socket_port": port,
    "response.timeout": timeout,
})

cherrypy.root = GenerateIndexPage()
cherrypy.quickstart(cherrypy.root)
