import os
import sys
from Nfa import *
from Dfa import *

# Example call - python Grephy.py -n nfaFile -d dfaFile tests/regex.txt tests/input.txt

# If they want an nfa created the following param will be the path name
if(str(sys.argv[1]) == "-n"):
    nfaFile = str(sys.argv[2])
    dfaFile = str(sys.argv[4])
# TODO: Add different combinations of -n and -d
# TODO: More error handling

inputFile = str(sys.argv[5])
regexFile = str(sys.argv[6])

# Check if file exists
if(os.path.isfile(inputFile) and os.path.isfile(regexFile)):
    print("Found input and regex files.")
    if(os.stat(inputFile).st_size == 0 and os.stat(regexFile).st_size == 0):
        print("Files are empty. Try again.")
    inputFile = open(inputFile)
    regexFile = open(regexFile)

    with regexFile as f:
        regex = f.readline()

    with inputFile as f:
        input = f.readlines()

    regex = regex.rstrip()

    nfaObject = Nfa(regex)
    nfa = nfaObject.getNFA()

    dfaObject = Dfa(nfa)
    dfa = dfaObject.getDFA()

    # Draw the graphs
    # drawGraph(nfa, "nfa")
    # drawGraph(dfa, "dfa")

    # Create the dot files
    dfa.createDotFile(dfaFile)
    nfa.createDotFile(nfaFile)
    
    for i in input:
        i = i.rstrip()
        # if(match(regex, i)):
            # print i

else:
    print("File not found. Try again")
