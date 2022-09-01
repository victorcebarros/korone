"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

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
        """Inserts item to Database."""

    @abstractmethod
    def cast(self, row: Row) -> T:
        """Casts row to T type."""

    def query(self, search: Cell, relation: Relation = Relation.EQ) -> Iterable[T]:
        """Queries item from database."""
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
        """Updates item on database."""
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
        """Deletes item from the database."""
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
        """Returns whether or not the instance is in a valid state."""
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
        """Inserts item to Database."""
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
        """Casts Row object to Chat object."""
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
        """Inserts User to Database."""

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
        user: User = User(
            id=row[self.columns[Column.UUID]],
            language_code=row[self.columns[Column.LANGUAGE]],
        )

        user.registrydate = row[self.columns[Column.REGISTRYDATE]]  # type: ignore

        return user
