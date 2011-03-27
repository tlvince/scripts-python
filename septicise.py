#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Convert a pathname to title case."""

import argparse
import string
import os.path

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", nargs="+", help="the path(s) to convert")
    return parser.parse_args()

def main():
    """Start execution of septicise."""
    args = parseArguments()
    paths = args.path
    paths = [p.replace("-", " ") for p in paths]        # Dash -> space
    paths = [string.capwords(p, " ") for p in paths]    # Title case words
    paths = [os.path.splitext(p)[0] for p in paths]     # Remove extension
    [print(p) for p in paths]

if __name__ == "__main__":
    main()
