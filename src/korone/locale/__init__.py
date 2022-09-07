"""
``korone.locale`` is the package that manages Korone's locales.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging
from io import TextIOWrapper
from os import path
from typing import Any

import yaml

from korone.utils.traverse import traverse

log = logging.getLogger(__name__)


class StringResource:
    """Get locale-specific string resources."""

    languages: dict[str, Any] = {}
    dirpath: str = path.dirname(__file__)

    @classmethod
    def load(cls, language_code: str) -> dict[str, str]:
        """
        The load function loads a language pack for the specified language code.
        If the file does not exist, it will load English instead.

        :param language_code: Specify the language code to load
        :type language_code: str
        :return: A dictionary of the language strings
        :rtype: dict[str, str]
        """
        if language_code in cls.languages:
            return cls.languages[language_code]

        log.info("Loading language locale for %s", language_code)

        langpack: str = path.join(cls.dirpath, f"{language_code}.yaml")

        if not path.isfile(langpack):
            return cls.load("en")

        try:
            langfile: TextIOWrapper
            with open(langpack, "r", encoding="utf-8") as langfile:
                content: dict = yaml.safe_load(langfile)

                cls.languages[language_code] = content

                return cls.languages[language_code]
        except OSError as err:
            log.critical("Could not open language pack file: %s", err)

        return {}

    @classmethod
    def get(cls, language_code: str, resource: str, default: str = "") -> str:
        """
        The get function is a helper function that retrieves the string from
        the resource file. If it is not found, then it will attempt to retrieve
        it from the English resource file. If that fails, then it returns the default.

        :param language_code: Specify the language of the string that is being looked up
        :type language_code: str
        :param resource: Specify the resource that is being loaded
        :type resource: str
        :param default: Set a default value if the resource is not found, defaults to ""
        :type default: str, optional
        :return: The string at the given resource
        :rtype: str
        """
        string: str

        try:
            string = traverse(cls.load(language_code), resource)
        except KeyError:
            try:
                string = traverse(cls.load("en"), resource)
            except KeyError:
                string = default

        return string
