# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2011-2025 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: svgcreate.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

import sys
import base64
import os
import re

try:
    from xml.dom.minidom import Document
except ImportError:
    # Very old/odd environments only; keeps the intent explicit
    from xml.dom.minidom import Document

# Import 'open' from 'io' to support 'encoding' parameter in both Python 2 and Python 3
from io import open

# Optional dependency: used only for web font embedding
try:
    from upcean.downloader import (
        download_file_from_internet_file,
        download_file_from_internet_string
    )
except ImportError:
    download_file_from_internet_file = None
    download_file_from_internet_string = None

version = (1, 4, 3, 'release')
VERSION = "1.4.3"


def _ensure_text(s, encoding='utf-8', errors='strict'):
    """
    Return a unicode/text string on both Py2 and Py3.
    - Py3: str
    - Py2: unicode
    """
    if sys.version_info[0] < 3:
        # Py2
        try:
            text_type = unicode  # noqa: F821
        except NameError:
            text_type = str
        if isinstance(s, text_type):
            return s
        # If it's bytes/str in Py2, decode
        try:
            return s.decode(encoding, errors)
        except Exception:
            return text_type(s)
    else:
        # Py3
        if isinstance(s, str):
            return s
        if isinstance(s, (bytes, bytearray)):
            return s.decode(encoding, errors)
        return str(s)


