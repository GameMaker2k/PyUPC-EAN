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

    $FileInfo: predraw.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

version = (1, 4, 3, 'release')
VERSION = "1.4.3"

try:
    # For Python 2 and 3 compatibility
    from xml.dom.minidom import Document
except ImportError:
    from xml.dom.minidom import Document

import base64
import os
import re

# Import 'open' from 'io' to support 'encoding' parameter in both Python 2 and Python 3
from io import open

# Import the download functions from upcean.xml.downloader
from upcean.xml.downloader import (
    download_file_from_internet_file,
    download_file_from_internet_string
)

class BaseElement(object):
    """
    Base class for all SVG elements.
    """
    def __init__(self, tag_name, **kwargs):
        self.tag_name = tag_name
        self.kwargs = kwargs
        self.children = []
        self._attribs = {}  # Renamed from 'attribs' to '_attribs'
        # Set attributes from kwargs
        for k, v in kwargs.items():
            self._attribs[k.replace('_', '-')] = v

    def set_iri(self, name, value):
        """
        Set an Internationalized Resource Identifier (IRI) attribute.
        """
        self._attribs[name.replace('_', '-')] = value

    def get_iri(self, name):
        """
        Get an IRI attribute.
        """
        return self._attribs.get(name.replace('_', '-'))

    def update(self, kwargs):
        """
        Update attributes.
        """
        for k, v in kwargs.items():
            self._attribs[k.replace('_', '-')] = v

    def set_desc(self, desc):
        """
        Set a description for the element.
        """
        desc_el = Description(desc)
        self.add(desc_el)

    def set_title(self, title):
        """
        Set a title for the element.
        """
        title_el = Title(title)
        self.add(title_el)

    def set_metadata(self, metadata):
        """
        Set metadata for the element.
        """
        metadata_el = Metadata(metadata)
        self.add(metadata_el)

    def add(self, element):
        """
        Add a child element.
        """
        # Default behavior; overridden in container classes
        self.children.append(element)

    def elements(self, descend=False):
        """
        Iterate over child elements.
        """
        for child in self.children:
            yield child
            if descend and hasattr(child, 'elements'):
                for subchild in child.elements(descend=True):
                    yield subchild

    def to_xml(self, doc):
        """
        Convert the element to an XML element.
        """
        el = doc.createElement(self.tag_name)
        for k, v in self._attribs.items():
            el.setAttribute(k, str(v))
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

    def __str__(self):
        return "<{}>".format(self.tag_name)

