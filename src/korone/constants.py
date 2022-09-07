"""
All Korone's constants that are used throughout the codebase.

.. data:: LOGGER_FORMAT_OUTPUT
    The format to be used in the logger.

.. data:: DATABASE_SETUP
    The database setup to be used.

.. data:: MODULES_PACKAGE_NAME
    The package that contains all the commands modules.

.. data:: DEFAULT_NAME
    The default bot name to be used when no name is provided.

.. data:: DEFAULT_WORKERS
    The default number of workers to be used when no number is provided.

.. data:: DEFAULT_CONFIG_PATH
    The default path to the config file.

.. data:: DEFAULT_DBFILE_PATH
    The default path to the database file.

.. data:: XDG_CONFIG_HOME
    The XDG_CONFIG_HOME environment variable.
    Where user-specific configurations should be written (analogous to /etc).

.. data:: XDG_DATA_HOME
    The XDG_DATA_HOME environment variable.
    Where user-specific data files should be written (analogous to /usr/share).

.. note::
    For more information related to the XDG constants, see: `XDG Base Directory`_.

.. _XDG Base Directory: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import os

LOGGER_FORMAT_OUTPUT: str = (
    "%(name)s"
    ":%(filename)s"
    ":%(funcName)s"
    ":%(lineno)s"
    "|%(levelname)s"
    "|%(message)s"
    "|%(created)i"
)

XDG_CONFIG_HOME: str = os.environ.get("XDG_CONFIG_HOME", "~/.config")
XDG_DATA_HOME: str = os.environ.get("XDG_DATA_HOME", "~/.local/share")

DEFAULT_CONFIG_PATH: str = f"{XDG_CONFIG_HOME}/korone/korone.conf"
DEFAULT_DBFILE_PATH: str = f"{XDG_DATA_HOME}/korone/korone.db"

DEFAULT_WORKERS: int = 24
DEFAULT_NAME: str = "korone"

DATABASE_SETUP: str = """\
CREATE TABLE IF NOT EXISTS Users (
    uuid INTEGER PRIMARY KEY,
    language VARCHAR(2) NOT NULL DEFAULT "en",
    registrydate INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Chats (
    uuid INTEGER PRIMARY KEY,
    language VARCHAR(2) NOT NULL DEFAULT "en",
    registrydate INTEGER NOT NULL,
    chattype TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DisabledCommands (
    chat_uuid INTEGER,
    command TEXT,
    state BIT
);

CREATE TABLE IF NOT EXISTS Filters (
    chat_uuid INTEGER,
    handler TEXT,
    data TEXT,
    file_id TEXT,
    filter_type TEXT
);

VACUUM;

PRAGMA journal_mode="WAL";
"""

MODULES_PACKAGE_NAME: str = "korone.commands"
