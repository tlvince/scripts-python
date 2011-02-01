#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Download and unpack the latest chromium dev build."""

import urllib.request
import os.path
import shutil
import zipfile
import logging

def getBuild(url):
    """Return the latest build number."""
    try:
        page = urllib.request.urlopen(url)
        build = page.read().decode()
        logging.info("Found build number: ${0}".format(build))
        return build
    except urllib.error.HTTPError as e:
        logging.error(e)
        logging.info("A proxy has been detected but not configured.")
        logging.info("Try setting 'http_proxy' in the active terminal.")

def download(url, file, dest):
    """Download the given file from the given url to the given destination."""
    remote = urllib.request.urlopen(url + "/" + file)
    savePath = os.path.join(dest, file)
    with open(savePath, mode="wb") as f:
        f.write(remote.read())

def isDownloaded(path):
    """Naively check if it's already downloaded"""
    try:
        if os.path.isfile(path):
            raise Exception
    except Exception:
        print("Skipping download...")
        return True

def extract(source, target, prefix):
    prefix = prefix[:-4]
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        zip = zipfile.ZipFile(source)
        zip.extractall(os.path.dirname(target))     # leading chrome-win32
        # move it to the real target
        shutil.move(os.path.join(os.path.dirname(target), prefix), target)
    except WindowsError:
        print("Have you closed Chromium?")

def getLogger():
    """Setup the console logger."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(filename)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def main():
    """Start execution of chromium-update."""
    url = "http://build.chromium.org/f/chromium/snapshots/chromium-rel-xp/"
    chrome = "chrome-win32.zip"
    local = os.path.join(os.path.expanduser("~"), "My Documents", "dwn", "unsorted")
    savePath = os.path.join(local, chrome)
    extractPath = os.path.join(os.path.expandvars("%ProgramFiles%"), "Chromium")

    getLogger()

    build = getBuild(url + "LATEST")
    #if not isDownloaded(savePath):
        #build = getBuild(url + "LATEST")
        #download(url + "/" + build, chrome, local)
    #extract(savePath, extractPath, chrome)

if __name__ == "__main__":
    main()
