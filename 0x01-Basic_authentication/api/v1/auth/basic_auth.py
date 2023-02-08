#!/usr/bin/env python3
"""
basic_auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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

        creds = decoded_base64_authorization_header.split(":")
        return (creds[0], creds[1])
