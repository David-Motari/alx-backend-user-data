#!/usr/bin/env python3
"""
filtered_logger
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str
                 ) -> str:
    """
    function that returns the log message obfuscated
    Args:
        - separator: a string representing by
        which character is separating all fields in the log line (message)
        - fields: a list of strings representing all fields to obfuscate
        - redaction: string representing by what the field will be obfuscated
        - message: string representing the log line
    """
    for j in fields:
        message = re.sub(f'{j}=.+?{separator}',
                      f'{j}={redaction}{separator}', message)
    return message
