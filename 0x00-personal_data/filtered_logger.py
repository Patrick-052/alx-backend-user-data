#!/usr/bin/env python3
""" Module implementing different functionalities of logging """

import re
import logging
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ Function that returns the log message obfuscated """
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Function that filters values in incoming log records using
        filter_datum. Values for fields in fields should be filtered.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            fields=self.fields,
            redaction=self.REDACTION,
            message=message,
            separator=self.SEPARATOR,
        )

# class RedactingFormatter(logging.Formatter):
#     """ Redacting Formatter class
#         """

#     REDACTION = "***"
#     FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
#     SEPARATOR = ";"

#     def __init__(self, fields: List[str] = None) -> None:
#         """ Constructor method """
#         super(RedactingFormatter, self).__init__(self.FORMAT)
#         self.fields = fields

#     def format(self, record: logging.LogRecord) -> str:
#         """ Function that returns a formatted log message """
#         message = super(RedactingFormatter, self).format(record)
#         return filter_datum(fields=self.fields,
#                             redaction=self.REDACTION,
#                             message=message,
#                             separator=self.SEPARATOR)
