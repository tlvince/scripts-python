#!/usr/bin/python3
# Copyright 2010-2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Convert the lastexport.py text-file format to match that of mpdscribble.

See: http://www.tlvince.com/linux/local-music-scrobbling/
"""

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
