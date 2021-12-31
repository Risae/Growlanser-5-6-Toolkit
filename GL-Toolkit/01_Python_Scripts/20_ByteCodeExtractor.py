from distutils.dir_util import copy_tree
from sys import builtin_module_names
import os
import subprocess
from pathlib import Path

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create a variable that holds the current path
currentFolderPath = os.getcwd()

# Set PATHs for Perl
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin") 
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin") 
os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin") 

# Set variables for the Python and Perl commands
inputFolder = (str(currentFolderPath) + "\\10_Input")
abcdeProgram = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\"")
abcdeByteCodeTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_ByteCode.tbl\"")
pythonByteCodeExtractor = ("\"" + str(currentFolderPath) + "\\01_Python_Scripts\\21_ByteCodePointerExtractor.py\"")

# List the files inside "inputFolder" and execute commands on each file
dir_list = os.listdir(inputFolder)
for filename in dir_list:

    # Create Python (pythonScriptExtractor) command and execute it
    pythonCMD = ("python " + str(pythonByteCodeExtractor) + " -i " + "\"" + str(inputFolder) + "\\" + str(filename) + "\"" + " -t " + str(abcdeByteCodeTableFile))
    subprocess.run(pythonCMD)

    # Create Perl (abcde) command and execute it
    perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text --multi-table-files -cm abcde::Cartographer " + "\"" + str(inputFolder) + "\\" + str(filename) + "\" \"" + str(inputFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(inputFolder) + "\\" + str(filename) + "_output\" -s")
    subprocess.run(perlCMD)