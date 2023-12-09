"""
The ``korone.locale`` is the package that manages Korone's locales.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Victor Cebarros <https://github.com/victorcebarros>

import logging
from io import TextIOWrapper
from pathlib import Path
from typing import Any, ClassVar

import yaml

from korone.utils.traverse import traverse

log = logging.getLogger(__name__)


class StringResource:
    """Get locale-specific string resources."""

    languages: ClassVar[dict[str, Any]] = {}
    """The languages dictionary."""

    dirpath: Path = Path(__file__).parent
    """The directory path of the package."""

    @classmethod
    def load(cls, language_code: str) -> dict[str, str]:
        """The load function loads a language pack for the specified language
        code. If the file does not exist, it will load English instead.

        Args:
            language_code (:obj:`str`): Specify the language code to load.

        Returns:
            :obj:`dict`\\[:obj:`str`, :obj:`str`]: A dictionary of the
                language strings.
        """
        if language_code in cls.languages:
            return cls.languages[language_code]

        log.info("Loading language locale for %s", language_code)

        langpack: Path = Path(cls.dirpath / f"{language_code}.yaml")

        if not Path(langpack).is_file():
            return cls.load("en")

        try:
            langfile: TextIOWrapper
            with Path(langpack).open(encoding="utf-8") as langfile:
                content: dict = yaml.safe_load(langfile)

                cls.languages[language_code] = content

                return cls.languages[language_code]
        except OSError as err:
            log.critical("Could not open language pack file: %s", err)

        return {}

    @classmethod
    def get(cls, language_code: str, resource: str, default: str = "") -> str:
        """The get function is a helper function that retrieves the string from
        the resource file. If it is not found, then it will attempt to retrieve
        it from the English resource file. If that fails, then it returns the
        default.

        Args:
            language_code (:obj:`str`): Specify the language of the string that is being looked up.
            resource (:obj:`str`): Specify the resource that is being loaded.
            default (:obj:`str`, *optional*): Set a default value if the resource is not found.
            Defaults to "".

        Returns:
            :obj:`str`: The string at the given resource.
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
