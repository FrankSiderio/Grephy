# Grephy

A utility tool to build Nfa/Dfas and test them against input.

To use you must have [Python](https://www.python.org/downloads/)

### How to use

`python Grephy.py -n nfaFile -d dfaFile tests/regex.txt tests/input.txt`

This will put the `.dot` files in the `/graphs` folder

To draw a png of the dfa/nfa add the `-draw` parameter

`python Grephy.py -n nfaFile -d dfaFile tests/regex.txt tests/input.txt -draw`

The `.png` files will be in the root directory
