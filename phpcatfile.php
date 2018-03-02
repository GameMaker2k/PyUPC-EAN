<?php
/*
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2018 Cool Dude 2k - http://idb.berlios.de/
    Copyright 2018 Game Maker 2k - http://intdb.sourceforge.net/
    Copyright 2018 Kazuki Przyborowski - https://github.com/KazukiPrzyborowski

    $FileInfo: phpcatfile.php - Last Update: 3/1/2018 Ver. 0.0.1 RC 1 - Author: cooldude2k $
*/

date_default_timezone_set('UTC');

$info['program_name'] = "PHPCatFile";
$info['project'] = $info['program_name'];
$info['project_url'] = "https://github.com/GameMaker2k/PyCatFile";
$info['version_info'] = array(0 => 0, 1 => 0, 2 => 1, 3 => "RC 1", 4 => 1);
$info['version_date_info'] = array(0 => 2018, 1 => 3, 2 => 1, 3 => "RC 1", 1);
$info['version_date'] = $info['version_date_info'][0].".".str_pad($info['version_date_info'][1], 2, "-=", STR_PAD_LEFT).".".str_pad($info['version_date_info'][2], 2, "-=", STR_PAD_LEFT);
if($info['version_info'][4]!==null):
 $info['version_date_plusrc'] = $info['version_date']."-".$info['version_date_info'][4];
if($info['version_info'][4]===null):
 $info['version_date_plusrc'] = $info['version_date'];
if($info['version_info'][3]!==null):
 $info['version'] = $info['version_info'][0].".".$info['version_info'][1].".".$info['version_info'][2]." ".$info['version_info'][3];
if($info['version_info'][3]===null):
 $info['version'] = $info['version_info'][0].".".$info['version_info'][1].".".$info['version_info'][2];

function RemoveWindowsPath($dpath) {
 if(DIRECTORY_SEPARATOR=="\\") {
  $dpath = str_replace(DIRECTORY_SEPARATOR, "/", $dpath); }
 $dpath = rtrim($dpath, '/');
 if($dpath=="." or $dpath==".."):
  $dpath = $dpath."/";
 return $dpath; }

function ListDir($dirname) {
 if(DIRECTORY_SEPARATOR=="\\") {
  $dirname = str_replace(DIRECTORY_SEPARATOR, "/", $dirname); }
 $fulllist[] = $dirname;
 if(is_dir($dirname)) {
  if($dh = opendir($dirname)) {
   while(($file = readdir($dh)) !== false) {
    if($file!="." && $file!=".." && is_dir($dirname."/".$file)) {
     $fulllistnew = ListDir($dirname."/".$file);
     foreach($fulllistnew as $fulllistary) {
      $fulllist[] = $fulllistary; } }
    if(!is_dir($dirname."/".$file)) {
     $fulllist[] = $dirname."/".$file; } } }
    closedir($dh); }
 return $fulllist; }

function ReadTillNullByte($fp) {
 $curbyte = "";
 $curfullbyte = "";
 $nullbyte = "\0";
 while($curbyte!=$nullbyte) {
  $curbyte = fread($fp, 1);
  if($curbyte!=$nullbyte) {
   $curbyted = $curbyte;
   $curfullbyte = $curfullbyte.$curbyted; } }
 return $curfullbyte; }

function ReadUntilNullByte($fp) {
 return ReadTillNullByte($fp); }

function ReadFileHeaderData($fp, $rounds=0) {
 $rocount = 0;
 $roend = intval($rounds);
 $HeaderOut = array();
 while($rocount<$roend) {
  $HeaderOut[$rocount] = ReadTillNullByte($fp);
  $rocount = $rocount + 1; }
 return $HeaderOut; }

function AppendNullByte($indata):
 $outdata = $indata."\0";
 return $outdata;

