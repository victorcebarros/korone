"""
A few proof-of-concept commands.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from korone.locale import StringResource

log = logging.getLogger(__name__)


def get_language_code(message: Message) -> str:
    """
    The get_language_code function takes a message object as an argument and
    returns the language code of the user who sent that message.
    If no language code is found, it defaults to "en" (English).

    Example:
        .. code-block:: python

            >>> get_language_code(message)
            pt-br

    :param message: Get the message that was sent by the user
    :type message: Message
    :return: The language code of the user that sends a message
    :rtype: str
    """
    language_code: str = "en"
    if message.from_user is None:
        return language_code

    if message.from_user.language_code is None:
        return language_code

    language_code = message.from_user.language_code

    return language_code


@Client.on_message(group=1)
async def catchall(_a: Client, _b: Message) -> None:
    log.debug("New message!")


@Client.on_message(filters.command("greet"))
async def command_greet(_: Client, message: Message) -> None:
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.get(language_code, "strings/greet/message"),
    )


@Client.on_message(filters.command("farewell"))
async def command_farewell(_: Client, message: Message) -> None:
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.get(language_code, "strings/farewell/message"),
    )
