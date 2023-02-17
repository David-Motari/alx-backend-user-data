#!/usr/bin/env python3
"""
auth
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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

    def create_session(self, email: str) -> str:
        """
        session id creator
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        finding user wit session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generates password reset token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password) -> None:
        """
        updates password in db
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hsh_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hsh_pwd)
        self._db.update_user(user.id, reset_token=None)


def _hash_password(password: str) -> bytes:
    """
    hashing a given password
    """
    encd_pwd = password.encode("utf=8")
    return hashpw(encd_pwd, gensalt())


def _generate_uuid() -> str:
    """
    generating a UUID
    """
    return str(uuid.uuid4())