class BaseElement(object):
    """
    Base class for all SVG elements.
    """
    def __init__(self, tag_name, **kwargs):
        self.tag_name = tag_name
        self.kwargs = kwargs
        self.children = []
        self._attribs = {}
        for k, v in kwargs.items():
            self._attribs[k.replace('_', '-')] = v

    def set_iri(self, name, value):
        self._attribs[name.replace('_', '-')] = value

    def get_iri(self, name):
        return self._attribs.get(name.replace('_', '-'))

    def update(self, kwargs):
        for k, v in kwargs.items():
            self._attribs[k.replace('_', '-')] = v

    def set_desc(self, desc):
        self.add(Description(desc))

    def set_title(self, title):
        self.add(Title(title))

    def set_metadata(self, metadata):
        self.add(Metadata(metadata))

    def add(self, element):
        self.children.append(element)

    def elements(self, descend=False):
        for child in self.children:
            yield child
            if descend and hasattr(child, 'elements'):
                for subchild in child.elements(descend=True):
                    yield subchild

    def to_xml(self, doc):
        el = doc.createElement(self.tag_name)
        for k, v in self._attribs.items():
            # Use robust text conversion to avoid Py2 UnicodeEncodeError
            el.setAttribute(k, _ensure_text(v))
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

    def __str__(self):
        s = "<{0}>".format(self.tag_name)
        if sys.version_info[0] < 3:
            return s.encode('utf-8')
        return s


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
        self._element_ids = set()
        self.defs = Defs()

        self.doc.appendChild(self.root)

    @property
    def size(self):
        return self._size

    @property
    def elements_list(self):
        # avoid name collision with elements() method
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
        self._attribs['width'] = _ensure_text(size[0])
        self._attribs['height'] = _ensure_text(size[1])
        self.root.setAttribute('width', _ensure_text(size[0]))
        self.root.setAttribute('height', _ensure_text(size[1]))

    def set_profile(self, name):
        self.profile = name

    def set_viewport(self, width, height):
        self._attribs['width'] = _ensure_text(width)
        self._attribs['height'] = _ensure_text(height)
        self.root.setAttribute('width', _ensure_text(width))
        self.root.setAttribute('height', _ensure_text(height))

    def set_viewbox(self, minx, miny, width, height, aspectratio='none'):
        viewbox_value = '{0} {1} {2} {3}'.format(minx, miny, width, height)
        self._attribs['viewBox'] = viewbox_value
        self._attribs['preserveAspectRatio'] = aspectratio
        self.root.setAttribute('viewBox', _ensure_text(viewbox_value))
        self.root.setAttribute('preserveAspectRatio', _ensure_text(aspectratio))

    def set_desc(self, desc):
        self.add(Description(desc))

    def set_title(self, title):
        self.add(Title(title))

    def set_metadata(self, metadata_content):
        self.add(Metadata(metadata_content))

    def add_stylesheet(self, href, title=None, alternate='no', media='screen'):
        key = ('stylesheet', href)
        if key in self.defs.child_elements:
            return

        style_el = ProcessingInstruction(
            'xml-stylesheet',
            'type="text/css" href="{0}" title="{1}" alternate="{2}" media="{3}"'.format(
                href, title or '', alternate, media
            )
        )
        self.doc.insertBefore(style_el.to_xml(self.doc), self.root)
        self.defs.child_elements[key] = style_el

    def add_external_stylesheet(self, href):
        key = ('external_stylesheet', href)
        if key in self.defs.child_elements:
            return

        link_el = BaseElement('link', rel='stylesheet', href=href)
        self.root.appendChild(link_el.to_xml(self.doc))
        self.defs.child_elements[key] = link_el

    def embed_stylesheet(self, css):
        key = ('embedded_stylesheet', _ensure_text(css).strip())
        if key in self.defs.child_elements:
            return
        style_el = Style(css)
        self.defs.add(style_el, key=key)

    def embed_font(self, name, font_file):
        font_key = ('font', name)
        if font_key in self.defs.child_elements:
            return

        with open(font_file, 'rb') as f:
            font_data = f.read()

        font_base64 = base64.b64encode(font_data).decode('ascii')

        ext = os.path.splitext(font_file)[1].lower()
        if ext == '.ttf':
            font_format = 'truetype'
        elif ext == '.otf':
            font_format = 'opentype'
        else:
            raise ValueError("Unsupported font format.")

        font_face = """
        @font-face {{
            font-family: '{0}';
            src: url(data:font/{1};base64,{2}) format('{1}');
            font-weight: normal;
            font-style: normal;
        }}
        """.format(name, font_format, font_base64)

        style_element = self.style(font_face)
        self.defs.add(style_element, key=font_key)

    def embed_google_web_font(self, name, uri=None):
        """
        Embeds a Google Web Font into the SVG (as data URIs).

        Requires optional dependency: upcean (upcean.downloader).
        """
        if download_file_from_internet_string is None or download_file_from_internet_file is None:
            raise ImportError("upcean is required for embed_google_web_font()")

        font_key = ('google_font', name)
        if font_key in self.defs.child_elements:
            return

        if uri is None:
            font_name_encoded = re.sub(r'\s+', '+', name)
            uri = "https://fonts.googleapis.com/css?family={0}".format(font_name_encoded)

        try:
            css_bytes = download_file_from_internet_string(uri)
            if not css_bytes:
                raise Exception("Failed to fetch Google Font CSS.")
            css = _ensure_text(css_bytes)
        except Exception as e:
            raise Exception("Error fetching Google Font: {0}".format(e))

        css = self._embed_font_data_in_css(css)

        style_element = self.style(css)
        self.defs.add(style_element, key=font_key)

    def _embed_font_data_in_css(self, css):
        if download_file_from_internet_file is None:
            raise ImportError("upcean is required for _embed_font_data_in_css()")

        url_pattern = re.compile(r'url\(([^)]+)\)')
        matches = url_pattern.findall(css)

        for match in matches:
            font_url = match.strip('\'"')
            try:
                font_file_obj = download_file_from_internet_file(font_url)
                if not font_file_obj:
                    continue

                font_data = font_file_obj.read()

                if '.woff2' in font_url:
                    font_format = 'woff2'
                elif '.woff' in font_url:
                    font_format = 'woff'
                elif '.ttf' in font_url:
                    font_format = 'truetype'
                elif '.otf' in font_url:
                    font_format = 'opentype'
                else:
                    continue

                font_base64 = base64.b64encode(font_data).decode('ascii')
                data_uri = "url(data:font/{0};base64,{1}) format('{0}')".format(font_format, font_base64)

                css = css.replace('url({0})'.format(match), data_uri)
            except Exception as e:
                print("Error embedding font from URL '{0}': {1}".format(font_url, e))
                continue

        return css

    def add(self, element):
        """
        Add an element to the drawing, ensuring it's not added multiple times.
        """
        element_id = getattr(element, 'id', id(element))
        if element_id in self._element_ids:
            return
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
        # Append defs once
        if self.defs.children and not any(
            getattr(child, 'tagName', None) == 'defs' for child in self.root.childNodes
        ):
            self.root.insertBefore(self.defs.to_xml(self.doc), self.root.firstChild)

        # Append other elements (NOTE: if tostring() is called multiple times, this will append again)
        # Keeping your original behavior; if you want idempotent tostring(), I can adjust it.
        for element in self._elements:
            self.root.appendChild(element.to_xml(self.doc))

        if pretty:
            xml_out = self.doc.toprettyxml(indent=" " * indent)
        else:
            xml_out = self.doc.toxml()

        # Normalize to text/unicode for both Py2/3 callers
        return _ensure_text(xml_out)

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
        Write XML to a file-like object.
        Works with both:
          - text mode streams (expects text)
          - binary mode streams (expects bytes)
        """
        svg_string = self.tostring(pretty=pretty, indent=indent)

        # Try text first
        try:
            fileobj.write(svg_string)
            return
        except TypeError:
            pass

        # Then bytes
        if isinstance(svg_string, (bytes, bytearray)):
            fileobj.write(svg_string)
        else:
            fileobj.write(svg_string.encode(encoding))

    # Factory methods to create SVG elements
    def line(self, start, end, **kwargs): return Line(start, end, **kwargs)
    def circle(self, center, r, **kwargs): return Circle(center, r, **kwargs)
    def rect(self, insert, size, **kwargs): return Rect(insert, size, **kwargs)
    def text(self, text_content, insert, **kwargs): return Text(text_content, insert, **kwargs)
    def path(self, d='', **kwargs): return Path(d, **kwargs)
    def polygon(self, points, **kwargs): return Polygon(points, **kwargs)
    def polyline(self, points, **kwargs): return Polyline(points, **kwargs)
    def ellipse(self, center, r, **kwargs): return Ellipse(center, r, **kwargs)
    def g(self, **kwargs): return Group(**kwargs)
    def style(self, css_text): return Style(css_text)
    def linearGradient(self, **kwargs): return LinearGradient(**kwargs)
    def radialGradient(self, **kwargs): return RadialGradient(**kwargs)
    def pattern(self, **kwargs): return Pattern(**kwargs)
    def stop(self, offset, **kwargs): return Stop(offset, **kwargs)


class ProcessingInstruction(object):
    """
    Represents an XML processing instruction.
    """
    def __init__(self, target, data):
        self.target = target
        self.data = data

    def to_xml(self, doc):
        return doc.createProcessingInstruction(self.target, _ensure_text(self.data))


class Description(BaseElement):
    def __init__(self, desc):
        super(Description, self).__init__('desc')
        self.desc = _ensure_text(desc)

    def to_xml(self, doc):
        el = super(Description, self).to_xml(doc)
        el.appendChild(doc.createTextNode(self.desc))
        return el


class Title(BaseElement):
    def __init__(self, title):
        super(Title, self).__init__('title')
        self.title = _ensure_text(title)

    def to_xml(self, doc):
        el = super(Title, self).to_xml(doc)
        el.appendChild(doc.createTextNode(self.title))
        return el


class Metadata(BaseElement):
    def __init__(self, metadata):
        super(Metadata, self).__init__('metadata')
        self.metadata = _ensure_text(metadata)

    def to_xml(self, doc):
        el = super(Metadata, self).to_xml(doc)
        el.appendChild(doc.createTextNode(self.metadata))
        return el


class Defs(BaseElement):
    def __init__(self):
        super(Defs, self).__init__('defs')
        self.child_elements = {}

    def add(self, element, key=None):
        if key is None:
            key = ('type', _ensure_text(str(element)))
        if key in self.child_elements:
            return
        self.child_elements[key] = element
        self.children.append(element)


class Group(BaseElement):
    def __init__(self, **kwargs):
        super(Group, self).__init__('g', **kwargs)
        self._element_ids = set()

    def add(self, element):
        element_id = getattr(element, 'id', id(element))
        if element_id in self._element_ids:
            return
        self._element_ids.add(element_id)
        self.children.append(element)


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
        self.text_content = _ensure_text(text_content)
        self._attribs['x'] = insert[0]
        self._attribs['y'] = insert[1]

    def to_xml(self, doc):
        el = super(Text, self).to_xml(doc)
        el.appendChild(doc.createTextNode(self.text_content))
        return el


class Path(BaseElement):
    def __init__(self, d='', **kwargs):
        super(Path, self).__init__('path', **kwargs)
        self._attribs['d'] = d


class Polygon(BaseElement):
    def __init__(self, points, **kwargs):
        super(Polygon, self).__init__('polygon', **kwargs)
        points_str = ' '.join(['{0},{1}'.format(p[0], p[1]) for p in points])
        self._attribs['points'] = points_str


class Polyline(BaseElement):
    def __init__(self, points, **kwargs):
        super(Polyline, self).__init__('polyline', **kwargs)
        points_str = ' '.join(['{0},{1}'.format(p[0], p[1]) for p in points])
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
        self.css_text = _ensure_text(css_text)

    def to_xml(self, doc):
        el = super(Style, self).to_xml(doc)
        el.appendChild(doc.createCDATASection(self.css_text))
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
        return 'rgb({0}%, {1}%, {2}%)'.format(r, g, b)
    return 'rgb({0}, {1}, {2})'.format(r, g, b)