class Drawing(BaseElement):
    def __init__(self, filename=None, size=('100%', '100%'), profile='full', **kwargs):
        super(Drawing, self).__init__('svg', **kwargs)
        self.filename = filename
        self._size = size
        self.profile = profile
        self.doc = Document()
        self.root = self.to_xml(self.doc)
        self.root.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self.root.setAttribute('version', '1.1')
        self.set_size(size)
        self._elements = []
        self._element_ids = set()  # To track added elements
        self.defs = Defs()
        self.doc.appendChild(self.root)

    @property
    def size(self):
        return self._size

    @property
    def elements(self):
        return self._elements

    @property
    def attribs(self):
        return self.root.attributes

    @property
    def width(self):
        return self.attribs.get('width')

    @property
    def height(self):
        return self.attribs.get('height')

    @property
    def viewbox(self):
        return self.attribs.get('viewBox')

    def set_size(self, size):
        self._size = size
        self._attribs['width'] = str(size[0])
        self._attribs['height'] = str(size[1])
        self.root.setAttribute('width', str(size[0]))
        self.root.setAttribute('height', str(size[1]))

    def set_profile(self, name):
        self.profile = name

    def set_viewport(self, width, height):
        self._attribs['width'] = str(width)
        self._attribs['height'] = str(height)
        self.root.setAttribute('width', str(width))
        self.root.setAttribute('height', str(height))

    def set_viewbox(self, minx, miny, width, height, aspectratio='none'):
        viewbox_value = '{} {} {} {}'.format(minx, miny, width, height)
        self._attribs['viewBox'] = viewbox_value
        self._attribs['preserveAspectRatio'] = aspectratio
        self.root.setAttribute('viewBox', viewbox_value)
        self.root.setAttribute('preserveAspectRatio', aspectratio)

    def set_desc(self, desc):
        desc_el = Description(desc)
        self.add(desc_el)

    def set_title(self, title):
        title_el = Title(title)
        self.add(title_el)

    def set_metadata(self, metadata_content):
        metadata_el = Metadata(metadata_content)
        self.add(metadata_el)

    def add_stylesheet(self, href, title=None, alternate='no', media='screen'):
        # Check if stylesheet is already added
        key = ('stylesheet', href)
        if key in self.defs.child_elements:
            return  # Stylesheet already added

        style_el = ProcessingInstruction(
            'xml-stylesheet',
            'type="text/css" href="{}" title="{}" alternate="{}" media="{}"'.format(
                href, title or '', alternate, media))
        self.doc.insertBefore(style_el.to_xml(self.doc), self.root)
        # Record in defs to prevent duplicates
        self.defs.child_elements[key] = style_el

    def add_external_stylesheet(self, href):
        # Check if external stylesheet is already added
        key = ('external_stylesheet', href)
        if key in self.defs.child_elements:
            return  # Stylesheet already added

        link_el = BaseElement('link', rel='stylesheet', href=href)
        self.root.appendChild(link_el.to_xml(self.doc))
        # Record in defs to prevent duplicates
        self.defs.child_elements[key] = link_el

    def embed_stylesheet(self, css):
        # Check if the stylesheet has already been embedded
        key = ('embedded_stylesheet', css.strip())
        if key in self.defs.child_elements:
            return  # Stylesheet already embedded

        style_el = Style(css)
        self.defs.add(style_el, key=key)

    def embed_font(self, name, font_file):
        # Check if the font has already been embedded
        font_key = ('font', name)
        if font_key in self.defs.child_elements:
            return  # Font already embedded

        # Read the font file
        with open(font_file, 'rb') as f:
            font_data = f.read()

        # Encode the font data in base64
        font_base64 = base64.b64encode(font_data).decode('utf-8')

        # Determine the font format based on the file extension
        ext = os.path.splitext(font_file)[1].lower()
        if ext == '.ttf':
            font_format = 'truetype'
        elif ext == '.otf':
            font_format = 'opentype'
        else:
            raise ValueError("Unsupported font format.")

        # Create the @font-face CSS
        font_face = """
        @font-face {{
            font-family: '{0}';
            src: url(data:font/{1};base64,{2}) format('{1}');
            font-weight: normal;
            font-style: normal;
        }}
        """.format(name, font_format, font_base64)

        # Add the style to the SVG
        style_element = self.style(font_face)
        self.defs.add(style_element, key=font_key)

    def embed_google_web_font(self, name, uri=None):
        """
        Embeds a Google Web Font into the SVG.

        Parameters:
        - name: The name of the font family.
        - uri: The URI of the font CSS. If None, a default URI is constructed.
        """
        # Check if the font has already been embedded
        font_key = ('google_font', name)
        if font_key in self.defs.child_elements:
            return  # Font already embedded

        # If no URI is provided, construct the default Google Fonts URI
        if uri is None:
            # Replace spaces with '+', encode special characters
            font_name_encoded = re.sub(r'\s+', '+', name)
            uri = "https://fonts.googleapis.com/css?family={}".format(font_name_encoded)

        # Fetch the CSS from the URI
        try:
            # Use the provided function to download the CSS as bytes
            css_bytes = download_file_from_internet_string(uri)
            if not css_bytes:
                raise Exception("Failed to fetch Google Font CSS.")
            css = css_bytes.decode('utf-8')
        except Exception as e:
            raise Exception("Error fetching Google Font: {}".format(e))

        # Modify the CSS to embed fonts as data URIs
        css = self._embed_font_data_in_css(css)

        # Add the style to the SVG
        style_element = self.style(css)
        self.defs.add(style_element, key=font_key)

    def _embed_font_data_in_css(self, css):
        """
        Helper function to modify CSS by embedding font files as data URIs.
        """
        # Find all URLs in the CSS
        url_pattern = re.compile(r'url\(([^)]+)\)')
        matches = url_pattern.findall(css)

        # For each URL, fetch the font file and encode it
        for match in matches:
            font_url = match.strip('\'"')
            # Fetch the font file
            try:
                # Use the provided function to download the font file as BytesIO
                font_file_obj = download_file_from_internet_file(font_url)
                if not font_file_obj:
                    continue  # Skip if failed to fetch
                # Read the font data from the BytesIO object
                font_data = font_file_obj.read()
                # Determine the font format
                if '.woff2' in font_url:
                    font_format = 'woff2'
                elif '.woff' in font_url:
                    font_format = 'woff'
                elif '.ttf' in font_url:
                    font_format = 'truetype'
                elif '.otf' in font_url:
                    font_format = 'opentype'
                else:
                    continue  # Unsupported format
                # Encode font data in base64
                font_base64 = base64.b64encode(font_data).decode('utf-8')
                # Create data URI
                data_uri = 'url(data:font/{0};base64,{1}) format(\'{0}\')'.format(font_format, font_base64)
                # Replace the URL in CSS
                css = css.replace('url({})'.format(match), data_uri)
            except Exception as e:
                print("Error embedding font from URL '{}': {}".format(font_url, e))
                continue  # Skip on any error

        return css

    def add(self, element):
        """
        Add an element to the drawing, ensuring it's not added multiple times.
        """
        element_id = getattr(element, 'id', id(element))
        if element_id in self._element_ids:
            return  # Element already added
        self._element_ids.add(element_id)
        self._elements.append(element)

    def elements(self, descend=False):
        for element in self._elements:
            yield element
            if descend and hasattr(element, 'elements'):
                for subelement in element.elements(descend=True):
                    yield subelement

    def get_xml(self):
        return self.root

    def tostring(self, pretty=False, indent=2):
        # Append defs if it has children and not already appended
        if self.defs.children and not any(child.tagName == 'defs' for child in self.root.childNodes):
            self.root.insertBefore(self.defs.to_xml(self.doc), self.root.firstChild)
        # Append other elements
        for element in self._elements:
            self.root.appendChild(element.to_xml(self.doc))
        if pretty:
            xml_str = self.doc.toprettyxml(indent=" " * indent)
        else:
            xml_str = self.doc.toxml()
        return xml_str

    def save(self, pretty=False, indent=2, encoding='utf-8'):
        svg_string = self.tostring(pretty=pretty, indent=indent)
        if self.filename:
            with open(self.filename, 'w', encoding=encoding) as f:
                f.write(svg_string)
        else:
            return svg_string

    def saveas(self, filename, pretty=False, indent=2, encoding='utf-8'):
        self.filename = filename
        self.save(pretty=pretty, indent=indent, encoding=encoding)

    def write(self, fileobj, pretty=False, indent=2, encoding='utf-8'):
        """
        Write XML string to a file-like object.

        Parameters:
        - fileobj: a file-like object with a write method.
        - pretty: True for pretty-printed output.
        - indent: indentation level for pretty-printed output.
        - encoding: character encoding for the output.
        """
        svg_string = self.tostring(pretty=pretty, indent=indent)
        if isinstance(svg_string, str):
            svg_string = svg_string.encode(encoding)
        fileobj.write(svg_string)

    # Factory methods to create SVG elements
    def line(self, start, end, **kwargs):
        return Line(start, end, **kwargs)

    def circle(self, center, r, **kwargs):
        return Circle(center, r, **kwargs)

    def rect(self, insert, size, **kwargs):
        return Rect(insert, size, **kwargs)

    def text(self, text_content, insert, **kwargs):
        return Text(text_content, insert, **kwargs)

    def path(self, d='', **kwargs):
        return Path(d, **kwargs)

    def polygon(self, points, **kwargs):
        return Polygon(points, **kwargs)

    def polyline(self, points, **kwargs):
        return Polyline(points, **kwargs)

    def ellipse(self, center, r, **kwargs):
        return Ellipse(center, r, **kwargs)

    def g(self, **kwargs):
        return Group(**kwargs)

    def style(self, css_text):
        return Style(css_text)

    def linearGradient(self, **kwargs):
        return LinearGradient(**kwargs)

    def radialGradient(self, **kwargs):
        return RadialGradient(**kwargs)

    def pattern(self, **kwargs):
        return Pattern(**kwargs)

    def stop(self, offset, **kwargs):
        return Stop(offset, **kwargs)

