"""
The ping module test the Korone's latency with Telegram's servers.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import time

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("ping"))
async def command_ping(_, message: Message) -> None:
    """Checks the latency between Korone and Telegram's servers.

    Send `/ping` in the chat to get the latency.
    """

    then = time.time()
    msg = await message.reply("Pong!")
    now = time.time()

    await msg.edit_text(f"Pong! <code>{(now - then) * 1e3}ms</code>")
