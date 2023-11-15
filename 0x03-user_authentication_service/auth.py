#!/usr/bin/env python3
""" Implementing password hashing """

from db import DB
from user import User
from uuid import uuid4
from typing import Union
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

    def create_session(self, email: str) -> Union[str, None]:
        """ Method that returns session_id based on the user """
        try:
            user = self._db.find_user_by(email=email)
            uid = _generate_uuid()

            self._db.update_user(user.id, session_id=uid)
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Method that returns a user object based on session id """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None


def _generate_uuid() -> str:
    """ Method that returns a string representation of a new UUID """
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """ Method that hashes a password and adds salt on the
        password to make it unique """
    pwd = password.encode()
    return hashpw(pwd, gensalt())
