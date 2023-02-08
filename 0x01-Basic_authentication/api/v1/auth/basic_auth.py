#!/usr/bin/env python3
"""
basic_auth
"""
from api.v1.auth.auth import Auth


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
