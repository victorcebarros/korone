"""
Module to help managing trees.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

from pyrogram.types import Message


def get_command_name(message: Message) -> str:
    """Gets command name.

    Args:
        message (Message): message

    Returns:
        str: stripped command name
    """
    if message.text is None:
        return ""

    if not message.text.startswith("/"):
        return ""

    pos: int = message.text.find(" ")
    if pos == -1:
        pos = len(message.text)

    return message.text[1:pos]


def get_language_code(message: Message) -> str:
    """The get_language_code function takes a message object as an argument and
    returns the language code of the user who sent that message.
    If no language code is found, it defaults to "en" (English).

    Args:
        message (:obj:`~pyrogram.types.Message`): Get the message that was
            sent by the user.

    Returns:
        str: The language code of the user that sends a message.
    """
    language_code: str = "en"
    if message.from_user is None:
        return language_code

    if message.from_user.language_code is None:
        return language_code

    language_code = message.from_user.language_code

    return language_code


def get_command_arg(message: Message) -> str:
    """Get the command argument from the message.

    Args:
        message (:class:`~pyrogram.types.Message`): The message to get the
            command argument from.

    Returns:
        :obj:`str`: The command argument.
    """
    if message is None or message.text is None:
        return ""

    pos: int = message.text.find(" ")

    if pos == -1:
        return ""

    return message.text[pos + 1:]
