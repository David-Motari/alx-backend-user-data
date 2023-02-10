#!/usr/bin/env python3
"""
basic_auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar, List
from models.user import User


class BasicAuth(Auth):
    """
    inherits from auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extracting auth header
        """
        if (
            authorization_header is None
            or isinstance(authorization_header, str) is False
            or not authorization_header.startswith("Basic ")
            and not authorization_header.endswith(" ")
        ):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if(
            base64_authorization_header is None
            or isinstance(base64_authorization_header, str) is False
        ):
            return None
        try:
            base_encode = base64_authorization_header.encode("utf-8")
            base_decode = b64decode(base_encode)
            decoded = base_decode.decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extracting user cridentials
        """
        if (
            decoded_base64_authorization_header is None
            or isinstance(decoded_base64_authorization_header, str) is False
            or ':' not in decoded_base64_authorization_header
             ):
            return (None, None)

        creds = decoded_base64_authorization_header.split(":", 1)
        return (creds[0], creds[1])

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        extracts user object
        """
        if (
            user_email is None or not isinstance(user_email, str)
            or user_pwd is None or not isinstance(user_pwd, str)
             ):
            return None
        try:
            curr_users: List[TypeVar('User')]
            curr_users = User.search({"email": user_email})

        except Exception:
            return None
        for user in curr_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        auth user
        """
        try:
            header = self.authorization_header(request)
            b64_header = self.extract_base64_authorization_header(header)
            dec_head = self.decode_base64_authorization_header(b64_header)
            user_creds = self.extract_user_credentials(dec_head)
            user = self.user_object_from_credentials(user_creds[0],
                                                     user_creds[1])

            return user
        except Exception:
            return None
