"""
This module contains all the Korone database managers.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from sqlite3 import Row
from typing import Any, Generic, Iterable, TypeVar

from pyrogram.types import Chat, User

from korone.database import Database

log = logging.getLogger(__name__)


class Column(Enum):
    """Selects column for tables in database."""

    UUID = auto()
    """Universally Unique Identifier column."""

    LANGUAGE = auto()
    """Chat language column."""

    REGISTRYDATE = auto()
    """Chat registration date column."""

    CHATTYPE = auto()
    """Chat type column."""

    COMMAND = auto()
    """Command column."""

    STATE = auto()
    """Command state column."""


class Operator(Enum):
    """Operator to be applied in a clause on a SQL Statement."""

    LT = "<"
    """Less than"""

    EQ = "="
    """Equal to."""

    GT = ">"
    """Greater than."""

    LE = "<="
    """Less than or equal to."""

    GE = ">="
    """Greater than or equal to."""

    def __str__(self) -> str:
        return str(self.value)


class BaseClause(ABC):
    """Base class for all Clauses."""

    def __and__(self, other):
        return AndClause(self, other)

    def __or__(self, other):
        return OrClause(self, other)

    def __invert__(self):
        return InvertClause(self)

    @abstractmethod
    def eval(self, columns: dict[Column, str]) -> tuple[str, tuple[Any, ...]]:
        """Evaluate the clause."""


@dataclass
class Clause(BaseClause):
    """Single SQL Clause."""

    column: Column
    """Column to be compared."""

    data: Any = None
    """Data to be compared."""

    operator: Operator = Operator.EQ
    """Operator to be applied in a clause on a SQL Statement."""

    def eval(self, columns: dict[Column, str]) -> tuple[str, tuple[Any, ...]]:
        """Evaluate the clause."""
        return f"{columns[self.column]} {self.operator} ?", (self.data,)


class AndClause(BaseClause):
    """AND Clause."""

    def __init__(self, base: Clause, other: Clause):
        self.base = base
        self.other = other

    def eval(self, columns: dict[Column, str]) -> tuple[str, tuple[Any, ...]]:
        """Evaluate the clause."""
        bclause, bdata = self.base.eval(columns)
        oclause, odata = self.other.eval(columns)
        return f"({bclause} AND {oclause})", (*bdata, *odata)


class OrClause(BaseClause):
    """OR Clause."""

    def __init__(self, base: Clause, other: Clause):
        self.base = base
        self.other = other

    def eval(self, columns: dict[Column, str]) -> tuple[str, tuple[Any, ...]]:
        """Evaluate the clause."""
        bclause, bdata = self.base.eval(columns)
        oclause, odata = self.other.eval(columns)
        return f"({bclause} OR {oclause})", (*bdata, *odata)


class InvertClause(BaseClause):
    """NOT Clause."""

    def __init__(self, base: Clause):
        self.base = base

    def eval(self, columns: dict[Column, str]) -> tuple[str, tuple[Any, ...]]:
        """Evaluate the clause."""
        bclause, bdata = self.base.eval(columns)
        return f"(NOT {bclause})", (*bdata,)


T = TypeVar("T")


class Manager(ABC, Generic[T]):
    """Base class for all database managers."""

    def __init__(self, database: Database):
        if database is None:
            log.critical("Database is not initialized!")
            raise RuntimeError("Database is not initialized!")

        self.database: Database = database
        self.table: str = ""
        self.columns: dict[Column, str] = {}

    @abstractmethod
    def insert(self, item: T) -> None:
        """The insert function inserts an item into the list.

        Args:
            item (T): Type of data and the item that is being inserted into
                the database.
        """

    @abstractmethod
    def cast(self, row: Row) -> T:
        """The cast function is used to convert a row into the desired type.

        Args:
            row (:class:`sqlite3.Row`): Indicate the row that is being casted.

        Returns:
            T: The row as dictionary.
        """

    def query(self, search: Clause | None = None) -> Iterable[T]:
        """The query function is a method of the Manager class. It takes a
        Clause as an argument. If search is None, it returns all rows
        in the table.

        Args:
            search (:class:`Clause` | :obj:`None`, *optional*): Search Clause.
                Defaults to None.

        Raises:
            RuntimeError: If the manager is used directly.

        Returns:
            :class:`~typing.Iterable`\\[T]: An iterable with all the objects
                that match the query.
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        if search is None:
            return map(self.cast, self.database.execute(f"SELECT * FROM {self.table}"))

        clause, data = search.eval(self.columns)

        return map(
            self.cast,
            self.database.execute(f"SELECT * FROM {self.table} WHERE {clause}", data),
        )

    def update(self, update: Clause, condition: Clause) -> None:
        """The update function is a method of the Manager class. It takes
        an update Clause, which tells which columns should be updated. It also
        takes a condition clause, which matches the rows it should update.

        Args:
            update (:class:`Clause`): Column to be updated.
            condition (:class:`Clause`): Condition to match the rows.

        Raises:
            RuntimeError: If the manager is used directly.
            AttributeError: If condition data is empty.
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        # FIXME: Appropriately check whether data is properly passed by the clause
        # if condition.data is None or condition.data == "":
        #     raise AttributeError("Condition data can't be empty!")

        uclause, udata = update.eval(self.columns)
        cclause, cdata = condition.eval(self.columns)

        self.database.execute(
            f"UPDATE {self.table} SET {uclause} WHERE {cclause}",
            (*udata, *cdata),
        )

    def delete(self, condition: Clause) -> None:
        """The delete function is used to delete rows from the database.

        Args:
            condition (:class:`Clause`): Condition to match the rows.

        Raises:
            RuntimeError: If the manager is used directly.
            AttributeError: If condition data is empty.
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        if condition is None or condition.data is None or condition.data == "":
            raise AttributeError("Condition data can't be empty!")

        clause, data = condition.eval(self.columns)

        self.database.execute(f"DELETE FROM {self.table} WHERE {clause}", data)

    def valid(self) -> bool:
        """The valid function returns :obj:`True` if the table and columns are
        not empty. Otherwise, it returns :obj:`False`.

        Returns:
            :obj:`bool`: Boolean indicating if the table and columns are
                not empty.
        """
        return not (self.table == "" or not self.columns)


