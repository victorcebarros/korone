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
DEFAULT_DBFILE_PATH: str = f"{XDG_DATA_HOME}/korone/korone.db"

DEFAULT_WORKERS: int = 24
DEFAULT_NAME: str = "korone"

DATABASE_SETUP: str = """\
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    language VARCHAR(2) NOT NULL DEFAULT "en",
    registration_time INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY,
    language VARCHAR(2) NOT NULL DEFAULT "en",
    registration_time INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS disabled (
    chat_id INTEGER,
    disabled_cmd TEXT
);

CREATE TABLE IF NOT EXISTS filters (
    chat_id INTEGER,
    handler TEXT,
    data TEXT,
    file_id TEXT,
    filter_type TEXT
);

VACUUM;

PRAGMA journal_mode="WAL";
"""

MODULES_PACKAGE_NAME: str = "korone.commands"
