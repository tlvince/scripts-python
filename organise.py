#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Organise music files into a strict naming heirarchy."""

import os
import argparse

import stagger

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("dirs", nargs="+", help="the directories to process")
    return parser.parse_args()

def mp3Files(dirname):
    """Return the absolute path to mp3 files in the given directory."""
    mp3s = []
    for root, dirs, files in os.walk(dirname):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".mp3":
                mp3s.append(os.path.join(root, file))
    return mp3s

def tagPath(mp3s):
    """Return a path built from the tags of the given mp3 files."""
    tagPaths = []
    for mp3 in mp3s:
        tag = stagger.read_tag(mp3)
        tagPaths.append(os.path.join(tag.artist, tag.album,
            " ".join(["{0:02d}".format(tag.track), tag.title])
        ))
    return tagPaths

def main():
    """Start execution of organise."""
    args = parseArguments()
    for dir in args.dirs:
        mp3s = mp3Files(dir)
        tags = tagPath(mp3s)
        [print(f) for f in tags]

if __name__ == "__main__":
    main()
