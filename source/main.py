import os
import shutil
import subprocess
import re

def clear_screen(): # Function to clear the command prompt screen
    os.system("cls")

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

    # Set PATHs for Perl
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\perl\\site\\bin"
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\perl\\bin"
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\c\\bin"

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
            sdfLocationHexbyte1 = sdfLocationHex[0] + sdfLocationHex[1]
            sdfLocationHexbyte2 = sdfLocationHex[2] + sdfLocationHex[3]
            sdfLocationHexbyte3 = sdfLocationHex[4] + sdfLocationHex[5]
            sdfLocationHexbyte4 = sdfLocationHex[6] + sdfLocationHex[7]

            newsdfLocationHex = sdfLocationHexbyte4 + sdfLocationHexbyte3 + sdfLocationHexbyte2 + sdfLocationHexbyte1

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

            scriptLocationHexbyte1 = scriptLocationHex[0] + scriptLocationHex[1]
            scriptLocationHexbyte2 = scriptLocationHex[2] + scriptLocationHex[3]
            scriptLocationHexbyte3 = scriptLocationHex[4] + scriptLocationHex[5]
            scriptLocationHexbyte4 = scriptLocationHex[6] + scriptLocationHex[7]

            newscriptLocationHex = scriptLocationHexbyte4 + scriptLocationHexbyte3 + scriptLocationHexbyte2 + scriptLocationHexbyte1

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


def ByteCodeExtractor():

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set PATHs for Perl
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\perl\\site\\bin"
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\perl\\bin"
    os.environ["PATH"] += f";{currentFolderPath}\\3rdparty\\strawberry-perl\\c\\bin"

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

        # Reorder bytes into proper order
        sdfLocationHexbyte1 = sdfLocationHex[0] + sdfLocationHex[1]
        sdfLocationHexbyte2 = sdfLocationHex[2] + sdfLocationHex[3]
        sdfLocationHexbyte3 = sdfLocationHex[4] + sdfLocationHex[5]
        sdfLocationHexbyte4 = sdfLocationHex[6] + sdfLocationHex[7]

        newSDFLocationHex = sdfLocationHexbyte4 + sdfLocationHexbyte3 + sdfLocationHexbyte2 + sdfLocationHexbyte1

        # Convert hexadecimal value to decimal, go back to the beginning of the file and jump to the SDF location
        sdfLocationDecimal = int(newSDFLocationHex, 16)
        bytestream.seek(fileBeginning, 1)
        bytestream.seek(sdfLocationDecimal, 1)


        bytestream.seek(288, 1)

        bCStartLocationHex = bytestream.read(4).hex()

        # ByteCode Start Location Hex
        bCStartLocationHexbyte1 = bCStartLocationHex[0] + bCStartLocationHex[1]
        bCStartLocationHexbyte2 = bCStartLocationHex[2] + bCStartLocationHex[3]
        bCStartLocationHexbyte3 = bCStartLocationHex[4] + bCStartLocationHex[5]
        bCStartLocationHexbyte4 = bCStartLocationHex[6] + bCStartLocationHex[7]
        newbCStartLocationHex = bCStartLocationHexbyte4 + bCStartLocationHexbyte3 + bCStartLocationHexbyte2 + bCStartLocationHexbyte1
        newbCStartLocationDecimal = int(newbCStartLocationHex, 16)


        # ByteCode End Location Hex
        bCEndLocationHex = bytestream.read(4).hex()
        bCEndLocationHexbyte1 = bCEndLocationHex[0] + bCEndLocationHex[1]
        bCEndLocationHexbyte2 = bCEndLocationHex[2] + bCEndLocationHex[3]
        bCEndLocationHexbyte3 = bCEndLocationHex[4] + bCEndLocationHex[5]
        bCEndLocationHexbyte4 = bCEndLocationHex[6] + bCEndLocationHex[7]
        newbCEndLocationHex = bCEndLocationHexbyte4 + bCEndLocationHexbyte3 + bCEndLocationHexbyte2 + bCEndLocationHexbyte1
        newbCEndLocationDecimal = int(newbCEndLocationHex, 16)

        bytestream.seek(-168, 1)
        bytestream.seek(newbCStartLocationDecimal, 1)

        bCRealStartLocationHex = bytestream.read(2).hex()
        bCRealStartLocationHexbyte1 = bCRealStartLocationHex[0] + bCRealStartLocationHex[1]
        bCRealStartLocationHexbyte2 = bCRealStartLocationHex[2] + bCRealStartLocationHex[3]
        newbCRealStartLocationHex = bCRealStartLocationHexbyte2 + bCRealStartLocationHexbyte1
        newbCRealStartLocationDecimal = int(newbCRealStartLocationHex, 16)

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
        subprocess.run(f"perl {abcdeProgram} -m bin2text --multi-table-files -cm abcde::Cartographer \"{inputFile}\" \"{inputFile}_commands.txt\" \"{outputFile}\" -s")


