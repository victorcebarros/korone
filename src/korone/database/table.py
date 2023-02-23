"""
Simplified interface between SQL Database and the user.

It allows for a DBMS agnostic implementation, thus hiding
the implementation details and preventing bugs.
"""

from typing import Any, NewType, Protocol

from korone.database.query import Query


class Document(dict[str, Any]):
    """
    Document represents a single row on the SQL Database
    Table.

    One should note that, due to the limitation of Table
    Rows, one cannot use a Collection or Mapping as a
    Document Value.

    For example:

    .. code-block:: python

        >>> invaliddoc: Document = {"key": [1, 2, 3, 4, 5, 6]}
    """


Documents = NewType("Documents", list[Document])
"""
A list of Documents.
"""


class Table(Protocol):
    """Table from the database.

    It provides a higher level interface to the
    database by using queries, thereby preventing
    the user from dealing with SQL Queries directly.
    """

    def insert(self, fields: Any | Document):
        """Insert a row on the table.

        The `fields` parameter may be of any type that
        contains object.__dict__. It may also be a
        Document type.

        Keep in mind that, in the former case, keys
        starting with _ will be ignored, whereas in
        the latter, they will not.

        For example:

            .. code-block:: python

                >>> class HappyLittleCustomer:
                ...     def __init__(self, name: str):
                ...         self._name = name
                ...
                >>> gummikunde = HappyLittleCustomer("nibble")
                >>> vars(gummikunde)
                {'_name': 'nibble'}
                >>> # it won't insert anything, since we are passing
                >>> # a class instead of a Document
                >>> table.insert(gummikunde)

        .. warning::

            Document values *cannot* have nested values, due to the
            limitation of database rows. Refer to the Document type
            for more information.


        Args:
            fields (Any | Document): fields to insert.
        """

    def query(self, query: Query) -> Documents:
        """Query rows that match the criteria.

        Args:
            query (Query): matching criteria.

        Returns:
            Documents: List of Documents of rows that matched
            the criteria.
        """

    def update(self, fields: Any | Document, query: Query):
        """Update fields on rows that match the criteria.

        The fields has a special behavior. You should check
        the method `insert` for more information.

        Args:
            fields (Any | Document): fields to update.
            query (Query): matching criteria.
        """

    def delete(self, query: Query):
        """Delete rows that match the criteria.

        Args:
            query (Query): matching criteria.
        """
