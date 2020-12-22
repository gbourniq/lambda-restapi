"""Main configuration parameters for FastAPI and Lambda powertools"""
from pathlib import Path
from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

# Paths
SAM_APP_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = SAM_APP_DIR / ".env"
print(f"Loading configs from {ENV_PATH}")
config = Config(env_file=ENV_PATH)

# Lambda config (Powertools)
# https://awslabs.github.io/aws-lambda-powertools-python/#environment-variables
LOG_FULL_EVENT: bool = config("LOG_FULL_EVENT", cast=bool)
LOG_LEVEL: str = config("LOG_LEVEL")
POWERTOOLS_METRICS_NAMESPACE: str = config("POWERTOOLS_METRICS_NAMESPACE")
POWERTOOLS_SERVICE_NAME: str = config("POWERTOOLS_SERVICE_NAME")

# FastAPI config
API_PREFIX: str = config("API_PREFIX")
ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
DEBUG: bool = config("DEBUG", cast=bool)
DESCRIPTION: str = config("DESCRIPTION")
PROJECT_NAME: str = config("PROJECT_NAME")
ROOT_PATH: str = config("ROOT_PATH", default="/")  # Set in sam-template.yaml
SECRET_KEY_HEADER: Secret = config("SECRET_KEY_HEADER", cast=Secret)
TEST_SERVER: str = config("TEST_SERVER")
VERSION: str = config("VERSION")

# Static assets
# ASSETS_PATH: str = config("ASSETS_PATH")
# ASSETS_PATH.mkdir(exist_ok=True)
