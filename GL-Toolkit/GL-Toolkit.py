import os
import shutil
import subprocess

# Delete the Input and output directory and recreate it
if os.path.exists("10_Input"):
    shutil.rmtree("10_Input")
if os.path.exists("11_Output"):
    shutil.rmtree("11_Output")
os.mkdir("10_Input")
os.mkdir("11_Output")

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Call the ToolDialogue and save the input in the variable "tool", clear command prompt
tool = input(
"""\
Welcome to the Growlanser 5 and 6 Toolkit! Made by Risae

Which Growlanser 5 / 6 Tool do you want to use?

[1] .SCEN/.SCEC/.SDMY/.STXT Extraction (Growlanser 5 / 6)
[2] (Script) Bytecode Extraction (Growlanser 6)
[3] GLX_XXXX.DAT Extraction (Growlanser 5 / 6)
[4] GLX_XXXX.DAT Reinsertion (Growlanser 5 / 6)

Enter your number of the option you choose: \
""")
clear()

# Execute the ScriptDump process 
if tool == "1":
    subprocess.call("python 01_Python_Scripts\\10_ScriptExtractor.py")

# Execute the ByteCodeDump process 
if tool == "2":
    subprocess.call("python 01_Python_Scripts\\20_ByteCodeExtractor.py")

# Execute the ByteCodeDump process 
if tool == "3":
    subprocess.call("python 01_Python_Scripts\\30_GameFileExtraction.py")

# Execute the ByteCodeDump process 
if tool == "4":
    subprocess.call("python 01_Python_Scripts\\40_GameFileInsertion.py")