#!/usr/bin/env python3
"""
auth
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers user and returns the user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pwd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=pwd)
            return user
        else:
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        validating login
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hsh_pwd = user.hashed_password
                return checkpw(password.encode("utf-8"), hsh_pwd)
        except NoResultFound:
            return False


def _hash_password(password: str) -> bytes:
    """
    hashing a given password
    """
    encd_pwd = password.encode("utf=8")
    return hashpw(encd_pwd, gensalt())