class ProcessingInstruction(object):
    """
    Represents an XML processing instruction.
    """
    def __init__(self, target, data):
        self.target = target
        self.data = data

    def to_xml(self, doc):
        return doc.createProcessingInstruction(self.target, self.data)

class Description(BaseElement):
    def __init__(self, desc):
        super(Description, self).__init__('desc')
        self.desc = desc

    def to_xml(self, doc):
        el = super(Description, self).to_xml(doc)
        text_node = doc.createTextNode(self.desc)
        el.appendChild(text_node)
        return el

class Title(BaseElement):
    def __init__(self, title):
        super(Title, self).__init__('title')
        self.title = title

    def to_xml(self, doc):
        el = super(Title, self).to_xml(doc)
        text_node = doc.createTextNode(self.title)
        el.appendChild(text_node)
        return el

class Metadata(BaseElement):
    def __init__(self, metadata):
        super(Metadata, self).__init__('metadata')
        self.metadata = metadata

    def to_xml(self, doc):
        el = super(Metadata, self).to_xml(doc)
        text_node = doc.createTextNode(self.metadata)
        el.appendChild(text_node)
        return el

class Defs(BaseElement):
    def __init__(self):
        super(Defs, self).__init__('defs')
        self.child_elements = {}

    def add(self, element, key=None):
        if key is None:
            key = ('type', str(element))
        if key in self.child_elements:
            return
        else:
            self.child_elements[key] = element
            self.children.append(element)

