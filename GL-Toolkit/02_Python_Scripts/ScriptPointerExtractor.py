import sys
import getopt


### Command line arguments code start
args=sys.argv[1:]
inputfile = ""
comments = ""
tablefile = ""

opts, args = getopt.getopt(args,"hi:c:t:",["inputfile=","comments=","tablefile="])

for opt, arg in opts:
    if opt == "-h":
        print ("PointerExtractor.py -i <inputfile> -c <comments> -t <tablefile>")
        sys.exit()
    elif opt in ("-i", "--inputfile"):
        inputfile = arg
    elif opt in ("-c", "--comments"):
        comments = arg
    elif opt in ("-t", "--tablefile"):
        tablefile = arg
### End


### Check what file it is and create variables for the SDF section based on the file
if inputfile.endswith(".SCEN"):
    #print("SCEN File!")
    sdfBytesPosition = 56
    fileBeginning = -60

elif inputfile.endswith(".SDMY"):
    #print("STXT File!")
    sdfBytesPosition = 56
    fileBeginning = -60

elif inputfile.endswith(".STXT"):
    #print("STXT File!")
    sdfBytesPosition = 32
    fileBeginning = -36

elif inputfile.endswith(".SCEC"):
    #print("SCEC File!")
    sdfBytesPosition = 40
    fileBeginning = -44


# Open file in "read byte", move pointer to the bytes that point to SDF and read the next 4 bytes
bytestream = open(inputfile, "rb")
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

#print("Pointer Table Start .SCEN:", pointerTableStartHexClean)
### End of Start of the pointer table


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

#print("Script Start Hex .SCEN:", scriptStartHexClean)
###


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

#print("Pointer Table End Hex .SCEN:", pointertableEndHexClean)
###

# Close bytestream since its not used at this point
bytestream.close()

### Start of writing the hex information to the abcde commands file
outputfile = (inputfile + "_commands.txt")
abcdeCommands = open(outputfile, "w")

abcdeCommands.write(
        "#GAME NAME:            Growlanser 5/6\n"
        "\n"
        "#BLOCK NAME:           Dialogue Block (POINTER_RELATIVE)\n"
        "#TYPE:                 NORMAL\n"
        "#METHOD:               POINTER_RELATIVE\n"
        "#POINTER ENDIAN:       LITTLE\n"
        "#POINTER TABLE START:  $" + pointerTableStartHexClean + "\n"
        "#POINTER TABLE STOP:   $" + pointertableEndHexClean + "\n"
        "#POINTER SIZE:         $04\n"
        "#POINTER SPACE:        $00\n"
        "#ATLAS PTRS:           Yes\n"
        "#BASE POINTER:         $" + scriptStartHexClean + "\n"
        "#TABLE:                " + tablefile + "\n"
        "#COMMENTS:             " + comments + "\n"
        "#SHOW END ADDRESS:     No\n"
        "#END BLOCK")

abcdeCommands.close()
### End of writing the hex information into the abcde commands file