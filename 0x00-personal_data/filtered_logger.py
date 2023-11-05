#!/usr/bin/env python3
""" Module implementing different functionalities of logging """

import os
import re
import logging
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
config = {
    'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
    'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
    'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
    'database': os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')
}


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


def get_logger() -> logging.Logger:
    """
    Function that returns a logger object set to the INFO level
    which contains an attached StreamHandler object and a
    formatter object(RedactingFormatter)
    """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Function that returns a connector to the database """
    try:
        conn = mysql.connector.connect(**config)
    except Exception as e:
        print(f"error connecting to database {config['host']}: {e}")
    else:
        print("connection established")
        return conn


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None):
        """ Constructor method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Function that returns a formatted log message """
        return filter_datum(self.fields,
                            self.REDACTION,
                            super().format(record),
                            self.SEPARATOR)


def main():
    """ Main function """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM users;")
    db_log = get_logger()
    for row in cur:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " + \
            f"ssn={row[3]}; password={row[4]}; ip={row[5]}; " + \
            f"last_login={row[6]}; user_agent={row[7]};"
        db_log.info(message)
    cur.close()
    db.close()


if __name__ == "__main__":
    main()
