"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from korone import config

from korone.commands import App, AppParameters
from korone.database import Database
from korone.utils import log


def main(argv: list[str]) -> int:
    """Entry point."""

    log.info("Program started")

    config.init("korone.conf")

    ipv6: bool = False

    if config.get("pyrogram", "USE_IPV6").lower() in ("yes", "true", "1"):
        ipv6 = True

    database: Database = Database("korone.db")
    database.open()
    database.setup()

    param: AppParameters = AppParameters(
        api_id=config.get("pyrogram", "API_ID"),
        api_hash=config.get("pyrogram", "API_HASH"),
        bot_token=config.get("pyrogram", "BOT_TOKEN"),
        ipv6=ipv6
    )

    app: App = App(database, param)
    app.setup()
    app.run()

    database.close()

    return len(argv) - 1
