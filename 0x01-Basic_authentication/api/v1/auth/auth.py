#!/usr/bin/env python3
"""
auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    class for authentiation
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns false, and true if auth is required
        """

        if path is None or excluded_paths is None:
            return True

        if path[-1] != '/':
            path += '/'

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
        returns None
        """
        if request is None or 'Authorization' not in request:
            return None
        return request['Authorization']

    def current_user(self, request=None) -> TypeVar("User"):
        """
        returns None
        """
        return None
