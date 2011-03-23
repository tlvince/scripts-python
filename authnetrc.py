#!/usr/bin/env python2.7
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Return the credentials from an encrypted netrc file."""

import netrc
import os.path
import subprocess
import argparse

def decrypt(netrc):
    """Decrypt the given GPG encrypted netrc file."""
    cmd = ["gpg", "--no-tty", "--use-agent", "-q", "-d", netrc]
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        print "Could not decrypt netrc file"
        quit()
    else:
        return out

class mynetrc(netrc.netrc):
    """Override netrc."""
    def __init__(self, netrc, netrcIO):
        self.hosts = {}
        self.macros = {}
        self._parse(netrc, netrcIO)

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
