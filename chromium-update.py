#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Download and unpack the latest chromium dev build."""

import urllib.request
import os.path
import shutil
import zipfile
import logging
import sys

def getBuild(url):
    """Return the latest build number."""
    try:
        page = urllib.request.urlopen(url)
        build = page.read().decode()
        logging.info("Found build number: {0}".format(build))
        return build
    except urllib.error.HTTPError as e:
        logging.error(e)
        logging.info("A proxy has been detected but not configured.")
        logging.info("Try setting 'http_proxy' in the active terminal.")

def download(remote, local):
    """Download 'file' from 'url' to the given destination."""
    logging.debug("Downloading from: {0}".format(remote))
    logging.debug("Saving to: {0}".format(local))

    response = urllib.request.urlopen(remote)
    # See: http://docs.python.org/py3k/library/email.message.html
    logging.debug(
        "Connection headers:\n\n{0}".format(response.headers.as_string())
    )
    total = int(response.headers.get("Content-Length"))
    block = 1024
    with open(local, mode="ab") as f:
        while block <= total:
            downloadProgress(block, total)
            data = response.read(block)
            f.write(data)
            block += block
    return total

def verifyDownload(fileSize, local):
    """Make some attempts to check the file was downloaded correctly."""
    try:
        assert os.stat(local).st_size == total
    except AssertionError:
        logging.warning("Downloaded file size does not match expect.")
        logging.info("The file maybe corrupt or incomplete.")

def downloadProgress(blockSize, totalSize):
    """A progress bar for download a file."""
    percent = int((blockSize * 100) / totalSize)
    sys.stdout.write("\rDownloaded: {0}%".format(percent))
    sys.stdout.flush()

def isDownloaded(path):
    """Naively check if it's already downloaded."""
    try:
        if os.path.isfile(path):
            raise Exception
    except Exception:
        logging.warning("Using existing file:\n{0}".format(path))
        logging.info("Skipping download")
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
        logging.error("Cannot extract to {0}".format(target))
        logging.info(
            "Windows prevents running programs from being overwritten."
        )
        logging.info("Please close Chromium and try again.")

def getLogger():
    """Setup the console logger."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
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
    if not isDownloaded(savePath):
        build = getBuild(url + "LATEST")
        size = download(url + "/" + build + "/" + chrome, savePath)
        verifyDownload(size, savePath)
    extract(savePath, extractPath, chrome)

if __name__ == "__main__":
    main()
