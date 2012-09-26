@echo off
set PYTHONPATH=%CD%\upcean
set PYTHONEXEC=C:\Python27
set PYTHONEXEC=C:\Python32
set OLDPATH=%PATH%;
set PATH=%PATH%;%PYTHONEXEC%;
python -c "import upc" %*
set PATH=%OLDPATH%

