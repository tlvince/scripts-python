#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Prints a one line synopsis of the given Python file(s)."""

import argparse
import os.path
import sys

def docSynopsis(file):
    """Return a docstring synposis from the given Python file."""
    if not os.path.isfile(file):
        raise Exception("'{0}' is not a file".format(file))

    name, ext = os.path.splitext(file)
    if ext != ".py":
        raise Exception("'{0}' is not a valid Python file".format(file))
    
    with open(file, encoding="utf-8") as f:
        # XXX: Relies on my coding style
        docstring = f.readlines()[3]
        formatted = docstring.strip('."\n').lower()
        return "{0}: {1}".format(file, formatted)

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("files", nargs="+",
        help="python file(s)")
    return parser.parse_args()

def main():
    """Start execution of whatis.py."""
    args = parseArguments()
    for file in args.files:
        try:
            print(docSynopsis(file))
        except Exception as e:
            print(e, file=sys.stderr)

if __name__ == "__main__":
    main()
