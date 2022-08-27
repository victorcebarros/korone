"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from korone.database import Database
from korone.utils import log


class Manager:  # pylint: disable=too-few-public-methods
    """Base Manager Class."""
    def __init__(self, database: Database):
        if database is None:
            log.critical("Database is None!")
            raise RuntimeError("Database is None")

        self.database: Database = database
