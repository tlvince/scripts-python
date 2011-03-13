#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Pad files with a leading zero."""

import os
import argparse
import logging

def ls(dirs):
    """Return the contents of the given directories."""
    paths = []
    for dir in dirs:
        assert os.path.isdir(dir) == True
        for root, dirs, files in os.walk(dir):
            for file in files:
                paths.append(os.path.join(root, file))
    return paths

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("dirs", nargs="+",
        help="the directory(s) containing files to pad")
    parser.add_argument("-n", "--dry-run", action="store_true",
        help="perform a trial run with no changes made")
    return parser.parse_args()

def pad(files, padding=2):
    """Add a leading zero to the contents of the given array of files."""
    matches = {}
    for f in files:
        dir = os.path.dirname(f)
        f = os.path.basename(f)
        start = f[:padding]
        try:
            # Leaded with >= 10
            int(start)
        except:
            start = start[0]
            try:
                int(start)
            except ValueError:
                logging.error(
                    "File '{file}' did not lead with a number".format(file=f)
                )
            else:
                matches[os.path.join(dir, f)] = os.path.join(
                    dir, "0{file}".format(file=f))
    return matches

def setLogger():
    """Setup the logging object."""
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)

def dryRun(matches):
    """Pretty-print what will happen."""
    dirs = set([os.path.dirname(d) for d in matches.keys()])
    for d in dirs:
        print("\n{0}".format(d), end="\n\n")
        for m in sorted(matches):
            if os.path.dirname(m) == d:
                print("{0} -> {1}".format(os.path.basename(m), 
                    os.path.basename(matches[m])))

def main():
    """Start execution of pad."""
    args = parseArguments()
    setLogger()
    files = ls(args.dirs)
    matches = pad(files)
    if args.dry_run:
        dryRun(matches)

if __name__ == "__main__":
    main()
