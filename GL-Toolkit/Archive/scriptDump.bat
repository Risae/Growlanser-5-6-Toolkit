setlocal EnableDelayedExpansion

cd..
for %%i in ("%~dp0..") do set "TOOLKITFOLDERPATH=%%~fi"

SET "PATH=%PATH%;%TOOLKITFOLDERPATH%\00_3rd_Party_Programs\abcde_v0_0_9\strawberry-perl-5.32.1.1-64bit-portable\perl\site\bin"
SET "PATH=%PATH%;%TOOLKITFOLDERPATH%\00_3rd_Party_Programs\abcde_v0_0_9\strawberry-perl-5.32.1.1-64bit-portable\perl\bin"
SET "PATH=%PATH%;%TOOLKITFOLDERPATH%\00_3rd_Party_Programs\abcde_v0_0_9\strawberry-perl-5.32.1.1-64bit-portable\c\bin"

set scriptFilesFolder=%TOOLKITFOLDERPATH%\10_GL_Script_Files
set abcdeProgram=%TOOLKITFOLDERPATH%\00_3rd_Party_Programs\abcde_v0_0_9\abcde.pl
set abcdeTableFile=%TOOLKITFOLDERPATH%\00_3rd_Party_Programs\abcde_v0_0_9\abcde.tbl
set pythonScriptExtractor=%TOOLKITFOLDERPATH%\02_Python_Scripts\ScriptPointerExtractor.py

set commentsOption=Yes
set scriptCleanup=No

cd /d "%scriptFilesFolder%"
for %%a in (*) do call :File_Dump %%a
goto End

:File_Dump
set SCRIPTFILE=%1
python "%pythonScriptExtractor%" -i "%scriptFilesFolder%\%SCRIPTFILE%" -c "%commentsOption%" -t "%abcdeTableFile%"
perl "%abcdeProgram%" -m bin2text -cm abcde::Cartographer "%scriptFilesFolder%\%SCRIPTFILE%" "%scriptFilesFolder%\%SCRIPTFILE%_commands.txt" "%scriptFilesFolder%\%SCRIPTFILE%_output" -s
del "%scriptFilesFolder%\%SCRIPTFILE%_commands.txt"
if %scriptCleanup% equ Yes del %SCRIPTFILE%

:End