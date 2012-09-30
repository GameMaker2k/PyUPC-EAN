#!/usr/bin/env python

import sys, re, upcean;
from sys import argv;
from upcean import *;

taskfound=False;
if(len(sys.argv)<2):
	taskfound=True;
	print(str("command: "+sys.argv[0]+"\nerror: syntax error missing arguments"));
	quit();
if(sys.argv[1]=="check"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==7):
		print(str(fix_upce_checksum(argv[2])));
	if(len(sys.argv[2])==11):
		print(str(fix_upca_checksum(argv[2])));
	if(len(sys.argv[2])==12):
		print(str(fix_ean13_checksum(argv[2])));
	if(len(sys.argv[2])==13):
		print(str(fix_itf14_checksum(argv[2])));
	if(len(sys.argv[2])<7):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>7 and len(sys.argv[2])<11):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="validate"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8):
		print(str(validate_upce(argv[2])));
	if(len(sys.argv[2])==12):
		print(str(validate_upca(argv[2])));
	if(len(sys.argv[2])==13):
		print(str(validate_ean13(argv[2])));
	if(len(sys.argv[2])==14):
		print(str(validate_itf14(argv[2])));
	if(len(sys.argv[2])<8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="fix"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8):
		print(str(fix_upce_checksum(argv[2])));
	if(len(sys.argv[2])==12):
		print(str(fix_upca_checksum(argv[2])));
	if(len(sys.argv[2])==13):
		print(str(fix_ean13_checksum(argv[2])));
	if(len(sys.argv[2])==14):
		print(str(fix_itf14_checksum(argv[2])));
	if(len(sys.argv[2])<8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="convert"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments;"));
		quit();
	if(len(sys.argv[3])==8):
		if(len(sys.argv)<4):
			print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
			quit();
		if(sys.argv[2]=="upca"):
			print(str(convert_upce_to_upca(argv[3])));
		if(sys.argv[2]=="ean13"):
			print(str(convert_upce_to_ean13(argv[3])));
		if(sys.argv[2]=="itf14"):
			print(str(convert_upce_to_itf14(argv[3])));
	if(len(sys.argv[3])==12):
		if(len(sys.argv)<4):
			print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
			quit();
		if(sys.argv[2]=="upce"):
			print(str(convert_upca_to_upce(argv[3])));
		if(sys.argv[2]=="ean13"):
			print(str(convert_upca_to_ean13(argv[3])));
		if(sys.argv[2]=="itf14"):
			print(str(convert_upca_to_itf14(argv[3])));
	if(len(sys.argv[3])==13):
		if(len(sys.argv)<4):
			print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
			quit();
		if(sys.argv[2]=="upce"):
			print(str(convert_ean13_to_upce(argv[3])));
		if(sys.argv[2]=="upca"):
			print(str(convert_ean13_to_upca(argv[3])));
		if(sys.argv[2]=="itf14"):
			print(str(convert_ean13_to_itf14(argv[3])));
	if(len(sys.argv[3])==14):
		if(len(sys.argv)<4):
			print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
			quit();
		if(sys.argv[2]=="upce"):
			print(str(convert_itf14_to_upce(argv[3])));
		if(sys.argv[2]=="upca"):
			print(str(convert_itf14_to_upca(argv[3])));
		if(sys.argv[2]=="ean13"):
			print(str(convert_itf14_to_ean13(argv[3])));
	if(len(sys.argv[3])<8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[3])>8 and len(sys.argv[3])<12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[3])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="getprefix" or sys.argv[1]=="getgs1"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8):
		print(str(get_gs1_prefix(convert_upce_to_ean13(argv[2]))));
	if(len(sys.argv[2])==12):
		print(str(get_gs1_prefix(convert_upca_to_ean13(argv[2]))));
	if(len(sys.argv[2])==13):
		print(str(get_gs1_prefix(argv[2])));
	if(len(sys.argv[2])==14):
		print(str(get_gs1_prefix(convert_itf14_to_ean13(argv[2]))));
	if(len(sys.argv[2])<8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genvw" or sys.argv[1]=="mkvw" or sys.argv[1]=="makevw"):
	taskfound=True;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==5):
		if(len(sys.argv[2])<5 or len(sys.argv[2])>5):
			print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
			quit();
		if(len(sys.argv[3])==4):
			if(len(sys.argv[2])<5 or len(sys.argv[2])>5):
				print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+"\nerror: syntax error missing arguments"));
				quit();
			print(str(make_vw_upca(sys.argv[2], sys.argv[3])));

if(sys.argv[1]=="genupca" or sys.argv[1]=="mkupca" or sys.argv[1]=="makeupca"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8):
		sys.argv[2] = convert_upce_to_upca(sys.argv[2]);
	if(len(sys.argv[2])==11):
		sys.argv[2] = fix_upca_checksum(argv[2]);
	if(len(sys.argv[2])==12):
		create_upca(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2])<12 or len(sys.argv[2])>12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genupce" or sys.argv[1]=="mkupce" or sys.argv[1]=="makeupce"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==12):
		sys.argv[2] = convert_upca_to_upce(sys.argv[2]);
	if(len(sys.argv[2])==7):
		sys.argv[2] = fix_upce_checksum(argv[2]);
	if(len(sys.argv[2])==8):
		create_upce(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2])<8 or len(sys.argv[2])>8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genean13" or sys.argv[1]=="mkean13" or sys.argv[1]=="makeean13"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8):
		sys.argv[2] = convert_upce_to_ean13(sys.argv[2]);
	if(len(sys.argv[2])==12):
		sys.argv[2] = fix_ean13_checksum(argv[2]);
	if(len(sys.argv[2])==13):
		create_ean13(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2])<13 or len(sys.argv[2])>13):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genean8" or sys.argv[1]=="mkean8" or sys.argv[1]=="makeean8"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==13):
		sys.argv[2] = fix_itf14_checksum(argv[2]);
	if(len(sys.argv[2])==8):
		create_ean8(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2])<8 or len(sys.argv[2])>8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genitf" or sys.argv[1]=="mkitf" or sys.argv[1]=="makeitf"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(not len(sys.argv[2]) % 2 and len(sys.argv[2]) > 6):
		create_itf(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2]) % 2 or len(sys.argv[2]) < 6):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genitf14" or sys.argv[1]=="mkitf14" or sys.argv[1]=="makeitf14"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(not len(sys.argv[2]) % 2 and len(sys.argv[2]) > 6):
		create_itf14(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2]) % 2 or len(sys.argv[2]) < 6):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="gencode39" or sys.argv[1]=="mkcode39" or sys.argv[1]=="makecode39"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2]) > 1):
		create_code39(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2]) < 1):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="gencode93" or sys.argv[1]=="mkcode93" or sys.argv[1]=="makecode93"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<4):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2]) > 1):
		create_code93(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2]) < 1):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(sys.argv[1]=="genbarcode" or sys.argv[1]=="mkbarcode" or sys.argv[1]=="makebarcode"):
	taskfound=True;
	if(sys.argv[4]==None):
		sys.argv[4] = 1;
	if(len(sys.argv)<3):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])==8 or len(sys.argv[2])==12 or len(sys.argv[2])==13 or len(sys.argv[2])==14):
		create_barcode(sys.argv[2],sys.argv[3],sys.argv[4],False);
	if(len(sys.argv[2])<8):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();
	if(len(sys.argv[2])>14):
		print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
		quit();

if(taskfound==False):
	print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
	quit();
