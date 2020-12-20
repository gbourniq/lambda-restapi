import os

from starlette.datastructures import CommaSeparatedStrings

ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))
API_V1_STR = "/api/v1"
PROJECT_NAME = "FastAPI-AWS-Lambda-Example-API"
