#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Setup cmd with some sane defaults."""

import os
import subprocess
import getpass
import logging

from urllib.request import getproxies_registry
from urllib.parse import urlparse

def setProxies(user, password, host, port):
    """Set proxy variables for the currently running shell."""
    schemes = ["http", "https"]

    for scheme in schemes:
        # XXX: https_proxy still uses http scheme
        base = scheme
        if scheme == "https":
            base = scheme[:-1]
        os.putenv(scheme + '_proxy',
            "{0}://{1}:{2}@{3}:{4}".format(base, user, password, host, port)
        )

def getProxyHost():
    """Return the proxy host and port from Windows registry."""
    try:
        proxy = getproxies_registry()["http"]
        return urlparse(proxy).netloc.split(":")
    except KeyError:
        logging.error("Cannot retreive proxy settings from registry")

def main():
    """Start execution of cmd."""
    un = getpass.getuser()
    pw = getpass.getpass()

    try:
        host, port = getProxyHost()
    except Exception:
        host = input("Host: ")
        port = input("Port: ")

    setProxies(un, pw, host, port)

    # Start a child shell to inherit the new environment variables
    subprocess.call(["cmd.exe", "/k", "title", "cmd"])

if __name__ == "__main__":
    main()
