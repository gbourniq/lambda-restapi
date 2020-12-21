"""This module defines tests for the api/v1/example endpoint"""
from http import HTTPStatus

from fastapi.testclient import TestClient

from lambda_restapi.core.config import TEST_SERVER

if TEST_SERVER == "http://testserver":
    EXAMPLE_API_PREFIX = "api/v1/example/"
else:
    EXAMPLE_API_PREFIX = f"{TEST_SERVER}/api/v1/example"


def test_get_example(mock_client: TestClient):
    """Asserts ping endpoint returns pong"""

    response = mock_client.get(f"{EXAMPLE_API_PREFIX}/")

    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"msg": "Hey!"}


def test_post_example(mock_client: TestClient):
    """Asserts ping endpoint returns pong"""

    response = mock_client.post(f"{EXAMPLE_API_PREFIX}/", json={"a": 2, "b": 4})

    assert response.status_code == HTTPStatus.OK.value
    assert response.json()["result"] == 8
