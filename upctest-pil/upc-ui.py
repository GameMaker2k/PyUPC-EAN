#!/usr/bin/env python

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2011-2012 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2011-2012 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2011-2012 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: upc-ui.py - Last Update: 10/04/2012 Ver. 2.0.0 - Author: cooldude2k $
'''

import os, sys, tempfile, upcean;
if(sys.version[0]=="2"):
 import Tkinter, tkMessageBox, tkFileDialog;
 from Tkinter import *;
if(sys.version[0]=="3"):
 import tkinter, messageBox, filedialog;
 from tkinter import *;
from upcean import *;
from PIL import Image, ImageTk;

updateimg = False;
rootwin = Tkinter.Tk();
rootwin.wm_title("PyUPC Test GUI");
rootwin.geometry(("%dx%d") % (350, 300));
# Code to add widgets will go here...

entry1 = Entry(rootwin);
entry1.place(x=40, y=132);
labeltxt1 = StringVar();
label1 = Label( rootwin, textvariable=labeltxt1);
labeltxt1.set("Value:");
label1.place(x=0, y=130);
listboxtxt1 = StringVar(rootwin);
listboxtxt1.set("Detect");
listbox1 = OptionMenu(rootwin, listboxtxt1, "Detect", "UPC-A", "UPC-E", "EAN-13", "EAN-8", "ITF", "ITF-14");
listbox1.place(x=60, y=164);
labeltxt2 = StringVar();
label2 = Label(rootwin, textvariable=labeltxt2);
labeltxt2.set("Symbology:");
label2.place(x=0, y=166);
magnify = Spinbox(rootwin, wrap=True, width=3, from_=1, to=10)
magnify.place(x=50, y=200);
labeltxt3 = StringVar();
label3 = Label(rootwin, textvariable=labeltxt3);
labeltxt3.set("Magnify:");
label3.place(x=0, y=197);

entrytxt2 = StringVar();
entry2 = Entry(rootwin, textvariable=entrytxt2);
entrytxt2.set("48");
entry2.place(x=70, y=225);
labeltxt4 = StringVar();
label4 = Label( rootwin, textvariable=labeltxt4);
labeltxt4.set("Bar 1 Height:");
label4.place(x=0, y=223);

entrytxt3 = StringVar();
entry3 = Entry(rootwin, textvariable=entrytxt3);
entrytxt3.set("54");
entry3.place(x=70, y=250);
labeltxt5 = StringVar();
label5 = Label( rootwin, textvariable=labeltxt5);
labeltxt5.set("Bar 2 Height:");
label5.place(x=0, y=248);

def GenerateBarcode():
 global updateimg, panel1, faddonsize;
 if(updateimg==True):
  panel1.destroy();
 (tmpfd, tmpfilename) = tempfile.mkstemp(".png");
 if(listboxtxt1.get()=="Detect"):
  validbc = create_barcode(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-A"):
  validbc = create_upca(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-E"):
  validbc = create_upce(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-13"):
  validbc = create_ean13(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-8"):
  validbc = create_ean8(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF"):
  validbc = create_itf(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF-14"):
  validbc = create_itf14(entry1.get(),tmpfilename,"2",(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(validbc==True):
  image1 = ImageTk.PhotoImage(Image.open(tmpfilename));
  panel1 = Tkinter.Label(rootwin, image=image1);
  panel1.place(x=0, y=0);
  panel1.image = image1;
  updateimg = True;
 os.close(tmpfd);
 os.remove(tmpfilename);

def SaveGeneratedBarcode():
 savefname=tkFileDialog.asksaveasfilename(parent=rootwin,title='Choose a file',filetypes=[('Windows Bitmap','*.bmp'), ('Portable Network Graphics','*.png'), ('JPEG / JFIF','*.jpg'), ('CompuServer GIF','*.gif')]);
 if(listboxtxt1.get()=="Detect"):
  create_barcode(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-A"):
  create_upca(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="UPC-E"):
  create_upce(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-13"):
  create_ean13(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="EAN-8"):
  create_ean8(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF"):
  create_itf(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));
 if(listboxtxt1.get()=="ITF-14"):
  create_itf14(entry1.get(),savefname,magnify.get(),(False, False, False),(int(entry2.get()),int(entry3.get())));

button1 = Tkinter.Button(rootwin, text="Generate", command = GenerateBarcode);
button1.place(x=0, y=274);
button2 = Tkinter.Button(rootwin, text="Save As", command = SaveGeneratedBarcode);
button2.place(x=60, y=274);

rootwin.mainloop();
