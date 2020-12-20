"""This module defines custom exceptions"""


class LambdaApplicationException(Exception):
    """
    Parent exception for the Lambda application
    """


class CustomException(LambdaApplicationException):
    """
    Exception to be raised when ...
    """
