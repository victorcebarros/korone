"""
The ``korone.database`` package is responsible for all database operations.
"""

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
    """Database wrapper."""

    path: str
    """Path to database file."""

    conn: Connection
    """Database connection."""

    @classmethod
    def isopen(cls) -> bool:
        """
        Verifies if the database is open.

        Returns:
            bool: :obj:`True` if database is ready to use,
                :obj:`False` otherwise.
        """
        return hasattr(cls, "conn") and isinstance(cls.conn, Connection)

    @classmethod
    def connect(cls, path: str = "") -> None:
        """
        Connects to the database file indicated by path. If no path is
        given, it defaults to constants.DEFAULT_DBFILE_PATH.

        Args:
            path (:obj:`str`, *optional*): Specify the path to the database
                file. Defaults to :obj:`korone.constants.DEFAULT_DBFILE_PATH`.

        Raises:
            DatabaseError: If the database is already connected.
        """

        if cls.isopen():
            raise DatabaseError("Database is already connected!")

        if not path.strip():
            path = constants.DEFAULT_DBFILE_PATH

        cls.path = path

        log.info("Connecting to database %s", cls.path)
        cls.conn = sqlite3.connect(cls.path)
        log.info("Successfully connected to database")

    @classmethod
    def setup(cls) -> None:
        """
        Sets up database tables needed for other database-related operations,
        essentially initializng it.

        Raises:
            DatabaseError: If the database is not connected.
        """
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
        """
        Executes SQL statements on the open database connection.

        The parameters are similar, if not equal, to those in the
        :class:`~sqlite3.Connection` class.

        Args:
            sql (:obj:`str`): SQL Statement to execute
            parameters (:obj:`tuple`, *optional*): Replaces qmark
                style placeholders in SQL Statement. Defaults to ().

        Raises:
            DatabaseError: If the database is not connected.

        Returns:
            :class:`~sqlite3.Cursor`: The cursor object.
        """

        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.debug("Executing '%s' with '%s' arguments", sql, parameters)
        with cls.conn:
            return cls.conn.execute(sql, parameters)

    @classmethod
    def close(cls) -> None:
        """
        Closes the database connection.

        Raises:
            DatabaseError: If the database is not connected.
        """
        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.info("Closing database")
        cls.conn.close()
