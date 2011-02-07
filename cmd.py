#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Setup cmd with some sane defaults."""

import os
import ctypes
import subprocess

def promptPass(user):
    """Ask for the user's password."""
    return input("Password: ")

def getMyDocs():
    """Return the path to My Documents.
    http://stackoverflow.com/questions/3927259/how-do-you-get-the-exact-path-to-my-documents/3927493#3927493"""
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)
    dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    return buf.value

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

def main():
    """Start execution of cmd."""
    un = os.path.expandvars("%USERNAME%")
    pw = promptPass(un)
    setProxies(un, pw, "", "8080")
    subprocess.call(["cmd.exe"])

if __name__ == "__main__":
    main()
