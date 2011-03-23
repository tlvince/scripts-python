#!/usr/bin/env python2.7
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Return the credentials from an encrypted netrc file.

Depends:
    gnupg: http://code.google.com/p/python-gnupg/
"""

import netrc
import os.path
import subprocess
import argparse
import logging

import gnupg

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
logger = logging.getLogger(os.path.basename(__file__))

def decrypt(netrc):
    """Decrypt the given GPG encrypted netrc file."""
    gpg = gnupg.GPG(use_agent=True)
    with open(netrc, mode="rb") as f:
        decrypted = gpg.decrypt_file(f)
    if not bool(decrypted):
        # Bad exit status from gpg
        logger.error(decrypted.status)
    else:
        return str(decrypted)

class mynetrc(netrc.netrc):
    """Override netrc to parse the already opened file.

    The parent netrc constructor calls open. Since the file has
    already been read using decrypt(), pass the contents (as a string)
    directly.
    """
    def __init__(self, name, contents):
        self.hosts = {}
        self.macros = {}
        self._parse(name, contents)

def parseArguments():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("host", help="the machine hostname")
    parser.add_argument("-u", "--username", action="store_true",
        help="print the hosts username")
    parser.add_argument("-p", "--password", action="store_true",
        help="print the hosts password")
    return parser.parse_args()

def authQuery(host, username=False, password=False):
    """docstring for query"""
    netrc = os.path.expanduser("~/.netrc.gpg")
    decrypted = decrypt(netrc)

    parsed = mynetrc(netrc, decrypted)
    try:
        (user, account, passw) = parsed.authenticators(host)

        if username:
            return(user)
        elif password:
            return(passw)
        else:
            return("\n".join([user, passw]))
    except TypeError:
        print "Invalid hostname"

def main():
    """Start execution of authnetrc."""
    args = parseArguments()
    print authQuery(args.host, args.username, args.password)

if __name__ == "__main__":
    main()
