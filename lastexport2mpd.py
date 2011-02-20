#!/usr/bin/python3
# lastexport2mpd.py
# Copyright 2010 Tom Vincent <http://www.tlvince.com/contact/>

import os
import sys
import time

file = sys.path[0] + "/exported_tracks.txt"

with open(file) as tracks:
    with open(sys.path[0] + "/mpd-formatted-tracks.txt", mode='w', encoding='utf-8') as outFile:
        for line in tracks:
            timestamp, track, artist, album, trackmbid, artistmbid, albummbid = line.strip("\n").split("\t")
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(timestamp)))
            outFile.write(timestamp + " " + artist + " - " + track + "\n")
