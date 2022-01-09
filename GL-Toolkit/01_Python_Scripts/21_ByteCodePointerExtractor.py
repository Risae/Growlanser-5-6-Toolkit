import sys
import getopt

### Command line arguments code start
args=sys.argv[1:]
inputfile = ""
comments = ""
tablefile = ""

opts, args = getopt.getopt(args,"hi:c:t:",["inputfile=","tablefile="])

for opt, arg in opts:
    if opt == "-h":
        print ("PointerExtractor.py -i <inputfile> -t <tablefile>")
        sys.exit()
    elif opt in ("-i", "--inputfile"):
        inputfile = arg
    elif opt in ("-t", "--tablefile"):
        tablefile = arg
### End

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

### Start of writing the hex information to the abcde commands file
outputfile = (inputfile + "_commands.txt")
with open(outputfile, "wt", encoding="utf8") as file:
    file.write(f"""\
#GAME NAME:            Growlanser 5/6

#BLOCK NAME:            Dialogue Block (RAW)
#TYPE:                  NORMAL
#METHOD:                RAW
#SCRIPT START:          ${bCStartHexClean}
#SCRIPT STOP:           ${bCEndHexClean}
#TABLE:                 {tablefile}
#COMMENTS:              No
#END BLOCK""")