function PHPCatFile($infiles, $outfile, $verbose=false) {
 global $info;
 $phpcatver = $info['version_info'][0].".".$info['version_info'][1].".".$info['version_info'][2];
 $infiles = RemoveWindowsPath($infiles);
 $outfile = RemoveWindowsPath($outfile);
 if(file_exists($outfile)) {
  unlink($outfile); }
 $catfp = fopen($outfile, "wb");
 $fileheaderver = intval(str_replace(".", "", $phpcatver));
 $fileheader = AppendNullByte("CatFile".$fileheaderver);
 fwrite($catfp, $fileheader);
 $GetDirList = ListDir($infiles);
 foreach($GetDirList as $curfname) {
  $fname = $curfname;
  if($verbose===true) {
   print($fname."\n"); }
  $fstatinfo = lstat($fname);
  $ftype = 0;
  if(is_file($fname)) {
   $ftype = 0; }
  if(is_link($fname)) {
   $ftype = 2; }
  if(is_dir($fname)) {
   $ftype = 5; }
  if($ftype==1 || $ftype==2 || $ftype==5) {
   $fsize = strtoupper(dechex(intval("0"))); }
  if($ftype==0) {
   $fsize = strtoupper(dechex(intval($fstatinfo['size']))); }
  $flinkname = "";
  if($ftype==1 || $ftype==2) {
   $flinkname = readlink($fname); }
  $fatime = strtoupper(dechex(intval($fstatinfo['atime'])));
  $fmtime = strtoupper(dechex(intval($fstatinfo['mtime'])));
  $fmode = strtoupper(dechex(intval($fstatinfo['mode'])));
  $fuid = strtoupper(dechex(intval($fstatinfo['uid'])));
  $fgid = strtoupper(dechex(intval($fstatinfo['gid'])));
  $fdev_minor = strtoupper(dechex(intval(0)));
  $fdev_major = strtoupper(dechex(intval(0)));
  $frdev_minor = strtoupper(dechex(intval(0)));
  $frdev_major = strtoupper(dechex(intval(0)));
  $fcontents = "";
  if($ftype==0) {
   $fpc = fopen($fname, "rb");
   $fcontents = fread($fpc, intval($fstatinfo['size']));
   fclose($fpc); }
  $ftypehex = strtoupper(dechex($ftype));
  $ftypeoutstr = $ftypehex;
  $catfileoutstr = AppendNullByte($ftypeoutstr);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fname);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fsize);
  $catfileoutstr = $catfileoutstr.AppendNullByte($flinkname);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fatime);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fmtime);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fmode);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fuid);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fgid);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fdev_minor);
  $catfileoutstr = $catfileoutstr.AppendNullByte($fdev_major);
  $catfileoutstr = $catfileoutstr.AppendNullByte($frdev_minor);
  $catfileoutstr = $catfileoutstr.AppendNullByte($frdev_major);
  $catfileheadercshex = strtoupper(dechex(crc32($catfileoutstr)));
  $catfileoutstr = $catfileoutstr.AppendNullByte($catfileheadercshex);
  $catfileoutstrecd = $catfileoutstr;
  $nullstrecd = "\0";
  $catfileout = $catfileoutstrecd.$fcontents.$nullstrecd;
  fwrite($catfp, $catfileout); }
 fclose($catfp);
 return true; }

function PHPCatToArray($infile, $seekstart=0, $seekend=0, $listonly=false) {
 $infile = RemoveWindowsPath($infile);
 $catfp = fopen($infile, "rb");
 fseek($catfp, 0, SEEK_END);
 $CatSize = ftell($catfp);
 $CatSizeEnd = $CatSize;
 fseek($catfp, 0, SEEK_SET);
 $phpcatstring = ReadFileHeaderData($catfp, 1)[0];
 $phpcatlist = array();
 $fileidnum = 0;
 if($seekstart!=0) {
  fseek($catfp, $seekstart, SEEK_SET); }
 if($seekstart==0) {
  $seekstart = ftell($catfp); }
 if($seekend==0) {
  $seekend = $CatSizeEnd; }
 while($seekstart<$seekend) {
  $phpcatfhstart = ftell($catfp);
  $phpcatheaderdata = ReadFileHeaderData($catfp, 14);
  $phpcatftype = hexdec($phpcatheaderdata[0]);
  $phpcatfname = $phpcatheaderdata[1];
  $phpcatfsize = hexdec($phpcatheaderdata[2]);
  $phpcatflinkname = $phpcatheaderdata[3];
  $phpcatfatime = hexdec($phpcatheaderdata[4]);
  $phpcatfmtime = hexdec($phpcatheaderdata[5]);
  $phpcatfmode = decoct(hexdec($phpcatheaderdata[6]));
  $phpcatfchmod = substr($phpcatfmode, -3);
  $phpcatfuid = hexdec($phpcatheaderdata[7]);
  $phpcatfgid = hexdec($phpcatheaderdata[8]);
  $phpcatfdev_minor = hexdec($phpcatheaderdata[9]);
  $phpcatfdev_major = hexdec($phpcatheaderdata[10]);
  $phpcatfrdev_minor = hexdec($phpcatheaderdata[11]);
  $phpcatfrdev_major = hexdec($phpcatheaderdata[12]);
  $phpcatfcs = hexdec($phpcatheaderdata[13]);
  $hc = 0;
  $hcmax = strlen($phpcatheaderdata) - 1;
  $hout = "";
  while($hc<$hcmax) {
   $hout = $hout.AppendNullByte($phpcatheaderdata[$hc]);
   $hc = $hc + 1; }
  $phpcatnewfcs = crc32(hout);
  if($phpcatfcs!=$phpcatnewfcs):
   print("Checksum Error with file "+$phpcatfname+" at offset "+$phpcatfhstart);
   return false;
  $phpcatfhend = ftell($catfp) - 1;
  $phpcatfcontentstart = ftell($catfp);
  $phpcatfcontents = "";
  $phphascontents = false;
  if($phpcatfsize>1 && $listonly===false) {
   $phpcatfcontents = fread($catfp, $phpcatfsize); 
   $phphascontents = true; }
  if($phpcatfsize>1 && $listonly===true) {
   fseek($catfp, $phpcatfsize, SEEK_CUR); 
   $phphascontents = false; }
  $phpcatfcontentend = ftell($catfp);
  $phpcatlist[$fileidnum] = array('fid' => $fileidnum, 'fhstart' => $phpcatfhstart, 'fhend' => $phpcatfhend, 'ftype' => $phpcatftype, 'fname' => $phpcatfname, 'fsize' => $phpcatfsize, 'flinkname' => $phpcatflinkname, 'fatime' => $phpcatfatime, 'fmtime' => $phpcatfmtime, 'fmode' => $phpcatfmode, 'fchmod' => $phpcatfchmod, 'fuid' => $phpcatfuid, 'fgid' => $phpcatfgid, 'fminor' => $phpcatfdev_minor, 'fmajor' => $phpcatfdev_major, 'fchecksum' => $phpcatfcs, 'fhascontents' => $phphascontents, 'fcontentstart' => $phpcatfcontentstart, 'fcontentend' => $phpcatfcontentend, 'fcontents' => $phpcatfcontents);
  fseek($catfp, 1, SEEK_CUR);
  $seekstart = ftell($catfp);
  $fileidnum = $fileidnum + 1; }
 fclose($catfp);
 return $phpcatlist; }

