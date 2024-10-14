import os
import shutil
import subprocess
import re
import logging
from pathlib import Path
from textwrap import dedent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Set general variables
current_folder_path = Path(__file__).resolve().parent
inputFolder = current_folder_path / "Input"
outputFolder = current_folder_path / "Output"

abcdeProgram = current_folder_path / "3rdparty" / "abcde" / "abcde.pl"
abcdeScriptTableFile = current_folder_path / "3rdparty" / "abcde" / "GL_Script.tbl"
abcdeByteCodeTableFile = current_folder_path / "3rdparty" / "abcde" / "GL_ByteCode.tbl"

quickBMSProgram = current_folder_path / "3rdparty" / "quickbms" / "quickbms.exe"
growlanserquickBMS = current_folder_path / "3rdparty" / "quickbms" / "growlanser.bms"


def clear_screen(): # Function to clear the command prompt screen
    os.system("cls")

def ScriptExtractor():

    clear_screen()

    # Call the commentsOptionDialogue and save the result in commentsOption
    commentsOption = input(dedent("""\
        Which abcde comments option do you want to use?

        [1] Yes - Which equals this formatting:
        //Anita[END-FF]

        [2] No - Which equals this formatting:
        Anita[END-FF]

        [3] Both - Which equals this formatting:
        //Anita[END-FF]
        Anita[END-FF]

        Enter your number of the option you choose: """))

    clear_screen()

    if commentsOption == "1":
        commentsOption = "Yes"

    elif commentsOption == "2":
        commentsOption = "No"

    elif commentsOption == "3":
        commentsOption = "Both"

    # Call the abcdeCodeOptionDialogue and save the result in abcdeAtlasOption
    abcdeAtlasOption = input(dedent("""\
        Do you want to add abcde Atlas code on top of each dumped script?

        [1] Yes
        [2] No

        Enter your number of the option you choose: """))

    clear_screen()

    # Call the growlanserVersionOptionDialogue and save the result in growlanserVersionOption
    growlanserVersionOptionDialogue = input(dedent("""\
        Which Game are you trying to dump the script from?

        [1] Growlanser 5 JPN
        [2] Growlanser 5 ENG
        [3] Growlanser 6 JPN

        Enter your number of the option you choose: """))

    clear_screen()

    logging.info("Starting the ScriptDump process, thank you for flying with Risae Nyan Airlines.")
    logging.info("We hope you will enjoy the ride and results of this tool!")

    if growlanserVersionOptionDialogue == "1":
        growlanserVersionOption = "GL5JPN"

    elif growlanserVersionOptionDialogue == "2":
        growlanserVersionOption = "GL5ENG"

    elif growlanserVersionOptionDialogue == "3":
        growlanserVersionOption = "GL6JPN"

    logging.info("The following files will be processed:")

    for filename in inputFolder.iterdir():
        logging.info(filename.name)

    # List the files inside "inputFolder" and execute commands on each file (loop)
    for filename in inputFolder.iterdir():

        logging.info(f"<><><><><> Working on {filename.name} <><><><><>")

        # Create variables for the files
        outputFileName = f"{filename}_{growlanserVersionOption}"

        try:

            logging.info(f"{filename.name}: Checking its is a dummy file...")

            with open(filename, "rb") as bytestream:

                bytestream.seek(128, 0)
                if (bytestream.read(16).hex()) == "835f837e815b837483408343838b0d0a":
                    logging.info(f"{filename.name}: is a dummy file, skipping file.")
                    continue

                bytestream.seek(1408, 0) # 0 = beginning of the file
                if (bytestream.read(16).hex()) == "53444600000001004000000030000000":
                    logging.info(f"{filename.name}: is a file that doesn't really have text in it, skipping file.")
                    continue

                bytestream.seek(1152, 0)
                if (bytestream.read(16).hex()) == "53444600000001004000000030000000":
                    logging.info(f"{filename.name}: is a file that doesn't really have text in it, skipping file.")
                    continue

            logging.info(f"{filename.name}: Checking what kind of script file it is, create variables for the SDF section based on the results...")

            # Depending on the file extension, set the sdfBytesPosition and fileBeginning variables
            if str(filename.name).endswith(".SCEN"):
                sdfBytesPosition = 56

            elif str(filename.name).endswith(".SDMY"):
                sdfBytesPosition = 56

            elif str(filename.name).endswith(".STXT"):
                sdfBytesPosition = 32

            elif str(filename.name).endswith(".SCEC"):
                sdfBytesPosition = 40

            logging.info(f"{filename.name}: Opening file in 'read byte' mode and doing some magic...")

            with open(filename, "rb") as bytestream:
                bytestream.seek(sdfBytesPosition, 1)
                sdfLocationHex = bytestream.read(4).hex()

                # Reorder bytes into proper order
                newsdfLocationHex = sdfLocationHex[6:8] + sdfLocationHex[4:6] + sdfLocationHex[2:4] + sdfLocationHex[0:2]

                # Convert hexadecimal value to decimal and jump to the SDF location
                sdfLocationDecimal = int(newsdfLocationHex, 16)
                bytestream.seek(sdfLocationDecimal, 0) # 0 = beginning of the file

                ### Get Start of the pointer table position into a variable
                # Move 32 bytes ahead to the start of the pointer table
                bytestream.seek(32, 1)

                # Save the start of the pointer table location as a hexadecimal string
                pointerTableStartHex = format(bytestream.tell(), 'x')

                # Move 32 bytes back to the original SDF location
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

                # Save the start of the script location as a hexadecimal string
                scriptStartHex = format(bytestream.tell(), 'x')

                ### Start of the pointer table end
                bytestream.seek(-4, 1)

                # Check for consecutive 4-byte sequences of zeros in the binary file.
                # When a non-zero 4-byte sequence is encountered, set `pointertableEndHex` to the current file location in hexadecimal.
                # If the first 4-byte sequence is non-zero, set `pointertableEndHex` to `scriptStartHex`.
                if (bytestream.read(4).hex()) == "00000000":
                    bytestream.seek(-8, 1)
                    if (bytestream.read(4).hex()) == "00000000":
                        bytestream.seek(-8, 1)
                        if (bytestream.read(4).hex()) == "00000000":
                            bytestream.seek(-8, 1)
                            if (bytestream.read(4).hex()) == "00000000":
                                bytestream.seek(-8, 1)
                            else:
                                pointertableEndHex = format(bytestream.tell(), 'x')
                        else:
                            pointertableEndHex = format(bytestream.tell(), 'x')
                    else:
                        pointertableEndHex = format(bytestream.tell(), 'x')
                else:
                    pointertableEndHex = scriptStartHex

            logging.info(f"{filename.name}: Finished intel gathering and preparing the script dump...")

            # Create the abcde commands file
            with open(f"{filename}_commands.txt", "wt", encoding="utf8") as file:
                file.write(dedent(f"""\
                    #GAME NAME:            Growlanser 5/6

                    #BLOCK NAME:           Dialogue Block (POINTER_RELATIVE)
                    #TYPE:                 NORMAL
                    #METHOD:               POINTER_RELATIVE
                    #POINTER ENDIAN:       LITTLE
                    #POINTER TABLE START:  ${pointerTableStartHex}
                    #POINTER TABLE STOP:   ${pointertableEndHex}
                    #POINTER SIZE:         $04
                    #POINTER SPACE:        $00
                    #ATLAS PTRS:           Yes
                    #BASE POINTER:         ${scriptStartHex}
                    #TABLE:                {abcdeScriptTableFile}
                    #COMMENTS:             {commentsOption}
                    #SHOW END ADDRESS:     No
                    #END BLOCK"""))

            # Start abcde
            subprocess.run(f"perl \"{abcdeProgram}\" --stats --mode bin2text -cm abcde::Cartographer \"{filename}\" \"{filename}_commands.txt\" \"{outputFileName}\" -s")

            logging.info(f"{filename.name}: Script dump finished, making some finishing touches on the dumped script...")

            # Open the file
            with open(f"{outputFileName}.txt", "r+", encoding="utf8") as file:
                # Read the file data
                filedata = file.read()

                # Replace the target string
                filedata = filedata.replace("//POINTER #", "\n\n\n\n\n//POINTER #")

                # Split the file data into lines and delete line 1-15 (premade abcde Atlas code)
                lines = filedata.splitlines()
                del lines[0:17]

                # Write 4 newlines at the end (5 would make it 6 in total at the end)
                lines.append("\n\n\n\n")

                # Move the pointer to the beginning of the file
                file.seek(0)

                # Write the modified data back to the file
                file.write('\n'.join(lines))

                # Truncate the file to remove any remaining original data
                file.truncate()

            # If abcdeAtlasOption = 1, then open the output file and read all lines
            if abcdeAtlasOption == "1":

                logging.info(f"{filename.name}: abcdeAtlasOption == '1'")

                with open(f"{outputFileName}.txt", "rt", encoding="utf8") as file:
                    lines = file.readlines()

                logging.info(f"{filename.name}: Copying the PointerStart and TextblockStart values from the first pointer...")
                # Example "$FA0" and "$FD0":
                # //POINTER #0 @ $FA0 - STRING #0 @ $FD0
                line2data  = lines[0].split() # Split the line into a list
                pointerStart = " ".join(line2data[3:-5]) # Join the list items together, starting from the 4th item and ending at the 5th last item
                textBlockStartBroken = line2data[8] # Get the 9th item in the list
                textBlockStart = textBlockStartBroken.strip() # Remove the "\n" from the 9th item

                logging.info(f"{filename.name}: Creating the Atlas code and inserting the values...")

                abcdeAtlasCode = dedent(f"""\
                    #VAR(dialogue, TABLE)
                    #ADDTBL("GL_Script.tbl", dialogue)
                    #ACTIVETBL(dialogue)

                    #VAR(PTR, CUSTOMPOINTER)
                    #CREATEPTR(PTR, "LINEAR", {textBlockStart}, 32)

                    #VAR(PTRTBL, POINTERTABLE)
                    #PTRTBL(PTRTBL, {pointerStart}, 4, PTR)

                    #JMP({textBlockStart})
                    #HDR({textBlockStart})""")

                logging.info(f"{filename.name}: Opening the file and saving the Atlas code + the actual script...")

                with open(f"{outputFileName}.txt",'rt', encoding="utf8") as contents:
                    save = contents.read()

                with open(f"{outputFileName}.txt",'wt', encoding="utf8") as contents:
                    contents.write(abcdeAtlasCode)
                    contents.write("\n\n\n") # 3 newlines to give proper spacing
                    contents.write(save)

            logging.info(f"{filename.name}: Moving file to output folder...")
            shutil.move(f"{outputFileName}.txt", outputFolder)

        except Exception as Error:
            logging.info(f"{filename.name}: does not contain a script or is a dummyfile, skipping the file.")
            logging.info(Error)
            continue


