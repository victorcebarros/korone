"""
The toggle module enables and disables commands on a per chat basis.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

from pyrogram import Client, filters
from pyrogram.types import Message

from korone.modules.hello import get_language_code
from korone.modules.modules import toggle
from korone.database.manager import Command
from korone.locale import StringResource


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

    return message.text[pos + 1 :]


@Client.on_message(filters.command("disable"))
async def command_disable(_, message: Message) -> None:
    """Disable a command in the current chat.

    Send `/disable <command>` in the chat to disable a command.
    """
    if message.chat is None or message.chat.id is None:
        return

    command: str = get_command_arg(message)
    language_code: str = get_language_code(message)

    if command == "":
        await message.reply(
            StringResource.get(
                language_code, "strings/enable/message/failure/emptycommand"
            )
        )
        return

    try:
        toggle(Command(command=command, chat_id=message.chat.id, state=False))
    except KeyError:
        await message.reply(
            StringResource.get(
                language_code, "strings/disable/message/failure/invalidcommand"
            ).format(command)
        )
        return

    await message.reply(
        StringResource.get(language_code, "strings/disable/message/success")
    )


@Client.on_message(filters.command("enable"))
async def command_enable(_, message: Message) -> None:
    """Enable a command in the current chat.

    Send `/enable <command>` in the chat to enable a command.
    """
    if message.chat is None or message.chat.id is None:
        return

    command: str = get_command_arg(message)
    language_code: str = get_language_code(message)

    if command == "":
        await message.reply(
            StringResource.get(
                language_code, "strings/enable/message/failure/emptycommand"
            )
        )
        return

    try:
        toggle(Command(command=command, chat_id=message.chat.id, state=True))
    except KeyError:
        await message.reply(
            StringResource.get(
                language_code, "strings/enable/message/failure/invalidcommand"
            ).format(command)
        )
        return

    await message.reply(
        StringResource.get(language_code, "strings/enable/message/success")
    )
