"""
SQLite3 implementation of the Connection and Table.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import sqlite3
from typing import Any, Protocol

from korone.database.query import Query
from korone.database.table import Document, Documents, Table


class _Conn(Protocol):
    """Class with SQLite3-specific bits and pieces."""

    _path: str
    _args: tuple
    _kwargs: dict
    _conn: sqlite3.Connection | None = None

    def _is_open(self):
        """Checks whether Database is open."""

    def _execute(self, sql: str, parameters: tuple = (), /):
        """Executes SQL Command without checking whether
        self._conn is null or not."""


class SQLite3Table:
    """Represents the specifics of a SQLitie3 Table."""

    _conn: _Conn
    _table: str

    def __init__(self, *, conn: _Conn, table: str):
        if conn is None:
            raise RuntimeError("Connecton cannot be None")

        self._conn = conn
        self._table = table

    def insert(self, fields: Any | Document):
        """Insert a row on the table."""
        msg = "Insertion has not been implemented yet."
        raise NotImplementedError(msg)

        if not isinstance(fields, Document):
            msg = "Types other than Document have not yet been implemented."
            raise NotImplementedError(msg)

    def query(self, query: Query) -> Documents:
        """Query rows that match the criteria."""

        msg = "Querying has not been implemented yet."
        raise NotImplementedError(msg)

    def update(self, fields: Any | Document, query: Query):
        """Update fields on rows that match the criteria."""

        msg = "Updating has not been implemented yet."
        raise NotImplementedError(msg)

    def delete(self, query: Query):
        """Delete rows that match the criteria."""

        msg = "Deleting has not been implemented yet."
        raise NotImplementedError(msg)


class SQLite3Connection:
    """SQLite3 Database Connection."""

    _path: str
    _args: tuple
    _kwargs: dict
    _conn: sqlite3.Connection | None = None

    def __init__(self, *args, path: str = ":memory", **kwargs):
        self._path: str = path
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _is_open(self):
        return self._conn is not None

    def _execute(self, sql: str, parameters: tuple = (), /):
        # this method should only be called
        # internally, thereby we can afford to not check
        # its nullity
        conn: sqlite3.Connection = self._conn  # type: ignore

        # for readability, we shorten self._conn to conn
        with conn:
            return conn.execute(sql, parameters)

    def connect(self):
        """Connect to the SQLite3 Database."""
        if self._is_open():
            raise RuntimeError("Connection is already in place.")

        self._conn = sqlite3.connect(self._path, *self._args, **self._kwargs)

    def table(self, name: str) -> Table:
        """Return a Table which can be operated upon."""
        return SQLite3Table(conn=self, table=name)

    def execute(self, sql: str, parameters: tuple = (), /):
        """Execute SQL operations."""
        if not self._is_open():
            raise RuntimeError("Connection is not yet open.")

        self._execute(sql, parameters)

    def close(self):
        """Close the SQLite3 Connection."""
        if not self._is_open():
            raise RuntimeError("Connection is not yet open.")

        self._conn.close()
