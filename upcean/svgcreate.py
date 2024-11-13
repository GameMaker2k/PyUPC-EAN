# -*- coding: utf-8 -*-
'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Cool Dude 2k
    Copyright 2011-2023 Game Maker 2k
    Copyright 2011-2023 Kazuki Przyborowski

    $FileInfo: svgcreate.py - Last Update: 04/27/2024 Ver. 1.0.0 - Author: ChatGPT $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes

version = (1, 4, 3, 'release')
VERSION = "1.4.3"

from io import open

try:
    # For Python 2 and 3 compatibility
    from xml.dom.minidom import Document
except ImportError:
    from xml.dom.minidom import Document

import base64
import os

class Drawing(object):
    def __init__(self, filename=None, size=('100%', '100%'), profile='full', **kwargs):
        self.filename = filename
        self._size = size
        self.profile = profile
        self.kwargs = kwargs
        self.doc = Document()
        self.root = self.doc.createElement('svg')
        self.root.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self.root.setAttribute('version', '1.1')
        self.root.setAttribute('width', str(size[0]))
        self.root.setAttribute('height', str(size[1]))
        for k, v in kwargs.items():
            self.root.setAttribute(k.replace('_', '-'), str(v))
        self._elements = []
        self.defs = Defs()  # Corrected: Now an attribute, not a method
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
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def add(self, element):
        self._elements.append(element)

    def set_desc(self, desc):
        desc_el = self.doc.createElement('desc')
        text_node = self.doc.createTextNode(desc)
        desc_el.appendChild(text_node)
        self.root.appendChild(desc_el)

    def set_title(self, title):
        title_el = self.doc.createElement('title')
        text_node = self.doc.createTextNode(title)
        title_el.appendChild(text_node)
        self.root.appendChild(title_el)

    def viewbox(self, minx, miny, width, height):
        viewbox_value = '{} {} {} {}'.format(minx, miny, width, height)
        self.root.setAttribute('viewBox', viewbox_value)

    def add_stylesheet(self, href, title=None, alternate='no', media='screen'):
        style_el = self.doc.createElement('style')
        style_el.setAttribute('type', 'text/css')
        style_el.setAttribute('media', media)
        if title:
            style_el.setAttribute('title', title)
        text_node = self.doc.createTextNode('@import url("{}");'.format(href))
        style_el.appendChild(text_node)
        self.defs.add(Style(style_el))

    def save(self, pretty=False, indent=2, encoding='utf-8'):
        # Append defs if it has children
        if self.defs.children:
            self.root.insertBefore(self.defs.to_xml(self.doc), self.root.firstChild)
        # Append other elements
        for element in self.elements:
            self.root.appendChild(element.to_xml(self.doc))
        if pretty:
            xml_str = self.doc.toprettyxml(indent=" " * indent, encoding=encoding)
            if isinstance(xml_str, bytes):
                xml_str = xml_str.decode(encoding)
        else:
            xml_str = self.doc.toxml(encoding=encoding)
            if isinstance(xml_str, bytes):
                xml_str = xml_str.decode(encoding)
        if self.filename:
            with open(self.filename, 'w', encoding=encoding) as f:
                f.write(xml_str)
        else:
            return xml_str

    def saveas(self, filename, pretty=False, indent=2, encoding='utf-8'):
        self.filename = filename
        self.save(pretty=pretty, indent=indent, encoding=encoding)

    def tostring(self, pretty=False, indent=2):
        # Append defs if it has children and not already appended
        if self.defs.children and not any(isinstance(child, Defs) for child in self.root.childNodes):
            self.root.insertBefore(self.defs.to_xml(self.doc), self.root.firstChild)
        # Append other elements
        for element in self.elements:
            if element.to_xml(self.doc) not in self.root.childNodes:
                self.root.appendChild(element.to_xml(self.doc))
        if pretty:
            xml_str = self.doc.toprettyxml(indent=" " * indent)
        else:
            xml_str = self.doc.toxml()
        return xml_str

    def get_xml(self):
        return self.root

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

    # Also, add the 'stop' factory method for gradients
    def stop(self, offset, **kwargs):
        return Stop(offset, **kwargs)

