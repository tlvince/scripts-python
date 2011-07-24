#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://tlvince.com/contact/>

"""Return high quality download links from the given list of TED videos.

Example usage:
    1. $ wget "https://raw.github.com/tlvince/topTED/master/data.txt"
    2. $ tedhd "data.txt" >> "videos.txt"
    3. $ aria2c -c -d "~/downloads" -i "videos.txt"
"""

import argparse
import urllib.request
import re
import time
import random
import sys

def parse_arguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("urls", help="newline separated list of TED urls")
    return parser.parse_args()

def main():
    """Start execution of tedhd."""
    args = parse_arguments()
    reg = re.compile('<a href="(.*?)">Watch high-res video \(MP4\)</a>')

    try:
        with open(args.urls) as f:
            urls = f.read().splitlines()
    except IOError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    for url in urls:
        try:
            sleep = random.randint(0, 5)
            time.sleep(sleep)
            con = urllib.request.urlopen(url)
            html = con.read().decode()
            video = reg.search(html).group(1)
            print("http://www.ted.com{0}".format(video))
        except AttributeError:
            print("No video URL found on page '{0}'".format(url),
                file=sys.stderr)
        except KeyboardInterrupt:
            sys.exit(1)

if __name__ == "__main__":
    main()
