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

from pyrogram.types import Chat

from korone.utils import log
from korone.database.manager import Manager

class ChatManager(Manager):
    """Manages Chat related operations."""
    def insert(self, chat: Chat):
        """Inserts chat into the database."""
        log.debug("Inserting chat to database.")

        if chat is None:
            raise RuntimeError("chat is None")

        if chat.id is None:
            raise RuntimeError("chat.id is None")

        self.database.execute(
            "INSERT INTO chats (id, registration_time) VALUES (?, ?)",
            (chat.id, int(time()))
        )

    # TODO: Return Iterable[Chat] instead
    def query(self, chat_id: int) -> Iterable[Row]:
        """Queries database with provided chat_id."""

        result: Cursor = self.database.execute(
            "SELECT * FROM chats WHERE id = ?",
            (chat_id,)
        )

        return result.fetchall()

    def delete(self, chat_id: int):
        """Removes chat from the database."""
        self.database.execute(
            "DELETE FROM chats WHERE id = ?",
            (chat_id,)
        )
