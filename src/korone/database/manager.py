"""
Manages Korone's Database.
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
    LANGUAGE = auto()
    REGISTRYDATE = auto()
    CHATTYPE = auto()
    COMMAND = auto()
    STATE = auto()


class Relation(Enum):
    """Relations for WHERE clause on SQL Statement."""

    LT = "<"
    EQ = "="
    GT = ">"
    LE = "<="
    GE = ">="


@dataclass
class Cell:
    """Data for a single cell in a row."""

    column: Column
    data: Any


T = TypeVar("T")


class Manager(ABC, Generic[T]):
    """Manager class."""

    def __init__(self, database: Database):
        if database is None:
            log.critical("Database is not initialized!")
            raise RuntimeError("Database is not initialized!")

        self.database: Database = database
        self.table: str = ""
        self.columns: dict[Column, str] = {}

    @abstractmethod
    def insert(self, item: T) -> None:
        """
        The insert function inserts an item into the list.

        :param self: Refer to the current instance of the class
        :param item:T: Type of data and the item that is being inserted into the database.
        :return: The item that was inserted into the list
        """

    @abstractmethod
    def cast(self, row: Row) -> T:
        """
        The cast function is used to convert a row into the desired type.

        :param self: Access the attributes and methods of the class
        :param row:Row: Indicate the row that is being casted
        :return: The row as a dictionary
        """

    def query(self, search: Cell, relation: Relation = Relation.EQ) -> Iterable[T]:
        """
        The query function is a method of the Manager class. It takes in a search
        cell and an optional relation, and returns all rows from the database that
        match that search cell. The relation defaults to Relation.Equals if it is not
        specified.

        :param self: Access the class attributes
        :param search:Cell: Search for a specific value in the database
        :param relation:Relation=Relation.EQ: Specify the type of query
        :return: An iterable of all the objects that match the search
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        if search.data is None or search.data == "":
            return map(self.cast, self.database.execute(f"SELECT * FROM {self.table}"))

        column: str = self.columns[search.column]
        return map(
            self.cast,
            self.database.execute(
                f"SELECT * FROM {self.table} WHERE {column} {relation.value} ?",
                (search.data,),
            ),
        )

    def update(
        self, update: Cell, condition: Cell, relation: Relation = Relation.EQ
    ) -> None:
        """
        The update function is a method of the Manager class. It takes in a update
        cell and a condition cell and an optional relation, and updates all rows from
        the database with that.

        :param self: Refer to the object itself
        :param update:Cell: Update the column specified by the update:cell parameter with data from another cell
        :param condition:Cell: Specify the condition for which a row should be updated
        :param relation:Relation=Relation.EQ: Specify the type of comparison to be used
        :return: None
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        if condition.data is None or condition.data == "":
            raise AttributeError("Condition data can't be empty!")

        self.database.execute(
            f"UPDATE {self.table} SET {self.columns[update.column]} = ? "
            f"WHERE {self.columns[condition.column]} {relation.value} ?",
            (update.data, condition.data),
        )

    def delete(self, condition: Cell, relation: Relation = Relation.EQ) -> None:
        """
        The delete function is used to delete a row from the database.
        It takes in two parameters, self and condition.
        The parameter self is required for all functions that are part of the Manager class.
        The parameter condition is a Cell object which contains information about what data should be deleted from the table.

        :param self: Refer to the object itself
        :param condition:Cell: Specify the column and value to be used in the delete statement
        :param relation:Relation=Relation.EQ: Specify the type of comparison that should be performed
        :return: None
        """
        if not self.valid():
            raise RuntimeError("You should not use the Manager class directly!")

        if condition.data is None or condition.data == "":
            raise AttributeError("Condition data can't be empty!")

        self.database.execute(
            f"DELETE FROM {self.table} WHERE "
            f"{self.columns[condition.column]} {relation.value} ?",
            (condition.data,),
        )

    def valid(self) -> bool:
        """
        The valid function returns True if the table and columns are not empty.
        Otherwise, it returns False.

        :param self: Access the attributes and methods of the class
        :return: A boolean value
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
        """
        The insert function inserts a new chat into the database.
        It accepts an item, which is expected to be of type Chat.
        If improperly initialized Chat Objects, then it will raise
        a RuntimeError.

        :param self: Access the class attributes
        :param item:Chat: Pass the chat object to the insert function
        :return: None
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
        """
        The cast function takes a row from the database and returns a Chat object.
        The cast function is used to convert rows from the database into objects of type Chat.

        :param self: Access the class attributes
        :param row:Row: Access the values in the row
        :return: A chat object with the values from the row
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
        """
        The insert function inserts a new user into the database.
        It takes two arguments: item and self.
        item is the user to be inserted, it must be a properly initialized User object.
        self is the table object that contains this function.

        :param self: Access the attributes and methods of the class in python
        :param item:User: Tell the function what type of data it is expecting
        :return: None
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
        """
        The cast function is a helper function that takes in a row and returns
        a User object. It is used by the Database class to convert rows into
        User objects.

        :param self: Access the class attributes
        :param row:Row: Access the values in the row
        :return: A user object
        """
        user: User = User(
            id=row[self.columns[Column.UUID]],
            language_code=row[self.columns[Column.LANGUAGE]],
        )

        user.registrydate = row[self.columns[Column.REGISTRYDATE]]  # type: ignore

        return user


@dataclass
class Command:
    """Simple command structure."""

    command: str
    chat_id: int
    state: bool


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
        if item.chat_id is None:
            raise RuntimeError("item.chat_id must not be None!")

        columns: str = (
            f"{self.columns[Column.UUID]}, "
            f"{self.columns[Column.COMMAND]}, "
            f"{self.columns[Column.STATE]}"
        )

        self.database.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES (?, ?, ?)",
            (item.chat_id, item.command, item.state)
        )

    def cast(self, row: Row) -> Command:
        return Command(
            command=row[self.columns[Column.COMMAND]],
            chat_id=row[self.columns[Column.UUID]],
            state=bool(row[self.columns[Column.STATE]]),
        )
