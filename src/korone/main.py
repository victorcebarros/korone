"""
Entry point of the Korone.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import logging

from korone import config
from korone.database.impl.sqlite3_impl import SQLite3Connection
from korone.modules import App, AppParameters

log = logging.getLogger(__name__)


def main(argv: list[str]) -> int:
    """The main function is the entry point for the program.
    It creates a new instance of an App object and runs it.

    Args:
        argv (:obj:`list`\\[:obj:`str`]): Pass command line arguments to the
            program.

    Returns:
        :obj:`int`: The number of arguments passed to it.
    """
    log.info("Program started")

    config.init()

    ipv6 = config.get("pyrogram", "USE_IPV6").lower() in ("yes", "true", "1")

    with SQLite3Connection() as conn:
        if not conn:
            log.error("Database connection failed")
            return 1

        conn.setup()

        param: AppParameters = AppParameters(
            api_id=config.get("pyrogram", "API_ID"),
            api_hash=config.get("pyrogram", "API_HASH"),
            bot_token=config.get("pyrogram", "BOT_TOKEN"),
            ipv6=ipv6,
            connection=conn,
        )

        app: App = App(param)
        app.setup()
        app.run()

    return len(argv) - 1
