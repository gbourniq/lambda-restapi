"""This module defines unit tests for the stuff endpoint"""

from http import HTTPStatus
from typing import Dict

import pytest
from aws_lambda_powertools.utilities.parser import parse
from fastapi.testclient import TestClient

from lambda_restapi.core.config import TEST_SERVER
from lambda_restapi.helpers.constants import CustomExceptionCodes
from lambda_restapi.models.input import OrderItem
from lambda_restapi.models.output import BucketNames

if TEST_SERVER == "http://testserver":
    STUFF_API_PREFIX = "api/v1/stuff/"
else:
    STUFF_API_PREFIX = f"{TEST_SERVER}/api/v1/stuff"

# pylint: disable=not-callable
@pytest.mark.parametrize(
    argnames="debug, id_, model_name",
    argvalues=[
        (True, 3, "resnet"),
        (False, 3, "alexnet"),
        (True, 53, "lenet"),
        (False, 42, "resnet"),
    ],
)
def test_get_stuff(
    mock_client: TestClient, mock_api_key: Dict, debug: bool, id_: int, model_name: str
):
    """Asserts get stuff endpoint works with expected parameters"""

    # Given: A url with path parameters and query parameters
    url = f"{STUFF_API_PREFIX}/{id_}?debug={debug}&model_name={model_name}"

    # When: calling the get method
    response = mock_client.get(url, headers=mock_api_key)

    # Then: Returned status code is 200
    assert response.status_code == HTTPStatus.OK.value
    # Then: Returned response is of the expected Pydantic model
    assert parse(event=response.json(), model=BucketNames)
    # Then: Returned values are what we expected
    assert response.json()["debug"] == debug
    assert response.json()["model_name"] == model_name


def test_get_42_with_debug_true_raises_error(
    mock_client: TestClient, mock_api_key: Dict
):
    """Asserts get stuff endpoint works with expected parameters"""

    # Given: A url with path parameters and query parameters
    url = f"{STUFF_API_PREFIX}/42?debug=true&model_name=resnet"

    # When: calling the get method
    response = mock_client.get(url, headers=mock_api_key)

    # Then: Returned status code is 419
    assert response.status_code == CustomExceptionCodes.HTTP_419_CREATION_FAILED.value
    # Then: Returned response is of the expected Pydantic model
    assert response.json() == {"errors": "oops.. id 42 does not work with Debug mode"}


def test_post_stuff(mock_client: TestClient, mock_api_key: Dict):
    """Asserts post stuff endpoint works with expected parameters"""

    # Given: A url with no path parameters / query parameters
    url = f"{STUFF_API_PREFIX}/"

    # Given: Valid body request parameters
    json = {"id": 42, "name": "mock_item_name"}

    # When: calling the post method
    response = mock_client.post(url, json=json, headers=mock_api_key)

    # Then: Returned status code is 201
    assert response.status_code == HTTPStatus.CREATED.value
    # Then: Returned response is of the expected Pydantic model
    assert parse(event=response.json(), model=OrderItem)
    # Then: Returned values are what we expected
    assert response.json() == {"id": 42, "name": "mock_item_name"}


def test_invalid_api_key(mock_client: TestClient):
    """Asserts post stuff endpoint works with expected parameters"""

    # Given: A url with no path parameters / query parameters
    url = f"{STUFF_API_PREFIX}/"
    # Given: Valid body request parameters
    json = {"id": 42, "name": "mock_item_name"}
    # Given: Invalid headers with missing or invalid api key
    headers = {"x-api-key": "nope"}

    # When: calling the post method
    response = mock_client.post(url, json=json, headers=headers)

    # Then: Returned custom status code 419
    assert response.status_code == CustomExceptionCodes.HTTP_419_CREATION_FAILED.value
    # Then: Returned values are what we expected
    assert response.json() == {"errors": "x-api-key header invalid"}
