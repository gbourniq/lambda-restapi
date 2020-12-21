"""This module defines unit tests for the healthcheck endpoint"""
from http import HTTPStatus

from fastapi.testclient import TestClient

from lambda_restapi.core.config import TEST_SERVER

if TEST_SERVER == "http://testserver":
    ROOT_PREFIX = ""
else:
    ROOT_PREFIX = f"{TEST_SERVER}/"


def test_healhcheck_endpoint(mock_client: TestClient):
    """Asserts ping endpoint returns pong"""

    response = mock_client.get(f"{ROOT_PREFIX}/ping")

    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"ping": "pong!"}
