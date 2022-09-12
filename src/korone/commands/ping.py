import time

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("ping"))
async def command_ping(_, message: Message) -> None:

    then = time.time()
    msg = await message.reply("Pong!")
    now = time.time()

    await msg.edit_text(f"Pong! <code>{(now - then) * 1e3}ms</code>")
