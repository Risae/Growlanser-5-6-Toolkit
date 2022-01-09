import os
import shutil
import subprocess

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create a variable that holds the current path
currentFolderPath = os.getcwd()

# Set variables for the filepaths and programs
inputFolder = f"{currentFolderPath}\\10_Input"
outputFolder = f"{currentFolderPath}\\11_Output"

dir_list = os.listdir(inputFolder)

jpn = []
eng = []

for names in dir_list:
    if names.endswith(".JPN"):
        jpn.append(names)
    elif names.endswith(".ENG"):
        eng.append(names)

jpnstring = "".join(jpn)
engstring = "".join(eng)

jpnfile = f"{str(currentFolderPath)}\{jpnstring}"
engfile = f"{str(currentFolderPath)}\{engstring}"

with open(jpnfile, "rt", encoding="utf8") as file:
    with open("test.txt", "wt", encoding="utf8") as output:
        lines = file.readlines()
        output.write(str(lines))

print(lines)