class ChatManager(Manager[Chat]):
    """Chat Manager for database."""

    def __init__(self, database: Database):
        super().__init__(database)
        self.table: str = "Chats"
        self.columns: dict[Column, str] = {
            Column.UUID: "uuid",
            Column.LANGUAGE: "language",
            Column.REGISTRYDATE: "registrydate",
            Column.CHATTYPE: "chattype",
        }

    def insert(self, item: Chat) -> None:
        """The insert function inserts a new chat into the database.
        It accepts an item, which is expected to be of type Chat.
        If improperly initialized Chat Objects, then it will raise
        a :obj:`RuntimeError`.

        Args:
            item (:class:`~pyrogram.types.Chat`): Pass the chat object to the
                insert function.

        Raises:
            RuntimeError: If chat object is :obj:`None`.
        """
        if item.id is None:
            raise RuntimeError("chat must not be None!")

        columns = (
            f"{self.columns[Column.UUID]}, "
            f"{self.columns[Column.CHATTYPE]}, "
            f"{self.columns[Column.REGISTRYDATE]}"
        )

        self.database.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES (?, ?, ?)",
            (item.id, item.type.value, int(time.time())),
        )

    def cast(self, row: Row) -> Chat:
        """The cast function takes a row from the database and returns
        a Chat Chat. The cast function is used to convert rows from
        the database into objects of type Chat.

        Args:
            row (:class:`~sqlite3.Row`): Access the values in the row.

        Returns:
            :class:`~pyrogram.types.Chat`: A chat object with the values from
            the row.
        """
        chat: Chat = Chat(
            id=row[self.columns[Column.UUID]], type=row[self.columns[Column.CHATTYPE]]
        )

        chat.registrydate = row[self.columns[Column.REGISTRYDATE]]  # type: ignore
        chat.language = row[self.columns[Column.LANGUAGE]]  # type: ignore

        return chat


