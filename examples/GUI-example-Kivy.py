#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv
from dataclasses import dataclass
from configparser import ConfigParser

import upcean
from PIL import Image

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.properties import (
    StringProperty, NumericProperty, ListProperty, BooleanProperty, ObjectProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.button import Button


KV = r"""
#:kivy 2.1.0

<BarcodeRV>:
    viewclass: "BarcodeRow"
    RecycleBoxLayout:
        id: rv_layout
        default_size: None, dp(34)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"

<BarcodeRow>:
    orientation: "horizontal"
    size_hint_y: None
    height: "34dp"
    padding: "6dp"
    spacing: "6dp"
    canvas.before:
        Color:
            rgba: (0.85, 0.87, 0.90, 1) if self.even else (1,1,1,1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: root.row_id
        size_hint_x: 0.15
        halign: "center"
        valign: "middle"
        text_size: self.size
    Label:
        text: root.barcodes
        size_hint_x: 0.35
        halign: "center"
        valign: "middle"
        text_size: self.size
    Label:
        text: root.bctype
        size_hint_x: 0.20
        halign: "center"
        valign: "middle"
        text_size: self.size
    Label:
        text: root.comment
        size_hint_x: 0.30
        halign: "left"
        valign: "middle"
        text_size: self.size

<RootUI>:
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"

    BoxLayout:
        size_hint_y: None
        height: "42dp"
        spacing: "8dp"

        Button:
            text: "File"
            on_release: root.open_file_menu()

        Button:
            text: "Settings"
            on_release: root.open_settings()

        Button:
            text: "Info"
            on_release: root.open_info()

        Widget:

        Label:
            text: "Barcode generator v1.0 (Kivy)"
            size_hint_x: 0.45
            halign: "right"
            valign: "middle"
            text_size: self.size

    # Main (inputs + preview)
    BoxLayout:
        spacing: "10dp"
        size_hint_y: 0.58

        # LEFT: Inputs
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.45
            spacing: "8dp"

            BoxLayout:
                size_hint_y: None
                height: "36dp"
                Label:
                    text: "Barcode type:"
                    size_hint_x: 0.45
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                Spinner:
                    id: sp_type
                    text: root.bctype
                    values: root.type_options
                    size_hint_x: 0.55
                    on_text: root.on_type_change(self.text)

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: "80dp"
                Label:
                    text: "Barcode size: [b]%d[/b]" % int(root.bcsize)
                    markup: True
                    size_hint_y: None
                    height: "24dp"
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                Slider:
                    id: sl_size
                    min: 1
                    max: 10
                    step: 1
                    value: root.bcsize
                    on_value: root.bcsize = int(self.value)

            Label:
                text: "Barcode value:"
                size_hint_y: None
                height: "22dp"
                halign: "left"
                valign: "middle"
                text_size: self.size

            TextInput:
                id: ti_value
                text: root.bcvalue
                font_size: "22sp"
                multiline: False
                on_text: root.bcvalue = self.text

            Label:
                text: "Comment:"
                size_hint_y: None
                height: "22dp"
                halign: "left"
                valign: "middle"
                text_size: self.size

            TextInput:
                id: ti_comment
                text: root.bccomment
                font_size: "16sp"
                multiline: True
                size_hint_y: None
                height: "90dp"
                on_text: root.bccomment = self.text

            BoxLayout:
                size_hint_y: None
                height: "40dp"
                spacing: "8dp"
                Button:
                    text: "Generate"
                    on_release: root.generate()
                Button:
                    text: "Save"
                    on_release: root.save_autoname()

        # RIGHT: Preview
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.55
            spacing: "8dp"

            BoxLayout:
                size_hint_y: None
                height: "40dp"
                spacing: "8dp"
                Button:
                    text: "Save As..."
                    on_release: root.save_dialog()
                Label:
                    text: "Preview"
                    halign: "right"
                    valign: "middle"
                    text_size: self.size

            ScrollView:
                do_scroll_x: True
                do_scroll_y: True
                bar_width: "10dp"
                canvas.before:
                    Color:
                        rgba: (0.76, 0.76, 0.76, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Image:
                    id: img_preview
                    texture: root.preview_texture
                    size_hint: None, None
                    size: root.preview_size
                    fit_mode: "contain"

    # TABLE / LIST
    BoxLayout:
        orientation: "vertical"
        spacing: "6dp"
        size_hint_y: 0.42

        BoxLayout:
            size_hint_y: None
            height: "28dp"
            padding: "6dp"
            canvas.before:
                Color:
                    rgba: (0.35, 0.35, 0.35, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "#"
                color: (1,1,1,1)
                size_hint_x: 0.15
            Label:
                text: "Barcodes"
                color: (1,1,1,1)
                size_hint_x: 0.35
            Label:
                text: "Type"
                color: (1,1,1,1)
                size_hint_x: 0.20
            Label:
                text: "Comment"
                color: (1,1,1,1)
                size_hint_x: 0.30

        ScrollView:
            do_scroll_x: False
            BarcodeRV:
                id: rv_table
                size_hint_y: None
                height: self.layout_manager.minimum_height
"""

DEFAULT_INI_TEXT = (
    "[DefaultValues]\n"
    "Type = EAN-13\n"
    "EAN13start = 4780000000010\n"
    "EAN08start = 47800010\n"
    "EAN05start = 00000\n"
    "Size = 2\n"
    "FileType = PDF\n"
    "FileDirectory =\n"
)

DATA_CSV = "data.csv"
CONFIG_INI = "config.ini"


def ensure_ini_exists():
    if not os.path.isfile(CONFIG_INI):
        with open(CONFIG_INI, "w", encoding="utf-8") as f:
            f.write(DEFAULT_INI_TEXT)


def pil_to_texture(pil_img: Image.Image) -> Texture:
    if pil_img.mode not in ("RGB", "RGBA"):
        pil_img = pil_img.convert("RGBA")
    w, h = pil_img.size
    tex = Texture.create(size=(w, h))
    tex.flip_vertical()
    tex.blit_buffer(pil_img.tobytes(), colorfmt=pil_img.mode.lower(), bufferfmt="ubyte")
    return tex


@dataclass
class BarcodeRowModel:
    row_id: str
    barcodes: str
    bctype: str
    comment: str


class BarcodeRow(RecycleDataViewBehavior, BoxLayout):
    row_id = StringProperty("")
    barcodes = StringProperty("")
    bctype = StringProperty("")
    comment = StringProperty("")
    even = BooleanProperty(False)

    _last_touch_time = 0.0

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        app = App.get_running_app()
        app.root_ui.load_row(self.row_id)

        t = touch.time_start
        if (t - self._last_touch_time) <= 0.35:
            app.root_ui.edit_mode = True
            app.root_ui.selected_id = self.row_id
        self._last_touch_time = t
        return True


class BarcodeRV(RecycleView):
    pass


class SettingsPopup(Popup):
    def __init__(self, root_ui, **kwargs):
        super().__init__(**kwargs)
        self.root_ui = root_ui
        self.title = "Default settings"
        self.size_hint = (None, None)
        self.size = (420, 520)
        self.auto_dismiss = False

        content = BoxLayout(orientation="vertical", spacing=8, padding=10)

        from kivy.uix.spinner import Spinner
        from kivy.uix.textinput import TextInput

        self.sp_type = Spinner(text=root_ui.default_type, values=["EAN-13", "EAN-8", "EAN-5"], size_hint_y=None, height=36)
        self.ti_size = TextInput(text=str(root_ui.default_size), multiline=False, input_filter="int", size_hint_y=None, height=36)
        self.sp_filetype = Spinner(text=root_ui.default_filetype, values=["PDF", "PNG", "JPG", "GIF"], size_hint_y=None, height=36)

        self.ti_ean13 = TextInput(text=root_ui.ean13start, multiline=False, size_hint_y=None, height=36, input_filter="int")
        self.ti_ean08 = TextInput(text=root_ui.ean08start, multiline=False, size_hint_y=None, height=36, input_filter="int")
        self.ti_ean05 = TextInput(text=root_ui.ean05start, multiline=False, size_hint_y=None, height=36, input_filter="int")

        self.ti_dir = TextInput(text=root_ui.filedir, multiline=False, size_hint_y=None, height=36)

        def row(label_text, widget):
            r = BoxLayout(size_hint_y=None, height=40, spacing=8)
            lab = Label(text=label_text, size_hint_x=0.45, halign="left", valign="middle")
            lab.bind(size=lambda *_: setattr(lab, "text_size", lab.size))
            r.add_widget(lab)
            r.add_widget(widget)
            return r

        content.add_widget(row("Barcode type:", self.sp_type))
        content.add_widget(row("Barcode size (1-10):", self.ti_size))
        content.add_widget(row("Default file type:", self.sp_filetype))

        content.add_widget(Label(text="EAN-13 initial value:", size_hint_y=None, height=22, halign="left", valign="middle"))
        content.add_widget(self.ti_ean13)

        content.add_widget(Label(text="EAN-08 initial value:", size_hint_y=None, height=22, halign="left", valign="middle"))
        content.add_widget(self.ti_ean08)

        content.add_widget(Label(text="EAN-05 initial value:", size_hint_y=None, height=22, halign="left", valign="middle"))
        content.add_widget(self.ti_ean05)

        content.add_widget(Label(text="File saving directory:", size_hint_y=None, height=22, halign="left", valign="middle"))
        content.add_widget(self.ti_dir)

        btns = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_save = Button(text="Save")
        btn_cancel = Button(text="Cancel")
        btns.add_widget(btn_save)
        btns.add_widget(btn_cancel)

        content.add_widget(btns)
        self.content = content

        def do_cancel(*_):
            self.dismiss()

        def do_save(*_):
            try:
                sz = int(self.ti_size.text.strip() or "2")
            except ValueError:
                sz = 2
            sz = max(1, min(10, sz))

            root_ui.default_type = self.sp_type.text
            root_ui.default_size = sz
            root_ui.default_filetype = self.sp_filetype.text
            root_ui.filedir = self.ti_dir.text.strip()

            root_ui.ean13start = self.ti_ean13.text.strip()
            root_ui.ean08start = self.ti_ean08.text.strip()
            root_ui.ean05start = self.ti_ean05.text.strip()

            root_ui.write_ini()
            root_ui.load_ini_into_ui()
            self.dismiss()

        btn_cancel.bind(on_release=do_cancel)
        btn_save.bind(on_release=do_save)


class RootUI(BoxLayout):
    type_options = ListProperty(["UPC-A", "UPC-E", "EAN-13", "EAN-8", "EAN-5"])

    bctype = StringProperty("EAN-13")
    bcsize = NumericProperty(2)
    bcvalue = StringProperty("")
    bccomment = StringProperty("")

    preview_texture = ObjectProperty(None, allownone=True)
    preview_size = ListProperty([1, 1])

    default_type = StringProperty("EAN-13")
    default_size = NumericProperty(2)
    default_filetype = StringProperty("PDF")
    filedir = StringProperty("")

    ean13start = StringProperty("")
    ean08start = StringProperty("")
    ean05start = StringProperty("")

    barcode_bg_color = (255, 255, 255)
    barcode_bar_color = (0, 0, 0)
    barcode_text_color = (0, 0, 0)

    barcode_list = {
        "UPC-A": "upca",
        "UPC-E": "upce",
        "EAN-13": "ean13",
        "EAN-8": "ean8",
        "EAN-5": "ean5",
    }

    edit_mode = BooleanProperty(False)
    selected_id = StringProperty("")
    oldvalue = StringProperty("")
    existcomment = StringProperty("")

    def on_type_change(self, text):
        self.bctype = text

    def open_file_menu(self):
        box = BoxLayout(orientation="vertical", spacing=8, padding=10)
        p = Popup(title="File", content=box, size_hint=(None, None), size=(320, 220))

        btn_save_as = Button(text="Save As...")
        btn_save_auto = Button(text="Save (auto name)")
        btn_close = Button(text="Close")

        box.add_widget(btn_save_as)
        box.add_widget(btn_save_auto)
        box.add_widget(btn_close)

        btn_close.bind(on_release=lambda *_: p.dismiss())
        btn_save_as.bind(on_release=lambda *_: (p.dismiss(), self.save_dialog()))
        btn_save_auto.bind(on_release=lambda *_: (p.dismiss(), self.save_autoname()))
        p.open()

    def open_settings(self):
        SettingsPopup(self).open()

    def open_info(self):
        text = (
            "Barcode generator v1.0\n\n"
            "Hamraqulov Boburmirzo © 2017\n"
            "Telegram: @bzimor\n"
            "Github: github.com/bzimor\n"
            "Email: bobzimor@gmail.com\n\n"
            "Kivy port: single-file app.py"
        )
        Popup(title="Info", content=Label(text=text), size_hint=(None, None), size=(420, 320)).open()

    def alert(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(420, 200)).open()

    def generatebarcode(self, bcodevalue: str):
        tmpbarcode = upcean.oopfuncs.barcode(self.barcode_list[self.bctype], bcodevalue)
        tmpbarcode.size = int(self.bcsize)
        tmpbarcode.barcolor = self.barcode_bar_color
        tmpbarcode.textcolor = self.barcode_text_color
        tmpbarcode.bgcolor = self.barcode_bg_color
        tmpbarcode.filename = None
        return tmpbarcode

    def previewbarcode(self, bcodevalue: str):
        try:
            tmpbarcode = self.generatebarcode(bcodevalue)
            valid_img = tmpbarcode.validate_draw_barcode()[1]
        except Exception:
            valid_img = False

        if not valid_img:
            self.alert("Error", "Barcode couldn't be generated!")
            return

        tex = pil_to_texture(valid_img)
        self.preview_texture = tex
        self.preview_size = [valid_img.size[0], valid_img.size[1]]

        if not self.isunique(bcodevalue):
            self.bccomment = self.existcomment

    def generate(self):
        if (not self.bcvalue) or self.edit_mode:
            self.bcvalue = ""
            self.bccomment = ""
            ok = self.GenerateCode()
            if not ok:
                return

        self.previewbarcode(self.bcvalue)
        self.edit_mode = False

    def save_autoname(self):
        if not self.bcvalue.strip():
            self.alert("Warning", "Generate any barcode first!")
            return
        if not self.filedir.strip():
            self.alert("Warning", "Set FileDirectory in Settings first (or use Save As...).")
            return

        fname = os.path.join(self.filedir, f"{self.bcvalue}.{self.default_filetype.lower()}")
        self._save_to_path(fname)
        self.updatetree_after_save()

    def save_dialog(self):
        if not self.bcvalue.strip():
            self.alert("Warning", "Generate any barcode first!")
            return

        box = BoxLayout(orientation="vertical", spacing=8, padding=10)
        from kivy.uix.textinput import TextInput

        ti = TextInput(
            text=os.path.join(self.filedir or ".", f"{self.bcvalue}.{self.default_filetype.lower()}"),
            multiline=False
        )
        box.add_widget(Label(text="Enter full path to save file:"))
        box.add_widget(ti)

        btns = BoxLayout(size_hint_y=None, height=44, spacing=10)
        btn_ok = Button(text="Save")
        btn_cancel = Button(text="Cancel")
        btns.add_widget(btn_ok)
        btns.add_widget(btn_cancel)
        box.add_widget(btns)

        p = Popup(title="Save As...", content=box, size_hint=(None, None), size=(600, 220), auto_dismiss=False)

        def do_cancel(*_):
            p.dismiss()

        def do_save(*_):
            path = ti.text.strip()
            if not path:
                self.alert("Warning", "Path is empty.")
                return
            p.dismiss()
            self._save_to_path(path)
            self.updatetree_after_save()

        btn_cancel.bind(on_release=do_cancel)
        btn_ok.bind(on_release=do_save)
        p.open()

    def _save_to_path(self, path: str):
        try:
            tmpbarcode = self.generatebarcode(self.bcvalue.strip())
            tmpbarcode.filename = path
            ok = tmpbarcode.validate_create_barcode()
        except Exception:
            ok = False

        if not ok:
            self.alert("Warning", "Barcode saving error")
        else:
            self.alert("Info", f"Barcode saved:\n{path}")

    def updatetree_after_save(self):
        bcitem = (self.bcvalue.strip(), self.bctype, self.bccomment)
        rows = self.read_all_rows()

        if self.isunique(bcitem[0]):
            new_id = str(self.last_id(rows) + 1)
            rows.append(BarcodeRowModel(new_id, bcitem[0], bcitem[1], bcitem[2]))
        else:
            if self.edit_mode and self.selected_id:
                if self.oldvalue == bcitem[0]:
                    for r in rows:
                        if r.row_id == self.selected_id:
                            r.comment = bcitem[2]
                            break
                else:
                    self.alert("Warning", "Barcode is already in table!")
                    return
            else:
                self.alert("Warning", "Barcode is already in table!")
                return

        self.write_all_rows(rows)
        self.refresh_table(rows)

        self.bcvalue = ""
        self.bccomment = ""
        self.edit_mode = False
        self.selected_id = ""
        self.oldvalue = ""

    def load_row(self, row_id: str):
        rows = self.read_all_rows()
        for r in rows:
            if r.row_id == row_id:
                self.selected_id = row_id
                self.edit_mode = True
                self.oldvalue = r.barcodes
                self.bctype = r.bctype
                self.bcvalue = r.barcodes
                self.bccomment = r.comment or ""
                if r.barcodes:
                    self.previewbarcode(r.barcodes)
                break

    def refresh_table(self, rows):
        data = []
        for idx, r in enumerate(rows):
            data.append({
                "row_id": r.row_id,
                "barcodes": r.barcodes,
                "bctype": r.bctype,
                "comment": r.comment,
                "even": (idx % 2 == 1),
            })
        self.ids.rv_table.data = data

    def load_ini(self):
        ensure_ini_exists()
        cfg = ConfigParser()
        cfg.read(CONFIG_INI, encoding="utf-8")
        sect = "DefaultValues"

        self.default_type = cfg.get(sect, "Type", fallback="EAN-13")
        self.default_size = cfg.getint(sect, "Size", fallback=2)
        self.default_filetype = cfg.get(sect, "FileType", fallback="PDF")
        self.filedir = cfg.get(sect, "FileDirectory", fallback="")

        self.ean13start = cfg.get(sect, "EAN13start", fallback="4780000000010")
        self.ean08start = cfg.get(sect, "EAN08start", fallback="47800010")
        self.ean05start = cfg.get(sect, "EAN05start", fallback="00000")

    def write_ini(self):
        cfg = ConfigParser()
        cfg.read(CONFIG_INI, encoding="utf-8")
        sect = "DefaultValues"
        if not cfg.has_section(sect):
            cfg.add_section(sect)

        cfg.set(sect, "Type", self.default_type)
        cfg.set(sect, "Size", str(int(self.default_size)))
        cfg.set(sect, "FileType", self.default_filetype)
        cfg.set(sect, "FileDirectory", self.filedir)

        cfg.set(sect, "EAN13start", self.ean13start)
        cfg.set(sect, "EAN08start", self.ean08start)
        cfg.set(sect, "EAN05start", self.ean05start)

        with open(CONFIG_INI, "w", encoding="utf-8") as f:
            cfg.write(f)

    def load_ini_into_ui(self):
        self.bctype = self.default_type
        self.bcsize = int(self.default_size)

    def read_all_rows(self):
        rows = []
        if not os.path.isfile(DATA_CSV):
            return rows
        try:
            with open(DATA_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    rows.append(BarcodeRowModel(
                        row_id=row.get("id", ""),
                        barcodes=row.get("barcodes", ""),
                        bctype=row.get("type", ""),
                        comment=row.get("comment", ""),
                    ))
        except Exception:
            self.alert("Error", "Error occurred while loading Data.csv!")
        return rows

    def write_all_rows(self, rows):
        try:
            with open(DATA_CSV, "w", encoding="utf-8", newline="") as f:
                fieldnames = ["id", "barcodes", "type", "comment"]
                w = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
                w.writeheader()
                for r in rows:
                    w.writerow({"id": r.row_id, "barcodes": r.barcodes, "type": r.bctype, "comment": r.comment})
        except Exception:
            self.alert("Error", "Error occurred while saving Data.csv!")

    def last_id(self, rows):
        mx = 0
        for r in rows:
            try:
                mx = max(mx, int(r.row_id))
            except Exception:
                pass
        return mx

    def isunique(self, bcode: str):
        if not os.path.isfile(DATA_CSV):
            return True
        try:
            with open(DATA_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    if row.get("barcodes") == bcode:
                        self.existcomment = row.get("comment", "")
                        return False
        except Exception:
            return True
        return True

    def validate_ean13(self, upc, return_check=False):
        upc = str(upc)
        if len(upc) > 13:
            fix_matches = re.findall(r"^(\d{13})", upc)
            if fix_matches:
                upc = fix_matches[0]
        if len(upc) > 13 or len(upc) < 12:
            return False

        digits = [int(x) for x in list(upc)]
        d1 = digits[0:][::2]
        d2 = digits[1:][::2]
        even_sum = (d2[0] + d2[1] + d2[2] + d2[3] + d2[4] + d2[5]) * 3
        odd_sum = d1[0] + d1[1] + d1[2] + d1[3] + d1[4] + d1[5]
        all_sum = odd_sum + even_sum
        check = all_sum % 10
        if check > 0:
            check = 10 - check

        if (not return_check) and len(upc) == 13:
            return check == d1[6]
        if return_check:
            return str(check)
        if len(upc) == 12:
            return str(check)

    def validate_ean08(self, upc, return_check=False):
        upc = str(upc)
        if len(upc) > 8:
            fix_matches = re.findall(r"^(\d{8})", upc)
            if fix_matches:
                upc = fix_matches[0]
        if len(upc) > 8 or len(upc) < 7:
            return False

        digits = [int(x) for x in list(upc)]
        d1 = digits[0:][::2]
        d2 = digits[1:][::2]
        even_sum = (d1[0] + d1[1] + d1[2] + d1[3]) * 3
        odd_sum = d2[0] + d2[1] + d2[2]
        all_sum = odd_sum + even_sum
        check = all_sum % 10
        if check > 0:
            check = 10 - check

        if (not return_check) and len(upc) == 8:
            return check == d2[3]
        if return_check:
            return str(check)
        if len(upc) == 7:
            return str(check)

    def GenerateCode(self):
        if self.bctype == "EAN-13":
            if self.ean13start.isdigit() and len(self.ean13start) > 12:
                newcode = int(self.ean13start[:12])
                while True:
                    chk = self.validate_ean13(newcode)
                    if chk and self.isunique(str(newcode) + str(chk)):
                        self.bcvalue = str(newcode) + str(chk)
                        return True
                    newcode += 1
            else:
                self.alert("Warning", "Enter initial value for EAN-13 (in Settings)!")
                return False

        elif self.bctype == "EAN-8":
            if self.ean08start.isdigit() and len(self.ean08start) > 7:
                newcode = int(self.ean08start[:7])
                while True:
                    chk = self.validate_ean08(newcode)
                    if chk and self.isunique(str(newcode) + str(chk)):
                        self.bcvalue = str(newcode) + str(chk)
                        return True
                    newcode += 1
            else:
                self.alert("Warning", "Enter initial value for EAN-08 (in Settings)!")
                return False

        elif self.bctype == "EAN-5":
            if self.ean05start.isdigit() and len(self.ean05start) == 5:
                newcode = int(self.ean05start)
                while True:
                    if self.isunique(str(newcode)):
                        self.bcvalue = str(newcode)
                        return True
                    newcode += 1
            else:
                self.alert("Warning", "Enter initial value for EAN-05 (in Settings)!")
                return False

        self.alert("Warning", "Enter a barcode value for this type (no auto-generate).")
        return False


class BarcodeApp(App):
    def build(self):
        # Set size first, then minimums (and ensure mins > 0)
        Window.size = (1100, 750)
        Window.minimum_width = 920
        Window.minimum_height = 680

        Builder.load_string(KV)
        root = RootUI()

        root.load_ini()
        root.load_ini_into_ui()
        rows = root.read_all_rows()
        root.refresh_table(rows)

        Clock.schedule_once(lambda *_: setattr(root, "preview_size", [1, 1]), 0)
        self.root_ui = root
        return root


if __name__ == "__main__":
    BarcodeApp().run()
