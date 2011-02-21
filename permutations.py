#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Print the permutations of the given string(s)."""

import argparse

TEST_WORDS = {
    "altruism",
    "orthodoxy",
    "extol",
    "pervade"
}

def rotate(word, i):
    print(word)
    word = word[1:] + word[0]
    i = i - 1
    if i != 0:
        rotate(word, i)

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("strings", nargs="*", help="the string(s) to permeate")
    parser.add_argument("-t", "--test", action="store_true", help="print some internal test strings")
    return parser.parse_args()

def main():
    """Start execution of permutations."""
    args = parseArguments()
    words = []
    if args.strings: words = args.strings
    if args.test: words = TEST_WORDS
    [rotate(word, len(word)) for word in words]

if __name__ == "__main__":
    main()
