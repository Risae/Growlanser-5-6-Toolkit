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
tool = input("""\
Welcome to the Growlanser 5 and 6 Toolkit!

Which Growlanser 5 / 6 Tool do you want to use?

[1] .SCEN/.SCEC/.SDMY/.STXT: Extraction (Growlanser 5 / 6)
[2] .SCEN/.SCEC/.SDMY/.STXT: Bytecode Extraction (Growlanser 6)
[3] GLX_XXXX.DAT: Extraction (Growlanser 5 / 6)
[4] GLX_XXXX.DAT: Reinsertion (Growlanser 5 / 6)
[5] .SCEN/.SCEC/.SDMY/.STXT: Merger (Growlanser 5 / 6)
[6] .SCEN/.SCEC/.SDMY/.STXT: Character Name Adder (Growlanser 5 / 6) (WIP)

Enter your number of the option you choose: """)
clear()

# Execute the ScriptDump process 
if tool == "1":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"10_Input\" and press enter.")
    clear()
    subprocess.call("python 01_Python_Scripts\\10_ScriptExtractor.py")

# Execute the ByteCodeDump process 
if tool == "2":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 6 file(s) inside the folder \"10_Input\" and press enter.")
    clear()
    subprocess.call("python 01_Python_Scripts\\20_ByteCodeExtractor.py")

# Execute the Extraction process 
if tool == "3":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"10_Input\" and press enter.")
    clear()
    subprocess.call("python 01_Python_Scripts\\30_GameFileExtraction.py")

# Execute the Reinsertion process 
if tool == "4":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) that you want to import inside the folder \"10_Input\".\nPlease place the Growlanser 5 / 6 \"GLX_XXXX.DAT\" file inside \"11_Output\" and press enter.")
    clear()
    subprocess.call("python 01_Python_Scripts\\40_GameFileInsertion.py")

# Execute the ScriptMerger process 
if tool == "5":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"10_Input\" and press enter.\nPlease make sure that the script files have the ending .ENG and .JPN!")
    clear()
    subprocess.call("python 01_Python_Scripts\\50_ScriptMerger.py")

# Execute the ScriptMerger process 
if tool == "6":
    # Tell the user to put the files into the "10_Input" directory, clear the screen and execute the script
    placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"10_Input\" and press enter.")
    clear()
    subprocess.call("python 01_Python_Scripts\\60_NameAdder.py")