#!/usr/bin/env python2
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

"""Create a Kindle periodical from given URLs."""

import os
import shutil
import datetime
import argparse
import tempfile
import subprocess
import ConfigParser

import yaml

from sys import exit

from boilerpipe.extract import Extractor

APP = "periodical"

def write_html(config, path, urls):
    """Generate stripped HTML file for the given URL."""
    i = 0
    section = os.path.join(path, "sections", str(i))
    os.makedirs(section)
    for url in urls:
        html = os.path.join(section, "{0}.html".format(i))
        with open(os.path.join(section, "_section.txt"), "w") as f:
            f.write(config.get("meta", "subject"))
        extractor = Extractor(extractor="ArticleExtractor", url=url)
        with open(html, "w") as f:
            f.write(extractor.getHTML().encode("utf8"))
        if os.path.getsize(html) == 0:
            os.remove(html)
        else:
            i = i + 1

def write_yaml(config, mobi, path, date):
    """Write document YAML."""
    doc = {
        "doc_uuid":     "{0}-{1}".format(APP, date.strftime("%Y%m%d%H%M%S")),
        "title":        "{0} {1}".format(config.get("meta", "title"),
                                         date.strftime("%Y-%m-%d")),
        "author":       config.get("meta", "author"),
        "publisher":    config.get("meta", "author"),
        "subject":      config.get("meta", "subject"),
        "date":         date.strftime("%Y-%m-%d"),
        "mobi_outfile": mobi,
    }

    with open(os.path.join(path, "_document.yml"), "w") as f:
        yaml.dump(doc, f)

def write_config(config, path):
    """Write the default configuration file."""
    if not os.path.exists(path):

        config.add_section("environment")
        config.set("environment", "kindle_ssh", "kindle")

        config.add_section("option")
        config.set("option", "logging", "true")

        config.add_section("meta")
        config.set("meta", "title", "Think")
        config.set("meta", "author", "Tom Vincent")
        config.set("meta", "subject", "Articles")

        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, "w") as configfile:
            config.write(configfile)

def log(path, urls, date):
    """Write a log of URLs."""
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, "a") as logfile:
        for url in urls:
            logfile.write("{0} {1}\n".format(date.strftime("%Y%m%d"), url))

def parse_args(config_path, log_path, urls_path):
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help="the webpage URL", nargs="*")
    parser.add_argument("-c", "--config", default=config_path,
        help="path to config file")
    parser.add_argument("-l", "--log", default=log_path,
        help="path to log file")
    parser.add_argument("-f", "--file", default=urls_path, nargs="?",
        help="path to a file containing a newline seperated list of URLs")
    return parser.parse_args()

def main():
    """Start execution of periodical."""
    config_path = os.getenv("XDG_CONFIG_HOME")
    if not config_path:
        config_path = os.path.join(os.getenv("HOME"), ".config")
    config_path = os.path.join(config_path, APP, APP + ".conf")

    data_path = os.getenv("XDG_DATA_HOME")
    if not data_path:
        data_path = os.path.join(os.getenv("HOME"), ".local", "share")
    log_path = os.path.join(data_path, APP, APP + ".log")
    url_path = os.path.join(data_path, APP, APP + "-urls.txt")
    
    args = parse_args(config_path, log_path, url_path)
    if not args.url:
        if not args.file: args.file = url_path
        if os.path.exists(args.file) and os.path.getsize(args.file) > 0:
            with open(args.file) as f:
                args.url = f.read().splitlines()
        else:
            exit(1)

    config = ConfigParser.ConfigParser()
    write_config(config, args.config)
    config.read(args.config)

    tmp = tempfile.mkdtemp()
    date = datetime.datetime.now()
    mobi = "{0}-{1}.mobi".format(APP, date.strftime("%Y%m%d%H%M%S"))

    write_yaml(config, mobi, tmp, date)
    write_html(config, tmp, args.url)

    if os.path.exists(os.path.join(tmp, "sections", "0", "0.html")):
        subprocess.call(["kindlerb", tmp])
        kindle = config.get("environment", "kindle_ssh")
        subprocess.call(["scp", os.path.join(tmp, mobi),
            "{0}:/mnt/us/documents/".format(kindle)])
        subprocess.call(["ssh", kindle, 
            "dbus-send --system /default com.lab126.powerd.resuming int32:1"])
    #shutil.rmtree(tmp)

    if config.get("option", "logging").title():
        log(args.log, args.url, date)

if __name__ == "__main__":
    main()
