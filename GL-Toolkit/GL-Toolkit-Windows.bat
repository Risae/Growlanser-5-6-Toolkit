@ECHO OFF

::Set current path as variable
for %%i in ("%~dp0..") do set "FOLDERPATH=%%~fi"

::Set Python embed into Path
SET "PATH=%PATH%;%FOLDERPATH%\00_3rd_Party_Programs\python-3.10.1-embed-amd64"

python GL-Toolkit.py

pause