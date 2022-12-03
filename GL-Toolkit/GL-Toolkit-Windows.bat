@ECHO OFF

:: Set the code page to UTF-8
CHCP 65001

:: Set the size and title of the command prompt window
mode 105,25
title GL-Toolkit

:: Set the current folder path as a variable
for %%i in ("%~dp0..") do set "ROOT_FOLDER=%%~fi"

:: Place the Python embed folder path into PATH
SET "PATH=%PATH%;%ROOT_FOLDER%\GL-Toolkit\00_3rd_Party_Programs\python"

:: Check if the GL-Toolkit script exists
IF EXIST "%~dp0GL-Toolkit.py" (

    :: Set the console color to green
    color 0A

    :: Run the GL-Toolkit script
    python GL-Toolkit.py

) ELSE (

    :: Set the console color to red
    color 04

    :: Display an error message
    echo. Script wasn't found! Closing in 15 seconds!

    :: Wait for 15 seconds before closing the command prompt window
    timeout 15 /nobreak > nul

    :: Exit the script
    exit
)

:: Wait for user input before closing the command prompt window
pause