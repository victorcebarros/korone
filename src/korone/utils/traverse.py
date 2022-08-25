"""Korone is a simple multipurpose Telegram Bot.

This is a complete rewrite of PyKorone, refer to
https://github.com/AmanoTeam/PyKorone and README.md for more
information."""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>


from typing import Any
from typing import Union


def traverse(tree: Union[dict, list], path: str, separator: str = "/") -> Any:
    """Gets dictionary node by using path."""

    if tree is None:
        return None

    nodes: list[str] = path.split(separator)

    for node in nodes:
        if node == "":
            continue

        if isinstance(tree, list):
            try:
                tree = tree[int(node)]
            except ValueError as err:
                raise TypeError("Index must be an integer.") from err
            continue

        if isinstance(tree, dict):
            if node in tree:
                tree = tree[node]
                continue

        raise ValueError(f"Trying to access nonexistent nodes: {node}")

    return tree
