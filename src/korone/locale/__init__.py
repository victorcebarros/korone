"""
The ``korone.locale`` is the package that manages Korone's locales.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import gettext
import logging
from typing import Any, Dict

log = logging.getLogger(__name__)


class StringResource:
    _translations: Dict[str, Any] = {}
    _localedir: str = "."
    _domain: str = "korone"

    @classmethod
    def _get_translation(cls, locale: str) -> Any:
        if locale not in cls._translations:
            translation = gettext.translation(
                cls._domain,
                cls._localedir,
                [locale],
                fallback=True,
            )
            cls._translations[locale] = translation
        return cls._translations[locale]

    @classmethod
    def ugettext(cls, locale: str, text: str) -> str:
        translation = cls._get_translation(locale)
        return translation.gettext(text)

    @classmethod
    def ungettext(cls, locale: str, singular: str, plural: str, number: int) -> str:
        translation = cls._get_translation(locale)
        return translation.ngettext(singular, plural, number)
