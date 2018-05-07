import os
import sys
from Nfa import *
from Dfa import *

# Example call - python Grephy.py -n nfaFile -d dfaFile tests/regex.txt tests/input.txt
nfaFile = None
dfaFile = None
regexFile = None
inputFile = None
draw = None

def main():
    handleInput()
    createAutomatas()


def handleInput():
    global regexFile
    global inputFile
    global nfaFile
    global dfaFile
    global draw

    # If the length is 5 enough paramters were supplied
    if(len(sys.argv) >= 5):
        # User wants an nfa
        if(str(sys.argv[1]) == "-n"):
            nfaFile = str(sys.argv[2])
            # Check if they also want a dfa
            if(str(sys.argv[3]) == "-d"):
                dfaFile = str(sys.argv[4])
                regexFile = str(sys.argv[5])
                inputFile = str(sys.argv[6])
            else:
                regexFile = str(sys.argv[3])
                inputFile = str(sys.argv[4])
        # Just want a dfa
        elif(str(sys.argv[1]) == "-d"):
            dfaFile = str(sys.argv[2])
            # Check if they also want an nfa
            if(str(sys.argv[3]) == "-n"):
                nfaFile = str(sys.argv[4])
                regexFile = str(sys.argv[5])
                inputFile = str(sys.argv[6])
            else:
                regexFile = str(sys.argv[3])
                inputFile = str(sys.argv[4])


        for i in sys.argv:
            if(i == "-draw"):
                draw = True


def createAutomatas():
    global regexFile
    global inputFile
    global nfaFile
    global dfaFile
    global draw

    # Check if file exists
    if(os.path.isfile(inputFile) and os.path.isfile(regexFile)):
        print("Found input and regex files.")
        if(os.stat(inputFile).st_size == 0 and os.stat(regexFile).st_size == 0):
            print("Files are empty. Try again.")

        else:
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

            # Draw the graphs if the user wants
            if(draw):
                if(nfaFile != None):
                    drawGraph(nfa, nfaFile)
                if(dfaFile != None):
                    drawGraph(dfa, dfaFile)

            # Create the dot files
            if(nfaFile != None):
                nfa.createDotFile(nfaFile)
            if(dfaFile != None):
                dfa.createDotFile(dfaFile)

            # dfa.display()

            # For each input see if it matches
            for i in input:
                i = i.rstrip()
                dfa.match(i)

            print "Done."

    else:
        print("File not found. Try again")

if __name__ == "__main__":
    main()
