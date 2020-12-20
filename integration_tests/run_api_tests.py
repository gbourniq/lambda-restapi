"""
Test basic GET and POST requests against a local or real API Gateway endpoint.
This ensures public AWS API Gateway endpoints are secured, and pointing to the latest
Lambda application code.
More extensive test cases are defined in unit-tests in sam-application/
"""

import inspect
import time
from argparse import ArgumentParser
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict

import requests


@dataclass
class RunTests:
    """
    class containing all tests to be run
    """

    endpoint: str
    api_key: str = "mock_api_key"

    def __post_init__(self):
        self.endpoint = self.endpoint.strip("/")

    def test_0_api_gtw_endpoint_is_secured(self):
        """Ensure API Key is required for non-localhost endpoints"""

        # Given: valid GET request data
        url = f"{self.endpoint}/ping"
        headers = {"x-api-key": None, "content-type": "application/json"}

        # When: GET request
        response = requests.get(url, headers=headers)

        # Then: Ensure API Key is required for non-localhost endpoints
        if all(val not in self.endpoint for val in ["localhost", "127.0.0.1"]):
            print("⛅️ Running on API Gateway")
            assert (
                response.status_code == HTTPStatus.FORBIDDEN.value
            ), f"{self.endpoint} returned {response} without providing an API Key👎"
        else:
            print("💻 API server running locally - API Key not required")
            assert (
                response.status_code == HTTPStatus.OK.value
            ), f"Got {response.__dict__}"

    def test_valid_get_debug_true(self):
        """Test a successful GET request API call"""

        # Given: valid GET request data
        url = f"{self.endpoint}/"
        qstr_params = {"debug": "true"}
        headers = {"x-api-key": self.api_key, "content-type": "application/json"}

        # When: GET request
        response = requests.get(url, params=qstr_params, headers=headers)

        # Then: 200 returned with expected JSON response
        assert (
            response.status_code == HTTPStatus.OK.value
        ), f"Returned {response.__dict__}"
        assert "GET request received" in response.json()["message"]
        assert response.json()["debug"] == "True"

    def test_valid_get(self):
        """Test a successful GET request API call"""

        # Given: valid GET request data
        url = f"{self.endpoint}/"
        qstr_params = None
        headers = {"x-api-key": self.api_key}

        # When: GET request
        response = requests.get(url, params=qstr_params, headers=headers)

        # Then: 200 returned with expected JSON responses
        assert (
            response.status_code == HTTPStatus.OK.value
        ), f"Returned {response.__dict__}"
        assert "GET request received" in response.json()["message"]

    def test_post_invalid_body_schema(self):
        """Test a malformed GET request API call returns 400"""

        # Given: malformed POST request data with invalid body
        url = f"{self.endpoint}/"
        qstr_params = None
        body = {"name": "missing_id"}
        headers = {"x-api-key": self.api_key, "content-type": "application/json"}

        # When: POST request
        response = requests.post(url, params=qstr_params, json=body, headers=headers)

        # Then: 400 returned
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST.value
        ), f"Returned {response.__dict__}"
        # Then: With an explicit error message
        response_body: Dict = response.json()
        assert response_body["message"] == "Error while parsing body request parameters"
        assert "ValidationError(model='OrderItem'" in response_body["exception_details"]
        assert "{'loc': ('id',)" in response_body["exception_details"]

    def test_valid_post(self):
        """Test a successful POST request API call"""

        # Given: valid POST request data
        url = f"{self.endpoint}/"
        qstr_params = None
        body = {"id": 4, "name": "event_mock_post_data"}
        headers = {"x-api-key": self.api_key, "content-type": "application/json"}

        # When: POST request
        response = requests.post(url, params=qstr_params, json=body, headers=headers)

        # Then: 200 returned with expected JSON responses
        assert response.status_code == HTTPStatus.OK.value


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--server",
        "-s",
        default="http://127.0.0.1:3000",
        help="Endpoint to run tests against",
    )
    parser.add_argument(
        "--api-key", "-k", default=None, help="API Key to access secure Endpoint",
    )
    args = parser.parse_args()

    print(f"Running tests against {args.server}")
    if args.api_key:
        print("🔑 API Key provided")

    run_tests = RunTests(endpoint=args.server, api_key=args.api_key)
    for name, func in inspect.getmembers(run_tests, predicate=inspect.ismethod):
        if not name.startswith("_") and callable(func):
            print(f"\n⏳ Running {func.__name__}")
            time.sleep(2)  # To prevent throttling
            func()
            print(f"✅ {func.__name__}")
