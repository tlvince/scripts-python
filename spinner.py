#!/usr/bin/env python3
# Tom Vincent <http://www.tlvince.com/contact/>

"""An ASCII progress "spinner".

Spinners are text-based progress bars back in the days when MUD's were
popular.  This module explores different implementations of spinners and
related concepts.
"""

import sys
import time
import itertools
import random

def spinner(chars="/-\|", delay=0.2):
    """Loop over the given characters and print to stdout."""
    for ch in chars:
        typewriter(ch)
        time.sleep(delay)

def miniSpinner():
    """Spinner, minified."""
    [print(c, end="\r") for c in "/-\|"]

def typewriter(str):
    """Print to terminal without newlines."""
    sys.stdout.write(str)
    sys.stdout.flush()
    # Overwrite the current line (think of a type-writer's arm returning)
    sys.stdout.write("\r")

def py3Typewriter(str):
    """Typewriter, in Python 3 style."""
    print(str, end="\r")

def permutations(str, delay=0.2):
    """A permutation implementation."""
    for pos in range(len(str)):
        for off in reversed(range(len(str))):
            typewriter(str[off-pos]+ str[off-pos-1]+ str[off-pos-2])
            time.sleep(delay)

def libPermutations():
    """Permutations using itertools."""
    p = itertools.permutations("toasasasvc")
    for i in p:
        print("".join(i), end="\r")
        time.sleep(0.1)

def main():
    """Main entry point."""
    while True:
        spinner()

if __name__ == "__main__":
    main()
