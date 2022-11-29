"""
Database queries.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging

from copy import copy
from typing import Any

log = logging.getLogger(__name__)


# Represents a string containing placeholders for the
# data which will be bound on the SQL Statement.
# For example:
# >>> clause: Clause = "user == ?"
Clause = str

# Represents the actual data which is bound to a given
# placeholder.
# For example:
# >>> data: BoundData = ("Oliver",)
BoundData = tuple[Any, ...]

# Represents the result produced by a query, which
# is used internally to execute the appropriate SQL
# statement.
# For example:
# >>> result: Result = ("user == ?", ("Oliver",))
Result = tuple[Clause, BoundData]


class Query:
    """Queries allows you to specify what element or
    elements to fetch from the database.

    Example:
        .. code-block:: python

            >>> # hypothetical, not yet implemented, connection class
            >>> conn = Connection()
            >>> table = conn.logicians()
            >>> logician = Query()
            >>> table.query(logician.name == "Kazimierz Kuratowski")
            [{'desc': 'Polish mathematician and logician. [...]',
              'name': 'Kazimierz Kuratowski'}]
    """

    def __init__(self, *, lhs=None, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __getattr__(self, name: str):
        # Allows for instance.name
        self.lhs = name
        return self

    def __getitem__(self, item: str):
        # Allows for instance['name']
        return self.__getattr__(item)

    def __copy__(self):
        return Query(lhs=self.lhs, operator=self.operator, rhs=self.rhs)

    def _new_node(self, *, lhs=None, operator=None, rhs=None) -> 'Query':
        query = Query(
            lhs=copy(lhs),
            operator=copy(operator),
            rhs=copy(rhs),
        )

        # consider this case, what should user by itself return?
        # >>> user = Query()
        # >>> (user.name == "Hyper Mega Chad Polyglot") & user
        # to keep a defined state, we clear previously defined keys
        self.lhs = None
        self.rhs = None

        return query
