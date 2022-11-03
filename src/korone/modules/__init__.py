"""
The ``korone.commands`` package is responsible for starting
Pyrogram's Client and handling with all the commands modules.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging
from dataclasses import dataclass

from pyrogram import Client

from korone import constants
from korone.modules import core

log = logging.getLogger(__name__)


@dataclass
class AppParameters:
    """:obj:`pyrogram.Client` parameters."""

    api_hash: str
    """API hash."""

    api_id: str
    """API ID."""

    bot_token: str
    """Bot token."""

    in_memory: bool = True
    """:obj:`True` if the Pyrogram session
    should be in memory, otherwise :obj:`False`."""

    ipv6: bool = False
    """:obj:`True` if the client should use IPv6, otherwise :obj:`False`."""

    name: str = constants.DEFAULT_NAME
    """Name of the client."""

    workers: int = constants.DEFAULT_WORKERS
    """Number of workers to be used by the client."""


class App:
    """Handles :obj:`~pyrogram.Client` and :obj:`~korone.database.Database`."""

    def __init__(self, parameters: AppParameters):
        self.app: Client | None = None
        self.parameters: AppParameters = parameters

    def setup(self) -> None:
        """The setup function is called when the module is loaded.
        It creates a new :obj:`~pyrogram.Client` object and stores
        it in self.app for later use.
        """
        log.debug("Creating Pyrogram Client object")
        self.app = Client(
            api_hash=self.parameters.api_hash,
            api_id=self.parameters.api_id,
            bot_token=self.parameters.bot_token,
            in_memory=self.parameters.in_memory,
            ipv6=self.parameters.ipv6,
            name=self.parameters.name,
            workers=self.parameters.workers,
        )

        log.debug("Loading modules")
        core.load_all(self.app)

    def run(self) -> None:
        """The run function is the main entry point for the client.
        It is responsible for initializing and running the application,
        as well as handling any errors that may occur during execution.

        Raises:
            :obj:`RuntimeError`: If the :obj:`~pyrogram.Client` is
                not initialized.
        """
        if self.app is None:
            raise RuntimeError("App is not initialized!")

        log.info("Running client")
        self.app.run()
