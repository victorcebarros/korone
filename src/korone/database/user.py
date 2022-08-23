"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from sqlite3 import Cursor
from sqlite3 import Row
from time import time
from typing import Iterable

from pyrogram.types import User

from korone.utils import log
from korone.database.manager import Manager


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

    def query(self, user_id: int) -> Iterable[Row]:
        """Queries database with provided user_id."""

        result: Cursor = self.database.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )

        return result.fetchall()

    def delete(self, user_id: int):
        """Removes chat from the database."""
        self.database.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
