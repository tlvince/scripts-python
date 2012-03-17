#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

"""A quvi-aria2 wrapper.

Parses a given media URL using quvi and passes its raw URL to an aria2 daemon.
"""

import urllib2
import base64
import json
import argparse
import logging

import quvi

def parse_args():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("url", help="A quvi-supported URL to download")
    return parser.parse_args()

def download(url, name, ext, username="aria2", password="aria2",
             host="localhost", port=25001):
    """Download the given URL using aria2.

    url         - The raw media URL to download.
    name        - The filename to write to.
    ext         - The media's file extension.
    username    - aria2 daemon username.
    password    - aria2 daemon password.
    host        - aria2 daemon hostname.
    port        - arai2 daemon port.
    """
    opts = dict(out=name + "." + ext)
    jsonreq = json.dumps({"id":name, "method":"aria2.addUri", "params":[[url],
        opts]})
    try:
        request = urllib2.Request("http://{0}:{1}/jsonrpc".format(host, port),
                jsonreq)
        auth = base64.encodestring("{0}:{1}".format(username, password))
        request.add_header("Authorization", "Basic {0}".format(auth))
        result = urllib2.urlopen(request)
        json_response = result.read()
        response = json.loads(json_response)
        logging.debug(response)
    except IOError as e:
        if hasattr(e, "reason"):
            if e.reason[0] == 111:
                logging.error("aria2 daemon not running")
        else:
            logging.error(e)

def main():
    """Start execution of quia."""
    logging.basicConfig(format="%(filename)s: %(levelname)s: %(message)s",
            level=logging.INFO)
    args = parse_args()
    props = quvi.get_properties_best_quality(args.url)
    download(props["mediaurl"], props["pagetitle"], props["filesuffix"])

if __name__ == "__main__":
    main()
