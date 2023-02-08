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

        for paths in excluded_paths:
            if paths.endswith('*'):
                if path.startswith(paths[:-1]):
                    return False
            elif path == paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        returns None
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar("User"):
        """
        returns None
        """
        return None
