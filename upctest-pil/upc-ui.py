#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2013 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2013 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2013 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: upc-ui.py - Last Update: 04/24/2013 Ver. 2.3.7 RC 4  - Author: cooldude2k $
'''

from __future__ import division, absolute_import, print_function;
import os, sys, tempfile, upcean;
if(sys.version[0]=="2"):
 import Tkinter, tkMessageBox, tkFileDialog;
 from Tkinter import *;
if(sys.version[0]=="3"):
 import tkinter as Tkinter;
 from tkinter import messagebox as tkMessageBox;
 from tkinter import filedialog as tkFileDialog;
 from tkinter import *;
from upcean import *;
from PIL import Image, ImageTk;

updateimg = False;
pro_app_name = "PyUPC-EAN";
pro_app_subname = " Test GUI";
pro_app_version = upcean.__version__;
rootwin = Tk();
rootwin.wm_title(str(pro_app_name)+str(pro_app_subname)+" - Version: "+str(pro_app_version));
rootwin.geometry(("%dx%d") % (350, 300));
rootwin.resizable(0,0);
def exit_ui(event):
 rootwin.quit();
rootwin.bind("<Escape>", exit_ui);
''' Right Click Box by: jepler @ http://bytes.com/topic/python/answers/156826-cut-paste-text-between-tkinter-widgets#post601326 
    http://ebook.pldworld.com/_eBook/_OReilly/133.Books/Python/programming_python_2ed-2001/1.9.htm '''
def make_ccp_menu(w):
 the_menu = Menu(w, tearoff=0);
 the_menu.add_command(label="Cut");
 the_menu.add_command(label="Copy");
 the_menu.add_command(label="Paste");
 the_menu.add_command(label="Delete");
 the_menu.add_command(label="Delete All");
 the_menu.add_command(label="Select All");
 return the_menu;
def show_ccp_menu(e):
 global rootwin;
 the_menu = make_ccp_menu(rootwin);
 w = e.widget;
 the_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"));
 the_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"));
 the_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"));
 the_menu.entryconfigure("Delete", command=lambda: w.delete(SEL_FIRST, SEL_LAST) if w.select_present() else None);
 the_menu.entryconfigure("Delete All", command=lambda: w.delete(0, END));
 the_menu.entryconfigure("Select All", command=lambda: w.selection_range(0, END));
 the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root);
def make_save_menu(w):
 the_menu = Menu(w, tearoff=0);
 the_menu.add_command(label="Generate");
 the_menu.add_command(label="Save As");
 return the_menu;
def show_save_menu(e):
 global rootwin;
 the_menu = make_save_menu(rootwin);
 w = e.widget;
 the_menu.entryconfigure("Generate", command = GenerateBarcode);
 the_menu.entryconfigure("Save As", command = SaveGeneratedBarcode);
 the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root);
entry1 = Entry(rootwin);
entry1.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_ccp_menu);
if(sys.platform=="win32"):
 entry1.place(x=40, y=150);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 entry1.place(x=45, y=148);
labeltxt1 = StringVar();
label1 = Label( rootwin, textvariable=labeltxt1);
labeltxt1.set("Value:");
if(sys.platform=="win32"):
 label1.place(x=0, y=148);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 label1.place(x=0, y=148);
listboxtxt1 = StringVar(rootwin);
listboxtxt1.set("Detect");
listbox1 = OptionMenu(rootwin, listboxtxt1, "Detect", "UPC-A", "UPC-E", "EAN-13", "EAN-8", "EAN-2", "EAN-5", "ITF", "ITF-14", "Code 11", "Code 39", "Code 93");
if(sys.platform=="win32"):
 listbox1.place(x=60, y=169);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 listbox1.place(x=75, y=169);
labeltxt2 = StringVar();
label2 = Label(rootwin, textvariable=labeltxt2);
labeltxt2.set("Symbology:");
if(sys.platform=="win32"):
 label2.place(x=0, y=173);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 label2.place(x=0, y=175);
magnify = Spinbox(rootwin, wrap=True, width=3, from_=1, to=10);
magnify.bind_class("Spinbox", "<Button-3><ButtonRelease-3>", show_ccp_menu);
if(sys.platform=="win32"):
 magnify.place(x=50, y=200);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 magnify.place(x=60, y=198);
