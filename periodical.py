#!/usr/bin/env python3
# Copyright 2012 Tom Vincent <http://tlvince.com/contact/>

"""Create a Kindle periodical from given URLs."""

import os
import yaml
import shutil
import argparse
import tempfile
import subprocess
import configparser

app = "periodical"

def write_html(config, path, urls):
    """Generate stripped HTML file for the given URL."""
    i = 0
    section = os.path.join(path, "sections", str(i))
    os.makedirs(section)
    for url in urls:
        cmd = ["java", "-jar", config["environment"]["stripper_path"], url]
        html = os.path.join(section, "{0}.html".format(i))
        with open(os.path.join(section, "_section.txt"), "w") as f:
            f.write(config["author"]["subject"])
        with open(html, "w") as f:
            subprocess.call(cmd, stdout=f)
        if os.path.getsize(html) == 0:
            os.remove(html)
        else:
            i = i + 1

def write_yaml(author, mobi, path):
    """Write document YAML."""
    date = "1223"
    doc = {
        "doc_uuid":     app,
        "title":        "{0} {1}: {2}".format(app, author["subject"], date),
        "author":       author["name"],
        "subject":      author["subject"],
        "date":         date,
        "mobi_outfile": mobi,
    }
    
    with open(os.path.join(path, "_document.yml"), "w") as f:
        yaml.dump(doc, f)

def write_config(path):
    """Write the default configuration file."""
    if not os.path.exists(path):
        config = configparser.ConfigParser()

        config["environment"] = {
            "stripper_path": "stripper.jar",
            "kindle":        "kindle",
        }

        config["author"] = {
            "title":        "periodical.py",
            "name":         "Tom Vincent",
            "subject":      "News",
        }

        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(path, "w") as configfile:
            config.write(configfile)

def parse_args(config):
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0],
             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("url", help="the article URL", nargs="+")
    parser.add_argument("-c", "--config", default=config,
        help="path to config file")
    return parser.parse_args()

def main():
    """Start execution of periodical."""
    config_path = os.getenv("XDG_CONFIG_HOME")
    if not config_path:
        config_path = os.path.join(os.getenv("HOME"), ".config")
    config_path = os.path.join(config_path, app, app + ".conf")

    args = parse_args(config_path)
    write_config(args.config)
    config = configparser.ConfigParser()
    config.read(args.config)

    tmp = tempfile.mkdtemp()
    mobi = "{0}-{1}.mobi".format(app, "123")
    write_yaml(config["author"], mobi, tmp)
    write_html(config, tmp, args.url)
    if os.path.exists(os.path.join(tmp, "sections", "0")):
        subprocess.call(["kindlerb", tmp])
        kindle = config["environment"]["kindle"]
        subprocess.call(["scp", os.path.join(tmp, mobi),
            "{0}:/mnt/us/documents/".format(kindle)])
        refresh = "dbus-send --system /default com.lab126.powerd.resuming int32:1"
        subprocess.call(["ssh", kindle, refresh])
    shutil.rmtree(tmp)

if __name__ == "__main__":
    main()
