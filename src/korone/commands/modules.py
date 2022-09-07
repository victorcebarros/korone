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
from typing import Iterable

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers.handler import Handler

from korone import constants
from korone.database import Database
from korone.database.manager import Command, CommandManager

log = logging.getLogger(__name__)


@dataclass
class Module:
    """Module metadata."""

    name: str
    author: str
    has_help: bool


MODULES: list[Module] = [
    Module(name="hello", author="Korone Devs", has_help=False),
    Module(name="toggle", author="Korone Devs", has_help=False),
]


COMMANDS: dict[str, dict[int, bool]] = {}

# FIXME: Properly implement togglabilty of commands
#        We should probably register commands on the load function
#        and then enable / disable them
def toggle(command: Command):
    """Toggles command."""

    if command.command not in COMMANDS:
        COMMANDS[command.command] = {}

    COMMANDS[command.command][command.chat_id] = command.state

    cmdmgr = CommandManager(Database())

    if command.state:
        cmdmgr.enable(command.command, command.chat_id)

    cmdmgr.disable(command.command, command.chat_id)


async def togglable(_, __, update: Message) -> bool:
    """Checks whether command is enabled or not."""
    if update.chat is None or update.chat.id is None:
        return False

    command: str = get_command_name(update)

    log.info("command: %s", command)

    if command not in COMMANDS:
        return True

    if update.chat.id not in COMMANDS[command]:
        return True

    return COMMANDS[command][update.chat.id]


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
    """
    The get_commands function takes a module and returns an iterable of functions
    that have been decorated with the @handler decorator. This function is used to
    determine which commands are available for use by the client.

    :param module:ModuleType: Get the module that contains the function
    :return: An iterable of functions that have a `handlers` attribute
    """
    functions = filter(
        inspect.isfunction, map(lambda var: getattr(module, var), vars(module))
    )
    return filter(lambda fun: hasattr(fun, "handlers"), functions)


def load(app: Client) -> None:
    """
    The load function is responsible for loading
    all of the modules in the modules package.

    :param app:Client: Call the load function
    :return: None
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

        def add(command: FunctionType) -> bool:
            """
            The add function adds a command to the bot.
            It takes in a function, and then for each handler that is associated with it,
            adds it to the bot.
            The add function returns True if successful or False if unsuccessful.

            :param command:FunctionType: Specify the command that is being added
            :return: True if the command was loaded successfully, false otherwise
            """
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

        # FIXME: Handle state of commands directly when registering them

        cmdmgr = CommandManager(Database())

        # loads the state of the commands
        # in case they are disabled
        for cmd in cmdmgr.query():
            toggle(cmd)
