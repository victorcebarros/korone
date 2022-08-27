"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from korone.utils import log

from korone.locale import StringResource


def get_language_code(message: Message) -> str:
    """Gets language code from message."""
    language_code: str = "en"
    if message.from_user is None:
        return language_code

    if message.from_user.language_code is None:
        return language_code

    language_code = message.from_user.language_code

    return language_code


@Client.on_message(group=1)
async def catchall(_a: Client, _b: Message) -> None:
    """Catches all messages from user."""

    log.debug("New message!")


@Client.on_message(filters.command("greet"))
async def command_greet(_: Client, message: Message) -> None:
    """Says hello."""
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.get(language_code, "strings/greet/message")
    )


@Client.on_message(filters.command("farewell"))
async def command_farewell(_: Client, message: Message) -> None:
    """Says farewell."""
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.get(language_code, "strings/farewell/message")
    )
