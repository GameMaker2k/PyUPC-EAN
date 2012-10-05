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

    $FileInfo: upc.py - Last Update: 10/04/2012 Ver. 2.0.0 - Author: cooldude2k $
'''

import sys, traceback, code, re, readline, upcean;
from sys import argv;
from upcean import *;

taskfound=False;
if(len(sys.argv)<2):
 taskfound=True;
 ps1="PyShell "+str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])+"> ";
 cmdinput=None;
 print("PyShell "+sys.version+" on "+sys.platform+"\nLoaded Python module upcean "+upcean.__version__+"\n");
 while(True):
  if(sys.version_info[0]==2):
   try:
    cmdinput = raw_input(ps1);
   except KeyboardInterrupt:
    print("\nKeyboardInterrupt");
   except EOFError:
    print("");
    sys.exit(0);
   except Exception:
    traceback.print_exc();
  if(sys.version_info[0]==3):
   try:
    cmdinput = input(ps1);
   except KeyboardInterrupt:
    print("\nKeyboardInterrupt");
   except EOFError:
    print("");
    sys.exit(0);
   except Exception:
    traceback.print_exc();
  ## exec(str(cmdinput));
  try:
   exec(code.compile_command(str(cmdinput)));
  except Exception:
   traceback.print_exc();
 sys.exit(0);

if(sys.argv[1]=="sh" or sys.argv[1]=="shell" or sys.argv[1]=="pysh" or sys.argv[1]=="pyshell" or sys.argv[1]=="python"):
 taskfound=True;
 ps1="PyShell "+str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])+"> ";
 cmdinput=None;
 print("PyShell "+sys.version+" on "+sys.platform+"\nLoaded Python module upcean "+upcean.__version__+"\n");
 while(True):
  if(sys.version_info[0]==2):
   try:
    cmdinput = raw_input(ps1);
   except KeyboardInterrupt:
    print("\nKeyboardInterrupt");
   except EOFError:
    print("");
    sys.exit(0);
   except Exception:
    traceback.print_exc();
  if(sys.version_info[0]==3):
   try:
    cmdinput = input(ps1);
   except KeyboardInterrupt:
    print("\nKeyboardInterrupt");
   except EOFError:
    print("");
    sys.exit(0);
   except Exception:
    traceback.print_exc();
  ## exec(str(cmdinput));
  try:
   exec(code.compile_command(str(cmdinput)));
  except Exception:
   traceback.print_exc();
 sys.exit(0);

if(sys.argv[1]=="shebang" or sys.argv[1]=="shabang" or sys.argv[1]=="hashbang" or sys.argv[1]=="poundbang" or sys.argv[1]=="hashexclam" or sys.argv[1]=="hashpling"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 shebang = "".join(open(sys.argv[2], "r").readlines());
 exec(compile(str(shebang), "", "exec"));
 sys.exit(0);

if(sys.argv[1]=="check"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
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
  sys.exit(0);
 if(len(sys.argv[2])>7 and len(sys.argv[2])<11):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="validate"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
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
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="fix"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
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
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="convert"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments;"));
  sys.exit(0);
 if(len(sys.argv[3])==8):
  if(len(sys.argv)<4):
   print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
   sys.exit(0);
  if(sys.argv[2]=="upca"):
   print(str(convert_upce_to_upca(argv[3])));
  if(sys.argv[2]=="ean13"):
   print(str(convert_upce_to_ean13(argv[3])));
  if(sys.argv[2]=="itf14"):
   print(str(convert_upce_to_itf14(argv[3])));
 if(len(sys.argv[3])==12):
  if(len(sys.argv)<4):
   print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
   sys.exit(0);
  if(sys.argv[2]=="upce"):
   print(str(convert_upca_to_upce(argv[3])));
  if(sys.argv[2]=="ean13"):
   print(str(convert_upca_to_ean13(argv[3])));
  if(sys.argv[2]=="itf14"):
   print(str(convert_upca_to_itf14(argv[3])));
 if(len(sys.argv[3])==13):
  if(len(sys.argv)<4):
   print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
   sys.exit(0);
  if(sys.argv[2]=="upce"):
   print(str(convert_ean13_to_upce(argv[3])));
  if(sys.argv[2]=="upca"):
   print(str(convert_ean13_to_upca(argv[3])));
  if(sys.argv[2]=="itf14"):
   print(str(convert_ean13_to_itf14(argv[3])));
 if(len(sys.argv[3])==14):
  if(len(sys.argv)<4):
   print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
   sys.exit(0);
  if(sys.argv[2]=="upce"):
   print(str(convert_itf14_to_upce(argv[3])));
  if(sys.argv[2]=="upca"):
   print(str(convert_itf14_to_upca(argv[3])));
  if(sys.argv[2]=="ean13"):
   print(str(convert_itf14_to_ean13(argv[3])));
 if(len(sys.argv[3])<8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[3])>8 and len(sys.argv[3])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[3])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="getprefix" or sys.argv[1]=="getgs1"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
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
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="getnsprefix" or sys.argv[1]=="getns"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==8):
  print(str(get_upca_ns(convert_upce_to_upca(argv[2]))));
 if(len(sys.argv[2])==12):
  print(str(get_upca_ns(argv[2])));
 if(len(sys.argv[2])==13):
  print(str(get_upca_ns(convert_ean13_to_upca(argv[2]))));
 if(len(sys.argv[2])==14):
  print(str(get_upca_ns(convert_itf14_to_upca(argv[2]))));
 if(len(sys.argv[2])<8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="getitf14type" or sys.argv[1]=="itf14type"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==8):
  print(str(get_itf14_type(convert_upce_to_itf14(argv[2]))));
 if(len(sys.argv[2])==12):
  print(str(get_itf14_type(convert_upca_to_itf14(argv[2]))));
 if(len(sys.argv[2])==13):
  print(str(get_itf14_type(convert_ean13_to_itf14(argv[2]))));
 if(len(sys.argv[2])==14):
  print(str(get_itf14_type(argv[2])));
 if(len(sys.argv[2])<8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="getvw" or sys.argv[1]=="getvwinfo"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==12):
  vwinfo = get_upca_vw_info(argv[2]);
  print("Code: "+vwinfo['code']);
  print("Price: "+vwinfo['price']);
 if(len(sys.argv[2])==13):
  vwinfo = get_upca_vw_info(convert_ean13_to_upca(argv[2]));
  print("Code: "+vwinfo['code']);
  print("Price: "+vwinfo['price']);
 if(len(sys.argv[2])==14):
  vwinfo = get_upca_vw_info(convert_itf14_to_upca(argv[2]));
  print("Code: "+vwinfo['code']);
  print("Price: "+vwinfo['price']);
 if(len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>12 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="getcoupon" or sys.argv[1]=="getcouponinfo"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==12):
  couponinfo = get_upca_coupon_info(argv[2]);
  print("Manufacturer: "+couponinfo['manufacturer']);
  print("Family: "+couponinfo['family']);
  print("Value 1: "+couponinfo['value']);
  print("Value 2: "+get_upca_coupon_value_code(couponinfo['value']));
 if(len(sys.argv[2])==13):
  couponinfo = get_upca_coupon_info(convert_ean13_to_upca(argv[2]));
  print("Manufacturer: "+couponinfo['manufacturer']);
  print("Family: "+couponinfo['family']);
  print("Value 1: "+couponinfo['value']);
  print("Value 2: "+get_upca_coupon_value_code(couponinfo['value']));
 if(len(sys.argv[2])==14):
  couponinfo = get_upca_coupon_info(convert_itf14_to_upca(argv[2]));
  print("Manufacturer: "+couponinfo['manufacturer']);
  print("Family: "+couponinfo['family']);
  print("Value 1: "+couponinfo['value']);
  print("Value 2: "+get_upca_coupon_value_code(couponinfo['value']));
 if(len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>12 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genvw" or sys.argv[1]=="mkvw" or sys.argv[1]=="makevw"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==5):
  if(len(sys.argv[2])<5 or len(sys.argv[2])>5):
   print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
   sys.exit(0);
  if(len(sys.argv[3])==4):
   if(len(sys.argv[2])<5 or len(sys.argv[2])>5):
    print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+"\nerror: syntax error missing arguments"));
    sys.exit(0);
   print(str(make_vw_upca(sys.argv[2], sys.argv[3])));

if(sys.argv[1]=="gencoupon" or sys.argv[1]=="mkcoupon" or sys.argv[1]=="makecoupon"):
 taskfound=True;
 if(len(sys.argv)<5):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])<1 or len(sys.argv[2])>1):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(int(sys.argv[2])!=5 and int(sys.argv[2])!=9):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[3])<5 or len(sys.argv[3])>5):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[4])<3 or len(sys.argv[4])> 3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[5])<2 or len(sys.argv[5])>2):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+" "+sys.argv[3]+" "+sys.argv[4]+" "+sys.argv[5]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==1):
  if(len(sys.argv[3])==5):
   if(len(sys.argv[4])==3):
    if(len(sys.argv[5])==2):
     print(str(make_coupon_upca(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])));

if(sys.argv[1]=="genupca" or sys.argv[1]=="mkupca" or sys.argv[1]=="makeupca" or sys.argv[1]=="genupc" or sys.argv[1]=="mkupc" or sys.argv[1]=="makeupc"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==8):
  sys.argv[2] = convert_upce_to_upca(sys.argv[2]);
 if(len(sys.argv[2])==11):
  sys.argv[2] = fix_upca_checksum(argv[2]);
 if(len(sys.argv[2])==12):
  create_upca(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2])<12 or len(sys.argv[2])>12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genupce" or sys.argv[1]=="mkupce" or sys.argv[1]=="makeupce"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==12):
  sys.argv[2] = convert_upca_to_upce(sys.argv[2]);
 if(len(sys.argv[2])==7):
  sys.argv[2] = fix_upce_checksum(argv[2]);
 if(len(sys.argv[2])==8):
  create_upce(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2])<8 or len(sys.argv[2])>8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genean13" or sys.argv[1]=="mkean13" or sys.argv[1]=="makeean13" or sys.argv[1]=="genean" or sys.argv[1]=="mkean" or sys.argv[1]=="makeean"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==8):
  sys.argv[2] = convert_upce_to_ean13(sys.argv[2]);
 if(len(sys.argv[2])==12):
  sys.argv[2] = fix_ean13_checksum(argv[2]);
 if(len(sys.argv[2])==13):
  create_ean13(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2])<13 or len(sys.argv[2])>13):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genean8" or sys.argv[1]=="mkean8" or sys.argv[1]=="makeean8"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==13):
  sys.argv[2] = fix_itf14_checksum(argv[2]);
 if(len(sys.argv[2])==8):
  create_ean8(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2])<8 or len(sys.argv[2])>8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genitf" or sys.argv[1]=="mkitf" or sys.argv[1]=="makeitf"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(not len(sys.argv[2]) % 2 and len(sys.argv[2]) > 6):
  create_itf(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2]) % 2 or len(sys.argv[2]) < 6):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genitf14" or sys.argv[1]=="mkitf14" or sys.argv[1]=="makeitf14"):
 taskfound=True;
 if(sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(not len(sys.argv[2]) % 2 and len(sys.argv[2]) > 6):
  create_itf14(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2]) % 2 or len(sys.argv[2]) < 6):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="gencode39" or sys.argv[1]=="mkcode39" or sys.argv[1]=="makecode39"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2]) > 1):
  create_code39(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2]) < 1):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="gencode93" or sys.argv[1]=="mkcode93" or sys.argv[1]=="makecode93"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2]) > 1):
  create_code93(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2]) < 1):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genbarcode" or sys.argv[1]=="mkbarcode" or sys.argv[1]=="makebarcode"):
 taskfound=True;
 if(len(sys.argv)<5 or sys.argv[4]==None):
  sys.argv.append(1);
 if(len(sys.argv)<4):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])==8 or len(sys.argv[2])==12 or len(sys.argv[2])==13 or len(sys.argv[2])==14):
  create_barcode(sys.argv[2],sys.argv[3],sys.argv[4],(False, False, False),(48, 54));
 if(len(sys.argv[2])<8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>8 and len(sys.argv[2])<12):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 if(len(sys.argv[2])>14):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genissn13" or sys.argv[1]=="mkissn13" or sys.argv[1]=="makeissn13"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 sys.argv[2] = sys.argv[2].replace("-", "");
 sys.argv[2] = sys.argv[2].replace(" ", "");
 if(len(sys.argv[2])==8):
  print(str(convert_issn8_to_issn13(argv[2])));
 if(len(sys.argv[2])>8 and len(sys.argv[2])<8):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genisbn13" or sys.argv[1]=="mkisbn13" or sys.argv[1]=="makeisbn13"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 sys.argv[2] = sys.argv[2].replace("-", "");
 sys.argv[2] = sys.argv[2].replace(" ", "");
 if(len(sys.argv[2])==10):
  print(str(convert_isbn10_to_isbn13(argv[2])));
 if(len(sys.argv[2])>10 and len(sys.argv[2])<10):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="genismn13" or sys.argv[1]=="mkismn13" or sys.argv[1]=="makeismn13"):
 taskfound=True;
 if(len(sys.argv)<3):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
  sys.exit(0);
 sys.argv[2] = sys.argv[2].replace("M", "");
 sys.argv[2] = sys.argv[2].replace("-", "");
 sys.argv[2] = sys.argv[2].replace(" ", "");
 if(len(sys.argv[2])==9):
  print(str(convert_ismn10_to_ismn13(argv[2])));
 if(len(sys.argv[2])>9 and len(sys.argv[2])<9):
  print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+" "+sys.argv[2]+"\nerror: syntax error missing arguments"));
  sys.exit(0);

if(sys.argv[1]=="exec" or sys.argv[1]=="run" or sys.argv[1]=="execute"):
 taskfound=True;
 argcmd = list(sys.argv);
 argcmd[0:1] = [];
 argcmd = list(argcmd);
 argcmd[0:1] = [];
 argcmd = list(argcmd);
 argcmd = " ".join(argcmd);
 exec(argcmd);

if(taskfound==False):
 print(str("command: "+sys.argv[0]+"\narguments: "+sys.argv[1]+"\nerror: syntax error missing arguments"));
 sys.exit(0);
