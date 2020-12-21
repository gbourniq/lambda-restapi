from http import HTTPStatus

from fastapi.testclient import TestClient

EXAMPLE_API_PREFIX = "/api/v1/example"


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