function PHPCatArrayIndex($infile, $seekstart=0, $seekend=0, $listonly=false) {
 $infile = RemoveWindowsPath($infile);
 $listcatfiles = PHPCatToArray($infile, $seekstart, $seekend, false);
 $phpcatarray = array('list': $listcatfiles, 'filetoid' => array(), 'idtofile' => array(), 'filetypes' => array('directories' => array('filetoid' => array(), 'idtofile' => array()), 'files' => array('filetoid' => array(), 'idtofile' => array()), 'links' => array('filetoid' => array(), 'idtofile' => array()), 'symlinks' => array('filetoid' => array(), 'idtofile' => array()), 'hardlinks' => array('filetoid' => array(), 'idtofile' => array()), 'character' => array('filetoid' => array(), 'idtofile' => array()), 'block' => array('filetoid' => array(), 'idtofile' => array()), 'fifo' => array('filetoid' => array(), 'idtofile' => array()), 'devices' => array('filetoid' => array(), 'idtofile' => array())));
 $lcfi = 0;
 $lcfx = count($listcatfiles);
 while($lcfi<$lcfx) {
  $fname = $listcatfiles[$lcfi]['fname'];
  $fid = $listcatfiles[$lcfi]['fid'];
  $phpcatarray['filetoid'][$fname] = $fid;
  $phpcatarray['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==0):
   $phpcatarray['filetypes']['files']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['files']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==1):
   $phpcatarray['filetypes']['hardlinks']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['hardlinks']['idtofile'][$fid] = $fname;
   $phpcatarray['filetypes']['links']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['links']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==2):
   $phpcatarray['filetypes']['symlinks']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['symlinks']['idtofile'][$fid] = $fname;
   $phpcatarray['filetypes']['links']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['links']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==3):
   $phpcatarray['filetypes']['character']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['character']['idtofile'][$fid] = $fname;
   $phpcatarray['filetypes']['devices']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['devices']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==4):
   $phpcatarray['filetypes']['block']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['block']['idtofile'][$fid] = $fname;
   $phpcatarray['filetypes']['devices']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['devices']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==5):
   $phpcatarray['filetypes']['directories']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['directories']['idtofile'][$fid] = $fname;
  if($listcatfiles[$lcfi]['ftype']==6):
   $phpcatarray['filetypes']['fifo']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['fifo']['idtofile'][$fid] = $fname;
   $phpcatarray['filetypes']['devices']['filetoid'][$fname] = $fid;
   $phpcatarray['filetypes']['devices']['idtofile'][$fid] = $fname;
  $lcfi = $lcfi + 1; }
 return $phpcatarray; }

