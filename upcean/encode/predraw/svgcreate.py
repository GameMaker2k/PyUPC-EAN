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
        self.size = size
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
        self.elements = []
        self.defs = Defs()
        # Do not append defs here; will be appended during save
        self.doc.appendChild(self.root)

    def add(self, element):
        self.elements.append(element)

    def save(self):
        # Append defs if it has children
        if self.defs.children:
            self.root.appendChild(self.defs.to_xml(self.doc))
        # Append other elements
        for element in self.elements:
            self.root.appendChild(element.to_xml(self.doc))
        xml_str = self.doc.toprettyxml(indent="  ")
        try:
            with open(self.filename, 'w') as f:
                f.write(xml_str)
        except TypeError:
            # Handle Unicode encoding in Python 2
            with open(self.filename, 'w') as f:
                f.write(xml_str.encode('utf-8'))

    def saveas(self, filename):
        self.filename = filename
        self.save()

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

def rgb(r, g, b, mode='%'):
    if mode == '%':
        return 'rgb({}%, {}%, {}%)'.format(r, g, b)
    else:
        return 'rgb({}, {}, {})'.format(r, g, b)
