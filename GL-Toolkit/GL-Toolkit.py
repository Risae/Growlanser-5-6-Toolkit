from distutils.dir_util import copy_tree
from sys import builtin_module_names
import os
import shutil
import subprocess
from pathlib import Path

# Delete the Input and output directory
if os.path.exists("10_Input"):
    shutil.rmtree("10_Input")

if os.path.exists("11_Output"):
    shutil.rmtree("11_Output")

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create Dialogue
ToolDialogue = (
"""\
Welcome to the Growlanser 5 and 6 Toolkit! Made by Risae

Which Growlanser 5 / 6 Tool do you want to use?

[1] .SCEN/.SCEC/.SDMY/.STXT Extraction (Growlanser 5 / 6)
[2] (Script) Bytecode Extraction (Growlanser 6)
[3] GLX_XXXX.DAT Extraction (Growlanser 5 / 6)
[4] GLX_XXXX.DAT Reinsertion (Growlanser 5 / 6)

Enter your number of the option you choose: \
""")

# Call the ToolDialogue and save the input in the variable "tool", clear command prompt
clear()
tool = input(ToolDialogue)
clear()

# Create the Script Files Input directory
os.mkdir("10_Input")

# Tell user to put the files into the Script Files directory, clear the screen
clear()
placeFilesinFolderDialogue = input("Please place the Growlanser 5 or 6 file(s) inside the folder \"10_Input\" and press enter.")
clear()

# Execute the ScriptDump process 
if tool == "1":
    subprocess.call("python 01_Python_Scripts\\10_ScriptExtractor.py")

# Execute the ByteCodeDump process 
if tool == "2":
    subprocess.call("python 01_Python_Scripts\\20_ByteCodeExtractor.py")

# Create Output directory, Copy folder contents of Input to Ouput
os.mkdir("11_Output")
copy_tree("10_Input\\", "11_Output\\")

# Delete all files inside the Input directory, Delete the Input directory
for file in os.listdir("10_Input\\"):
    os.remove(os.path.join("10_Input\\", file))
os.rmdir("10_Input")