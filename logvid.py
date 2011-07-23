#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://tlvince.com/contact/>

"""Log played videos and their rating."""

import os
import random
import logging
import argparse
import subprocess

def set_environment():
    """Setup the environment."""
    data_home = os.path.expandvars("$XDG_DATA_HOME")
    if not data_home:
        data_home = os.path.join(os.path.expanduser("~"), ".local", "share")
    data_home = os.path.join(data_home, "logvid")
    if not os.path.isdir(data_home):
        os.mkdirs(data_home)

    watched = os.path.join(data_home, "watched.txt")

    return watched

def queue(videos, watched_videos):
    """Find an unwatched video."""
    unwatched = videos.difference(watched_videos)
    try:
        return random.choice(list(unwatched))
    except IndexError:
        raise Exception("No more videos to watch")

def parse_arguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", nargs="?", default=".", help="path to videos")
    parser.add_argument("-p", "--player", nargs="?",
        default="mplayer -really-quiet -fs",
        help="the command to the play the video")
    return parser.parse_args()

def read_watched(path):
    """Return a set of the contents of a watched file."""
    watched = set()
    with open(path, encoding="utf-8") as file:
        for f in file:
            watched.add(f.split("\t")[0])
    return watched

def log(video, watched_file):
    """Log a watched video if it was rated."""
    rating = input(os.path.basename(__file__) + ": rating: ")
    if (rating == "0" or rating == "1"):
        with open(watched_file, mode="a+") as file:
            file.write(video + "\t" + rating)

def main():
    """Start execution of logvid."""
    args = parse_arguments()

    # Configure the stdout logger
    logging.basicConfig(format="%(filename)s: %(levelname)s: %(message)s",
        level=logging.DEBUG)

    try:
        watched_file = set_environment()
        videos = set(os.listdir(args.path))
        watched_videos = read_watched(watched_file)
        video = queue(videos, watched_videos)
        logging.info("playing: " + video)
        subprocess.call(args.player.split() + [os.path.join(args.path, video)])
        log(video, watched_file)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()
