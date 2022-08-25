"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from dataclasses import dataclass
from sqlite3 import Cursor
from sqlite3 import Row
from time import time
from typing import Iterable

from pyrogram.types import User

from korone.utils import log
from korone.database.manager import Manager


@dataclass
class UserRow:
    """User Row returned by query method."""
    user_id: int
    language_code: str
    registration_time: int


class UserManager(Manager):
    """Manages User related operations."""
    def insert(self, user: User):
        """Inserts user into the database."""
        log.debug("Inserting user to database.")

        if user is None:
            raise RuntimeError("user is None")

        if user.id is None:
            raise RuntimeError("user.id is None")

        self.database.execute(
            "INSERT INTO users (id, registration_time) VALUES (?, ?)",
            (user.id, int(time()))
        )

    def query(self, user_id: int) -> Iterable[UserRow]:
        """Queries database with provided user_id."""

        result: Cursor = self.database.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )

        def user(user_row: Row) -> UserRow:
            return UserRow(user_id=user_row['id'],
                           language_code=user_row['language'],
                           registration_time=user_row['registration_time'])

        return map(user, result.fetchall())

    def delete(self, user_id: int):
        """Removes chat from the database."""
        self.database.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
