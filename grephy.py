import os
import sys

inputFile = str(sys.argv[1])
regexFile = str(sys.argv[2])

# Check if file exists
if(os.path.isfile(inputFile) and os.path.isfile(regexFile)):
    print("Found files!")
    if(os.stat(inputFile).st_size == 0 and os.stat(regexFile).st_size == 0):
        print("Files are empty")
    inputFile = open(inputFile)
    regexFile = open(regexFile)

    with inputFile as f:
        input = f.readline()
    with regexFile as f:
        regex = f.readline()

    # Get alphabet from regex
    alphabet = regex.translate(None, '*()')

    if(sorted(alphabet) == sorted(input)):
        print "Alphabet matches!"
    else:
        print "Input is not in the alphabet"
else:
    print("File not found. Try again")