def ByteCodeExtractor():

    clear_screen()

    logging.info("Starting the ByteCode Dump process, thank you for flying with Risae Nyan Airlines.")
    logging.info("We hope you will enjoy the ride and results of this tool!")

    # List the files inside "input_folder" and execute commands on each file (loop)
    for filename in inputFolder.iterdir():

        # Open file in "read byte", move pointer to the bytes that point to SDF and read the next 4 bytes
        with open(filename, "rb") as bytestream:
            bytestream.seek(40, 0) # 0 = beginning of the file
            sdfLocationHex = bytestream.read(4).hex()

            # Reorder bytes into proper order
            newSDFLocationHex = sdfLocationHex[6:8] + sdfLocationHex[4:6] + sdfLocationHex[2:4] + sdfLocationHex[0:2]

            # Convert hexadecimal value to decimal, go back to the beginning of the file and jump to the SDF location
            sdfLocationDecimal = int(newSDFLocationHex, 16)
            bytestream.seek(sdfLocationDecimal, 0) # 0 = beginning of the file

            # ???
            bytestream.seek(288, 1)

            # ByteCode Start Location Hex
            bCStartLocationHex = bytestream.read(4).hex()

            # Reorder bytes into proper order
            newbCStartLocationHex = bCStartLocationHex[6:8] + bCStartLocationHex[4:6] + bCStartLocationHex[2:4] + bCStartLocationHex[0:2]

            # Convert hexadecimal value to decimal
            newbCStartLocationDecimal = int(newbCStartLocationHex, 16)

            # ByteCode End Location Hex
            bCEndLocationHex = bytestream.read(4).hex()

            # Reorder bytes into proper order
            newbCEndLocationHex = bCEndLocationHex[6:8] + bCEndLocationHex[4:6] + bCEndLocationHex[2:4] + bCEndLocationHex[0:2]

            # Convert hexadecimal value to decimal
            newbCEndLocationDecimal = int(newbCEndLocationHex, 16)

            bytestream.seek(-168, 1)
            bytestream.seek(newbCStartLocationDecimal, 1)

            # ByteCode Real Start Location Hex
            bCRealStartLocationHex = bytestream.read(2).hex()

            # Reorder bytes into proper order
            newbCRealStartLocationHex = bCRealStartLocationHex[2:4] + bCRealStartLocationHex[0:2]

            # Convert hexadecimal value to decimal
            newbCRealStartLocationDecimal = int(newbCRealStartLocationHex, 16)

            bytestream.seek(-2, 1)
            bytestream.seek(-newbCStartLocationDecimal, 1)
            bytestream.seek(newbCRealStartLocationDecimal, 1)

            # Save ByteCode Start Hex in variable
            bCStartHex = format(bytestream.tell(), 'x')

            bytestream.seek(-newbCRealStartLocationDecimal, 1)
            bytestream.seek(newbCEndLocationDecimal, 1)

            # Save ByteCode End Hex in variable
            bCEndHex = format(bytestream.tell(), 'x')

        # Start of writing the hex information to the abcde commands file
        with open(f"{filename}_commands.txt", "wt", encoding="utf8") as file:
            file.write(dedent(f"""\
                #GAME NAME:            Growlanser 5/6

                #BLOCK NAME:            Dialogue Block (RAW)
                #TYPE:                  NORMAL
                #METHOD:                RAW
                #SCRIPT START:          ${bCStartHex}
                #SCRIPT STOP:           ${bCEndHex}
                #TABLE:                 {abcdeByteCodeTableFile}
                #COMMENTS:              No
                #END BLOCK"""))

        # Start abcde
        subprocess.run(f"perl \"{abcdeProgram}\" --stats --mode bin2text --multi-table-files -cm abcde::Cartographer \"{filename}\" \"{filename}_commands.txt\" \"{filename}\" -s")

        logging.info("Moving file to output folder...")
        shutil.move(f"{filename}.txt", outputFolder)


