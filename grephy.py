import os
import sys
from Nfa import *
from Dfa import *

inputFile = str(sys.argv[1])
regexFile = str(sys.argv[2])

# Check if file exists
if(os.path.isfile(inputFile) and os.path.isfile(regexFile)):
    print("Found files!")
    if(os.stat(inputFile).st_size == 0 and os.stat(regexFile).st_size == 0):
        print("Files are empty")
    inputFile = open(inputFile)
    regexFile = open(regexFile)

    with regexFile as f:
        regex = f.readline()

    with inputFile as f:
        input = f.readlines()

    regex = regex.rstrip()

    nfaObject = Nfa(regex)
    nfa = nfaObject.getNFA()
    print "\nNFA: "
    nfaObject.displayNFA()

    dfaObject = Dfa(nfa)
    dfa = dfaObject.getDFA()
    print "\nDFA: "
    dfaObject.displayMinimisedDFA()

    for i in input:
        i = i.rstrip()
        # if(match(regex, i)):
            # print i

else:
    print("File not found. Try again")
