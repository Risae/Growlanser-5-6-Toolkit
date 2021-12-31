from distutils.dir_util import copy_tree
from sys import builtin_module_names
import getopt
import os,glob
import shutil
import subprocess
import sys

# Delete the Input and output directory
if os.path.exists("10_Input"):
    shutil.rmtree("10_Input")

if os.path.exists("11_Output"):
    shutil.rmtree("11_Output")

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create Dialogues
ToolDialogue = (
"""\
Welcome to the Growlanser 5 and 6 Toolkit! Made by Risae

Which Growlanser 5 / 6 Tool do you want to use?

[1] ScriptDump (Growlanser 5 / 6)
[2] ByteCodeDump (Growlanser 6)

Enter your number of the option you choose: \
""")

commentsOptionDialogue = (
"""\
Which abcde comments option do you want to use?
The following options are available for ScriptDump:

[1] Yes - Which equals this formatting:
//Anita[END-FF]

[2] No - Which equals this formatting:
Anita[END-FF]

[3] Both - Which equals this formatting:
//Anita[END-FF]
Anita[END-FF]

Enter your number of the option you choose: \
""")

abcdeCodeOptionDialogue = (
"""\
Do you want to add abcde Atlas code on top of each dumped script?

[1] Yes
[2] No

Enter your number of the option you choose: \
""")

scriptCleanupOptionDialogue = (
"""\
Do you want to keep the original GL5 / 6 Script and abcde commands file after the script has been dumped?

[1] Yes - Keep both files
[2] No - Deletes both the GL5 / 6 Script and abcde commands file
[3] Original Script File Only - Keeps the original GL5 / 6 Script file
[4] Created Commands File Only - Keeps the abcde commands file

Enter your number of the option you choose: \
""")

# Call the ToolDialogue and save the input in the variable "tool", clear command prompt
tool = input(ToolDialogue)
clear()

# Create the Script Files Input directory
os.mkdir("10_Input")

# Tell user to put the files into the Script Files directory, clear the screen
placeScriptFilesinFolderDialogue = input("Please place the Growlanser 5 or 6 .SCEN/.SCEC/.SDMY/.STXT Script files inside the folder \"10_Input\" and press enter.")
clear()

# If Tool = Scriptdump, ask commentsOptionDialogue and abcdeCodeOptionDialogue
if tool == "1":
    commentsOption = input(commentsOptionDialogue)
    clear()
    if commentsOption == "1":
        commentsOption = "Yes"
    
    elif commentsOption == "2":
        commentsOption = "No"

    elif commentsOption == "3":
        commentsOption = "Both"
    clear()
    abcdeAtlasOption = input(abcdeCodeOptionDialogue)

# Call the scriptCleanupOptionDialogue and save the input in the variable "scriptCleanupOption", clear command prompt
clear()
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
    glScriptFilesFolder = (str(currentFolderPath) + "\\10_Input")
    abcdeProgram = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\"")
    abcdeScriptTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_Script.tbl\"")
    pythonScriptExtractor = ("\"" + str(currentFolderPath) + "\\01_Python_Scripts\\ScriptPointerExtractor.py\"")

    # List the files inside "glScriptFilesFolder" and execute commands on each file (loop)
    dir_list = os.listdir(glScriptFilesFolder)
    for filename in dir_list:

        # Create Python (pythonScriptExtractor) command and execute it
        pythonCMD = ("python " + str(pythonScriptExtractor) + " -i " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\"" + " -c " + str(commentsOption) + " -t " + str(abcdeScriptTableFile))
        subprocess.run(pythonCMD)

        # Create Perl (abcde) command and execute it
        perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text -cm abcde::Cartographer " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "\" \"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(glScriptFilesFolder) + "\\" + str(filename) + "_output\" -s")
        subprocess.run(perlCMD)

        outputFileName = (str(glScriptFilesFolder) + "\\" + str(filename) + "_output.txt")

        # Read in the file, Replace the target string, Write the file out again
        with open(outputFileName, "rt", encoding="utf8") as file:
            filedata = file.read()
        filedata = filedata.replace("//POINTER #", "\n\n\n\n\n//POINTER #")
        with open(outputFileName, "wt", encoding="utf8") as file:
            file.write(filedata)

        # Readlines in the file, delete line 1-16 (premade abcde Atlas code), Write the file out again
        with open(outputFileName, "rt", encoding="utf8") as file:
            lines = file.readlines()
        del lines[0:15]
        with open(outputFileName, "wt", encoding="utf8") as file:
            for line in lines:
                file.write(line)
    
        # If abcdeAtlasOption = 1, then open the output file and read all lines
        if abcdeAtlasOption == "1":
            with open(outputFileName, "rt", encoding="utf8") as file:
                lines = file.readlines()

            # Copy the PointerStart and TextblockStart values from the first pointer
            # Example "$FA0" and "$FD0":
            # //POINTER #0 @ $FA0 - STRING #0 @ $FD0
            line2data  = lines[2]
            textBlockStart = (" ".join(line2data.split()[3:-5]))
            pointerStartBroken = (line2data.split(" ")[8:][0])
            pointerStart = pointerStartBroken.strip()

            # Create the Atlas code and insert the values
            abcdeAtlasCode = (
f"""\
#VAR(dialogue, TABLE)
#ADDTBL({abcdeScriptTableFile}, dialogue)
#ACTIVETBL(dialogue)

#VAR(PTR, CUSTOMPOINTER)
#CREATEPTR(PTR, "LINEAR", {textBlockStart}, 32)

#VAR(PTRTBL, POINTERTABLE)
#PTRTBL(PTRTBL, {pointerStart}, 4, PTR)

#JMP({textBlockStart})
#HDR({textBlockStart})
""")

            # Open the outputFileName and save the Atlas code and after that the actual script in the file
            with open(outputFileName,'rt', encoding="utf8") as contents:
                save = contents.read()
            with open(outputFileName,'wt', encoding="utf8") as contents:
                contents.write(abcdeAtlasCode)
                contents.write(save)


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
    glScriptFilesFolder = (str(currentFolderPath) + "\\10_Input")
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


# Create Output directory, Copy folder contents of Input to Ouput
os.mkdir("11_Output")
copy_tree("10_Input\\", "11_Output\\")

# Delete all files inside the Input directory, Delete the Input directory
for file in os.listdir("10_Input\\"):
    os.remove(os.path.join("10_Input\\", file))
os.rmdir("10_Input")