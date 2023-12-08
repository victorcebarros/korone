"""
Korone's Custom Module System.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import inspect
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from importlib import import_module
from types import FunctionType, ModuleType
from typing import Any

from pyrogram import Client, filters
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message

from korone import constants
from korone.database import Database
from korone.database.manager import Clause, Column, Command, CommandManager
from korone.utils.misc import get_command_name
from korone.utils.traverse import bfs_attr_search

log = logging.getLogger(__name__)


@dataclass
class Module:
    """Module Metadata."""

    name: str
    """Module Name."""

    author: str
    """Module Author."""


# global module table which gets loaded on boot
MODULES: list[Module] = [
    Module(name="hello", author="Korone Devs"),
    Module(name="ping", author="Korone Devs"),
    Module(name="toggle", author="Korone Devs"),
]


# global command table which allows aliasing
COMMANDS: dict[str, Any] = {}
"""
Korone's command structure.

Example:
    .. code-block:: python

        >>> COMMANDS = {
        ...     "command": {
        ...         "chat": {
        ...             1000: True,
        ...             1001: False,
        ...         },
        ...         "children": [
        ...             "cmd",
        ...             "cm",
        ...         ],
        ...     },
        ...     "cmd": {
        ...         "parent": "command",
        ...     },
        ...     "cm": {
        ...         "parent": "command",
        ...     },
        ... }
"""


async def togglable(_, __, update: Message) -> bool:
    """Filter to handle state of command for Pyrogram's Handlers.

    Args:
        update (Message): update

    Returns:
        bool: True if it handles the command, False otherwise.
    """

    if update.chat is None or update.chat.id is None:
        return False

    command: str = get_command_name(update)

    log.debug("command: %s", command)

    if command not in COMMANDS:
        return False

    if "parent" in COMMANDS[command]:
        command = COMMANDS[command]["parent"]

    if update.chat.id not in COMMANDS[command]["chat"]:
        return True

    return COMMANDS[command]["chat"][update.chat.id]


# we make the filter accessible to all other modules
filters.togglable = filters.create(togglable)  # type: ignore


def toggle(command: Command) -> None:
    """Enable or disable commands.

    Args:
        command (Command): command
    """

    if command.command not in COMMANDS:
        raise KeyError(f"Command '{command.command}' has not been registered!")

    if "parent" in COMMANDS[command.command]:
        command.command = COMMANDS[command.command]["parent"]

    COMMANDS[command.command]["chat"][command.chat_id] = command.state

    cmdmgr = CommandManager(Database())

    if command.state:
        cmdmgr.enable(command.command, command.chat_id)
        return

    cmdmgr.disable(command.command, command.chat_id)


def register_command(app: Client, command: FunctionType) -> bool:
    """Registers command handlers to Pyrogram.

    Args:
        app (Client): Pyrogram's Client
        command (FunctionType): Function with Pyrogram's Handler

    Returns:
        bool: True if successful, False otherwise.
    """
    if app is None:
        return False

    successful: bool = False

    for handler, group in command.handlers:  # type: ignore
        if isinstance(handler, Handler) and isinstance(group, int):
            log.info("Registering command %s", command)
            log.info("\thandler: %s", handler)
            log.info("\tgroup:   %d", group)

            successful = True

            app.add_handler(handler, group)

            log.debug("Checking for command filters.")
            if handler.filters is None:
                continue

            log.debug("Getting command aliases.")
            try:
                alias: list[str]
                alias = list(bfs_attr_search(handler.filters, "commands"))
            except AttributeError:
                continue

            log.info('Found "%s" command(s)!', alias)

            parent: str = alias[0]
            children: list[str] = alias[1:]

            COMMANDS[parent] = {
                "chat": {},
                "children": children,
            }

            for cmd in children:
                COMMANDS[cmd] = {
                    "parent": parent,
                }

            cmdmgr = CommandManager(Database())

            for each in cmdmgr.query(Clause(Column.COMMAND, parent)):
                log.debug(
                    "Fetched chat state from the database: %s => %s",
                    each.chat_id,
                    str(each.state),
                )
                COMMANDS[parent]["chat"][each.chat_id] = each.state

            log.debug("New command node: %s", COMMANDS[parent])

    return successful


def load_module(app: Client, module: Module) -> None:
    """Loads all handlers within module.

    Args:
        app (Client): Pyrogram Client
        module (Module): Korone Module
    """

    if app is None:
        log.critical("Pyrogram's Client app has not been initialized!")
        log.critical("User attempted to load commands before init.")

        raise TypeError("app has not been initialized!")

    try:
        log.info("Loading module %s", module.name)

        name: str = module.name
        pkg: str = constants.MODULES_PACKAGE_NAME

        component: ModuleType = import_module(f".{name}", pkg)

    except ModuleNotFoundError as err:
        log.error("Could not load module %s: %s", module.name, err)
        raise

    commands: Iterable[FunctionType] = filter(
        lambda fun: hasattr(fun, "handlers"),
        filter(inspect.isfunction, (getattr(component, var) for var in vars(component))),
    )

    for command in commands:
        log.info("Adding command %s from module", command)
        if not register_command(app, command):
            log.info("Could not add command %s", command)
            continue

        log.info("Successfully added command %s", command)


def load_all(app: Client) -> None:
    """Loads all modules declared within core modules.

    Args:
        app (Client): Pyrogram's Client
    """

    for module in MODULES:
        load_module(app, module)
