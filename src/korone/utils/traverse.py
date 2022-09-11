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

    :param tree:Union[dict, list]: The tree to traverse
    :param path:str: Specify the path to the node that we want to access
    :param separator:str="/": Specify the path separator
    :return: The -value +node at that path.
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


def bfs_attr_search(root: Any, attr: str) -> Any:
    """
    Searches for attribute in object using the BFS algorithm.

    Note: attributes starting with '_' are ignored.

        .. code-block:: python
            >>> def fun():
            ...     pass
            >>> fun.hello = lambda x: x * 2
            >>> fun.hello.again = lambda x: x / 4
            >>> fun.hallo = lambda x: x - 7
            >>> fun.hallo.wieder = lambda x: x ** 3
            >>> fun.hola = lambda x: x + 2
            >>> fun.hola.otravez = lambda x: x * 8
            >>> bfs_attr_search(fun, "again")
            <function <lambda> at ???>
            >>> bfs_attr_search(fun, "again")(20)
            5.0

    :param root: Root of search
    :type root:  object
    :param attr: Attribute name to search
    :type attr:  str

    :return:     The attribute with name attr found in search
    :rtype:      object

    :raises AttributeError: When could not find the attribute
    """

    queue: list = []
    visited: list = []

    queue.append(root)
    visited.append(id(root))

    while queue:
        obj = queue.pop()

        if hasattr(obj, attr):
            return getattr(obj, attr)

        try:
            objs = map(lambda attr: getattr(obj, attr),
                       filter(lambda s: not s.startswith("_"),
                              vars(obj)))
        except TypeError:
            continue

        for neighbor in objs:
            if id(neighbor) not in visited:
                queue.append(neighbor)
                visited.append(id(neighbor))

    raise AttributeError(f"Could not find attribute {attr}")
