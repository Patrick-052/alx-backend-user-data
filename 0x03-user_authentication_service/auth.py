#!/usr/bin/env python3
""" Implementing password hashing """

from db import DB
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Method that registers a user and returns the user object """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))


def _hash_password(password: str) -> bytes:
    """ Method that hashes a password and adds salt on the
        password to make it unique """
    pwd = password.encode()
    return hashpw(pwd, gensalt())
