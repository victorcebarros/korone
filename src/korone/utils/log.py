"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


# NOTE: I'm not sure if this is the appropriate way to re-export things
#       from other modules in Python. If anyone has an idea on how to
#       do it the Pythonic way, feel free to include the changes as needed.
from logging import (  # pylint: disable=unused-import
        critical,
        debug,
        error,
        exception,
        info,
        log,
        warning
)

import logging
import sys

from korone import constants


LEVEL: int = logging.INFO


if "--debug" in sys.argv:
    LEVEL = logging.DEBUG


logging.basicConfig(
    format=constants.LOGGER_FORMAT_OUTPUT,
    level=LEVEL,
)
