import os
import subprocess

from functions.ClearScreen import clear_screen

def GameFileInsertion():

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set variables for the filepaths and programs
    inputFolder = f"{currentFolderPath}\\Input"
    outputFolder = f"{currentFolderPath}\\Output"
    quickBMSProgram = f"\"{currentFolderPath}\\3rdparty\\quickbms\\quickbms.exe\""
    growlanserquickBMS = f"\"{currentFolderPath}\\3rdparty\\quickbms\\growlanser.bms\""

    # List the files inside "inputFolder" and execute commands on each file (loop)
    dir_list = os.listdir(outputFolder)
    for filename in dir_list:

        # Execute quickBMS command
        subprocess.run(f"{quickBMSProgram} -w -r -r {growlanserquickBMS} \"{outputFolder}\\{filename}\" \"{inputFolder}\"")