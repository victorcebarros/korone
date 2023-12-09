"""
SQLite3 implementation of the Connection and Table.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import sqlite3
from pathlib import Path
from typing import Any, Protocol

from korone.constants import DATABASE_SETUP, DEFAULT_DBFILE_PATH
from korone.database.query import Query
from korone.database.table import Document, Documents, Table


class _Conn(Protocol):
    """Class with SQLite3-specific bits and pieces."""

    _path: Path
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
        if isinstance(fields, Document):
            values = tuple(fields.values())
        elif isinstance(fields, tuple | list):
            values = fields
        else:
            raise TypeError("Fields must be a Document, tuple, or list")

        placeholders = ", ".join(["?"] * len(values))

        sql = f"INSERT INTO {self._table} VALUES ({placeholders})"

        self._conn._execute(sql, tuple(values))

    def query(self, query: Query) -> Documents:
        """Query rows that match the criteria."""
        clause, data = query.compile()

        sql = f"SELECT * FROM {self._table} WHERE {clause}"

        rows = self._conn._execute(sql, data).fetchall()

        return [Document(row) for row in rows]

    def update(self, fields: Any | Document, query: Query):
        """Update fields on rows that match the criteria."""
        if isinstance(fields, Document):
            pairs = list(fields.items())
        elif isinstance(fields, tuple | list):
            pairs = fields
        else:
            raise TypeError("Fields must be a Document, tuple, or list")

        assignments = [f"{key} = ?" for key, value in pairs]

        assignments = ", ".join(assignments)

        values = [value for key, value in pairs]

        clause, data = query.compile()

        sql = f"UPDATE {self._table} SET {assignments} WHERE {clause}"

        self._conn._execute(sql, (*values, *data))

    def delete(self, query: Query):
        """Delete rows that match the criteria."""
        clause, data = query.compile()

        sql = f"DELETE FROM {self._table} WHERE {clause}"

        self._conn._execute(sql, data)


class SQLite3Connection:
    """SQLite3 Database Connection."""

    _path: Path
    _args: tuple
    _kwargs: dict
    _conn: sqlite3.Connection | None = None

    def __init__(self, *args, path: Path = DEFAULT_DBFILE_PATH, **kwargs):
        self._path: Path = path
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        self.connect()
        return self

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

    def _executescript(self, sql: str):
        # this method should only be called
        # internally, thereby we can afford to not check
        # its nullity
        conn: sqlite3.Connection = self._conn  # type: ignore

        # for readability, we shorten self._conn to conn
        with conn:
            return conn.executescript(sql)

    def connect(self):
        """Connect to the SQLite3 Database."""
        if self._is_open():
            raise RuntimeError("Connection is already in place.")

        self._conn = sqlite3.connect(
            self._path.expanduser().resolve(), *self._args, **self._kwargs
        )

    def setup(self):
        """Setup the SQLite3 Database."""
        if not self._is_open():
            raise RuntimeError("Connection is not yet open.")

        self._executescript(DATABASE_SETUP)

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
