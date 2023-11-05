#!/usr/bin/env python3
""" Module implementing Encryption and validation of passwords """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Function that takes in a password string arguments
        and returns bytes. """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function that accepts two args and returns a boolean indicating
        whether or not the provided password matches the hashed password. """
    return bcrypt.checkpw(password.encode(), hashed_password)
