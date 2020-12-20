from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

API_PREFIX = "/api"
VERSION = "1.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
ROOT_PATH: str = config("ROOT_PATH", default="/")
PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*",
)


# Lambda Powertool variables:
# https://awslabs.github.io/aws-lambda-powertools-python/#environment-variables
# Service name used for tracing namespace, metrics dimension and structured logging
POWERTOOLS_SERVICE_NAME: str = config(
    "POWERTOOLS_SERVICE_NAME", default="Mylambdaservice"
)
POWERTOOLS_METRICS_NAMESPACE: str = config(
    "POWERTOOLS_METRICS_NAMESPACE", default="MyLambdaMetricNamespace"
)
BOTOCORE_LEVEL_LOGGING: bool = config(
    "BOTOCORE_LEVEL_LOGGING", cast=bool, default=False
)
LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
LOG_FULL_EVENT: bool = config("LOG_FULL_EVENT", cast=bool, default=False)
