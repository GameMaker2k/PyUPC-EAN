#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2025 Game Maker 2k
    Copyright 2011-2025 Kazuki Przyborowski

    $FileInfo: upc-ui.py - Last Update: 7/2/2025 Ver. 2.20.2 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import os
from io import BytesIO

import upcean
from PIL import Image

# Kivy imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image as KivyImage
from kivy.uix.scrollview import ScrollView
from kivy.core.image import Image as CoreImage

KV = '''
<MainWidget>:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    ScrollView:
        size_hint_y: None
        height: '300dp'
        GridLayout:
            id: input_grid
            cols: 2
            size_hint_y: None
            spacing: 5
            padding: 5
            row_default_height: '40dp'
            row_force_default: True
            # rows will adjust automatically

    BoxLayout:
        size_hint_y: None
        height: '120dp'
        orientation: 'vertical'
        spacing: 5
        BoxLayout:
            spacing: 10
            CheckBox:
                id: cb_hidesn
            Label:
                text: 'Hide Start Number'
        BoxLayout:
            spacing: 10
            CheckBox:
                id: cb_hidecd
            Label:
                text: 'Hide Check Digit'
        BoxLayout:
            spacing: 10
            CheckBox:
                id: cb_hidetext
            Label:
                text: 'Hide Text'

    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        Button:
            text: 'Generate'
            on_release: root.generate_barcode()
        Button:
            text: 'Save As'
            on_release: root.open_save_popup()
        Button:
            text: 'Colors'
            on_release: root.change_colors()

    ScrollView:
        do_scroll_x: True
        do_scroll_y: True
        KivyImage:
            id: barcode_image
            size_hint: None, None
            allow_stretch: False
'''

