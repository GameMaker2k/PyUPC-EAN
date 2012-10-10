@echo off
set PYTHONPATH=%CD%\upcean
set PYTHONDONTWRITEBYTECODE=x
set PYTHONEXEC=C:\Python27
set PYTHONEXEC=C:\Python33
set OLDPATH=%PATH%;
set PATH=%PATH%;%PYTHONEXEC%;
python -b -B -x "./upc.py" %*
set PATH=%OLDPATH%

