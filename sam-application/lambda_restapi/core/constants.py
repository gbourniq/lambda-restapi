"""
This module defines all constants used across the code base, including
variables names used to retrieve data from the SSM Parameter store
"""

from enum import Enum

MAX_ORDER_ITEM_ID = 100  # For Pydantic validation
MIN_ORDER_ITEM_ID = 1  # For Pydantic validation


class MetricsData(Enum):
    """
    Config for custom metrics pushed by the Lambda function
    """

    DIMENSION_NAME = "category"
    DIMENSION_VALUE = "all"
    NAME = "CurrentBucketCount"


class SSMParametersKeys(Enum):
    """
    Name for SSM Parameters to retrieve the value from
    """

    AMZ_LINUX2_LATEST = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"


class ImplementedHttpMethods(Enum):
    """Enum for the implemented HTTP methods"""

    GET = "GET"
    POST = "POST"


class CustomExceptionCodes(Enum):
    HTTP_419_CREATION_FAILED = 419