# barcode types mapping
barcode_list = {
    'UPC-A': 'upca', 'UPC-E': 'upce', 'EAN-13': 'ean13', 'EAN-8': 'ean8',
    'EAN-2': 'ean2', 'EAN-5': 'ean5', 'ITF': 'itf', 'STF': 'stf',
    'ITF-14': 'itf14', 'Code 11': 'code11', 'Code 39': 'code39',
    'Code 93': 'code93', 'Codabar': 'codabar', 'MSI': 'msi'
}

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        Builder.load_string(KV)
        # initial colors
        self.barcode_bg_color = (255, 255, 255)
        self.barcode_bar_color = (0, 0, 0)
        self.barcode_text_color = (0, 0, 0)
        self.last_pil = None
        # build input grid
        self.build_inputs()

    def build_inputs(self):
        grid = self.ids.input_grid
        # Value
        grid.add_widget(Label(text='Value:'))
        self.value_input = TextInput(multiline=False)
        grid.add_widget(self.value_input)
        # Symbology
        grid.add_widget(Label(text='Symbology:'))
        self.symbology = Spinner(text='UPC-A', values=list(barcode_list.keys()))
        grid.add_widget(self.symbology)
        # Magnify
        grid.add_widget(Label(text='Magnify:'))
        self.magnify = Spinner(text='1', values=[str(i) for i in range(1, 11)])
        grid.add_widget(self.magnify)
        # Bar heights / widths
        grid.add_widget(Label(text='Bar 1 Height:'))
        self.entry2 = TextInput(text='48', multiline=False, input_filter='int')
        grid.add_widget(self.entry2)
        grid.add_widget(Label(text='Bar 2 Height:'))
        self.entry3 = TextInput(text='54', multiline=False, input_filter='int')
        grid.add_widget(self.entry3)
        grid.add_widget(Label(text='Bar Width:'))
        self.entry_barwidth = TextInput(text='1', multiline=False, input_filter='int')
        grid.add_widget(self.entry_barwidth)
        grid.add_widget(Label(text='Text Size:'))
        self.entry_textsize = TextInput(text='1', multiline=False, input_filter='int')
        grid.add_widget(self.entry_textsize)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint_y=None, height='40dp')
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(None, None), size=('400dp', '200dp'))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def preprocess_value(self, value):
        import re
        sym = self.symbology.text
        if sym in ['UPC-A', 'UPC-E', 'EAN-13', 'EAN-8']:
            m = re.match(r"(\d+)[ |\|](\d{2,5})$", value)
            if m:
                return m.group(1)
        return value

    def pil_to_texture(self, pil_img):
        data = BytesIO()
        pil_img.save(data, format='png')
        data.seek(0)
        core = CoreImage(data, ext='png')
        tex = core.texture
        # set image size to natural size
        img = self.ids.barcode_image
        img.texture = tex
        img.width, img.height = tex.size
        return tex

    def generate_barcode(self):
        # validate inputs
        try:
            bh1 = int(self.entry2.text)
            bh2 = int(self.entry3.text)
            mag = int(self.magnify.text)
            bw = int(self.entry_barwidth.text)
            ts = int(self.entry_textsize.text)
        except ValueError:
            self.show_popup('Error', 'Heights, Width, Text Size, and Magnify must be integers.')
            return
        hidesn = self.ids.cb_hidesn.active
        hidecd = self.ids.cb_hidecd.active
        hidetext = self.ids.cb_hidetext.active
        val = self.preprocess_value(self.value_input.text)
        # generate barcode
        bc = upcean.oopfuncs.barcode(barcode_list[self.symbology.text], val)
        bc.size = mag
        bc.barheight = (bh1, bh2)
        bc.barwidth = (bw, ts)
        bc.barcolor = self.barcode_bar_color
        bc.textcolor = self.barcode_text_color
        bc.bgcolor = self.barcode_bg_color
        bc.hidesn = hidesn
        bc.hidecd = hidecd
        bc.hidetext = hidetext
        bc.filename = None
        valid = bc.validate_draw_barcode()[1]
        if not valid:
            self.show_popup('Error', 'Could not generate barcode.')
            return
        self.last_pil = valid
        self.pil_to_texture(valid)

    def change_colors(self):
        # sequential color pickers
        from kivy.uix.colorpicker import ColorPicker
        def pick(title, initial, callback):
            content = BoxLayout(orientation='vertical')
            cp = ColorPicker()
            cp.hsv = (initial[0]/255., initial[1]/255., initial[2]/255.)
            btn = Button(text='Select', size_hint_y=None, height='40dp')
            content.add_widget(cp)
            content.add_widget(btn)
            popup = Popup(title=title, content=content, size_hint=(0.8,0.8))
            btn.bind(on_release=lambda *a: (callback(tuple(int(c*255) for c in cp.color[:3])), popup.dismiss()))
            popup.open()
        # chain callbacks
        pick('Background Color', self.barcode_bg_color, lambda c: (setattr(self, 'barcode_bg_color', c), pick('Bar Color', self.barcode_bar_color, lambda c2: (setattr(self, 'barcode_bar_color', c2), pick('Text Color', self.barcode_text_color, lambda c3: (setattr(self, 'barcode_text_color', c3), self.generate_barcode()))))))

    def open_save_popup(self):
        if not self.last_pil:
            self.generate_barcode()
            if not self.last_pil:
                return
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        chooser = Builder.load_string("""
FileChooserListView:
    path: '.'
    filters: ['*.png','*.jpg','*.jpeg','*.gif','*.bmp','*.tif','*.tiff']
""")
        fname_input = TextInput(text='barcode.png', size_hint_y=None, height='40dp', multiline=False)
        btn_box = BoxLayout(size_hint_y=None, height='40dp', spacing=10)
        save_btn = Button(text='Save')
        cancel_btn = Button(text='Cancel')
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(chooser)
        content.add_widget(fname_input)
        content.add_widget(btn_box)
        popup = Popup(title='Save Image As', content=content, size_hint=(0.9,0.9))
        save_btn.bind(on_release=lambda *a: self.perform_save(chooser.path, fname_input.text, popup))
        cancel_btn.bind(on_release=lambda *a: popup.dismiss())
        popup.open()

    def perform_save(self, path, filename, popup):
        full = os.path.join(path, filename)
        try:
            self.last_pil.save(full)
            popup.dismiss()
            self.show_popup('Success', 'Barcode saved successfully.')
        except Exception:
            self.show_popup('Error', 'Failed to save barcode.')

class BarcodeApp(App):
    def build(self):
        return MainWidget()

if __name__ == '__main__':
    BarcodeApp().run()
