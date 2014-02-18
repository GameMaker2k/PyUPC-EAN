@echo off
set PYTHONPATH=%CD%\upcean
set PYTHONDONTWRITEBYTECODE=x
set PyVer=3.3
set PyVer=2.7
set OLDPATH=%PATH%;
FOR /f "tokens=3* delims=	" %%! in ('REG.EXE QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore\%PyVer%\InstallPath" /ve ^| Findstr.exe /ri "\<NO NAME\>"') DO set PATH=%PATH%;%%!;
python -b -B -x "./upc-demo.py" %*
set PATH=%OLDPATH%
pause
