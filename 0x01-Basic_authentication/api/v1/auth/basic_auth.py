#!/usr/bin/env python3
""" Basic Authentication Implementation """

from api.v1.auth.auth import Auth


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
