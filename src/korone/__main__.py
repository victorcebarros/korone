"""
Starts logging system.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging
import sys

from korone import constants
from korone.main import main

LEVEL: int = logging.INFO


if "--debug" in sys.argv:
    LEVEL = logging.DEBUG


logging.basicConfig(
    format=constants.LOGGER_FORMAT_OUTPUT,
    level=LEVEL,
)

sys.exit(main(sys.argv))