def GameFileExtraction():

    clear_screen()

    # Ask the user how to extract the files
    quickBMSExtractionOption = input("""\
Choose your Extraction Option:

[1] Extract only the files inside GLX_XXXX.DAT
[2] Extract the files inside GLX_XXXX.DAT and inside the extracted files

Enter the number of the option you choose: """)

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set variables for the filepaths and programs
    inputFolder = f"{currentFolderPath}\\Input"
    outputFolder = f"{currentFolderPath}\\Output"
    quickBMSProgram = f"\"{currentFolderPath}\\3rdparty\\quickbms\\quickbms.exe\""
    growlanserquickBMS = f"\"{currentFolderPath}\\3rdparty\\quickbms\\growlanser.bms\""

    # If option 1 was chosen, start the quickBMSExtraction process
    if quickBMSExtractionOption == "1":

        # List the files inside "inputFolder" and execute commands on each file (loop)
        dir_list = os.listdir(inputFolder)
        for filename in dir_list:

            # Execute quickBMS command
            subprocess.run(f"{quickBMSProgram} -w -d {growlanserquickBMS} \"{inputFolder}\\{filename}\" \"{outputFolder}\"")

    # If option 2 was chosen, start the extrended quickBMSExtraction process
    if quickBMSExtractionOption == "2":

        # List the files inside "inputFolder" and execute commands on each file (loop)
        dir_list = os.listdir(inputFolder)
        for filename in dir_list:

            # Execute quickBMS command
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


