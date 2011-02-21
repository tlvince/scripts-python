#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Count the frequency of unique words in a file.

See: https://code.activestate.com/recipes/576699/#c4
"""

import re
import sys
import argparse

from collections import Counter

def words(f):
    """Return each word in a line."""
    wordre = re.compile(r'\w+')
    for line in f:
        for word in wordre.findall(line):
            yield word

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("files", nargs="+", help="the file(s) to process")
    parser.add_argument("-c", "--count", type=int, default=20,
        help="the amount of words to consider"
    )
    return parser.parse_args()

def main():
    """Start execution of word-frequency."""
    args = parseArguments()
    for file in args.files:
        with open(file) as f:
            c = Counter(words(f))
        if len(args.files) > 1: print(file + ":")
        [print(w) for w in c.most_common(args.count)]

if __name__ == "__main__":
    main()
