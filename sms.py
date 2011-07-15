#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://tlvince.com/contact/>

"""Send an sms from the command line."""

import argparse
import subprocess

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("number", help="recipients phone number")
    parser.add_argument("message", help="the sms message")
    return parser.parse_args()

def main():
    """Start execution of sms.py."""
    args = parseArguments()
    length = len(args.message)

    subprocess.call(
        ["gammu", "--sendsms", "TEXT", args.number, "-autolen", str(length), 
         "-save", "-folder", "2", "-text", args.message])

if __name__ == "__main__":
    main()
