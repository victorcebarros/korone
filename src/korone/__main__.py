"""
Starts logging system.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import logging
import sys

from korone import constants
from korone.main import main

LEVEL = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logging.basicConfig(
    format=constants.LOGGER_FORMAT_OUTPUT,
    level=LEVEL,
)

sys.exit(main(sys.argv))
