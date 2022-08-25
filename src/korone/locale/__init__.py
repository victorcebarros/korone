"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from io import TextIOWrapper
from os import path
from typing import Any

import yaml

from korone.utils import log
from korone.utils.traverse import traverse


class StringResource:
    """Get locale-specific string resources."""
    languages: dict[str, Any] = {}
    dirpath: str = path.dirname(__file__)

    @classmethod
    def load(cls, language_code: str) -> dict[str, str]:
        """Loads language to cache."""
        if language_code in cls.languages:
            return cls.languages[language_code]

        log.info("Loading language locale for %s", language_code)

        langpack: str = path.join(cls.dirpath, language_code + ".yaml")

        if not path.isfile(langpack):
            return cls.load("en")

        try:
            langfile: TextIOWrapper
            with open(langpack, "r", encoding="utf-8") as langfile:
                loader: Any = yaml.Loader

                if hasattr(yaml, "CLoader"):
                    loader = yaml.CLoader

                content: dict = yaml.load(langfile, loader)

                cls.languages[language_code] = content

                return cls.languages[language_code]
        except OSError as err:
            log.critical("Could not open language pack file: %s", err)

        return {}

    @classmethod
    def get(cls, language_code: str, resource: str, default: str = "") -> str:
        """Returns locale-specific resource for a given language."""
        string: str

        try:
            string = traverse(cls.load(language_code), resource)
        except KeyError:
            string = traverse(cls.load("en"), resource)

        if not isinstance(string, str):
            string = default

        return string
