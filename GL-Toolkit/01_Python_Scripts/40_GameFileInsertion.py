import os
import subprocess

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create a variable that holds the current path
currentFolderPath = os.getcwd()

# Set variables for the filepaths and programs
inputFolder = f"{currentFolderPath}\\10_Input"
outputFolder = f"{currentFolderPath}\\11_Output"
quickBMSProgram = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\quickbms\\quickbms.exe\""
growlanserquickBMS = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\quickbms\\growlanser.bms\""

# List the files inside "inputFolder" and execute commands on each file (loop)
dir_list = os.listdir(outputFolder)
for filename in dir_list:

    # Execute quickBMS command
    subprocess.run(f"{quickBMSProgram} -w -r -r {growlanserquickBMS} \"{outputFolder}\\{filename}\" \"{inputFolder}\"")