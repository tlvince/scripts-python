#!/usr/bin/env python3
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

"""Extract SMS messages from a Gammu backup.

Consider rewriting using python-gammu:
https://github.com/gammu/gammu/blob/master/python/examples/read-sms-backup.py
"""

import configparser
import binascii
import argparse

def parse_args():
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("file", help="Gammu input file")
    parser.add_argument("-p", "--phone", nargs="+",
        help="Grep on given phone number(s)")
    parser.add_argument("-e", "--encoding", default="latin-1",
        help="Encoding format")
    return parser.parse_args()

def main():
    """Start execution of smsparse."""
    args = parse_args()
    if args.phone:
        phone = [x + '"' for x in args.phone]
    config = configparser.ConfigParser()
    config.read(args.file, encoding=args.encoding)

    for section in config:
        sms = config[section]
        try:
            msg = ""
            if any(sms["Number"].endswith(x) for x in phone):
                for i in range(0, 9):
                    try:
                        text = sms["Text0{0}".format(i)]
                        uhex = binascii.unhexlify(text.encode(args.encoding))
                        msg  = msg + uhex.decode(args.encoding).replace("\x00", "")
                    except:
                        pass
                if sms["State"] == "Sent":
                    print("> " + msg)
                else:
                    print("< " + msg, sms["DateTime"])
        except KeyError:
            pass

if __name__ == "__main__":
    main()

