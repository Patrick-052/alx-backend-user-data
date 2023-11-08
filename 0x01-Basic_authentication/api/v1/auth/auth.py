#!/usr/bin/env python3
""" Implementing the API authentication """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Function that implements authentication requirement or not
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Function that handles authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Function that handles current user
        """
        return None
