#!/usr/bin/env python3
""" Module implementing Encryption and validation of passwords """

import bcrypt


def hash_password(password: str) -> bytes:
    """ Function that takes in a password string arguments
        and returns bytes. """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
