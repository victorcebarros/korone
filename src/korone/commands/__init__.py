"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from pyrogram import Client

from korone import config
from korone.utils import log


app: Client | None = None


def init(api_id: str, api_hash: str, bot_token: str,
        use_ipv6: bool, workers: int) -> None:
    """Initializes Pyrogram's Client."""
    # NOTE: Yes, we could encapsulate app into a class, however it
    #       wouldn't necessarily fix the problem of "simultaneously
    #       accessing and modifying global variables", as we would
    #       still be able to modify the object's internal attributes.
    #       This app object should only be used within the commands
    #       modules by other modules which the client in order to
    #       work.
    global app  # pylint: disable=global-statement,invalid-name
    app = Client(
        session_name=":memory:",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        ipv6=use_ipv6,
        workers=workers
    )