class Group(BaseElement):
    def __init__(self, **kwargs):
        super(Group, self).__init__('g', **kwargs)
        self._element_ids = set()

    def add(self, element):
        element_id = getattr(element, 'id', id(element))
        if element_id in self._element_ids:
            return  # Element already added
        self._element_ids.add(element_id)
        self.children.append(element)

# Element classes remain the same, inheriting from BaseElement
class Line(BaseElement):
    def __init__(self, start, end, **kwargs):
        super(Line, self).__init__('line', **kwargs)
        self._attribs['x1'] = start[0]
        self._attribs['y1'] = start[1]
        self._attribs['x2'] = end[0]
        self._attribs['y2'] = end[1]

class Circle(BaseElement):
    def __init__(self, center, r, **kwargs):
        super(Circle, self).__init__('circle', **kwargs)
        self._attribs['cx'] = center[0]
        self._attribs['cy'] = center[1]
        self._attribs['r'] = r

class Rect(BaseElement):
    def __init__(self, insert, size, **kwargs):
        super(Rect, self).__init__('rect', **kwargs)
        self._attribs['x'] = insert[0]
        self._attribs['y'] = insert[1]
        self._attribs['width'] = size[0]
        self._attribs['height'] = size[1]

class Text(BaseElement):
    def __init__(self, text_content, insert, **kwargs):
        super(Text, self).__init__('text', **kwargs)
        self.text_content = text_content
        self._attribs['x'] = insert[0]
        self._attribs['y'] = insert[1]

    def to_xml(self, doc):
        el = super(Text, self).to_xml(doc)
        text_node = doc.createTextNode(self.text_content)
        el.appendChild(text_node)
        return el

class Path(BaseElement):
    def __init__(self, d='', **kwargs):
        super(Path, self).__init__('path', **kwargs)
        self._attribs['d'] = d

class Polygon(BaseElement):
    def __init__(self, points, **kwargs):
        super(Polygon, self).__init__('polygon', **kwargs)
        points_str = ' '.join(['{},{}'.format(p[0], p[1]) for p in points])
        self._attribs['points'] = points_str

class Polyline(BaseElement):
    def __init__(self, points, **kwargs):
        super(Polyline, self).__init__('polyline', **kwargs)
        points_str = ' '.join(['{},{}'.format(p[0], p[1]) for p in points])
        self._attribs['points'] = points_str

class Ellipse(BaseElement):
    def __init__(self, center, r, **kwargs):
        super(Ellipse, self).__init__('ellipse', **kwargs)
        self._attribs['cx'] = center[0]
        self._attribs['cy'] = center[1]
        self._attribs['rx'] = r[0]
        self._attribs['ry'] = r[1]

class Style(BaseElement):
    def __init__(self, css_text):
        super(Style, self).__init__('style', type='text/css')
        self.css_text = css_text

    def to_xml(self, doc):
        el = super(Style, self).to_xml(doc)
        # Wrap the CSS content in a CDATA section
        cdata_section = doc.createCDATASection(self.css_text)
        el.appendChild(cdata_section)
        return el

class LinearGradient(BaseElement):
    def __init__(self, **kwargs):
        super(LinearGradient, self).__init__('linearGradient', **kwargs)

class RadialGradient(BaseElement):
    def __init__(self, **kwargs):
        super(RadialGradient, self).__init__('radialGradient', **kwargs)

class Stop(BaseElement):
    def __init__(self, offset, **kwargs):
        super(Stop, self).__init__('stop', **kwargs)
        self._attribs['offset'] = offset

class Pattern(BaseElement):
    def __init__(self, **kwargs):
        super(Pattern, self).__init__('pattern', **kwargs)

def rgb(r, g, b, mode='%'):
    if mode == '%':
        return 'rgb({}%, {}%, {}%)'.format(r, g, b)
    else:
        return 'rgb({}, {}, {})'.format(r, g, b)
