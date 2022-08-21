"""
Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information.
"""

from yaml import load
from os import listdir, path

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

loaded_locales: dict = {}


def load_locale(locale_path: str) -> None:
    """Load locale to cache

    Arguments:
        locale_path {str} -- a full path for locale, e.g /home/user/korone/.../en.yaml
    """
    locale = path.basename(locale_path).replace(".yaml", "")
    with open(locale_path, "r", encoding="utf8") as file:
        content = load(file.read(), Loader)
        loaded_locales[locale] = content["strings"]


def load_locales() -> None:
    """Loads all locales to cache"""
    locale_dir = "korone/locales"
    for file in listdir(locale_dir):
        load_locale(f"{locale_dir}/{file}")


def gettext(message: str, locale: str) -> str | None:
    """Get a text from locales

    Arguments:
        message {str} -- the message to return
        locale {str} -- the locale to get the message. default en 

    Raises:
        KeyError -- raises if the locale or message does not exists
    Returns:
        str -- the message
    """
    try:
        return loaded_locales.get(locale, "en")[message]
    except KeyError as exc:
        raise exc
