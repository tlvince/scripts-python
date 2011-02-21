#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Print a random line from files.

Use cases:
    * Selecting a TODO item to work on
"""

import random
import logging
import argparse

def randomLine(file):
    """Try to return a random line from the given file."""
    with open(file, encoding="utf-8") as f:
        lines = f.readlines()
        try:
            num = random.randint(0, len(lines)-1)
            line = lines[num]
            if not line:
                randomLine(file)
            return line
        except ValueError:
            logging.error("{0} is empty".format(file))

def buildArguments():
    """Return an argparse object with the known arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n")[0])

    parser.add_argument("files", nargs="+")
    return parser

def parseArguments(parser):
    """Parse the command-line arguments."""
    args = parser.parse_args()
    return args.files

def main():
    """Start execution of random-line."""
    files = parseArguments(buildArguments())
    [print(randomLine(f)) for f in files]

if __name__ == "__main__":
    main()
