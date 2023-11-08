#!/usr/bin/env python3
""" Basic Authentication Implementation """

from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Return Base64 part of Authorization header """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str) \
                or not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Return decoded value of Base64 string """
        if base64_authorization_header is None or not isinstance(base64_authorization_header,
                                                                 str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None