def GameFileExtraction():

    clear_screen()

    # Ask the user how to extract the files
    quickBMSExtractionOption = input(dedent("""\
        Choose your Extraction Option:

        [1] Extract only the files inside GLX_XXXX.DAT
        [2] Extract the files inside GLX_XXXX.DAT and inside the extracted files

        Enter the number of the option you choose: """))

    clear_screen()

    # If option 1 was chosen, start the quickBMSExtraction process
    if quickBMSExtractionOption == "1":

        # Execute quickBMS command
        for filename in inputFolder.iterdir():
            subprocess.run(f"{quickBMSProgram} -w -d \"{growlanserquickBMS}\" \"{filename}\" \"{outputFolder}\"")

    # If option 2 was chosen, start the extrended quickBMSExtraction process
    if quickBMSExtractionOption == "2":

        # Execute quickBMS command
        for filename in inputFolder.iterdir():
            subprocess.run(f"{quickBMSProgram} -w -d \"{growlanserquickBMS}\" \"{filename}\" \"{outputFolder}\"")

            # Create a list of all the file extentions in the newOutputFolder
            SplitTypes=[]
            for file in os.listdir(outputFolder):
                SplitTypes.append(file.split('.')[-1])

            # Remove dublicates from the list
            newList = list(dict.fromkeys(SplitTypes))

            # Create blacklist of files that can't be extracted a second time (at least with the current quickbms script)
            blacklist = ["000", "v_0", "b00", "sel", "her", "mot", "MAPTBL", "txt", "MAPOBJ", "IRX"]

            # If a blacklistItem is exists in newList, remove it from the list
            for blacklistItem in blacklist:
                if blacklistItem in newList:
                    newList.remove(blacklistItem)

            # List the files inside "inputFolder" and execute commands on each file (loop)
            newOutputFolder = outputFolder / filename.name

            # Start the extended quickBMS extration process
            for fileType in newList:

                # Create quickBMS command and execute it
                subprocess.run(f"{quickBMSProgram} -w -d -F \"*.{fileType}\" \"{growlanserquickBMS}\" \"{newOutputFolder}\" \"{newOutputFolder}\"")


