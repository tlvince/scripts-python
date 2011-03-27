#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Convert a filename to title case."""

import argparse
import string
import os.path

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", nargs="+", help="the file(s) to convert")
    return parser.parse_args()

def main():
    """Start execution of septicise."""
    args = parseArguments()
    files = args.file
    files = [os.file.basename(f) for f in files]        # Get files
    files = [f.replace("-", " ") for f in files]        # Dash -> space
    files = [string.capwords(f, " ") for f in files]    # Title case words
    files = [os.file.splitext(f)[0] for f in files]     # Remove extension
    [print(f) for f in files]

if __name__ == "__main__":
    main()
