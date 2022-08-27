import sys
import getopt

### Command line arguments
args=sys.argv[1:]
inputfile = ""
comments = ""
tablefile = ""

opts, args = getopt.getopt(args,"hi:c:t:",["inputfile=","comments=","tablefile="])

for opt, arg in opts:
    if opt == "-h":
        print("PointerExtractor.py -i <inputfile> -c <comments> -t <tablefile>")
        sys.exit()
    elif opt in ("-i", "--inputfile"):
        inputfile = arg
    elif opt in ("-c", "--comments"):
        comments = arg
    elif opt in ("-t", "--tablefile"):
        tablefile = arg

### Check what file it is and create variables for the SDF section based on the file
if inputfile.endswith(".SCEN"):
    sdfBytesPosition = 56
    fileBeginning = -60

elif inputfile.endswith(".SDMY"):
    sdfBytesPosition = 56
    fileBeginning = -60

elif inputfile.endswith(".STXT"):
    sdfBytesPosition = 32
    fileBeginning = -36

elif inputfile.endswith(".SCEC"):
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

### Start of writing the hex information to the abcde commands file
outputfile = f"{inputfile}_commands.txt"
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
#TABLE:                {tablefile}
#COMMENTS:             {comments}
#SHOW END ADDRESS:     No
#END BLOCK""")