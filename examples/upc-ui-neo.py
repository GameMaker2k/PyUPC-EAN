#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2023 Game Maker 2k
    Copyright 2011-2023 Kazuki Przyborowski

    $FileInfo: upc-ui.py - Last Update: 11/15/2024 Ver. 2.12.0 RC 1 - Author: cooldude2k $
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import re
import sys
import upcean

try:
    import Tkinter as tk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    import tkColorChooser as colorchooser
except ImportError:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
    from tkinter import colorchooser

from PIL import Image, ImageTk

# Global variables and initial setup
pro_app_name = "PyUPC-EAN"
pro_app_subname = " Test GUI"
pro_app_version = upcean.__version__
barcode_bg_color = (255, 255, 255)
barcode_bar_color = (0, 0, 0)
barcode_text_color = (0, 0, 0)

barcode_list = {
    "UPC-A": "upca", "UPC-E": "upce", "EAN-13": "ean13", "EAN-8": "ean8",
    "EAN-2": "ean2", "EAN-5": "ean5", "ITF": "itf", "STF": "stf",
    "ITF-14": "itf14", "Code 11": "code11", "Code 39": "code39",
    "Code 93": "code93", "Codabar": "codabar", "MSI": "msi"
}

# Initialize the main window
rootwin = tk.Tk()
rootwin.title("{}{} - Version: {}".format(pro_app_name, pro_app_subname, pro_app_version))
rootwin.geometry("400x500")
rootwin.resizable(0, 0)

def exit_ui(event=None):
    rootwin.quit()

rootwin.bind("<Escape>", exit_ui)

def hex_color_to_tuple(color):
    if not color.startswith("#") or len(color) != 7:
        return False
    try:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        return (r, g, b)
    except ValueError:
        return False

def tuple_color_to_hex(color):
    if not isinstance(color, tuple) or len(color) != 3:
        return False
    return "#{:02X}{:02X}{:02X}".format(*color)

def tkColorPicker(color, title):
    return colorchooser.askcolor(title=title, initialcolor=color, parent=rootwin)[1]

def ch_barcode_colors():
    global barcode_bg_color, barcode_bar_color, barcode_text_color
    messagebox.showinfo("Background Color", "Select a color for the background.")
    bg_color = tkColorPicker(tuple_color_to_hex(barcode_bg_color), "Background Color")
    if bg_color:
        barcode_bg_color = hex_color_to_tuple(bg_color)
    messagebox.showinfo("Bar Color", "Select a color for the bars.")
    bar_color = tkColorPicker(tuple_color_to_hex(barcode_bar_color), "Bar Color")
    if bar_color:
        barcode_bar_color = hex_color_to_tuple(bar_color)
    messagebox.showinfo("Text Color", "Select a color for the text.")
    text_color = tkColorPicker(tuple_color_to_hex(barcode_text_color), "Text Color")
    if text_color:
        barcode_text_color = hex_color_to_tuple(text_color)
    GenerateBarcode()

def preprocess_barcode_value(value):
    symbology = listboxtxt1.get()
    if symbology in ["UPC-A", "UPC-E", "EAN-13", "EAN-8"]:
        match = re.match(r"(\d+)[ |\|](\d{2,5})$", value)
        if match:
            value = match.group(1)
    return value

def GenerateBarcode():
    global image1
    # Validate inputs
    try:
        barheight1 = int(entry2.get())
        barheight2 = int(entry3.get())
        magnify_value = int(magnify.get())
    except ValueError:
        messagebox.showerror("Error", "Bar Heights and Magnify must be integer values.")
        return

    barcode_value = preprocess_barcode_value(entry1.get())

    # Generate barcode
    tmpbarcode = upcean.oopfuncs.barcode(
        barcode_list[listboxtxt1.get()], barcode_value)
    tmpbarcode.size = magnify_value
    tmpbarcode.barheight = (barheight1, barheight2)
    tmpbarcode.barcolor = barcode_bar_color
    tmpbarcode.textcolor = barcode_text_color
    tmpbarcode.bgcolor = barcode_bg_color
    tmpbarcode.filename = None
    validbc = tmpbarcode.validate_draw_barcode()[1]

    if not validbc:
        messagebox.showerror("PyUPC-EAN - Error", "Could not generate barcode.")
        rootwin.title("{}{} - Version: {}".format(pro_app_name, pro_app_subname, pro_app_version))
        return

    rootwin.title("{}{} - {}".format(pro_app_name, pro_app_subname, barcode_value))

    image1 = ImageTk.PhotoImage(validbc)

    panel1.delete("all")
    panel1.create_image(0, 0, anchor='nw', image=image1)
    panel1.config(scrollregion=panel1.bbox("all"))
    panel1.image = image1  # Keep a reference

def SaveGeneratedBarcode():
    try:
        barheight1 = int(entry2.get())
        barheight2 = int(entry3.get())
        magnify_value = int(magnify.get())
    except ValueError:
        messagebox.showerror("Error", "Bar Heights and Magnify must be integer values.")
        return

    barcode_value = preprocess_barcode_value(entry1.get())

    tmpbarcode = upcean.oopfuncs.barcode(
        barcode_list[listboxtxt1.get()], barcode_value)
    tmpbarcode.size = magnify_value
    tmpbarcode.barheight = (barheight1, barheight2)
    tmpbarcode.barcolor = barcode_bar_color
    tmpbarcode.textcolor = barcode_text_color
    tmpbarcode.bgcolor = barcode_bg_color

    savefname = filedialog.asksaveasfilename(
        title='Save Image As',
        filetypes=[
            ('PNG', '*.png'), ('JPEG', '*.jpg *.jpeg'), ('GIF', '*.gif'),
            ('BMP', '*.bmp'), ('TIFF', '*.tif *.tiff'), ('PDF', '*.pdf'),
            ('PostScript', '*.ps *.eps'), ('PCX', '*.pcx'),
            ('PNM', '*.pbm *.pgm *.ppm'), ('All Files', '*.*')
        ]
    )

    if not savefname:
        return  # User cancelled the save dialog

    tmpbarcode.filename = savefname
    savestate = tmpbarcode.validate_create_barcode()

    if not savestate:
        messagebox.showerror("PyUPC-EAN - Error", "Failed to save barcode.")
    else:
        messagebox.showinfo("Success", "Barcode saved successfully.")

