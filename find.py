#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""A (rather limited) UNIX find replacement."""

import os
import argparse

def findFiles(path, fileType):
    """Recursively return files of given extension from the given path."""
    results = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1] == '.' + fileType:
                results.append(os.path.join(root, f))
    return results

def buildArguments():
    parser = argparse.ArgumentParser(
        description="Recursively find files of a given file type.")
    parser.add_argument('-d', '--dir',
        help="directory to search in (defaults to current directory)")
    parser.add_argument('-t', '--type', default="py",
        help="file type to look for (defaults to 'py')")
    parser.add_argument('-q', '--quiet', action='store_true',
        help="don't print results to stdout")
    return parser

def parseArguments(parser):
    args = parser.parse_args()
    if not args.dir:
        args.dir = os.getcwd()
    return args

def main():
    args = parseArguments(buildArguments())
    if not args.quiet:
        files = findFiles(args.dir, args.type)
        for f in files:
            print(f)

if __name__ == '__main__':
    main()
