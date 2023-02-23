"""
Represents connections to databases.
"""

from typing import Protocol

from korone.database.table import Table


class Connection(Protocol):
    """Database connection.

    Connection Classes should receive the DBMS-specific
    parameters directly through the __init__ method.

    For example:

        .. code-block:: python

            >>> class SQLite3Connection:
            ...     # SQLite3-specific parameters are
            ...     # passed through __init__
            ...     def __init__(self, path: str):
            ...         self.path = path
            ...     # Context Manager
            ...     def __enter__(self):
            ...         ...
            ...         self.connect()
            ...     def __exit__(self):
            ...         ...
            ...         self.close()
            ...     def connect(self):
            ...         ...
            ...     def table(self, name: str) -> Table:
            ...         ...
            ...     def close(self):
            ...         ...
    """

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_value, traceback): ...

    def connect(self):
        """Opens a connection to a database."""

    def execute(self, sql: str, parameters: tuple = (), /):
        """Execute SQL operations."""

    def table(self, name: str) -> Table:
        """Returns a Table, which can be used for
        database related operations.

        Args:
            name (str): SQL Table name to operate on.

        Returns:
            Table: Table object.
        """

    def close(self):
        """Closes the connection."""