def GameFileInsertion():

    clear_screen()

    # Execute quickBMS command
    for filename in outputFolder.iterdir():
        subprocess.run(f"{quickBMSProgram} -w -r -r \"{growlanserquickBMS}\" \"{filename}\" \"{inputFolder}\"")


def ScriptMerger():

    clear_screen()

    jpn = []
    eng = []

    for filename in inputFolder.iterdir():
        if filename.endswith("JPN.txt"):
            jpn.append(filename)

        elif filename.endswith("ENG.txt"):
            eng.append(filename)

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
        engfile_chunks = [
            re.sub(r'(\n#W32).+?(?=\n)', '',
            re.sub(r'(\n//POINTER).+?(?=\n)', '',
            re.sub(r'//POINTER #0', '\n//POINTER #0',
                    chunk)
                )
            )
            for chunk in engfile_chunks
        ]

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
        question = input(dedent("""\
            The Japanese and English script does not have the same amount of entries.
            Do you want to semi-automatically perform the merge?

            [1] Yes
            [2] No

            Enter your number of the option you choose: """))

        clear_screen()

        # Execute the semi-automatic script merger
        if question == "1":

            # Add "\n" to the first "//POINTER" and remove the lines that contain "//POINTER" and "#W32" in the engfile list
            engfile_chunks = [
                re.sub(r'(\n#W32).+?(?=\n)', '',
                re.sub(r'(\n//POINTER).+?(?=\n)', '',
                re.sub(r'//POINTER #0', '\n//POINTER #0',
                       chunk)
                    )
                )
                for chunk in engfile_chunks
            ]

            # Create empty list for the combined chunks
            out_chunks = []

            # Combine the chunks
            for jpnstrings, engstrings in zip(jpnfile_chunks, engfile_chunks):

                decision = input(dedent(f"""\
                    Japanese and English script below:
                    {jpnstrings}
                    {engstrings}

                    [Enter] Both scripts match, continue to the next
                    [1] No

                    Enter your number of the option you choose: """))

                clear_screen()

                if decision == "1":
                    merged = "\n\n\n\n\n" + engstrings
                else:
                    merged = jpnstrings + engstrings
                out_chunks.append(merged)

            # Merge the chunks using the separator
            merged_content = separator.join(out_chunks)

            # Save the merged script in an output file
            with open(outputFileName, "wt", encoding="utf8") as file:
                file.write(merged_content)


