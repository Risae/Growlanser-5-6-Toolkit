import os
import subprocess
from functions.ClearScreen import clear_screen

def ByteCodeExtractor():

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set variables for the Python and Perl commands
    inputFolder = f"{currentFolderPath}\\Input"
    outputFolder = f"{currentFolderPath}\\Output"
    abcdeProgram = f"\"{currentFolderPath}\\3rdparty\\abcde\\abcde.pl\""
    abcdeByteCodeTableFile = f"\"{currentFolderPath}\\3rdparty\\abcde\\GL_ByteCode.tbl\""

    # List the files inside "inputFolder" and start a loop to execute commands on each file
    dir_list = os.listdir(inputFolder)

    for filename in dir_list:

        # Create variables for the files
        inputFile = f"{inputFolder}\\{filename}"
        outputFile = f"{outputFolder}\\{filename}_output"
        outputFileName = f"{outputFile}.txt"

        # Execute pythonByteCodeExtractor and abcde
        sdfBytesPosition = 40
        fileBeginning = -44

        # Open file in "read byte", move pointer to the bytes that point to SDF and read the next 4 bytes
        bytestream = open(inputFile, "rb")
        bytestream.seek(sdfBytesPosition, 1)
        sdfLocationHex = bytestream.read(4).hex()

        # Reorder bytes into proper order, example: 00 18 00 00 > 00 00 18 00
        newSDFLocationHex = sdfLocationHex[6:8] + sdfLocationHex[4:6] + sdfLocationHex[2:4] + sdfLocationHex[0:2]

        # Convert hexadecimal value to decimal, go back to the beginning of the file and jump to the SDF location
        sdfLocationDecimal = int(newSDFLocationHex, 16)
        bytestream.seek(fileBeginning, 1)
        bytestream.seek(sdfLocationDecimal, 1)

        # Go to the ByteCode Start Location
        bytestream.seek(288, 1)
        bCStartLocationHex = bytestream.read(4).hex()

        # ByteCode Start Location Hex
        newbCStartLocationHex = bCStartLocationHex[6:8] + bCStartLocationHex[4:6] + bCStartLocationHex[2:4] + bCStartLocationHex[0:2]

        # Convert hexadecimal value to decimal
        newbCStartLocationDecimal = int(newbCStartLocationHex, 16)


        # ByteCode End Location Hex
        bCEndLocationHex = bytestream.read(4).hex()
        newbCEndLocationHex = bCEndLocationHex[6:8] + bCEndLocationHex[4:6] + bCEndLocationHex[2:4] + bCEndLocationHex[0:2]

        # Convert hexadecimal value to decimal
        newbCEndLocationDecimal = int(newbCEndLocationHex, 16)

        # Go back to the start of the bytecode section and jump to the beginning
        bytestream.seek(-168, 1)
        bytestream.seek(newbCStartLocationDecimal, 1)

        # ByteCode Real Start Location Hex
        bCRealStartLocationHex = bytestream.read(2).hex()
        newbCRealStartLocationHex = bCRealStartLocationHex[2:4] + bCRealStartLocationHex[0:2]
        newbCRealStartLocationDecimal = int(newbCRealStartLocationHex, 16)

        # Go back to the start of the bytecode section and jump to the beginning
        bytestream.seek(-2, 1)
        bytestream.seek(-newbCStartLocationDecimal, 1)
        bytestream.seek(newbCRealStartLocationDecimal, 1)

        # Save ByteCode Start Hex in variable
        bCStartDecimal = bytestream.tell()
        bCStartHex = hex(bCStartDecimal)
        bCStartHexClean = bCStartHex.replace("0x", "")

        bytestream.seek(-newbCRealStartLocationDecimal, 1)
        bytestream.seek(newbCEndLocationDecimal, 1)

        # Save ByteCode End Hex in variable
        bCEndDecimal = bytestream.tell()
        bCEndHex = hex(bCEndDecimal)
        bCEndHexClean = bCEndHex.replace("0x", "")

        # Close bytestream since its not used at this point
        bytestream.close()

        # Start of writing the hex information to the abcde commands file
        outputfile = (inputFile + "_commands.txt")
        with open(outputfile, "wt", encoding="utf8") as file:
            file.write(f"""\
#GAME NAME:            Growlanser 5/6

#BLOCK NAME:            Dialogue Block (RAW)
#TYPE:                  NORMAL
#METHOD:                RAW
#SCRIPT START:          ${bCStartHexClean}
#SCRIPT STOP:           ${bCEndHexClean}
#TABLE:                 {abcdeByteCodeTableFile}
#COMMENTS:              No
#END BLOCK""")

        # Start abcde
        subprocess.run(f"perl {abcdeProgram} -m bin2text --multi-table-files -cm abcde::Cartographer \"{inputFile}\" \"{inputFile}_commands.txt\" \"{outputFileName}\" -s")