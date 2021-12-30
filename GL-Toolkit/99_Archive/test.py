import subprocess
from sys import builtin_module_names
import sys
import getopt
import os
from distutils.dir_util import copy_tree

currentFolderPath = os.getcwd()
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin") 
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin") 
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin") 

glScriptFilesFolder = (currentFolderPath + "\\10_GL_Script_Files_Input")
abcdeProgram = (currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl")
abcdeTableFile = (currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.tbl")
pythonScriptExtractor = (currentFolderPath + "\\02_Python_Scripts\\ScriptPointerExtractor.py")
scriptFile = os.listdir(glScriptFilesFolder)
pythonCMD = ("python " + pythonScriptExtractor + " -i " + glScriptFilesFolder + "\\" + scriptFile + " -c " + commentsOption + " -t " + abcdeTableFile)
perlCMD = ("perl " + abcdeProgram + " -m bin2text -cm abcde::Cartographer " + glScriptFilesFolder + "\\" + scriptFile + "_commands.txt " + glScriptFilesFolder + "\\" + scriptFile + "_output")

for file in scriptFile:
    os.system("start /wait cmd /c {pythonCMD}")
    os.system("start /wait cmd /c {perlCMD}")