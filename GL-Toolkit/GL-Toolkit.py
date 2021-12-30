import subprocess
from sys import builtin_module_names
import sys
import getopt
import os,glob
from distutils.dir_util import copy_tree
from time import sleep, time

clear = lambda: os.system('cls')

ToolDialogue = (
"Welcome to the Growlanser 5 and 6 Toolkit! Made by Risae\n\
\n\
Which Growlanser 5 / 6 Tool do you want to use?\n\
The following options are available:\n\
[1] ScriptDump\n\
[2] ByteCodeDump\n\
\n\
Enter your toolname: ")

commentsOptionDialogue = (
"Which abcde comments option do you want to use?\n\
The following options are available for ScriptDump:\n\
\n\
[1] Yes - Which equals this formatting:\n\
//Anita[END-FF]\n\
\n\
[2] No - Which equals this formatting:\n\
Anita[END-FF]\n\
\n\
[3] Both - Which equals this formatting:\n\
//Anita[END-FF]\n\
Anita[END-FF]\n\
\n\
Enter your comments option: ")

scriptCleanupOptionDialogue = (
"Do you want to keep the original GL5 / 6 Script and abcde commands file?\n\
The following options are available:\n\
\n\
[1] Yes - Deletes both files after the extracted script file was created.\n\
[2] No - Keeps both of the GL5 / 6 Script and abcde commands file\n\
[3] Original Script File Only - Keeps the original GL5 / 6 Script file\n\
[4] Created Commands File Only - Keeps the abcde commands file\n\
\n\
Enter your Script Cleanup option: ")


clear()
tool = input(ToolDialogue)
clear()

if tool == "1":
    commentsOption = input(commentsOptionDialogue)
    clear()
    if commentsOption == "1":
        commentsOption = "Yes"
    
    elif commentsOption == "2":
        commentsOption = "No"

    elif commentsOption == "3":
        commentsOption = "Both"

    scriptCleanupOption = input(scriptCleanupOptionDialogue)
    clear()

if tool == "1":
    currentFolderPath = os.getcwd()

    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin") 

    glScriptFilesFolder = (str(currentFolderPath) + "\\10_GL_Script_Files_Input")
    abcdeProgram = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\"")
    abcdeTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.tbl\"")
    pythonScriptExtractor = ("\"" + str(currentFolderPath) + "\\02_Python_Scripts\\ScriptPointerExtractor.py\"")

    dir_list = os.listdir(glScriptFilesFolder)
    for filename in dir_list:
        pythonCMD = ("python " + str(pythonScriptExtractor) + " -i " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\"" + " -c " + str(commentsOption) + " -t " + str(abcdeTableFile))
        perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text -cm abcde::Cartographer " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\" \"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_output\" -s")
        subprocess.run(pythonCMD)
        subprocess.run(perlCMD)
        if scriptCleanupOption == "1":
            continue
        elif scriptCleanupOption == "2":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "3":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "4":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))

copy_tree("10_GL_Script_Files_Input\\", "11_GL_Script_Files_Output\\")
for file in os.listdir("10_GL_Script_Files_Input\\"):
    os.remove(os.path.join("10_GL_Script_Files_Input\\", file))