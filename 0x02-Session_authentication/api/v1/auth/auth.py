#!/usr/bin/env python3
"""
auth
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    class for authentiation
    """

    SESSION_NAME = getenv("SESSION_NAME")

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns false, and true if auth is required
        """

        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        l_path = len(path)
        if l_path == 0:
            return True

        slash_path = True if path[l_path - 1] == "/" else False

        tmp_path = path
        if not slash_path:
            tmp_path += "/"

        for exc in excluded_paths:
            l_exc = len(exc)
            if l_exc == 0:
                continue

            if exc[l_exc - 1] != "*":
                if tmp_path == exc:
                    return False
            else:
                if exc[:-1] == path[: l_exc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        returns None
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """
        returns None
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request is None:
            return None
        return request.cookies.get(self.SESSION_NAME)
