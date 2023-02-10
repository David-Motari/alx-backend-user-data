#!/usr/bin/env python3
"""
session_auth
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    session authentication class, inherits from auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session[session_id] = user_id
        return session_id
