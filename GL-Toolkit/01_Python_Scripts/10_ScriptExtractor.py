from distutils.dir_util import copy_tree
from sys import builtin_module_names
import os
import subprocess

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create Dialogue option
commentsOptionDialogue = (
"""\
Which abcde comments option do you want to use?

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

# Call the commentsOptionDialogue and save the result in commentsOption
clear()
commentsOption = input(commentsOptionDialogue)
clear()

if commentsOption == "1":
    commentsOption = "Yes"

elif commentsOption == "2":
    commentsOption = "No"

elif commentsOption == "3":
    commentsOption = "Both"

# Call the abcdeCodeOptionDialogue and save the result in abcdeAtlasOption
clear()
abcdeAtlasOption = input(abcdeCodeOptionDialogue)
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
abcdeScriptTableFile = ("\"" + str(currentFolderPath) + "\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_Script.tbl\"")
pythonScriptExtractor = ("\"" + str(currentFolderPath) + "\\01_Python_Scripts\\11_ScriptPointerExtractor.py\"")

# List the files inside "inputFolder" and execute commands on each file (loop)
dir_list = os.listdir(inputFolder)
for filename in dir_list:

    # Create Python (pythonScriptExtractor) command and execute it
    pythonCMD = ("python " + str(pythonScriptExtractor) + " -i " + "\"" + str(inputFolder) + "\\" + str(filename) + "\"" + " -c " + str(commentsOption) + " -t " + str(abcdeScriptTableFile))
    subprocess.run(pythonCMD)

    # Create Perl (abcde) command and execute it
    perlCMD = ("perl " + str(abcdeProgram) + " -m bin2text -cm abcde::Cartographer " + "\"" + str(inputFolder) + "\\" + str(filename) + "\" \"" + str(inputFolder) + "\\" + str(filename) + "_commands.txt\" " + "\"" + str(inputFolder) + "\\" + str(filename) + "_output\" -s")
    subprocess.run(perlCMD)

    outputFileName = (str(inputFolder) + "\\" + str(filename) + "_output.txt")

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