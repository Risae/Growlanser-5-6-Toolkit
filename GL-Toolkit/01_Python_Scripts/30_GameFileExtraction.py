import os
import subprocess

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Ask the user how to extract the files
clear()
quickBMSExtractionOption = input(
"""\
Choose your Extraction Option:

[1] Extract only the files inside GLX_XXXX.DAT
[2] Extract the files inside GLX_XXXX.DAT and inside the extracted files

Enter your number of the option you choose: \
""")
clear()

# Tell user to put the files into the Script Files directory, clear the screen
clear()
placeFilesinFolderDialogue = input("Please place the Growlanser 5 or 6 file(s) inside the folder \"10_Input\" and press enter.")
clear()

# Create a variable that holds the current path
currentFolderPath = os.getcwd()

# Set variables for the filepaths and programs
inputFolder = f"{currentFolderPath}\\10_Input"
outputFolder = f"{currentFolderPath}\\11_Output"
quickBMSProgram = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\quickbms\\quickbms.exe\""
growlanserquickBMS = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\quickbms\\growlanser.bms\""

# If option 1 was chosen, start the quickBMSExtraction process
if quickBMSExtractionOption == "1":

    # List the files inside "inputFolder" and execute commands on each file (loop)
    dir_list = os.listdir(inputFolder)
    for filename in dir_list:

        # Execute quickBMS
        subprocess.run(f"{quickBMSProgram} -w -d {growlanserquickBMS} \"{inputFolder}\\{filename}\" \"{outputFolder}\"")

# If option 2 was chosen, start the extrended quickBMSExtraction process
if quickBMSExtractionOption == "2":

    # List the files inside "inputFolder" and execute commands on each file (loop)
    dir_list = os.listdir(inputFolder)
    for filename in dir_list:

        # Execute quickBMS
        subprocess.run(f"{quickBMSProgram} -w -d {growlanserquickBMS} \"{inputFolder}\\{filename}\" \"{outputFolder}\"")

        # List the files inside "inputFolder" and execute commands on each file (loop)
        newOutputFolder = f"{outputFolder}\\{filename}"

        # Create a list of all the file extentions in the newOutputFolder
        SplitTypes=[]
        for file in os.listdir(newOutputFolder):
            SplitTypes.append(file.split('.')[-1])

        # Remove dublicates from the list
        newList = list(dict.fromkeys(SplitTypes))

        # Create blacklist of files that can't be extracted a second time (at least with the current quickbms script)
        blacklist = ["000", "v_0", "b00", "sel", "her", "mot", "MAPTBL", "txt", "MAPOBJ"]

        # If a blacklistItem is exists in newList, remove it from the list
        for blacklistItem in blacklist:
            if blacklistItem in newList:
                newList.remove(blacklistItem)

        # Start the extended quickBMS extration process
        for fileType in newList:

            # Create quickBMS command and execute it
            quickBMSCMD2 = f"{quickBMSProgram} -w -d -F \"*.{fileType}\" {growlanserquickBMS} \"{newOutputFolder}\" \"{newOutputFolder}\""
            subprocess.run(quickBMSCMD2)