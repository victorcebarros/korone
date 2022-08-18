"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from configparser import ConfigParser
from os import path

import os
import sys

from korone import constants
from korone.utils import log


config: ConfigParser = ConfigParser()

config["pyrogram"] = {
    "API_ID": "",
    "API_HASH": "",
    "BOT_TOKEN": "",
    "USE_IPV6": "no",
    "WORKERS": "24",
}


def init(cfgpath: str = "") -> None:
    """Initializes configuration file."""

    if cfgpath == "":
        cfgpath = constants.DEFAULT_CONFIG_PATH

    dirname: str = path.dirname(cfgpath)

    log.info("Initializing configuration module")
    log.debug("Using path %s", path)

    if dirname != "" and not path.isdir(dirname):
        log.info("Could not find configuration directory")
        try:
            log.debug("Creating configuration directory")
            os.mkdir(dirname)
        except OSError as err:
            log.critical("Could not create directory: %s", err)
            sys.exit(1)

    if not path.isfile(cfgpath):
        log.info("Could not find configuration file")
        try:
            log.debug("Creating configuration file")
            with open(cfgpath, "w", encoding="utf-8") as configfile:
                config.write(configfile)
        except OSError as err:
            log.critical("Could not create configuration file: %s", err)

    config.read(cfgpath)


def get(section: str, option: str, fallback: str = "") -> str:
    """Gets an option value for a given section.

    Wraps around ConfigParser's get method."""
    return config.get(section, option, fallback=fallback)