function PHPUnCatFile($infile, $outdir=null, $verbose=False) {
 $infile = RemoveWindowsPath($infile);
 if($outdir!==null) {
  $outdir = RemoveWindowsPath($outdir); }
 $listcatfiles = PHPCatToArray($infile, 0, 0, false);
 if($listcatfiles==false) {
  return false; }
 $lcfi = 0;
 $lcfx = count($listcatfiles);
 while($lcfi<$lcfx) {
  if($verbose===true) {
   print($listcatfiles[$lcfi]['fname']."\n"); }
  if($listcatfiles[$lcfi]['ftype']==0) {
   $fpc = fopen($listcatfiles[$lcfi]['fname'], "wb");
   fwrite($fpc, $listcatfiles[$lcfi]['fcontents']);
   fclose($fpc);
   chown($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fuid']);
   chgrp($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fgid']);
   chmod($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fchmod']);
   touch($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fmtime'], $listcatfiles[$lcfi]['fatime']); }
  if($listcatfiles[$lcfi]['ftype']==1) {
   link($listcatfiles[$lcfi]['flinkname'], $listcatfiles[$lcfi]['fname']); }
  if($listcatfiles[$lcfi]['ftype']==2) {
   symlink($listcatfiles[$lcfi]['flinkname'], $listcatfiles[$lcfi]['fname']); }
  if($listcatfiles[$lcfi]['ftype']==5) {
   mkdir($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fchmod']);
   chown($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fuid']);
   chgrp($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fgid']);
   chmod($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fchmod']);
   touch($listcatfiles[$lcfi]['fname'], $listcatfiles[$lcfi]['fmtime'], $listcatfiles[$lcfi]['fatime']); }
  $lcfi = $lcfi + 1; }
 return true; }

function PHPCatListFiles($infile, $seekstart=0, $seekend=0, $verbose=false) {
 $infile = RemoveWindowsPath($infile);
 $listcatfiles = PHPCatToArray($infile, $seekstart, $seekend, true);
 if($listcatfiles==false) {
  return false; }
 $lcfi = 0;
 $lcfx = count($listcatfiles);
 while($lcfi<$lcfx) {
  if($verbose===false) {
   print($listcatfiles[$lcfi]['fname']."\n"); }
  if($verbose===true) {
   $permissionstr = "";
   if($listcatfiles[$lcfi]['ftype']==0) {
    $permissionstr = "-"; }
   if($listcatfiles[$lcfi]['ftype']==1) {
    $permissionstr = "h"; }
   if($listcatfiles[$lcfi]['ftype']==2) {
    $permissionstr = "l"; }
   if($listcatfiles[$lcfi]['ftype']==3) {
    $permissionstr = "c"; }
   if($listcatfiles[$lcfi]['ftype']==4) {
    $permissionstr = "b"; }
   if($listcatfiles[$lcfi]['ftype']==5) {
    $permissionstr = "d"; }
   if($listcatfiles[$lcfi]['ftype']==6) {
    $permissionstr = "f"; }
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0100) ? 'r' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0080) ? 'w' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0040) ?
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0800) ? 's' : 'x' ) :
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0800) ? 'S' : '-'));
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0020) ? 'r' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0010) ? 'w' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0008) ?
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0400) ? 's' : 'x' ) :
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0400) ? 'S' : '-'));
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0004) ? 'r' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0002) ? 'w' : '-');
   $permissionstr .= (($listcatfiles[$lcfi]['fchmod'] & 0x0001) ?
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0200) ? 't' : 'x' ) :
                     (($listcatfiles[$lcfi]['fchmod'] & 0x0200) ? 'T' : '-'));
   $printfname = $listcatfiles[$lcfi]['fname'];
   if($listcatfiles[$lcfi]['ftype']==1):
    $printfname = $listcatfiles[$lcfi]['fname']." link to "+$listcatfiles[$lcfi]['flinkname'];
   if($listcatfiles[$lcfi]['ftype']==2):
    $printfname = $listcatfiles[$lcfi]['fname']." -> "+$listcatfiles[$lcfi]['flinkname'];
   print($permissionstr." ".$listcatfiles[$lcfi]['fuid']."/".$listcatfiles[$lcfi]['fgid']." ".str_pad($listcatfiles[$lcfi]['fsize'], 15, " ", STR_PAD_LEFT)." ".gmdate('Y-m-d H:i', $listcatfiles[$lcfi]['fmtime'])." ".$printfname."\n"); }
  $lcfi = $lcfi + 1; }
 return true; }
?>
