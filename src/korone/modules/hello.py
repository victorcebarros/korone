"""
A few proof-of-concept commands.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from korone.locale import StringResource
from korone.utils.misc import get_language_code

log = logging.getLogger(__name__)


@Client.on_message(group=1)
async def catchall(_a: Client, _b: Message) -> None:
    log.debug("New message!")


@Client.on_message(filters.command("greet") & filters.togglable)  # type: ignore
async def command_greet(_: Client, message: Message) -> None:
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.ugettext(language_code, "Hello there!"),
    )


@Client.on_message(filters.command("farewell") & filters.togglable)  # type: ignore
async def command_farewell(_: Client, message: Message) -> None:
    language_code: str = get_language_code(message)

    await message.reply(
        StringResource.ugettext(language_code, "Farewell!"),
    )
