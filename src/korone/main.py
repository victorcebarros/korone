# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging

from korone import config
from korone.commands import App, AppParameters
from korone.database import Database

log = logging.getLogger(__name__)


def main(argv: list[str]) -> int:
    """
    The main function is the entry point for the program.

    It creates a new instance of an App object and runs it.

    :param argv:list[str]: Pass command line arguments to the program
    :return: The number of arguments passed to it
    """
    log.info("Program started")

    config.init("korone.conf")

    ipv6: bool = False

    if config.get("pyrogram", "USE_IPV6").lower() in ("yes", "true", "1"):
        ipv6 = True

    Database.connect("korone.db")
    Database.setup()

    param: AppParameters = AppParameters(
        api_id=config.get("pyrogram", "API_ID"),
        api_hash=config.get("pyrogram", "API_HASH"),
        bot_token=config.get("pyrogram", "BOT_TOKEN"),
        ipv6=ipv6,
    )

    app: App = App(param)
    app.setup()
    app.run()

    Database.close()

    return len(argv) - 1
