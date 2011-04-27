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
        "file.MP3": "file.mp3",
        ".dotfile.txt": ".dotfile.txt",
        "---heLLO": "hello",
        "infix----dashes": "infix-dashes",
        "---hello....txt.": "hello.txt",
    }

    i = 1
    for case in cases:
        expected = cases[case]
        actual = sanitise(case)
        print("({0}) {1}: {2} -> {3}".format(i, case, expected, actual))
        assert expected == actual
        i += 1

def main():
    """Start execution of test-sanitise."""
    testAll()

if __name__ == "__main__":
    main()
