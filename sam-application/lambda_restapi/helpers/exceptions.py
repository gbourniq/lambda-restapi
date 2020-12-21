"""This module defines custom exceptions"""


class MyCustomException(Exception):
    """MyCustomException to be raised when..."""

    # pylint: disable=super-init-not-called
    def __init__(self, name: str):
        self.name = name
