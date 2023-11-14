#!/usr/bin/env python3
""" Implementing password hashing """

from db import DB
from user import User
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw
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

    def valid_login(self, email: str, password: str) -> bool:
        """ Method that validates the password provided with the hashed
            password for the email provided """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    @property
    def _generate_uuid(self):
        """ Returns a string representation of a new UUID """
        new_id = str(uuid4)
        return new_id


def _hash_password(password: str) -> bytes:
    """ Method that hashes a password and adds salt on the
        password to make it unique """
    pwd = password.encode()
    return hashpw(pwd, gensalt())
