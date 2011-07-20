#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://tlvince.com/contact/>

"""Sanitise given filenames."""

import shutil
import os.path
import argparse

from sanitise import sanitise

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", nargs="+", help="the file(s) to sanitise")
    return parser.parse_args()

def main():
    """Start execution of sanename."""
    args = parseArguments()

    for f in args.file:
        sane = sanitise(os.path.basename(f))
        shutil.move(f, os.path.join(os.path.dirname(f), sane))

if __name__ == "__main__":
    main()