class UserManager(Manager[User]):
    """User Manager for database."""

    def __init__(self, database: Database):
        super().__init__(database)

        self.table: str = "Users"
        self.columns: dict[Column, str] = {
            Column.UUID: "uuid",
            Column.LANGUAGE: "language",
            Column.REGISTRYDATE: "registrydate",
        }

    def insert(self, item: User) -> None:
        """The insert function inserts a new user into the database.

        Args:
            item (:class:`~pyrogram.types.User`): the user to be inserted, it
                must be a properly initialized User object.

        Raises:
            RuntimeError: If item.id is :obj:`None`.
        """
        if item.id is None:
            raise RuntimeError("item.id must not be None!")

        columns: str = (
            f"{self.columns[Column.UUID]}, {self.columns[Column.REGISTRYDATE]}"
        )

        self.database.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES (?, ?)",
            (item.id, int(time.time())),
        )

    def cast(self, row: Row) -> User:
        """The cast function is a helper function that takes in a row and
        returns a User object. It is used by the Database class to convert
        rows into User objects.

        Args:
            row (:class:`~sqlite3.Row`): Access the values in the row.

        Returns:
            :class:`~pyrogram.types.User`: A Pyrogram user object.
        """
        user: User = User(
            id=row[self.columns[Column.UUID]],
            language_code=row[self.columns[Column.LANGUAGE]],
        )

        user.registrydate = row[self.columns[Column.REGISTRYDATE]]  # type: ignore

        return user


@dataclass
class Command:
    """Command structure."""

    command: str
    """The command."""

    chat_id: int
    """Chat ID."""

    state: bool
    """Command state."""


class CommandManager(Manager[Command]):
    """Command manager for database."""

    def __init__(self, database: Database):
        super().__init__(database)

        self.table: str = "DisabledCommands"
        self.columns: dict[Column, str] = {
            Column.UUID: "chat_uuid",
            Column.COMMAND: "command",
            Column.STATE: "state",
        }

    def insert(self, item: Command) -> None:
        """The insert function inserts a new item into the database.
        It accepts an item as its parameter, and returns None.
        The insert function raises RuntimeError if the chat_id of
        the given item is None.

        Args:
            item (:class:`Command`): Tell the database what kind of data is
                going to be inserted.

        Raises:
            RuntimeError: If item.chat_id is :obj:`None`.
        """
        if item.chat_id is None:
            raise RuntimeError("item.chat_id must not be None!")

        columns: str = (
            f"{self.columns[Column.UUID]}, "
            f"{self.columns[Column.COMMAND]}, "
            f"{self.columns[Column.STATE]}"
        )

        self.database.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES (?, ?, ?)",
            (item.chat_id, item.command, item.state),
        )

    def cast(self, row: Row) -> Command:
        """The cast function is a helper function that converts the row object
        into a Command object. This is necessary because the database returns
        rows as tuples, but we want to work with objects.

        Args:
            row (:class:`~sqlite3.Row`): Access the values in the row.

        Returns:
            :class:`Command`: A command object.
        """
        return Command(
            command=row[self.columns[Column.COMMAND]],
            chat_id=row[self.columns[Column.UUID]],
            state=bool(row[self.columns[Column.STATE]]),
        )

    def toggle(self, command: str, chat_id: int, state: bool) -> None:
        """The toggle function is used to toggle the state of a command.

        Args:
            command (:obj:`str`): The command to have its state changed.
            chat_id (:obj:`int`): Identifier of the chat that the command will
                be toggled.
            state (:obj:`bool`): Determine whether the command should be
                enabled or disabled.
        """
        query = Clause(Column.COMMAND, command) & Clause(Column.UUID, chat_id)
        result = list(self.query(query))

        if len(result) < 1:
            self.insert(Command(command=command, chat_id=chat_id, state=state))
            return

        self.update(Clause(Column.STATE, state), query)

    def enable(self, command: str, chat_id: int) -> None:
        """The enable function enables a command for a given chat.

        Args:
            command (:obj:`str`): The command to be enabled.
            chat_id (:obj:`int`): Identifier of the chat that the command will
                be enabled.
        """
        self.toggle(command, chat_id, True)

    def disable(self, command: str, chat_id: int) -> None:
        """The disable function disables a command a given chat.

        Args:
            command (:obj:`str`): The command to be disabled.
            chat_id (:obj:`int`): Identifier of the chat that the command will
                be disabled.
        """
        self.toggle(command, chat_id, False)

    def is_enabled(self, command: str, chat_id: int) -> bool:
        """The is_enabled function checks if a command is enabled for a chat.

        Args:
            command (:obj`str`): The command to be checked.
            chat_id (:obj:`int`): Identifier of the chat that the command will
                be checked.

        Returns:
            :obj:`bool`: :obj:`True` if the command is enabled
                otherwise :obj:`False`.
        """
        query = Clause(Column.COMMAND, command) & Clause(Column.UUID, chat_id)

        result = list(self.query(query))

        if len(result) < 1:
            return True

        return result[0].state
