#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Simply append the given arguments to the file in $1."""

import sys

def append(file, arr):
    """Append the contents of arr to file."""
    str = " ".join(arr)
    with open(file, mode="a+") as theFile:
        theFile.write(str + "\n")

def main():
    """Start execution of append."""
    append(sys.argv[1], sys.argv[2:])

if __name__ == "__main__":
    main()