class SVGElement(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.children = []

    def set_attributes(self, element):
        for k, v in self.kwargs.items():
            element.setAttribute(k.replace('_', '-'), str(v))

    def add(self, element):
        self.children.append(element)

    def to_xml(self, doc):
        pass  # To be implemented in subclasses

class Line(SVGElement):
    def __init__(self, start, end, **kwargs):
        super(Line, self).__init__(**kwargs)
        self.start = start
        self.end = end

    def to_xml(self, doc):
        el = doc.createElement('line')
        el.setAttribute('x1', str(self.start[0]))
        el.setAttribute('y1', str(self.start[1]))
        el.setAttribute('x2', str(self.end[0]))
        el.setAttribute('y2', str(self.end[1]))
        self.set_attributes(el)
        return el

class Circle(SVGElement):
    def __init__(self, center, r, **kwargs):
        super(Circle, self).__init__(**kwargs)
        self.center = center
        self.r = r

    def to_xml(self, doc):
        el = doc.createElement('circle')
        el.setAttribute('cx', str(self.center[0]))
        el.setAttribute('cy', str(self.center[1]))
        el.setAttribute('r', str(self.r))
        self.set_attributes(el)
        return el

class Rect(SVGElement):
    def __init__(self, insert, size, **kwargs):
        super(Rect, self).__init__(**kwargs)
        self.insert = insert
        self.size = size

    def to_xml(self, doc):
        el = doc.createElement('rect')
        el.setAttribute('x', str(self.insert[0]))
        el.setAttribute('y', str(self.insert[1]))
        el.setAttribute('width', str(self.size[0]))
        el.setAttribute('height', str(self.size[1]))
        self.set_attributes(el)
        return el

class Text(SVGElement):
    def __init__(self, text_content, insert, **kwargs):
        super(Text, self).__init__(**kwargs)
        self.text_content = text_content
        self.insert = insert

    def to_xml(self, doc):
        el = doc.createElement('text')
        el.setAttribute('x', str(self.insert[0]))
        el.setAttribute('y', str(self.insert[1]))
        self.set_attributes(el)
        text_node = doc.createTextNode(self.text_content)
        el.appendChild(text_node)
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

class TSpan(SVGElement):
    def __init__(self, text_content, **kwargs):
        super(TSpan, self).__init__(**kwargs)
        self.text_content = text_content

    def to_xml(self, doc):
        el = doc.createElement('tspan')
        self.set_attributes(el)
        text_node = doc.createTextNode(self.text_content)
        el.appendChild(text_node)
        return el

class Path(SVGElement):
    def __init__(self, d='', **kwargs):
        super(Path, self).__init__(**kwargs)
        self.d = d

    def to_xml(self, doc):
        el = doc.createElement('path')
        el.setAttribute('d', self.d)
        self.set_attributes(el)
        return el

class Polygon(SVGElement):
    def __init__(self, points, **kwargs):
        super(Polygon, self).__init__(**kwargs)
        self.points = points

    def to_xml(self, doc):
        el = doc.createElement('polygon')
        points_str = ' '.join(['{},{}'.format(p[0], p[1]) for p in self.points])
        el.setAttribute('points', points_str)
        self.set_attributes(el)
        return el

class Polyline(SVGElement):
    def __init__(self, points, **kwargs):
        super(Polyline, self).__init__(**kwargs)
        self.points = points

    def to_xml(self, doc):
        el = doc.createElement('polyline')
        points_str = ' '.join(['{},{}'.format(p[0], p[1]) for p in self.points])
        el.setAttribute('points', points_str)
        self.set_attributes(el)
        return el

class Ellipse(SVGElement):
    def __init__(self, center, r, **kwargs):
        super(Ellipse, self).__init__(**kwargs)
        self.center = center
        self.r = r

    def to_xml(self, doc):
        el = doc.createElement('ellipse')
        el.setAttribute('cx', str(self.center[0]))
        el.setAttribute('cy', str(self.center[1]))
        el.setAttribute('rx', str(self.r[0]))
        el.setAttribute('ry', str(self.r[1]))
        self.set_attributes(el)
        return el

class Group(SVGElement):
    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

    def to_xml(self, doc):
        el = doc.createElement('g')
        self.set_attributes(el)
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

class Defs(SVGElement):
    def __init__(self):
        super(Defs, self).__init__()
        self.child_elements = {}  # Key: element's unique identifier, Value: element

    def add(self, element):
        # Create a unique identifier for the element
        # For Style elements, we can use the css_text
        if isinstance(element, Style):
            key = ('style', element.css_text.strip())
        else:
            # For other elements, use their 'id' attribute if available
            element_id = element.kwargs.get('id')
            if element_id:
                key = ('id', element_id)
            else:
                # Fallback to element type and string representation
                key = ('type', str(element))

        if key in self.child_elements:
            # Element already exists, do not add it again
            return
        else:
            self.child_elements[key] = element
            self.children.append(element)

    def to_xml(self, doc):
        el = doc.createElement('defs')
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

class Style(SVGElement):
    def __init__(self, css_text):
        super(Style, self).__init__()
        self.css_text = css_text

    def to_xml(self, doc):
        el = doc.createElement('style')
        el.setAttribute('type', 'text/css')
        text_node = doc.createTextNode(self.css_text)
        el.appendChild(text_node)
        return el

class LinearGradient(SVGElement):
    def __init__(self, **kwargs):
        super(LinearGradient, self).__init__(**kwargs)

    def to_xml(self, doc):
        el = doc.createElement('linearGradient')
        self.set_attributes(el)
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

class RadialGradient(SVGElement):
    def __init__(self, **kwargs):
        super(RadialGradient, self).__init__(**kwargs)

    def to_xml(self, doc):
        el = doc.createElement('radialGradient')
        self.set_attributes(el)
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

class Stop(SVGElement):
    def __init__(self, offset, **kwargs):
        super(Stop, self).__init__(**kwargs)
        self.offset = offset

    def to_xml(self, doc):
        el = doc.createElement('stop')
        el.setAttribute('offset', str(self.offset))
        self.set_attributes(el)
        return el

class Pattern(SVGElement):
    def __init__(self, **kwargs):
        super(Pattern, self).__init__(**kwargs)

    def to_xml(self, doc):
        el = doc.createElement('pattern')
        self.set_attributes(el)
        for child in self.children:
            el.appendChild(child.to_xml(doc))
        return el

def rgb(r, g, b, mode='%'):
    if mode == '%':
        return 'rgb({}%, {}%, {}%)'.format(r, g, b)
    else:
        return 'rgb({}, {}, {})'.format(r, g, b)
