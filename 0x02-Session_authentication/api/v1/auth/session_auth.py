#!/usr/bin/env python3
""" Implementing Session Authentication """

from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ Session Authentication class """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
