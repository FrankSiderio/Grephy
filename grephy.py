import os
import sys

file = str(sys.argv[1])

# Check if file exists
if(os.path.isfile(file)):
    print("Found file!")
    file = open(file)
else:
    print("File not found. Try again")
