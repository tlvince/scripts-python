#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Sanitise the given string(s) into (a subset of) ASCII."""

import argparse
import string
import unicodedata
import re

def removeAccents(str):
    """Remove any form of UTF-8 accents.

    See: http://stackoverflow.com/questions/517923/
    """
    nkfd_form = unicodedata.normalize('NFKD', str)
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)])

def regex(str):
    """Perform detailed substitutions using regex."""

    # List of (pattern, replacement) tuples
    regex = [
        ("&", "and"),           # Replace ampersand with a safe string
        ("( |_)", "-"),         # See: http://webmasters.stackexchange.com/q/374
        ("(\.|-){2,}", "\\1"),  # Flatten a series of two or more dots or dashes
        ("^-", ""),             # Remove a leading dash
        ("(-$|\.$)", ""),       # Remove a trailing dash or dot
    ]

    for handler in regex:
        pattern, replacement = handler
        str = re.sub(pattern, replacement, str)

    return str

def sanitise(str):
    """Perform substitutions and return the string."""

    str = removeAccents(str)
    str = regex(str)

    # Permit only letters, digits, dash (seperator) and dot (file extension)
    valid = string.ascii_letters + string.digits + "-."
    str = "".join([chr for chr in str if chr in valid])

    return str.lower()

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("strings", nargs="+", help="the string(s) to sanitise")
    return parser.parse_args()

def main():
    """Start execution of sanitise."""
    args = parseArguments()
    [print(sanitise(s)) for s in args.strings]

if __name__ == "__main__":
    main()
