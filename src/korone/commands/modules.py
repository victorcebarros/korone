"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from dataclasses import dataclass
from importlib import import_module
from types import FunctionType, ModuleType
from typing import Iterable

import inspect
import logging

from pyrogram import Client
from pyrogram.handlers.handler import Handler

from korone import constants


log = logging.getLogger(__name__)


@dataclass
class Module:
    """Module metadata."""
    name: str
    author: str
    has_help: bool


MODULES: list[Module] = [
    Module(name="hello", author="foo", has_help=False),
]


def get_commands(module: ModuleType) -> Iterable[FunctionType]:
    """Get commands from a module."""
    functions = filter(inspect.isfunction,
                       map(lambda var: getattr(module, var),
                           vars(module)))
    return filter(lambda fun: hasattr(fun, "handlers"), functions)


def load(app: Client) -> None:
    """Loads commands after initialization."""
    if app is None:
        log.critical("Pyrogram's Client app has not been initialized!")
        log.critical("User attempted to load commands before init.")

        raise TypeError("app has not been initialized!")

    for module in MODULES:
        try:
            log.info("Loading module %s", module.name)
            component = import_module(f".{module.name}",
                                      constants.MODULES_PACKAGE_NAME)
        except ModuleNotFoundError as err:
            log.error("Could not load module %s: %s", module.name, err)
            continue

        commands: Iterable[FunctionType] = get_commands(component)

        def add(command: FunctionType) -> bool:
            successful: bool = False
            for handler, group in command.handlers:  # type: ignore
                if isinstance(handler, Handler) and isinstance(group, int):
                    log.info("Loading command %s", command)
                    log.info("\thandler: %s", handler)
                    log.info("\tgroup:   %d", group)
                    app.add_handler(handler, group)
                    successful = True

            return successful

        for command in commands:
            log.info("Adding command %s from module", command)
            if not add(command):
                log.info("Could not add command %s", command)
                continue
            log.info("Successfully added command %s", command)
