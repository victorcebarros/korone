"""
Module to help managing trees.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

from pyrogram.types import Message


def get_command_name(message: Message) -> str:
    """Gets command name.

    Example:
        .. code-block:: python

            >>>     # id=0 is required to create the message type
            >>> m = Message(text="/command arg1 arg2 ... argN", id=0)
            >>> c = get_command_name(m)
            >>> c
            "command"

    Args:
        message (:obj:`~pyrogram.types.Message`): Pyrogram Message.

    Returns:
        str: Stripped command name
    """
    if message.text is None:
        return ""

    if not message.text.startswith("/"):
        return ""

    pos: int = message.text.find(" ")
    if pos == -1:
        pos = len(message.text)

    return message.text[1:pos]


def get_command_arg(message: Message) -> str:
    """Get the command argument from message.

    Example:
        .. code-block:: python

            >>>     # id=0 is required to create the message type
            >>> m = Message(text="/command arg1 arg2 ... argN", id=0)
            >>> c = get_command_name(m)
            >>> c
            "arg1 arg2 ... argN"

    Args:
        message (:class:`~pyrogram.types.Message`): Pyrogram's Message.

    Returns:
        :obj:`str`: Arguments passed to the command.
    """
    if message is None or message.text is None:
        return ""

    pos: int = message.text.find(" ")

    if pos == -1:
        return ""

    return message.text[pos + 1 :]


def get_language_code(message: Message) -> str:
    """Returns appropriate language code. Default return value is 'en'.

    Args:
        message (:obj:`~pyrogram.types.Message`): Pyrogram Message.

    Returns:
        str: Sender's Language Code.
    """
    language_code: str = "en"
    if message.from_user is None:
        return language_code

    if message.from_user.language_code is None:
        return language_code

    return message.from_user.language_code
