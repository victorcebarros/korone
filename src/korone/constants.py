"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


import os


LOGGER_FORMAT_OUTPUT: str = "%(filename)s"  \
                           ":%(funcName)s"  \
                           ":%(lineno)s"    \
                           "|%(levelname)s" \
                           "|%(message)s"   \
                           "|%(created)i"

XDG_CONFIG_HOME: str = os.environ.get("XDG_CONFIG_HOME", "~/.config")
XDG_DATA_HOME: str = os.environ.get("XDG_DATA_HOME", "~/.local/share")

DEFAULT_CONFIG_PATH: str = f"{XDG_CONFIG_HOME}/korone/korone.conf"
