import os
import shutil

from functions.ByteCodeExtractor import ByteCodeExtractor
from functions.ClearScreen import clear_screen
from functions.GameFileExtraction import GameFileExtraction
from functions.GameFileInsertion import GameFileInsertion
from functions.ScriptExtractor import ScriptExtractor
from functions.ScriptMerger import ScriptMerger

def main(): # Main function

    clear_screen()

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

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Delete the Input and Output directory and recreate it
    if os.path.exists("Input"):
        shutil.rmtree("Input")
    if os.path.exists("Output"):
        shutil.rmtree("Output")
    os.mkdir("Input")
    os.mkdir("Output")

    if tool == "1": # Execute the ScriptDump process
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.")
        ScriptExtractor()

    if tool == "2": # Execute the ByteCodeDump process
        placeFilesinFolderDialogue = input("Please place the Growlanser 6 file(s) inside the folder \"Input\" and press enter.")
        ByteCodeExtractor()

    if tool == "3": # Execute the Extraction process
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.")
        GameFileExtraction()

    if tool == "4": # Execute the Reinsertion process
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) that you want to import inside the folder \"Input\".\nPlease place the Growlanser 5 / 6 \"GLX_XXXX.DAT\" file inside \"Output\" and press enter.")
        GameFileInsertion()

    if tool == "5": # Execute the ScriptMerger process
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.\nPlease make sure that the script files have the ending '*ENG.txt' and '*JPN.txt'!")
        ScriptMerger()


if __name__ == "__main__":
    main()