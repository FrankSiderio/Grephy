import os
import sys

file = str(sys.argv[1])

# Check if file exists
if(os.path.isfile(file)):
    print("Found file!")
    if(os.stat(file).st_size == 0):
        print("File is empty")
    file = open(file)
else:
    print("File not found. Try again")
