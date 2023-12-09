# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto
from sqlite3 import Row
from typing import Any, Generic, TypeVar

from korone.database.connection import Connection
from korone.database.query import Query
from korone.database.table import Document, Table


class Column(Enum):
    UUID = auto()
    LANGUAGE = auto()
    REGISTRYDATE = auto()
    CHATTYPE = auto()
    COMMAND = auto()
    STATE = auto()


T = TypeVar("T")


class Manager(Generic[T]):
    """Base class for all database managers."""

    def __init__(self, connection: Connection, table: str):
        self._connection: Connection = connection
        self._table: str = table
        self.table = self._connection.table(self._table)

    def insert(self, item: T) -> None:
        self.table.insert(item)

    def cast(self, row: Row) -> T: ...

    def query(self, query: Query | None = None) -> Iterable[T]:
        return map(self.cast, self.table.query(query))

    def update(self, fields: Any | Document, query: Query) -> None:
        self.table.update(fields, query)

    def delete(self, query: Query) -> None:
        self.table.delete(query)


@dataclass
class Command:
    command: str
    chat_id: int
    state: bool


class CommandManager(Manager[Command]):
    def __init__(self, connection: Connection):
        self._table: str = "DisabledCommands"
        self.table: Table = connection.table(self._table)

        super().__init__(connection, self._table)

        self.columns: dict[Column, str] = {
            Column.UUID: "chat_id",
            Column.COMMAND: "command",
            Column.STATE: "state",
        }

    def insert(self, item: Command) -> None:
        if item.chat_id is None:
            raise RuntimeError("item.chat_id must not be None!")

        self.table.insert(Document(item.__dict__))

    def cast(self, row: Row) -> Command:
        return Command(
            command=row[self.columns[Column.COMMAND]],
            chat_id=row[self.columns[Column.UUID]],
            state=bool(row[self.columns[Column.STATE]]),
        )

    def toggle(self, command: str, chat_id: int, state: bool) -> None:
        query = (Query().command == command) & (Query().chat_id == chat_id)

        result = list(self.query(query))

        if len(result) < 1:
            self.insert(Command(command=command, chat_id=chat_id, state=state))
            return

        self.update(Query().state == state, query)

    def enable(self, command: str, chat_id: int) -> None:
        self.toggle(command, chat_id, True)

    def disable(self, command: str, chat_id: int) -> None:
        self.toggle(command, chat_id, False)

    def is_enabled(self, command: str, chat_id: int) -> bool:
        query = (Query().command == command) & (Query().chat_id == chat_id)

        result = list(self.query(query))

        if len(result) < 1:
            return True

        return result[0].state
