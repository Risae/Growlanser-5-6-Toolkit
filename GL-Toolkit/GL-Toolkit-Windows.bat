@ECHO OFF
mode 105,25

::Set current path as variable
for %%i in ("%~dp0..") do set "FOLDERPATH=%%~fi"

::Set Python embed into Path
SET "PATH=%PATH%;%FOLDERPATH%\GL-Toolkit\00_3rd_Party_Programs\python-3.10.6-embed-amd64"

title GL-Toolkit
IF EXIST "%~dp0GL-Toolkit.py" (
	color 00
	python GL-Toolkit.py
) ELSE (
	color 04
	echo. Script wasn't found! Closing in 10 seconds!
	timeout 10 /nobreak > nul
	exit
)

pause