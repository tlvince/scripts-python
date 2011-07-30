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

def queue_path(videos, watched_videos):
    """Find an unwatched video."""
    unwatched = videos.difference(watched_videos)
    try:
        return random.choice(list(unwatched))
    except IndexError:
        raise Exception("No more videos to watch")

def queue_file(playlist, watched_videos):
    """Return an unwatched video from a playlist file."""
    for video in playlist:
        basename = os.path.basename(video)
        if basename not in watched_videos:
            unwatched = video
            break

    try:
        return unwatched
    except NameError:
        raise Exception("No more videos to watch")

def parse_arguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", nargs="?", default=".", help="path to videos")
    parser.add_argument("-p", "--player", nargs="?",
        default="mplayer -really-quiet -fs",
        help="the command to the play the video")
    parser.add_argument("-f", "--file", nargs="?",
        help="read video paths from a playlist file")
    return parser.parse_args()

def parse_watched(watched_arr):
    """Return a set of filenames from a read watched file."""
    return set([f.split("\t")[0] for f in watched_arr])

def read_file(path):
    """Return the contents of a file."""
    with open(path, encoding="utf-8") as file:
        return file.read().splitlines()

def log(video, watched_file):
    """Log a watched video if it was rated."""
    rating = input(os.path.basename(__file__) + ": rating: ")
    if (rating == "0" or rating == "1"):
        with open(watched_file, mode="a+") as file:
            file.write("{0}\t{1}\n".format(os.path.basename(video), rating))

def main():
    """Start execution of logvid."""
    args = parse_arguments()

    # Configure the stdout logger
    logging.basicConfig(format="%(filename)s: %(levelname)s: %(message)s",
        level=logging.DEBUG)

    try:
        watched_file = set_environment()
        if args.file:
            videos = read_file(os.path.expanduser(args.file))
        else:
            videos = set(os.listdir(args.path))
        watched_videos = read_file(watched_file)
        watched_videos = parse_watched(watched_videos)
        if args.file:
            video = queue_file(videos, watched_videos)
        else:
            video = queue_path(videos, watched_videos)
        logging.info("playing: " + video)
        subprocess.call(args.player.split() + [os.path.join(args.path, video)])
        log(video, watched_file)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()
