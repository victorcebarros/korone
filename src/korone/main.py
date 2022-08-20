"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


import asyncio

from korone import commands
from korone import config

from korone.commands import modules
from korone.utils import log


def main(argv: list[str]) -> int:
    """Entry point."""

    log.info("Program started")

    config.init("korone.conf")

    ipv6: bool = False
    use_ipv6: str = config.get("pyrogram", "USE_IPV6").lower() 

    if use_ipv6 in ("yes", "true"):
        ipv6 = True

    commands.init(
        api_id=config.get("pyrogram", "API_ID"),
        api_hash=config.get("pyrogram", "API_HASH"),
        bot_token=config.get("pyrogram", "BOT_TOKEN"),
        use_ipv6=ipv6,
        workers=int(config.get("pyrogram", "WORKERS"))
    )

    if commands.app:
        modules.load(commands.app)
        commands.app.run()

    return len(argv) - 1
