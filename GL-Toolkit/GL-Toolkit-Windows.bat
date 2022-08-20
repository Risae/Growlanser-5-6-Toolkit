@ECHO OFF
::Set the size of the cmd window and the title of it
mode 105,25
title GL-Toolkit

::Set the current folder path as a variable
for %%i in ("%~dp0..") do set "FOLDERPATH=%%~fi"

::Place the Python embed folder path into PATH
SET "PATH=%PATH%;%FOLDERPATH%\GL-Toolkit\00_3rd_Party_Programs\python-3.10.6-embed-amd64"

::Check if the file "GL-Toolkit.py" exists - If it doesn't: tell the user
IF EXIST "%~dp0GL-Toolkit.py" (
	color 00
	python GL-Toolkit.py
) ELSE (
	color 04
	echo. Script wasn't found! Closing in 15 seconds!
	timeout 15 /nobreak > nul
	exit
)

pause