labeltxt3 = StringVar();
label3 = Label(rootwin, textvariable=labeltxt3);
labeltxt3.set("Magnify:");
label3.place(x=0, y=197);
entrytxt2 = StringVar();
entry2 = Entry(rootwin, textvariable=entrytxt2);
entry2.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_ccp_menu);
entrytxt2.set("48");
if(sys.platform=="win32"):
 entry2.place(x=70, y=225);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 entry2.place(x=85, y=223);
labeltxt4 = StringVar();
label4 = Label( rootwin, textvariable=labeltxt4);
labeltxt4.set("Bar 1 Height:");
label4.place(x=0, y=223);
entrytxt3 = StringVar();
entry3 = Entry(rootwin, textvariable=entrytxt3);
entry3.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_ccp_menu);
entrytxt3.set("54");
if(sys.platform=="win32"):
 entry3.place(x=70, y=250);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 entry3.place(x=85, y=248);
labeltxt5 = StringVar();
label5 = Label( rootwin, textvariable=labeltxt5);
labeltxt5.set("Bar 2 Height:");
label5.place(x=0, y=248);
def GenerateBarcode():
 global updateimg, panel1, faddonsize, rootwin, pro_app_name;
 rootwin.wm_title(str(pro_app_name)+str(pro_app_subname)+" - "+str(entry1.get()));
 upc_validate = entry1.get();
 if(listboxtxt1.get()=="Detect" or listboxtxt1.get()=="UPC-A" or listboxtxt1.get()=="UPC-E" or listboxtxt1.get()=="EAN-13" or listboxtxt1.get()=="EAN-8"):
  if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", entry1.get())):
   upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", entry1.get());
   upc_pieces = upc_pieces[0];
   upc_validate = upc_pieces[0];
  if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", entry1.get())):
   upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", entry1.get());
   upc_pieces = upc_pieces[0];
   upc_validate = upc_pieces[0];
 if(updateimg==True):
  panel1.destroy();
 '''(tmpfd, tmpfilename) = tempfile.mkstemp(".png");'''
 validbc = False;
 if(listboxtxt1.get()=="Detect" and (validate_barcode(upc_validate)==True or len(entry1.get())==2 or len(entry1.get())==5 or len(entry1.get())==14)):
  validbc = draw_barcode(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="UPC-A" and validate_barcode(upc_validate)==True):
  validbc = draw_upca(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="UPC-E" and validate_barcode(upc_validate)==True):
  validbc = draw_upce(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="EAN-13" and validate_barcode(upc_validate)==True):
  validbc = draw_ean13(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="EAN-8" and validate_ean8(upc_validate)==True):
  validbc = draw_ean8(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="EAN-2" and len(entry1.get())==2):
  validbc = draw_ean2(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="EAN-5" and len(entry1.get())==5):
  validbc = draw_ean5(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="ITF" and not (len(entry1.get()) % 2) and len(entry1.get()) > 5):
  validbc = draw_itf(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="ITF-14" and not (len(entry1.get()) % 2) and len(entry1.get()) > 5):
  validbc = draw_itf14(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="Code 11" and len(entry1.get()) > 0 and re.findall("([0-9\-]+)", entry1.get())):
  validbc = draw_code11(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="Code 39" and len(entry1.get()) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", entry1.get())):
  validbc = draw_code39(entry1.get(),"2",(False, False, False),(47, 53));
 if(listboxtxt1.get()=="Code 93" and len(entry1.get()) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", entry1.get())):
  validbc = draw_code93(entry1.get(),"2",(False, False, False),(47, 53));
 if(validbc!=False):
  image1 = ImageTk.PhotoImage(validbc);
  imageframe1 = Frame(rootwin, width=350, height=validbc.size[1] + 20);
  xscrollbar1 = Scrollbar(imageframe1, orient=HORIZONTAL);
  if(sys.platform=="win32"):
   xscrollbar1.place(x=0, y=130);
  if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
   xscrollbar1.place(x=0, y=132);
  panel1 = Canvas(imageframe1, xscrollcommand=xscrollbar1.set, width=350, height=validbc.size[1]);
  panel1.bind_class("Canvas", "<Button-3><ButtonRelease-3>", show_save_menu);
  panel1.create_image(validbc.size[0]/2,validbc.size[1]/2,image=image1);
  panel1.place(x=0, y=0);
  panel1.image = image1;
  xscrollbar1.config(command=panel1.xview);
  panel1.config(scrollregion=panel1.bbox(ALL));
  if(sys.platform=="win32"):
   imageframe1.place(x=0, y=0);
  if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
   imageframe1.place(x=0, y=0);
  updateimg = True;
 '''os.close(tmpfd);
 os.remove(tmpfilename);'''
def GenerateBarcodeAlt(event):
 GenerateBarcode();
def ShowSaveDialog():
 return tkFileDialog.asksaveasfilename(parent=rootwin,title='Save Image As',filetypes=[('Portable Network Graphics','*.png'), ('JPEG / JFIF','*.jpg *.jpeg *.jpe *.jfif *.jfi'), ('CompuServer GIF','*.gif'), ('Windows Bitmap','*.bmp *.dib'), ('Tag Image File Format','*.tif *.tiff'), ('Adobe Portable Document Format','*.pdf'), ('Adobe Encapsulated PostScript','*.ps *.eps'), ('Personal Computer Exchange','*.pcx'), ('Portable Anymap Format','*.pbm *.pgm *.ppm'), ('All File Formats','*.*')]);
def SaveGeneratedBarcode():
 GenerateBarcode();
 upc_validate = entry1.get();
 if(listboxtxt1.get()=="Detect" or listboxtxt1.get()=="UPC-A" or listboxtxt1.get()=="UPC-E" or listboxtxt1.get()=="EAN-13" or listboxtxt1.get()=="EAN-8"):
  if(re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", entry1.get())):
   upc_pieces = re.findall("([0-9]+)([ |\|]{1})([0-9]{2})$", entry1.get());
   upc_pieces = upc_pieces[0];
   upc_validate = upc_pieces[0];
  if(re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", entry1.get())):
   upc_pieces = re.findall("([0-9]+)([ |\|]){1}([0-9]{5})$", entry1.get());
   upc_pieces = upc_pieces[0];
   upc_validate = upc_pieces[0];
 if(listboxtxt1.get()=="Detect" and (validate_barcode(upc_validate)==True or len(entry1.get())==2 or len(entry1.get())==5 or len(entry1.get())==14)):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_barcode(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-A" and validate_barcode(upc_validate)==True):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_upca(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-E" and validate_barcode(upc_validate)==True):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_upce(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-13" and validate_barcode(upc_validate)==True):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_ean13(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-8" and validate_ean8(upc_validate)==True):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_ean8(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-2" and len(entry1.get())==2):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_ean2(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-5" and len(entry1.get())==5):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_ean5(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF" and not (len(entry1.get()) % 2) and len(entry1.get()) > 5):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_itf(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF-14" and not (len(entry1.get()) % 2) and len(entry1.get()) > 5):
  if(savefname!=""):
   savefname = ShowSaveDialog();
  create_itf14(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="Code 11" and len(entry1.get()) > 0 and re.findall("([0-9\-]+)", entry1.get())):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_code11(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="Code 39" and len(entry1.get()) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", entry1.get())):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_code39(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="Code 93" and len(entry1.get()) > 0 and re.findall("([0-9a-zA-Z\-\.\$\/\+% ]+)", entry1.get())):
  savefname = ShowSaveDialog();
  if(savefname!=""):
   create_code93(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
def SaveGeneratedBarcodeAlt(event):
 SaveGeneratedBarcode();
entry1.bind("<Return>", GenerateBarcodeAlt);
listbox1.bind("<Return>", GenerateBarcodeAlt);
magnify.bind("<Return>", GenerateBarcodeAlt);
entry2.bind("<Return>", GenerateBarcodeAlt);
entry3.bind("<Return>", GenerateBarcodeAlt);
button1 = Button(rootwin, text="Generate", command = GenerateBarcode);
if(sys.platform=="win32"):
 button1.place(x=0, y=274);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 button1.place(x=0, y=272);
button2 = Button(rootwin, text="Save As", command = SaveGeneratedBarcode);
if(sys.platform=="win32"):
 button2.place(x=60, y=274);
if(sys.platform=="linux" or sys.platform=="linux2" or sys.platform=="bsdos" or sys.platform=="freebsd" or sys.platform=="netbsd"):
 button2.place(x=90, y=272);
button1.bind("<Return>", GenerateBarcodeAlt);
button2.bind("<Return>", SaveGeneratedBarcodeAlt);
rootwin.mainloop();