# Right-Click Context Menus
def make_ccp_menu(w):
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    the_menu.add_command(label="Delete")
    the_menu.add_command(label="Delete All")
    the_menu.add_command(label="Select All")
    return the_menu

def show_ccp_menu(event):
    w = event.widget
    the_menu = make_ccp_menu(w)
    the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Delete", command=lambda: w.delete(tk.SEL_FIRST, tk.SEL_LAST) if w.select_present() else None)
    the_menu.entryconfigure("Delete All", command=lambda: w.delete(0, tk.END))
    the_menu.entryconfigure("Select All", command=lambda: w.select_range(0, tk.END))
    try:
        the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)
    except tk.TclError:
        pass  # On some platforms, this may cause an error.

def make_save_menu(w):
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Generate Image")
    the_menu.add_command(label="Save Image As")
    the_menu.add_command(label="Colors")
    return the_menu

def show_save_menu(event):
    w = event.widget
    the_menu = make_save_menu(w)
    the_menu.entryconfigure("Generate Image", command=GenerateBarcode)
    the_menu.entryconfigure("Save Image As", command=SaveGeneratedBarcode)
    the_menu.entryconfigure("Colors", command=ch_barcode_colors)
    try:
        the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)
    except tk.TclError:
        pass  # On some platforms, this may cause an error.

# GUI Widgets
label1 = tk.Label(rootwin, text="Value:")
label1.grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry1 = tk.Entry(rootwin)
entry1.grid(row=0, column=1, padx=5, pady=5)
entry1.bind("<Button-3>", show_ccp_menu)

label2 = tk.Label(rootwin, text="Symbology:")
label2.grid(row=1, column=0, sticky='e', padx=5, pady=5)
listboxtxt1 = tk.StringVar(rootwin)
listboxtxt1.set("UPC-A")
listbox1 = tk.OptionMenu(rootwin, listboxtxt1, *barcode_list.keys())
listbox1.grid(row=1, column=1, padx=5, pady=5, sticky='w')
listbox1.bind("<Button-3>", show_ccp_menu)

label3 = tk.Label(rootwin, text="Magnify:")
label3.grid(row=2, column=0, sticky='e', padx=5, pady=5)
magnify = tk.Spinbox(rootwin, from_=1, to=10, width=5)
magnify.grid(row=2, column=1, padx=5, pady=5, sticky='w')
magnify.bind("<Button-3>", show_ccp_menu)

label4 = tk.Label(rootwin, text="Bar 1 Height:")
label4.grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry2 = tk.Entry(rootwin, width=5)
entry2.insert(0, "48")
entry2.grid(row=3, column=1, padx=5, pady=5, sticky='w')
entry2.bind("<Button-3>", show_ccp_menu)

label5 = tk.Label(rootwin, text="Bar 2 Height:")
label5.grid(row=4, column=0, sticky='e', padx=5, pady=5)
entry3 = tk.Entry(rootwin, width=5)
entry3.insert(0, "54")
entry3.grid(row=4, column=1, padx=5, pady=5, sticky='w')
entry3.bind("<Button-3>", show_ccp_menu)

# Buttons
button_frame = tk.Frame(rootwin)
button_frame.grid(row=5, column=0, columnspan=2, pady=10)

button1 = tk.Button(button_frame, text="Generate", command=GenerateBarcode)
button1.pack(side='left', padx=5)
button1.bind("<Return>", lambda event: GenerateBarcode())
button1.bind("<Button-3>", show_ccp_menu)

button2 = tk.Button(button_frame, text="Save As", command=SaveGeneratedBarcode)
button2.pack(side='left', padx=5)
button2.bind("<Return>", lambda event: SaveGeneratedBarcode())
button2.bind("<Button-3>", show_ccp_menu)

button3 = tk.Button(button_frame, text="Colors", command=ch_barcode_colors)
button3.pack(side='left', padx=5)
button3.bind("<Return>", lambda event: ch_barcode_colors())
button3.bind("<Button-3>", show_ccp_menu)

# Canvas for barcode image
imageframe1 = tk.Frame(rootwin, width=350, height=200)
imageframe1.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

xscrollbar1 = tk.Scrollbar(imageframe1, orient=tk.HORIZONTAL)
xscrollbar1.pack(side=tk.BOTTOM, fill=tk.X)

yscrollbar1 = tk.Scrollbar(imageframe1, orient=tk.VERTICAL)
yscrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

panel1 = tk.Canvas(imageframe1, xscrollcommand=xscrollbar1.set, yscrollcommand=yscrollbar1.set)
panel1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
panel1.bind("<Button-3>", show_save_menu)

xscrollbar1.config(command=panel1.xview)
yscrollbar1.config(command=panel1.yview)

# Bindings
entry1.bind("<Return>", lambda event: GenerateBarcode())
magnify.bind("<Return>", lambda event: GenerateBarcode())
entry2.bind("<Return>", lambda event: GenerateBarcode())
entry3.bind("<Return>", lambda event: GenerateBarcode())

rootwin.mainloop()
