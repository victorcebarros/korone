"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from sqlite3 import Cursor
from sqlite3 import Connection

import sqlite3

from korone import constants
from korone.utils import log


class DatabaseError(Exception):
    """Database related exceptions."""


class Database:
    """Database manager."""
    def __init__(self, path: str = ""):
        if path.strip() == "":
            path = constants.DEFAULT_DBFILE_PATH

        self.path: str = path
        self.conn: Connection | None = None

    def open(self) -> None:
        """Connects to database."""
        if self.conn is not None:
            raise DatabaseError("Database is already connected!")

        log.info("Connecting to database %s", self.path)
        self.conn = sqlite3.connect(self.path)
        log.info("Successfully connected to database")

    def setup(self) -> None:
        """Sets up tables for database."""
        if self.conn is None:
            raise DatabaseError("Database is not yet connected!")

        log.info("Setting up database")

        with self.conn:
            self.conn.executescript(constants.DATABASE_SETUP)

        log.info("Committing initial setup changes to database")

        # Creates a "Dictionary Cursor"
        # Refer to https://stackoverflow.com/questions/44009452
        # /what-is-the-purpose-of-the-row-factory-method-of-an
        # -sqlite3-connection-object
        self.conn.row_factory = sqlite3.Row

    def execute(self, sql: str, parameters: tuple = (), /) -> Cursor:
        """Executes SQL Statement."""
        if self.conn is None:
            raise DatabaseError("Database is not yet connected!")

        log.debug("Executing '%s' with '%s' arguments", sql, parameters)
        with self.conn:
            return self.conn.execute(sql, parameters)

    def close(self):
        """Closes database connection."""
        if self.conn is None:
            raise DatabaseError("Database is not yet connected!")

        log.info("Closing database")
        self.conn.close()
