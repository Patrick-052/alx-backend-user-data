#!/usr/bin/env python3
""" Implementing the API authentication """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Function that implements authentication requirement or not
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths or path + '/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Function that handles authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Function that handles current user
        """
        return None
