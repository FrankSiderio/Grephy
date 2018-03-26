import os
import sys

input = raw_input('Enter grephy command: ')
input = str.split(input)

if(input[0] != "grephy"):
    print(input[0] + " is not a valid input")
    # Restarts the script
    os.execl(sys.executable, sys.executable, *sys.argv)

# Check if file exists
if(os.path.isfile(input[1])):
    print("Found file!")
    file = open(input[1])
else:
    print("File not found. Try again")
    os.execl(sys.executable, sys.executable, *sys.argv)
