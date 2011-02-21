#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

from sanitise import sanitise

"""Test strings for sanitise."""

def testAll():
    cases = {
        "hello": "hello",
        "foo-bar#baz?qux@127/\\9]": "foo-barbazqux1279",
        "éèêàùçÇ": "eeeaucc",
        "CRaZyCASE": "crazycase",
        "Bill & Ted": "bill-and-ted",
        "file.mp3": "file.mp3",
    }

    for case in cases:
        assert sanitise(case) == cases[case]

def main():
    """Start execution of test-sanitise."""
    testAll()

if __name__ == "__main__":
    main()
