#!/usr/bin/env python3
"""
filtered_logger
"""
from re import sub


def filter_datum(fields, redaction, message, separator):
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
        message = sub(j + '=.*?' + separator,
                      j + '=' + redaction + separator,
                      message)
    return message