def ScriptMerger():

    clear_screen()

    # Create a variable that holds the current path
    currentFolderPath = os.getcwd()

    # Set variables for the filepaths and programs
    inputFolder = f"{currentFolderPath}\\Input"
    outputFolder = f"{currentFolderPath}\\Output"

    # Create variables based on the files in the inputFolder
    dir_list = os.listdir(inputFolder)

    jpn = []
    eng = []

    for names in dir_list:
        if names.endswith("JPN.txt"):
            jpn.append(names)
        elif names.endswith("ENG.txt"):
            eng.append(names)

    jpnstring = "".join(jpn)
    engstring = "".join(eng)

    outputFile = f"{outputFolder}\\{engstring}_output"
    outputFileName = f"{outputFile}.txt"

    jpnfile = f"{str(inputFolder)}\{jpnstring}"
    engfile = f"{str(inputFolder)}\{engstring}"

    # Separator for the text chunks
    separator = "\n\n\n\n\n"

    # Split the script into chunks and save it in a variable
    jpnfile_chunks = open(jpnfile, "rt", encoding="utf8").read().split(separator)
    engfile_chunks = open(engfile, "rt", encoding="utf8").read().split(separator)

    # Count the number of items in the lists
    print("jpnfile list items: ", len(jpnfile_chunks))
    print("engfile list items: ", len(engfile_chunks))

    # Check if both lists have the same amount of items
    if len(jpnfile_chunks) == len(engfile_chunks):

        # Add "\n" to the first "//POINTER" and remove the lines that contain "//POINTER" and "#W32" in the engfile list
        engfile_chunks = [re.sub(r'//POINTER #0', '\n//POINTER #0', chunks) for chunks in engfile_chunks]
        engfile_chunks = [re.sub(r'(\n//POINTER).+?(?=\n)', '', chunks) for chunks in engfile_chunks]
        engfile_chunks = [re.sub(r'(\n#W32).+?(?=\n)', '', chunks) for chunks in engfile_chunks]

        # Create empty list for the combined chunks
        out_chunks = []

        # Combine the chunks
        for jpnstrings, engstrings in zip(jpnfile_chunks, engfile_chunks):
            merged = jpnstrings + engstrings
            out_chunks.append(merged)

        # Merge the chunks using the separator
        merged_content = separator.join(out_chunks)

        # Save the merged script in an output file
        with open(outputFileName, "wt", encoding="utf8") as file:
            file.write(merged_content)
            print("Successfully merged the script.")    

    # If the scripts do not match
    else:
    
        # Ask the user if he wants to semi-automatically merge the scripts
        question = input("""\
The Japanese and English script does not have the same amount of entries.
Do you want to semi-automatically perform the merge?

[1] Yes
[2] No

Enter your number of the option you choose: """)
        clear_screen()

        # Execute the semi-automatic script merger
        if question == "1":

            # Add "\n" to the first "//POINTER" and remove the lines that contain "//POINTER" and "#W32" in the engfile list
            engfile_chunks = [re.sub(r'//POINTER #0', '\n//POINTER #0', chunks) for chunks in engfile_chunks]
            engfile_chunks = [re.sub(r'(\n//POINTER).+?(?=\n)', '', chunks) for chunks in engfile_chunks]
            engfile_chunks = [re.sub(r'(\n#W32).+?(?=\n)', '', chunks) for chunks in engfile_chunks]

            # Create empty list for the combined chunks
            out_chunks = []

            # Combine the chunks
            for jpnstrings, engstrings in zip(jpnfile_chunks, engfile_chunks):
                decision = input(f"""\
Japanese and English script below:
{jpnstrings}
{engstrings}

[Enter] Both scripts match, continue to the next
[1] No

Enter your number of the option you choose: """)
                if decision == "1":
                    merged = "\n\n\n\n\n" + engstrings
                else:
                    merged = jpnstrings + engstrings
                out_chunks.append(merged)
                clear_screen()

            # Merge the chunks using the separator
            merged_content = separator.join(out_chunks)

            # Save the merged script in an output file
            with open(outputFileName, "wt", encoding="utf8") as file:
                file.write(merged_content)


def NameAdder():

    clear_screen()
    print("Currently not implemented.")


def main(): # Main function

    # Delete the Input and output directory and recreate it
    if os.path.exists("Input"):
        shutil.rmtree("Input")
    if os.path.exists("Output"):
        shutil.rmtree("Output")
    os.mkdir("Input")
    os.mkdir("Output")

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

    # Execute the ScriptDump process 
    if tool == "1":
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.")
        ScriptExtractor()

    # Execute the ByteCodeDump process 
    if tool == "2":
        placeFilesinFolderDialogue = input("Please place the Growlanser 6 file(s) inside the folder \"Input\" and press enter.")
        ByteCodeExtractor()

    # Execute the Extraction process 
    if tool == "3":
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.")
        GameFileExtraction()

    # Execute the Reinsertion process 
    if tool == "4":
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) that you want to import inside the folder \"Input\".\nPlease place the Growlanser 5 / 6 \"GLX_XXXX.DAT\" file inside \"Output\" and press enter.")
        GameFileInsertion()

    # Execute the ScriptMerger process 
    if tool == "5":
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.\nPlease make sure that the script files have the ending '*ENG.txt' and '*JPN.txt'!")
        ScriptMerger()

    # Execute the ScriptMerger process 
    if tool == "6":
        placeFilesinFolderDialogue = input("Please place the Growlanser 5 / 6 file(s) inside the folder \"Input\" and press enter.")
        NameAdder()


if __name__ == "__main__":
    main()