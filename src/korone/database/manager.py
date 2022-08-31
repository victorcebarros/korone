"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from enum import auto
from sqlite3 import Row
from typing import Any
from typing import Generic
from typing import Iterable
from typing import TypeVar

import logging
import time

from pyrogram.types import Chat

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

    @abstractmethod
    def insert(self, item: T) -> None:
        """Inserts item to Database."""

    @abstractmethod
    def query(self, search: Cell, relation: Relation = Relation.EQ) -> Iterable[T]:
        """Queries item from database."""

    @abstractmethod
    def update(self, update: Cell, condition: Cell,
               relation: Relation = Relation.EQ) -> None:
        """Updates item on database."""

    @abstractmethod
    def delete(self, condition: Cell,
               relation: Relation = Relation.EQ) -> None:
        """Deletes item from the database."""

    @abstractmethod
    def cast(self, row: Row) -> T:
        """Casts row to T type."""


class ChatManager(Manager[Chat]):
    """Chat Manager for database."""
    def __init__(self, database: Database):
        super().__init__(database)
        self.table: str = "Chats"
        self.columns: dict[Column, str] = {
            Column.UUID: "uuid",
            Column.LANGUAGE: "language",
            Column.REGISTRYDATE: "registrydate",
            Column.CHATTYPE: "chattype"
        }

    def insert(self, item: Chat) -> None:
        """Inserts item to Database."""
        if item.id is None:
            raise RuntimeError("chat must not be None!")

        columns = f"{self.columns[Column.UUID]}, "       \
                  f"{self.columns[Column.CHATTYPE]}, "   \
                  f"{self.columns[Column.REGISTRYDATE]}"

        self.database.execute(
            f"INSERT INTO {self.table} ({columns}) VALUES (?, ?, ?)",
            (item.id, item.type.value, int(time.time()))
        )

    def query(self, search: Cell, relation: Relation = Relation.EQ) -> Iterable[Chat]:
        """Queries item from database."""

        if search.data is None or search.data == "":
            return map(self.cast,
                       self.database.execute(f"SELECT * FROM {self.table}"))

        column: str = self.columns[search.column]
        return map(self.cast,
                   self.database.execute(
                       f"SELECT * FROM {self.table} WHERE {column} {relation.value} ?",
                       (search.data,)))

    def update(self, update: Cell, condition: Cell,
               relation: Relation = Relation.EQ) -> None:
        """Updates item on database."""
        if condition.data is None or condition.data == "":
            raise AttributeError("Condition data can't be empty!")

        self.database.execute(
            f"UPDATE {self.table} SET {self.columns[update.column]} = ?"
            f"WHERE {self.columns[condition.column]} {relation.value} ?",
            (update.data, condition.data)
        )

    def delete(self, condition: Cell, relation: Relation = Relation.EQ) -> None:
        """Deletes item from the database."""
        if condition.data is None or condition.data == "":
            raise AttributeError("Condition data can't be empty!")

        self.database.execute(
                f"DELETE FROM {self.table} WHERE "
                f"{self.columns[condition.column]} {relation.value} ?",
                (condition.data,)
        )

    def cast(self, row: Row) -> Chat:
        """Casts Row object to Chat object."""
        chat: Chat = Chat(
            id=row[self.columns[Column.UUID]],
            type=row[self.columns[Column.CHATTYPE]]
        )

        chat.registrydate = row[self.columns[Column.REGISTRYDATE]]  # type: ignore
        chat.language = row[self.columns[Column.LANGUAGE]]  # type: ignore

        return chat
