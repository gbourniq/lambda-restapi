"""This file defines pytest fixtures"""

from typing import Dict, Generator

import pytest
import requests
from fastapi.testclient import TestClient

from lambda_restapi import main
from lambda_restapi.core.config import TEST_SERVER


@pytest.fixture(scope="module")
def mock_client() -> Generator:
    """
    Returns a fastapi test client or the request module
    to test against a running server
    """
    if TEST_SERVER == "http://testserver":
        with TestClient(main.app) as client:
            yield client
    else:
        yield requests


@pytest.fixture(scope="module")
def mock_api_key() -> Dict:
    """Retuns the valid mock x-api-key headers"""
    return {"x-api-key": "secret"}