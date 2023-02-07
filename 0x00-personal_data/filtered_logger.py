#!/usr/bin/env python3
"""
filtered_logger
"""
from typing import List, Tuple
import re
import logging
from os import getenv
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filters values in incoming log records using filter_datum
        """
        return filter_datum(self.__fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    takes no arguments and returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    strmHandler = logging.StreamHandler()
    frmtter = RedactingFormatter(PII_FIELDS)
    strmHandler.setFormatter(frmtter)
    logger.addHandler(strmHandler)

    return logger


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
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
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pssword = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    connct = mysql.connector.connection.MySQLConnection(
        host=host,
        username=username,
        password=pssword,
        database=db_name
    )

    return connct


def main():
    """
    takes no arguments and returns nothing.
    """
    db: mysql.connector.connection.MySQLConnection = get_db()
    cursor = db.cursor()
    fields = (field[0] for field in cursor.description)
    cursor.execute("SELECT * FROM users;")
    logger: logging.Logger = get_logger()

    for j in cursor:
        data_row = ''.join(f'{fld}={str(row)}, ' for row, fld in zip(
                           j, fields))
        logger.info(data_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
