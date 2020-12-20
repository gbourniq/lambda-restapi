"""
This module defines all constants used across the code base, including
variables names used to retrieve data from the SSM Parameter store
"""

from distutils.util import strtobool
from enum import Enum
from os import getenv
from starlette.datastructures import CommaSeparatedStrings


MAX_ORDER_ITEM_ID = 100  # For Pydantic validation
MIN_ORDER_ITEM_ID = 1  # For Pydantic validation


ALLOWED_HOSTS = CommaSeparatedStrings(getenv("ALLOWED_HOSTS", ""))
API_V1_STR = "/api/v1"
PROJECT_NAME = "FastAPI-AWS-Lambda-Example-API"

class PowertoolsVariables(Enum):
    """
    https://awslabs.github.io/aws-lambda-powertools-python/#environment-variables
    Defines variables:
    - service name used for tracing namespace, metrics dimension and structured logging
    - Custom metrics namespace name
    """

    POWERTOOLS_SERVICE_NAME = getenv("POWERTOOLS_SERVICE_NAME", "Mylambdaservice")
    POWERTOOLS_METRICS_NAMESPACE = getenv(
        "POWERTOOLS_METRICS_NAMESPACE", "MyLambdaMetricNamespace"
    )
    LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
    BOTOCORE_LEVEL_LOGGING = bool(strtobool(getenv("BOTOCORE_LEVEL_LOGGING", "false")))
    LOG_FULL_EVENT = bool(strtobool(getenv("LOG_FULL_EVENT", "false")))


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
