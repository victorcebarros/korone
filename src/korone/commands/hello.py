"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from pyrogram import Client
from pyrogram import filters

from pyrogram.types import Message

from korone import commands
from korone.utils import log


@commands.app.on_message(filters=filters.command("hello"))  # type: ignore
async def command_hello(client: Client, message: Message) -> None:
    """Says hello."""
    log.info("user started interaction")

    if client is None or message is None or message.chat is None:
        return

    await client.send_message(chat_id=message.chat.id, text="Hello!")
