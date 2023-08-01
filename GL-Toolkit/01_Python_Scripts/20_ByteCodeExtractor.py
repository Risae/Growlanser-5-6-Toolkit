import os
import subprocess

# Create "clear command prompt" variable and execute it
clear = lambda: os.system("cls")
clear()

# Create a variable that holds the current path
currentFolderPath = os.getcwd()

# Set PATHs for Perl
os.environ["PATH"] += f";{currentFolderPath}\\00_3rd_Party_Programs\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\site\\bin"
os.environ["PATH"] += f";{currentFolderPath}\\00_3rd_Party_Programs\\strawberry-perl-5.32.1.1-64bit-portable\\perl\\bin"
os.environ["PATH"] += f";{currentFolderPath}\\00_3rd_Party_Programs\\strawberry-perl-5.32.1.1-64bit-portable\\c\\bin"

# Set variables for the Python and Perl commands
inputFolder = f"{currentFolderPath}\\10_Input"
outputFolder = f"{currentFolderPath}\\11_Output"
abcdeProgram = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\abcde_v0_0_9\\abcde.pl\""
abcdeByteCodeTableFile = f"\"{currentFolderPath}\\00_3rd_Party_Programs\\abcde_v0_0_9\\GL_ByteCode.tbl\""
pythonByteCodeExtractor = f"\"{currentFolderPath}\\01_Python_Scripts\\21_ByteCodePointerExtractor.py\""

# List the files inside "inputFolder" and start a loop to execute commands on each file
dir_list = os.listdir(inputFolder)
for filename in dir_list:

    # Create variables for the files
    inputFile = f"{inputFolder}\\{filename}"
    outputFile = f"{outputFolder}\\{filename}_output"
    outputFileName = f"{outputFile}.txt"

    # Execute pythonByteCodeExtractor and abcde
    subprocess.run(f"python {pythonByteCodeExtractor} -i \"{inputFile}\" -t \"{abcdeByteCodeTableFile}\"")
    subprocess.run(f"perl {abcdeProgram} -m bin2text --multi-table-files -cm abcde::Cartographer \"{inputFile}\" \"{inputFile}_commands.txt\" \"{outputFile}\" -s")