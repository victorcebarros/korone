"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

from dataclasses import dataclass
from importlib import import_module

from pyrogram import Client

from korone import constants
from korone.database import Database
from korone.utils import log


@dataclass
class Module:
    """Module metadata."""
    name: str
    author: str
    has_help: bool


APP: Client | None = None
DATABASE: Database | None = None

MODULES: list[Module] = [
    Module(name="hello", author="foo", has_help=False),
]


def load(app: Client, database: Database) -> None:
    """Loads commands after initialization."""
    if app is None:
        log.critical("Pyrogram's Client app has not been initialized!")
        log.critical("User attempted to load commands before init.")

        raise TypeError("app has not been initialized!")

    # NOTE: This is a bit hacky, however it allows me to
    #       create a cleaner module interface for Korone commands.
    global APP, DATABASE  # pylint: disable=global-statement
    APP = app
    DATABASE = database

    for module in MODULES:
        try:
            log.info("Loading module %s", module.name)
            import_module(f".{module.name}",
                          constants.MODULES_PACKAGE_NAME)
        except ModuleNotFoundError as err:
            log.error("Could not load module %s: %s", module.name, err)
