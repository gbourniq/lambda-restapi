from http import HTTPStatus

from fastapi.testclient import TestClient

ENDPOINT_API_PREFIX = ""


def test_healhcheck_endpoint(mock_client: TestClient):
    """Asserts ping endpoint returns pong"""

    response = mock_client.get(f"{ENDPOINT_API_PREFIX}/ping")

    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"ping": "pong!"}
