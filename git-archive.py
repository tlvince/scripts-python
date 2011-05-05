#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Automated git archive creation."""

import argparse
import logging
import os
import subprocess

from sanitise import sanitise

def createArchive(path, tag, type="zip", treeish="HEAD"):
    """Create an archive from the repository in the given path."""

    # Sanitised basename of the repository root
    name = sanitise(os.path.basename(path))

    # Create a build directory in the repository (if it doesn't already exist)
    build = os.path.join(path, "build")
    if not os.path.exists(build):
        os.mkdir(build)

    cmd = ["git", "archive", "--format", "{0}".format(type), "-9",
        "--prefix", "{0}/".format(name), 
        "--output", "{0}-{1}.{2}".format(os.path.join(build, name), tag, type),
        treeish]

    try:
        subprocess.check_call(cmd)
    except CalledProcessError as e:
        logging.error(e)

def describe(path):
    """Return the output from git describe on the given path."""

    # Git path
    git = os.path.join(path, ".git")

    # Append any existing tag to the archive file name or use the commit
    gitDescribe = ["git", "--git-dir={0}".format(git),
        "--work-tree={0}".format(path), "describe", "--tags", "--always"]

    try:
        tag = subprocess.check_output(gitDescribe)
    except CalledProcessError as e:
        logging.error(e)

    # Just get the tag as a string
    return tag.decode().split("\n")[0]

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("repos", nargs="+",
        help="repository path(s) to create archives")
    return parser.parse_args()

def hasRepo(path):
    """Confirm the given path contains a repository."""
    git = os.path.join(path, ".git")
    if not os.path.exists(git):
        raise GitArchiveException(
            "No git repository found in '{0}'".format(path))

class GitArchiveException(Exception):
    """Custom exception raised by internal functions."""
    def __init__(self, string):
        """Initialise the exception with an error string."""
        self.msg = string
    def __str__(self):
        return self.msg

def main():
    """Start execution of git-archive."""
    args = parseArguments()

    # Configure the stdout logger
    logging.basicConfig(format="%(filename)s: %(levelname)s: %(message)s",
        level=logging.DEBUG)

    for repo in args.repos:
        try:
            hasRepo(repo)
            tag = describe(repo)
            createArchive(repo, tag)
        except GitArchiveException as e:
            logging.error(e)
            logging.info("Please specify a path containing a git repository")

if __name__ == "__main__":
    main()
