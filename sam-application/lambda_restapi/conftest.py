"""This file defines pytest fixtures"""

from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from lambda_restapi import main


@pytest.fixture(scope="module")
def mock_client() -> Generator:
    """Returns a fastapi test client"""
    with TestClient(main.app) as client:
        yield client


@pytest.fixture(scope="module")
def mock_api_key() -> Dict:
    """Retuns the valid mock x-api-key headers"""
    return {"x-api-key": "secret"}
