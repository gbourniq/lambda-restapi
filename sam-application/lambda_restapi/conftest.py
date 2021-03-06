"""This file defines pytest fixtures"""

from typing import Generator

import pytest
import requests
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from lambda_restapi.core.config import TEST_SERVER
from lambda_restapi.main import get_application


@pytest.fixture(scope="module")
def mock_client() -> Generator:
    """
    Returns a fastapi test client or the request module
    to test against a running server
    """
    if TEST_SERVER == "http://testserver":
        app = get_application()
        with TestClient(app) as client:
            yield client
    else:
        yield requests


@pytest.fixture(scope="module")
def mock_secret_key() -> Headers:
    """Retuns the valid mock x-secret-key headers"""
    return Headers({"x-secret-key": "secret"})
