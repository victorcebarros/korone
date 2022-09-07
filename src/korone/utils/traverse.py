"""
Module to help managing trees.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

from typing import Any, Union


def traverse(tree: Union[dict, list], path: str, separator: str = "/") -> Any:
    """
    The traverse function takes a tree and a path, and returns the value at that
    path. The tree can be either a list or dictionary, but the path must be valid
    for that type of tree. For example:

        .. code-block:: python

            >>> root = {
            >>>     "weekdays": {
            >>>         "monday": "hello",
            >>>         "tuesday": "hola",
            >>>         "wednesday": "hallo",
            >>>         "thursday": "bonjour",
            >>>         "friday": "Здраво",
            >>>     },
            >>>     "fibonacci": [
            >>>         1, 1, 2, 3, 5, 8, 13
            >>>     ]
            >>> }

            >>> traverse(root, "weekday/monday)
            "hello"

            >>> traverse(root, "fibonacci/4")
            5

    :param tree: The tree to traverse
    :type tree: Union[dict, list]
    :param path: Specify the path to the node that we want to access
    :type path: str
    :param separator: Specify the path separator, defaults to "/"
    :type separator: str, optional
    :return: The node at that path.
    :rtype: Any
    """
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
                raise ValueError("Index must be an integer.") from err
            continue

        if isinstance(tree, dict) and node in tree:
            tree = tree[node]
            continue

        raise KeyError(f"Trying to access nonexistent nodes: {node}")

    return tree
