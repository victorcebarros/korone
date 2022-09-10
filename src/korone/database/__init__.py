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
    """Base class for database."""

    path: str
    "Path to the database file."

    conn: Connection
    "Connection to the database."

    @classmethod
    def isopen(cls) -> bool:
        """
        The isopen function is a class method that is used to mark class as having an open connection.
        It's purpose is to make sure that the connection isn't closed before the class' __del__ method
        is called, which would close the database connection.

        :return: :obj:`True` if the class has an attribute named conn and it is an instance of connection
        :rtype: bool
        """
        return hasattr(cls, "conn") and isinstance(cls.conn, Connection)

    @classmethod
    def connect(cls, path: str = "") -> None:
        """
        The connect function is used to connect to the database. It takes one argument,
        which is the path of the database file. If no path is given, it will default to
        the constant DEFAULT_DBFILE_PATH.

        :param path: Specify the path to the database file, defaults to ""
        :type path: str, optional
        :return: None
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
        The setup function is called when the database is first initialized.
        It creates all of the tables and indexes that are required for operation.

        :return: None
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
        The execute function is a class method of the Connection class. It is
        used to execute SQL statements on the database connection that was
        opened by the connect function.

        :param sql: Pass in the sql statement that you want to execute
        :type sql: str
        :param parameters: Pass a tuple of arguments to the sql statement, defaults to ()
        :type parameters: tuple, optional
        :param /: Indicate that the function has a variable number of parameters
        :return: The cursor object
        :rtype: Cursor
        """

        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.debug("Executing '%s' with '%s' arguments", sql, parameters)
        with cls.conn:
            return cls.conn.execute(sql, parameters)

    @classmethod
    def close(cls) -> None:
        """
        The close function closes the database connection.

        :return: None
        """
        if not cls.isopen():
            raise DatabaseError("Database is not yet connected!")

        log.info("Closing database")
        cls.conn.close()
