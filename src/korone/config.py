"""
Manages Korone's configuration.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import logging
import sys
from configparser import ConfigParser
from os import path
from pathlib import Path

from korone import constants

log = logging.getLogger(__name__)


config: ConfigParser = ConfigParser()

config["pyrogram"] = {
    "API_ID": "",
    "API_HASH": "",
    "BOT_TOKEN": "",
    "USE_IPV6": "no",
    "WORKERS": "24",
}


def init(cfgpath: Path) -> None:
    """The init function initializes the configuration module.
    It reads the default configuration file from DEFAULT_CONFIG_PATH, and
    creates the directory containing it if it does not exist. If the file does
    not exist, it is created with a basic structure. The function then reads
    its contents into a ConfigParser object for use by other functions.

    Args:
        cfgpath (:obj:`str`, *optional*): Specify a custom path to the config
            file. Defaults to "".
    """
    if not cfgpath:
        cfgpath = constants.DEFAULT_CONFIG_PATH

    dirname: Path = Path(cfgpath).parent

    log.info("Initializing configuration module")
    log.debug("Using path %s", path)

    if dirname != "" and not Path(dirname).is_dir():
        log.info("Could not find configuration directory")
        try:
            log.debug("Creating configuration directory")
            Path(dirname).mkdir()
        except OSError as err:
            log.critical("Could not create directory: %s", err)
            sys.exit(1)

    if not Path(cfgpath).is_file():
        log.info("Could not find configuration file")
        try:
            log.debug("Creating configuration file")
            with Path(cfgpath).open("w", encoding="utf-8") as configfile:
                config.write(configfile)
        except OSError as err:
            log.critical("Could not create configuration file: %s", err)

    config.read(cfgpath)


def get(section: str, option: str, fallback: str = "") -> str:
    """The get function is a helper function that retrieves the value of an
    option in a given section. If no such option exists, it returns the
    fallback instead.

    Args:
        section (:obj:`str`): Specify the section of the config file to read
            from.
        option (:obj:`str`): Specify which option in the section you want to
            get.
        fallback (:obj:`str`, *optional*): Set a default value if the option
            is not found in the config file. Defaults to "".

    Returns:
        :obj:`str`: The value of the option in the given section.
    """
    return config.get(section, option, fallback=fallback)
