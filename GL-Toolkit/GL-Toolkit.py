from distutils.dir_util import copy_tree
from sys import builtin_module_names
import getopt
import os,glob
import shutil
import subprocess
import sys

# Delete the Input and output directory
if os.path.exists("10_GL_Script_Files_Input"):
    shutil.rmtree("10_GL_Script_Files_Input")

if os.path.exists("11_GL_Script_Files_Output"):
    shutil.rmtree("11_GL_Script_Files_Output")

# Create "clear command prompt" variable and execute it
clear = lambda: os.system('cls')
clear()

# Create Dialogues
ToolDialogue = (
"Welcome to the Growlanser 5 and 6 Toolkit! Made by Risae\n\
\n\
Which Growlanser 5 / 6 Tool do you want to use?\n\
[1] ScriptDump (Growlanser 5 / 6)\n\
[2] ByteCodeDump (Growlanser 6)\n\
\n\
Enter your Tool number: ")

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
Enter your comments number: ")

scriptCleanupOptionDialogue = (
"Do you want to keep the original GL5 / 6 Script and abcde commands file after the script has been dumped?\n\
\n\
[1] Yes - Keep both files\n\
[2] No - Deletes both the GL5 / 6 Script and abcde commands file\n\
[3] Original Script File Only - Keeps the original GL5 / 6 Script file\n\
[4] Created Commands File Only - Keeps the abcde commands file\n\
\n\
Enter your Script cleanup number: ")

# Call the ToolDialogue and save the input in the variable "tool", clear command prompt
tool = input(ToolDialogue)
clear()

# Create the Script Files Input directory
os.mkdir("10_GL_Script_Files_Input")

# Tell user to put the files into the Script Files directory, clear the screen
placeScriptFilesinFolderDialogue = input("Please place the Growlanser 5 or 6 .SCEN/.SCEC/.SDMY/.STXT Script files inside the folder \"10_GL_Script_Files_Input\" and press enter.")
clear()

# Change the commentsOption number to a string
if tool == "1":
    commentsOption = input(commentsOptionDialogue)
    clear()
    if commentsOption == "1":
        commentsOption = "Yes"
    
    elif commentsOption == "2":
        commentsOption = "No"

    elif commentsOption == "3":
        commentsOption = "Both"

# Call the scriptCleanupOptionDialogue and save the input in the variable "scriptCleanupOption", clear command prompt 
scriptCleanupOption = input(scriptCleanupOptionDialogue)
clear()

# Execute the ScriptDump process 
if tool == "1":

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set PATHs for Perl
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin") 

    # Set variables for the Python and Perl commands
    glScriptFilesFolder = (str(currentFolderPath) + "\\10_GL_Script_Files_Input")
    abcdeProgram = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\"")
    abcdeScriptTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_Script.tbl\"")
    pythonScriptExtractor = ("\"" + str(currentFolderPath) + "\\01_Python_Scripts\\ScriptPointerExtractor.py\"")

    # List the files inside "glScriptFilesFolder" and execute commands on each file
    dir_list = os.listdir(glScriptFilesFolder)
    for filename in dir_list:

        # Create Python (pythonScriptExtractor) command and execute it
        pythonCMD = ("python " + str(pythonScriptExtractor) + " -i " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\"" + " -c " + str(commentsOption) + " -t " + str(abcdeScriptTableFile))
        subprocess.run(pythonCMD)

        # Create Perl (abcde) command and execute it
        perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text -cm abcde::Cartographer " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\" \"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_output\" -s")
        subprocess.run(perlCMD)

        # Check if the user wants to clean up files and delete those files
        if scriptCleanupOption == "1":
            continue
        elif scriptCleanupOption == "2":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "3":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "4":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))

# Execute the ByteCodeDump process 
if tool == "2":

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set PATHs for Perl
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin") 
    os.environ["PATH"] += (";" + currentFolderPath + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin") 

    # Set variables for the Python and Perl commands
    glScriptFilesFolder = (str(currentFolderPath) + "\\10_GL_Script_Files_Input")
    abcdeProgram = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\"")
    abcdeByteCodeTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_ByteCode.tbl\"")
    pythonByteCodeExtractor = ("\"" + str(currentFolderPath) + "\\01_Python_Scripts\ByteCodePointerExtractor.py\"")

    # List the files inside "glScriptFilesFolder" and execute commands on each file
    dir_list = os.listdir(glScriptFilesFolder)
    for filename in dir_list:

        # Create Python (pythonScriptExtractor) command and execute it
        pythonCMD = ("python " + str(pythonByteCodeExtractor) + " -i " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\"" + " -t " + str(abcdeByteCodeTableFile))
        subprocess.run(pythonCMD)

        # Create Perl (abcde) command and execute it
        perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text --multi-table-files -cm abcde::Cartographer " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\" \"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_output\" -s")
        subprocess.run(perlCMD)

        # Check if the user wants to clean up files and delete those files
        if scriptCleanupOption == "1":
            continue
        elif scriptCleanupOption == "2":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "3":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt")
        elif scriptCleanupOption == "4":
            os.remove(str(glScriptFilesFolder) + "\\" + str(filename))


# Create Output directory
os.mkdir("11_GL_Script_Files_Output")

# Copy folder contents of Input to Ouput
copy_tree("10_GL_Script_Files_Input\\", "11_GL_Script_Files_Output\\")

# Delete all files inside the Input directory
for file in os.listdir("10_GL_Script_Files_Input\\"):
    os.remove(os.path.join("10_GL_Script_Files_Input\\", file))

# Delete the Input directory
os.rmdir("10_GL_Script_Files_Input")