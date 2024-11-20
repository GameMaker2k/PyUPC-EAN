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

# Enhanced argument parser
parser = argparse.ArgumentParser(
    description="PyUPC-EAN Barcode Generator Web Server using CherryPy."
)
parser.add_argument(
    "--port", "-p", default=8080, type=int,
    help="Port number to use for the server. Default is 8080."
)
parser.add_argument(
    "--host", "-H", default="127.0.0.1",
    help="Host name or IP address to use for the server. Default is 127.0.0.1."
)
parser.add_argument(
    "--timeout", "-t", default=6000, type=int,
    help="Response timeout in seconds. Default is 6000."
)
parser.add_argument(
    "--gzip", "-g", action="store_true",
    help="Enable gzip compression for HTTP responses."
)
parser.add_argument(
    "--log-access", "-a", default="./access.log",
    help="File to store access logs. Default is './access.log'."
)
parser.add_argument(
    "--log-error", "-e", default="./error.log",
    help="File to store error logs. Default is './error.log'."
)
parser.add_argument(
    "--environment", "-E", default="production",
    choices=["production", "development"],
    help="Set the server environment mode. Default is 'production'."
)
parser.add_argument(
    "--verbose", "-v", action="store_true",
    help="Enable verbose logging to the terminal."
)
parser.add_argument(
    "--debug", "-d", action="store_true",
    help="Enable debug mode for troubleshooting."
)
parser.add_argument(
    "--output-dir", "-o", default=tempfile.gettempdir(),
    help="Directory to store temporary output files. Default is the system's temp directory."
)
parser.add_argument(
    "--max-size", "-m", type=int, default=5,
    help="Maximum size multiplier for barcode generation (e.g., 5x). Default is 5."
)
parser.add_argument(
    "--default-format", "-f", default="png",
    choices=supported_image_formats,
    help="Default output image format if none is specified. Default is 'png'."
)
parser.add_argument(
    "--rotate-only", "-r", action="store_true",
    help="Restrict barcode generation to only apply rotation."
)

getargs = parser.parse_args()

# Set server configurations
port = getargs.port
host = getargs.host
timeout = getargs.timeout
accesslog = getargs.log_access
errorlog = getargs.log_error
serv_environ = getargs.environment
debug_mode = getargs.debug
output_dir = getargs.output_dir
max_size = getargs.max_size
default_format = getargs.default_format
rotate_only = getargs.rotate_only

# Generate dynamic options for the form
size_options = "".join(
    '<option value="{0}">{0}x</option>'.format(i) for i in range(1, max_size + 1)
)
image_type_options = "".join(
    '<option value="{0}">{1}</option>'.format(fmt, fmt.upper()) for fmt in supported_image_formats
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
            <input type="number" id="rotate" name="rotate" value="0" {1}>
            <label for="imgtype">Select Image Type:</label>
            <select id="imgtype" name="imgtype">
                {2}
            </select>
            <button type="submit">Generate Barcode</button>
        </form>
    </div>
</body>
</html>
""".format(size_options, 'readonly' if rotate_only else '', image_type_options)

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
            raise cherrypy.HTTPRedirect("/", 303)

        # Default values and validations
        bcsize = int(bcsize) if bcsize.isdigit() and int(bcsize) <= max_size else 1
        bcrotate = int(bcrotate) if bcrotate.isdigit() else 0

        # Restrict to rotation-only mode if enabled
        if rotate_only and bcrotate == 0:
            raise cherrypy.HTTPRedirect("/", 303)

        # Check if barcode type is supported
        if bctype not in upcean.support.supported_barcodes("tuple"):
            raise cherrypy.HTTPRedirect("/", 303)

        # Check if image format is supported
        if imgtype.lower() not in supported_image_formats:
            raise cherrypy.HTTPRedirect("/", 303)

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
