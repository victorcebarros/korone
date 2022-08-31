"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


import logging
import sqlite3
from sqlite3 import Connection, Cursor

from korone import constants

log = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Database related exceptions."""


class Database:
    """Database manager."""

    path: str
    conn: Connection

    @classmethod
    def isopen(cls):
        """Checks if database is open."""
        return hasattr(cls, "conn") and isinstance(cls.conn, Connection)

    @classmethod
    def connect(cls, path: str = "") -> None:
        """Connects to database."""
        if cls.isopen():
            raise DatabaseError("Database is already connected!")

        if path.strip() == "":
            path = constants.DEFAULT_DBFILE_PATH

        cls.path = path

        log.info("Connecting to database %s", cls.path)
        cls.conn = sqlite3.connect(cls.path)
        log.info("Successfully connected to database")

    @classmethod
    def setup(cls) -> None:
        """Sets up tables for database."""
        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.info("Setting up database")

        with cls.conn:
            cls.conn.executescript(constants.DATABASE_SETUP)

        log.info("Committing initial setup changes to database")

        # Creates a "Dictionary Cursor"
        # Refer to https://stackoverflow.com/questions/44009452
        # /what-is-the-purpose-of-the-row-factory-method-of-an
        # -sqlite3-connection-object
        cls.conn.row_factory = sqlite3.Row

    @classmethod
    def execute(cls, sql: str, parameters: tuple = (), /) -> Cursor:
        """Executes SQL Statement."""
        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.debug("Executing '%s' with '%s' arguments", sql, parameters)
        with cls.conn:
            return cls.conn.execute(sql, parameters)

    @classmethod
    def close(cls):
        """Closes database connection."""
        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.info("Closing database")
        cls.conn.close()
