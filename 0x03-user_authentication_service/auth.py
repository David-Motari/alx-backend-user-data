#!/usr/bin/env python3
"""
auth
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    hashing a given password
    """
    encd_pwd = password.encode("utf=8")
    return hashpw(encd_pwd, gensalt())
