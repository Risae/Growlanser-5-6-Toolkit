import os
import subprocess
from functions.ClearScreen import clear_screen

def ScriptExtractor():

    clear_screen()

    # Call the commentsOptionDialogue and save the result in commentsOption
    commentsOption = input("""\
Which abcde comments option do you want to use?

[1] Yes - Which equals this formatting:
//Anita[END-FF]

[2] No - Which equals this formatting:
Anita[END-FF]

[3] Both - Which equals this formatting:
//Anita[END-FF]
Anita[END-FF]

Enter your number of the option you choose: \
""")

    clear_screen()

    if commentsOption == "1":
        commentsOption = "Yes"

    elif commentsOption == "2":
        commentsOption = "No"

    elif commentsOption == "3":
        commentsOption = "Both"

    # Call the abcdeCodeOptionDialogue and save the result in abcdeAtlasOption
    abcdeAtlasOption = input("""\
Do you want to add abcde Atlas code on top of each dumped script?

[1] Yes
[2] No

Enter your number of the option you choose: \
""")

    clear_screen()

    # Call the growlanserVersionOptionDialogue and save the result in growlanserVersionOption
    growlanserVersionOptionDialogue = input("""\
Which Game are you trying to dump the script from?

[1] Growlanser 5 JPN
[2] Growlanser 5 ENG
[3] Growlanser 6 JPN

Enter your number of the option you choose: \
""")

    clear_screen()

    if growlanserVersionOptionDialogue == "1":
        growlanserVersionOption = "GL5JPN"

    elif growlanserVersionOptionDialogue == "2":
        growlanserVersionOption = "GL5ENG"

    elif growlanserVersionOptionDialogue == "3":
        growlanserVersionOption = "GL6JPN"

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set variables for the Python and Perl commands
    inputFolder = f"{currentFolderPath}\\Input"
    outputFolder = f"{currentFolderPath}\\Output"
    abcdeProgram = f"\"{currentFolderPath}\\3rdparty\\abcde\\abcde.pl\""
    abcdeScriptTableFile = f"\"{currentFolderPath}\\3rdparty\\abcde\\GL_Script.tbl\""

    # List the files inside "inputFolder" and execute commands on each file (loop)
    dir_list = os.listdir(inputFolder)
    for filename in dir_list:

        # Create variables for the files
        inputFile = f"{inputFolder}\\{filename}"
        outputFile = f"{outputFolder}\\{filename}_{growlanserVersionOption}"
        outputFileName = f"{outputFile}.txt"

        # Everything else should be a real script file -> start the actual script extraction.
        try:
            # Check what file it is and create variables for the SDF section based on the file
            if inputFile.endswith(".SCEN"):
                sdfBytesPosition = 56
                fileBeginning = -60

            elif inputFile.endswith(".SDMY"):
                sdfBytesPosition = 56
                fileBeginning = -60

            elif inputFile.endswith(".STXT"):
                sdfBytesPosition = 32
                fileBeginning = -36

            elif inputFile.endswith(".SCEC"):
                sdfBytesPosition = 40
                fileBeginning = -44

            # Open file in "read byte", move pointer to the bytes that point to SDF and read the next 4 bytes
            bytestream = open(inputFile, "rb")
            bytestream.seek(sdfBytesPosition, 1)
            sdfLocationHex = bytestream.read(4).hex()

            # Reorder bytes into proper order
            newsdfLocationHex = sdfLocationHex[6:8] + sdfLocationHex[4:6] + sdfLocationHex[2:4] + sdfLocationHex[0:2]

            # Convert hexadecimal value to decimal, go back to the beginning of the file and jump to the SDF location
            sdfLocationDecimal = int(newsdfLocationHex, 16)
            bytestream.seek(fileBeginning, 1)
            bytestream.seek(sdfLocationDecimal, 1)


            ### Get Start of the pointer table position into a variable
            # Move 32 bytes ahead (to the start of the pointer table)
            bytestream.seek(32, 1)

            # Create variable based of the current location in the file, convert from Decimal to Hex, remove 0x from Hex variable
            pointerTableStartDecimal = bytestream.tell()
            pointerTableStartHex = hex(pointerTableStartDecimal)
            pointerTableStartHexClean = pointerTableStartHex.replace("0x", "")

            # Go to the SDF location
            bytestream.seek(-32, 1)

            ### Get Start of the script position into a variable 
            # Move 12 bytes ahead, read 4 bytes (start of the script) and reorder bytes into proper order
            bytestream.seek(12, 1)
            scriptLocationHex = bytestream.read(4).hex()

            # Reorder bytes into proper order
            newscriptLocationHex = scriptLocationHex[6:8] + scriptLocationHex[4:6] + scriptLocationHex[2:4] + scriptLocationHex[0:2]


            # Convert hexadecimal value to decimal, go back 16 bytes and move the amount of bytes ahead based of the locationdecimal
            scriptLocationDecimal = int(newscriptLocationHex, 16)
            bytestream.seek(-16, 1)
            bytestream.seek(scriptLocationDecimal, 1)

            # Create variable based of the current location in the file, Convert variable from Decimal to Hex, Remove 0x from Hex variable
            scriptStartDecimal = bytestream.tell()
            scriptStartHex = hex(scriptStartDecimal)
            scriptStartHexClean = scriptStartHex.replace("0x", "")

            ### Start of the pointer table end
            bytestream.seek(-4, 1)

            if (bytestream.read(4).hex()) == "00000000":
                bytestream.seek(-8, 1)
                if (bytestream.read(4).hex()) == "00000000":
                    bytestream.seek(-8, 1)
                    if (bytestream.read(4).hex()) == "00000000":
                        bytestream.seek(-8, 1)
                        if (bytestream.read(4).hex()) == "00000000":
                            bytestream.seek(-8, 1)
                        else:
                            pointertableEndDecimal = bytestream.tell()
                            pointertableEndHex = hex(pointertableEndDecimal)
                            pointertableEndHexClean = pointertableEndHex.replace("0x", "")
                    else:
                        pointertableEndDecimal = bytestream.tell()
                        pointertableEndHex = hex(pointertableEndDecimal)
                        pointertableEndHexClean = pointertableEndHex.replace("0x", "")
                else:
                    pointertableEndDecimal = bytestream.tell()
                    pointertableEndHex = hex(pointertableEndDecimal)
                    pointertableEndHexClean = pointertableEndHex.replace("0x", "")
            else:
                pointertableEndHexClean = scriptStartHexClean


            # Close bytestream since its not used at this point
            bytestream.close()

            # Start of writing the hex information to the abcde commands file
            outputfile = f"{inputFile}_commands.txt"
            with open(outputfile, "wt", encoding="utf8") as file:
                file.write(f"""\
#GAME NAME:            Growlanser 5/6

#BLOCK NAME:           Dialogue Block (POINTER_RELATIVE)
#TYPE:                 NORMAL
#METHOD:               POINTER_RELATIVE
#POINTER ENDIAN:       LITTLE
#POINTER TABLE START:  ${pointerTableStartHexClean}
#POINTER TABLE STOP:   ${pointertableEndHexClean}
#POINTER SIZE:         $04
#POINTER SPACE:        $00
#ATLAS PTRS:           Yes
#BASE POINTER:         ${scriptStartHexClean}
#TABLE:                {abcdeScriptTableFile}
#COMMENTS:             {commentsOption}
#SHOW END ADDRESS:     No
#END BLOCK""")

            # Start abcde
            subprocess.run(f"perl {abcdeProgram} -m bin2text -cm abcde::Cartographer \"{inputFile}\" \"{inputFile}_commands.txt\" \"{outputFile}\" -s")

            # Read in the file, Replace the target string, Write the file out again
            with open(outputFileName, "rt", encoding="utf8") as file:
                filedata = file.read()
            filedata = filedata.replace("//POINTER #", "\n\n\n\n\n//POINTER #")
            with open(outputFileName, "wt", encoding="utf8") as file:
                file.write(filedata)

            # Readlines in the file, delete line 1-18 (premade abcde Atlas code), write 5 newlines at the end and write the file out again
            with open(outputFileName, "rt", encoding="utf8") as file:
                lines = file.readlines()
            del lines[0:17]
            with open(outputFileName, "wt", encoding="utf8") as file:
                for line in lines:
                    file.write(line)
                file.write("\n\n\n\n\n")

            # If abcdeAtlasOption = 1, then open the output file and read all lines
            if abcdeAtlasOption == "1":
                with open(outputFileName, "rt", encoding="utf8") as file:
                    lines = file.readlines()

                # Copy the PointerStart and TextblockStart values from the first pointer
                # Example "$FA0" and "$FD0":
                # //POINTER #0 @ $FA0 - STRING #0 @ $FD0
                line2data  = lines[2]
                pointerStart = (" ".join(line2data.split()[3:-5]))
                textBlockStart = (" ".join(line2data.split()[3:-5]))
                textBlockStartBroken = (line2data.split(" ")[8:][0])
                textBlockStart = textBlockStartBroken.strip()

                # Create the Atlas code and insert the values
                abcdeAtlasCode = (f"""\
#VAR(dialogue, TABLE)
#ADDTBL({abcdeScriptTableFile}, dialogue)
#ACTIVETBL(dialogue)

#VAR(PTR, CUSTOMPOINTER)
#CREATEPTR(PTR, "LINEAR", {textBlockStart}, 32)

#VAR(PTRTBL, POINTERTABLE)
#PTRTBL(PTRTBL, {pointerStart}, 4, PTR)

#JMP({textBlockStart})
#HDR({textBlockStart})
""")

                # Open the outputFileName and save the Atlas code and after that the actual script in the file
                with open(outputFileName,'rt', encoding="utf8") as contents:
                    save = contents.read()
                with open(outputFileName,'wt', encoding="utf8") as contents:
                    contents.write(abcdeAtlasCode)
                    contents.write(save)
        except:
            print(inputFile + " does not contain a script or is a dummyfile, skipping the file.")
            continue