def NameAdder():
    # Open the file '00000031.SCEN Chapter X' in read mode
    with open('00000031.SCEN Chapter X', 'r') as infile:
        # Read all lines from the file
        lines = infile.readlines()

    # Join all lines into a single string, then split it into sections by five consecutive newline characters
    sections = ''.join(lines).split('\n\n\n\n\n')

    # Iterate over each section with its index
    for i, section in enumerate(sections):
        # Split the section into lines
        lines_in_section = section.split('\n')
        # Find the index of the first line that doesn't start with '//' or '#' and is not empty
        first_non_comment_index = next((i for i, line in enumerate(lines_in_section) if not line.startswith('//') and not line.startswith('#') and line.strip()), len(lines_in_section))
        # Insert '//Systems Message\\\\' at the found index
        lines_in_section.insert(first_non_comment_index, '//Systems Message\\\\')
        # Join the lines back together and replace the section in the list
        sections[i] = '\n'.join(lines_in_section)

    # Open 'output.txt' in write mode
    with open('output.txt', 'w') as outfile:
        # Join the sections back together with five newline characters between each, and write it to the file
        outfile.write('\n\n\n\n\n'.join(sections))


def main(): # Main function

    clear_screen()

    # Call the ToolDialogue and save the input in the variable "tool", clear command prompt
    tool = input(dedent("""\
        Welcome to the Growlanser 5 and 6 Toolkit!

        Which Growlanser 5 / 6 Tool do you want to use?

        [1] .SCEN/.SCEC/.SDMY/.STXT: Extraction (Growlanser 5 / 6)
        [2] .SCEN/.SCEC/.SDMY/.STXT: Bytecode Extraction (Growlanser 6)
        [3] GLX_XXXX.DAT: Extraction (Growlanser 5 / 6)
        [4] GLX_XXXX.DAT: Reinsertion (Growlanser 5 / 6)
        [5] .SCEN/.SCEC/.SDMY/.STXT: Merger (Growlanser 5 / 6)
        [6] .SCEN/.SCEC/.SDMY/.STXT: Character Name Adder (Growlanser 5 / 6) (WIP)

        Enter your number of the option you choose: """))

    clear_screen()

    # Delete the Input and output directory and recreate it
    if os.path.exists(inputFolder):
        logging.info("Input folder found, removing it")
        shutil.rmtree(inputFolder)

    logging.info("Creating Input folder")
    os.mkdir(inputFolder)

    if os.path.exists(outputFolder):
        logging.info("Output folder found, removing it")
        shutil.rmtree(outputFolder)

    logging.info("Creating Output folder")
    os.mkdir(outputFolder)

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