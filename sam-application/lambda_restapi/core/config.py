from os import getenv
from pathlib import Path
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

API_PREFIX = "/api"
VERSION = "1.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY_HEADER: Secret = config(
    "SECRET_KEY_HEADER", cast=Secret, default="qwefj23r982ufluhf293"
)
# ROOT_PATH must match the API GTW deployment stage if FastAPI server running on Lambda
ROOT_PATH: str = config("ROOT_PATH", default="/")
PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
DESCRIPTION: str = config("DESCRIPTION", default="RESTful APIs to create <...>")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)

# Remove for production
DEFAULT_KEY_HEADER: str = str(SECRET_KEY_HEADER)

# Static assets
if getenv("ASSETS_PATH"):
    ASSETS_PATH = Path(getenv("ASSETS_PATH"))
else:
    ASSETS_PATH = Path(__file__).resolve().parent / "assets"
ASSETS_PATH.mkdir(exist_ok=True)

# Lambda Powertool variables:
# https://awslabs.github.io/aws-lambda-powertools-python/#environment-variables
# Service name used for tracing namespace, metrics dimension and structured logging
POWERTOOLS_SERVICE_NAME: str = config(
    "POWERTOOLS_SERVICE_NAME", default="Mylambdaservice"
)
POWERTOOLS_METRICS_NAMESPACE: str = config(
    "POWERTOOLS_METRICS_NAMESPACE", default="MyLambdaMetricNamespace"
)
LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
LOG_FULL_EVENT: bool = config("LOG_FULL_EVENT", cast=bool, default=False)
