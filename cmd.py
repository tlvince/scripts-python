#!/usr/bin/env python3
# cmd.py: Setup cmd with some sane defaults.
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

import os
import ctypes
import subprocess

def promptPass(user):
    return input("Password: ")

def getMyDocs():
    """http://stackoverflow.com/questions/3927259/how-do-you-get-the-exact-path-to-my-documents/3927493#3927493"""
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)
    dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    return buf.value

def main():
    un = os.path.expandvars("%USERNAME%")
    pw = promptPass(un)
    pxy = "http://" + un + ":" + pw + "@:8080"
    cmd = ['cmd.exe', '/k', 'set', 'http_proxy=', pxy, '/k', 'cd', getMyDocs()]
    subprocess.call(cmd)

if __name__ == '__main__':
    main()
