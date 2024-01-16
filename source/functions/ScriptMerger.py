import os
import re

from functions.ClearScreen import clear_screen

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