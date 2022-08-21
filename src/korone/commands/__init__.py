"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

from dataclasses import dataclass

from pyrogram import Client

from korone import config
from korone import constants
from korone.commands import modules
from korone.database import Database
from korone.utils import log


@dataclass
class AppParameters:
    """Pyrogram's Client parameters."""
    api_hash: str
    api_id: str
    bot_token: str
    in_memory: bool = True
    ipv6: bool = False
    name: str = constants.DEFAULT_NAME
    workers: int = constants.DEFAULT_WORKERS


class App:
    """Handles Pyrogram's Client and Korone's Database."""
    def __init__(self, database: Database, parameters: AppParameters):
        self.app: Client | None = None
        self.database = database
        self.parameters: AppParameters = parameters

    def setup(self) -> None:
        """Sets up Pyrogram's Client and load modules."""
        log.debug("Creating Pyrogram Client object")
        self.app = Client(
            api_hash=self.parameters.api_hash,
            api_id=self.parameters.api_id,
            bot_token=self.parameters.bot_token,
            in_memory=self.parameters.in_memory,
            ipv6=self.parameters.ipv6,
            name=self.parameters.name,
            workers=self.parameters.workers
        )

        log.debug("Loading modules")
        modules.load(self.app, self.database)

    def run(self) -> None:
        """Runs the Pyrogram's Client. Same as Pyrogram's run() method."""
        if self.app is None:
            raise RuntimeError("App is not initialized!")

        log.info("Running client")
        self.app.run()