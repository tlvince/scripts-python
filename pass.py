#!/usr/bin/env python2.7
# Copyright 2013 Tom Vincent <http://tlvince.com/contact>

"""Thin Python wrapper for PASS(1)."""

import subprocess

def password(name):
    command = "pass show {0}".format(name)
    return subprocess.check_output(command, shell=True).rstrip()
