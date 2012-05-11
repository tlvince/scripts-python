#!/usr/bin/env python3
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

"""Create a Kindle periodical from given URLs."""

import os
import yaml
import shutil
import datetime
import argparse
import tempfile
import subprocess
import configparser

from sys import exit

app = "periodical"

def write_html(config, path, urls):
    """Generate stripped HTML file for the given URL."""
    i = 0
    section = os.path.join(path, "sections", str(i))
    os.makedirs(section)
    for url in urls:
        cmd = config["environment"]["extractor_cmd"].split()
        cmd.append(url)
        html = os.path.join(section, "{0}.html".format(i))
        with open(os.path.join(section, "_section.txt"), "w") as f:
            f.write(config["meta"]["subject"])
        with open(html, "w") as f:
            subprocess.call(cmd, stdout=f)
        if os.path.getsize(html) == 0:
            os.remove(html)
        else:
            i = i + 1

def write_yaml(meta, mobi, path, date):
    """Write document YAML."""
    doc = {
        "doc_uuid":     "{0}-{1}".format(app, date.strftime("%Y%m%d%H%M%S")),
        "title":        "{0} {1}".format(meta["title"],
                                         date.strftime("%Y-%m-%d")),
        "author":       meta["author"],
        "publisher":    meta["author"],
        "subject":      meta["subject"],
        "date":         date.strftime("%Y-%m-%d"),
        "mobi_outfile": mobi,
    }

    with open(os.path.join(path, "_document.yml"), "w") as f:
        yaml.dump(doc, f)

def write_config(path):
    """Write the default configuration file."""
    if not os.path.exists(path):
        config = configparser.ConfigParser()

        config["environment"] = {
            "extractor_cmd": "java -jar extractor.jar",
            "kindle_ssh":    "kindle",
        }

        config["option"] = {
            "logging":      "true",
        }

        config["meta"] = {
            "title":        "Think",
            "author":       "Tom Vincent",
            "subject":      "Articles",
        }

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
    with open(path, "w") as logfile:
        for url in urls:
            logfile.write("{0} {1}\n".format(date.strftime("%Y%m%d"), url))

def parse_args(config, log, url):
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help="the article URL", nargs="*")
    parser.add_argument("-c", "--config", default=config,
        help="path to config file")
    parser.add_argument("-l", "--log", default=log,
        help="path to log file")
    parser.add_argument("-f", "--file", default=url, nargs="?",
        help="path to a file containing URLs")
    return parser.parse_args()

def main():
    """Start execution of periodical."""
    config_path = os.getenv("XDG_CONFIG_HOME")
    if not config_path:
        config_path = os.path.join(os.getenv("HOME"), ".config")
    config_path = os.path.join(config_path, app, app + ".conf")

    data_path = os.getenv("XDG_DATA_HOME")
    if not data_path:
        data_path = os.path.join(os.getenv("HOME"), ".local", "share")
    log_path = os.path.join(data_path, app, app + ".log")
    url_path = os.path.join(data_path, app, app + "-urls.txt")
    
    args = parse_args(config_path, log_path, url_path)
    if not args.url:
        if not args.file: args.file = url_path
        if os.path.exists(args.file) and os.path.getsize(args.file) > 0:
            with open(args.file) as f:
                args.url = f.read().splitlines()
        else:
            exit(1)

    write_config(args.config)
    config = configparser.ConfigParser()
    config.read(args.config)

    tmp = tempfile.mkdtemp()
    date = datetime.datetime.now()
    mobi = "{0}-{1}.mobi".format(app, date.strftime("%Y%m%d%H%M%S"))
    write_yaml(config["meta"], mobi, tmp, date)
    write_html(config, tmp, args.url)

    if os.path.exists(os.path.join(tmp, "sections", "0", "0.html")):
        subprocess.call(["kindlerb", tmp])
        kindle = config["environment"]["kindle_ssh"]
        subprocess.call(["scp", os.path.join(tmp, mobi),
            "{0}:/mnt/us/documents/".format(kindle)])
        subprocess.call(["ssh", kindle, 
            "dbus-send --system /default com.lab126.powerd.resuming int32:1"])
    shutil.rmtree(tmp)

    if config["option"]["logging"].title():
        log(args.log, args.url, date)
        os.remove(args.file)

if __name__ == "__main__":
    main()
