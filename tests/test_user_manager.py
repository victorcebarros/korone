"""
Tests for the user manager.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 hytalo-bassi <https://github.com/hytalo-bassi>

from faker import Faker
from pyrogram.types import User
from pytest import fixture

from korone.database import Database
from korone.database.manager import Clause, Column, UserManager

Database.connect("korone-test.db")
Database.setup()


class TestUserManager:
    """Tests the management of user in database"""

    user_manager = UserManager(Database())

    def test_insert_and_query(self):
        """Inserts a random user and query it"""
        usermgr = self.user_manager

        user = TestUserManager.random_user()
        usermgr.insert(user)
        query = list(usermgr.query(Clause(Column.UUID, user.id)))

        assert len(query) == 1

    @staticmethod
    def random_user() -> User:
        """Creates a random user"""
        Faker.seed(0)
        fake = Faker()

        id = fake.numerify(text="#" * 10)  # length 10 number
        first_name = fake.first_name()
        username = fake.user_name()

        return User(id=id, first_name=first_name, username=username)


@fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleans and closes database."""

    def drop_and_close():
        Database.execute("DROP TABLE users;")  # removes all data in user
        Database.close()

    request.addfinalizer(drop_and_close)
