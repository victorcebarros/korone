"""
Custom Pyrogram modules system that loads modules from the modules package.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import inspect
import logging
from dataclasses import dataclass
from importlib import import_module
from types import FunctionType, ModuleType
from typing import Any, Iterable

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers.handler import Handler

from korone import constants
from korone.database import Database
from korone.database.manager import Command, CommandManager, Clause, Column
from korone.utils.traverse import bfs_attr_search

log = logging.getLogger(__name__)


@dataclass
class Module:
    """Module structure."""

    name: str
    """Module name"""

    author: str
    """Module author"""

    has_help: bool
    """:obj:`True` if the module has help, otherwise :obj:`False`"""


MODULES: list[Module] = [
    Module(name="hello", author="Korone Devs", has_help=False),
    Module(name="toggle", author="Korone Devs", has_help=False),
    Module(name="ping", author="Korone Devs", has_help=False),
]


"""
Example structure
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
COMMANDS: dict[str, Any] = {}


def toggle(command: Command):
    """Toggles command."""

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


async def togglable(_, __, update: Message) -> bool:
    """Checks whether command is enabled or not."""
    if update.chat is None or update.chat.id is None:
        return False

    command: str = get_command_name(update)

    log.info("command: %s", command)

    if command not in COMMANDS:
        return False

    if "parent" in COMMANDS[command]:
        command = COMMANDS[command]["parent"]

    if update.chat.id not in COMMANDS[command]["chat"]:
        return True

    return COMMANDS[command]["chat"][update.chat.id]


filters.togglable = filters.create(togglable)  # type: ignore


# TODO: Move this to some korone.util module
def get_command_name(message: Message) -> str:
    """Get command name.

    """
    if message.text is None:
        return ""

    if not message.text.startswith("/"):
        return ""

    pos: int = message.text.find(" ")
    if pos == -1:
        pos = len(message.text)

    return message.text[1:pos]


def get_commands(module: ModuleType) -> Iterable[FunctionType]:
    """The get_commands function takes a module and returns an iterable
    of functions that have been decorated with the @handler decorator.
    This function is used to determine which commands are available
    for use by the client.

    Args:
        module (:obj:`~types.ModuleType`): Get the module that contains
            the function.

    Returns:
        :class:`~typing.Iterable`\[:obj:`~types.FunctionType`]: An iterable of
        functions that have a `handlers` attribute.
    """
    functions = filter(
        inspect.isfunction, map(lambda var: getattr(module, var), vars(module))
    )
    return filter(lambda fun: hasattr(fun, "handlers"), functions)


def load(app: Client) -> None:
    """The load function is responsible for loading
    all of the modules in the modules package.

    Args:
        app (:class:`~pyrogram.Client`): Call the load function.

    Raises:
        TypeError: If app is not initalized.
    """
    if app is None:
        log.critical("Pyrogram's Client app has not been initialized!")
        log.critical("User attempted to load commands before init.")

        raise TypeError("app has not been initialized!")

    for module in MODULES:
        try:
            log.info("Loading module %s", module.name)
            component = import_module(
                f".{module.name}",
                constants.MODULES_PACKAGE_NAME,
            )
        except ModuleNotFoundError as err:
            log.error("Could not load module %s: %s", module.name, err)
            continue

        commands: Iterable[FunctionType] = get_commands(component)

        def register(command: FunctionType) -> bool:
            """
            Registers command handlers to Pyrogram.

            The argument is a function containing at least one handler.

            Args:
                command (:class:`~types.FunctionType`): Function containing handler

            Returns:
                bool: :obj:`True` if successful, :obj:`False` otherwise.
            """
            successful: bool = False
            for handler, group in command.handlers:  # type: ignore
                if isinstance(handler, Handler) and isinstance(group, int):
                    log.info("Loading command %s", command)
                    log.info("\thandler: %s", handler)
                    log.info("\tgroup:   %d", group)
                    app.add_handler(handler, group)

                    successful = True

                    log.debug("Detecting if handler has filters...")
                    if handler.filters is None:
                        continue

                    log.debug("Checking for commands filter...")
                    try:
                        alias: list[str] = list(bfs_attr_search(handler.filters, "commands"))
                    except AttributeError:
                        continue

                    log.info("Found \"%s\" command(s)!", alias)
                    parent: str = alias[0]
                    children: list[str] = alias[1:]

                    COMMANDS[parent] = {
                        'chat': {},
                        'children': children,
                    }

                    for cmd in children:
                        COMMANDS[cmd] = {
                            'parent': parent,
                        }

                    cmdmgr = CommandManager(Database())

                    for each in cmdmgr.query(Clause(Column.COMMAND, parent)):
                        log.debug("Fetched chat state from the database: %s => %s",
                                  each.chat_id, str(each.state))
                        COMMANDS[parent]['chat'][each.chat_id] = each.state

                    log.debug("New command node: %s", COMMANDS[parent])

            return successful

        for command in commands:
            log.info("Adding command %s from module", command)
            if not register(command):
                log.info("Could not add command %s", command)
                continue

            log.info("Successfully added command %s", command)
