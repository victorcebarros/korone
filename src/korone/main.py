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

    commands.init(
        api_id=config.get("Authentication", "API_ID"),
        api_hash=config.get("Authentication", "API_HASH"),
        bot_token=config.get("Authentication", "BOT_TOKEN")
    )

    if commands.app:
        modules.load(commands.app)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(commands.app.run())
        loop.close()

    return len(argv) - 1
