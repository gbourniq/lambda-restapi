# """
# This module defines the unit tests for the Lambda function hander
# """
# import json
# from distutils.util import strtobool
# from http import HTTPStatus
# from typing import Any, Dict, List

# import pytest
# from aws_lambda_powertools.utilities.typing import LambdaContext
# from aws_lambda_powertools.utilities.validation import envelopes, validate

# from hello_world import app
# from hello_world.constants import MAX_ORDER_ITEM_ID, MIN_ORDER_ITEM_ID


# def build_mock_event(
#     mock_api_event: Dict[str, Any],
#     multi_values_qstr_params: Dict[str, List[str]] = None,
#     body: Dict[str, Any] = None,
#     headers: Dict[str, Any] = None,
# ) -> Dict[str, Any]:
#     """
#     Build, validate and return a mock API Gateway Proxy event
#     """
#     mock_api_event["multiValueQueryStringParameters"] = multi_values_qstr_params
#     mock_api_event["body"] = json.dumps(body)
#     mock_api_event["headers"] = headers
#     validate(event=mock_api_event, schema={}, envelope=envelopes.API_GATEWAY_REST)
#     return mock_api_event


# def test_lambda_context_is_set(
#     # pylint: disable=no-self-use
#     mock_context: LambdaContext,
# ):
#     """Test Lambda configurations (Lambda context)"""

#     assert mock_context.function_name == "MockFunctionName"
#     assert mock_context.memory_limit_in_mb == "128"
#     assert mock_context.function_version == "$LATEST"
#     assert (
#         mock_context.invoked_function_arn
#         == "arn:aws:lambda:eu-west-2:1686915728:function:test"
#     )
#     assert (
#         mock_context.identity == "<bootstrap.CognitoIdentity object at 0x7f27ad1ec910>"
#     )


# # pylint: disable=not-callable
# @pytest.mark.parametrize(
#     argnames="unsupported_method", argvalues=["PUT", "PATCH", "DELETE", "UPDATE"],
# )
# def test_put_http_not_implemented(
#     mock_base_get_event: Dict[str, Any],
#     mock_context: LambdaContext,
#     unsupported_method: str,
# ):
#     """Test PUT HTTP method not implemented"""
#     # When: some non-implemented HTTP method is passed to the Lambda handler
#     mock_put_event = mock_base_get_event.copy()
#     mock_put_event["httpMethod"] = unsupported_method
#     mock_put_event["requestContext"]["httpMethod"] = unsupported_method
#     response: Dict[str, str] = app.lambda_handler(mock_put_event, mock_context)
#     # Then: 400 status code is returned
#     assert response["statusCode"] == HTTPStatus.BAD_REQUEST.value
#     # Then: Explicit message is returned
#     response_body: Dict = json.loads(response["body"])
#     assert (
#         response_body["message"]
#         == f"HTTP Method {unsupported_method} is not implemented"
#     )


# # pylint: disable=no-self-use
# def test_ping(
#     mock_base_get_event: Dict[str, Any], mock_context: LambdaContext,
# ):
#     """Test GET /api/ping returns pong"""

#     # Given a GET request with invalid values body request params
#     mock_base_get_event["path"] += "/ping"
#     unexpected_api_event = build_mock_event(mock_base_get_event)

#     # When: The event is passed to the Lambda handler
#     response: Dict[str, str] = app.lambda_handler(unexpected_api_event, mock_context)

#     # Then: 200 status code is returned
#     assert response["statusCode"] == HTTPStatus.OK.value
#     # Then: Expected error message is returned
#     response_body: Dict = json.loads(response["body"])
#     assert response_body["message"] == "pong"


# # pylint: disable=not-callable
# @pytest.mark.parametrize(
#     argnames="mock_path",
#     argvalues=["/invalid/path", "/", "/invalid/api/", "/api/nope",],
# )
# # pylint: disable=no-self-use
# def test_invalid_request_path(
#     mock_base_get_event: Dict[str, Any], mock_context: LambdaContext, mock_path: str
# ):
#     """Test any request to a path other than /api/ returns a 400"""

#     # Given a GET request with invalid values body request params
#     mock_base_get_event["path"] = mock_path
#     unexpected_api_event = build_mock_event(mock_base_get_event)

#     # When: The event is passed to the Lambda handler
#     response: Dict[str, str] = app.lambda_handler(unexpected_api_event, mock_context)

#     # Then: 200 status code is returned
#     assert response["statusCode"] == HTTPStatus.BAD_REQUEST.value
#     # Then: Expected error message is returned
#     response_body: Dict = json.loads(response["body"])
#     assert response_body["message"] == f"Oops.. path {mock_path} is not implemented!"


# class TestGet:
#     """Class to test GET events against the Lambda handler"""

#     # pylint: disable=not-callable
#     @pytest.mark.parametrize(
#         argnames="multi_values_qstr_params, headers",
#         argvalues=[
#             ({"debug": ["true"]}, {"x-api-key": "key"}),
#             ({"debug": ["true"]}, None),
#             ({"debug": ["True"]}, None),
#             ({"debug": ["yes"]}, None),
#             ({"debug": ["false"]}, None),
#             ({"debug": ["no"]}, None),
#             ({"debug": ["no"], "unkwn": ["param"]}, None,),
#             (None, None),
#         ],
#     )
#     # pylint: disable=too-many-arguments
#     # pylint: disable=no-self-use
#     def test_valid_request(
#         self,
#         mock_base_get_event: Dict[str, Any],
#         mock_context: LambdaContext,
#         multi_values_qstr_params: Dict[str, List[str]],
#         headers: Dict[str, Any],
#     ):
#         """unit test for valid GET call to lambda handler"""

#         # Given a GET request with valid headers, query strings & body request params
#         expected_api_event = build_mock_event(
#             mock_api_event=mock_base_get_event,
#             multi_values_qstr_params=multi_values_qstr_params,
#             headers=headers,
#         )

#         # When: The event is passed to the Lambda handler
#         response: Dict[str, str] = app.lambda_handler(expected_api_event, mock_context)
#         # Then: 200 status code is returned with expected response
#         assert response["statusCode"] == HTTPStatus.OK.value

#         response_body: Dict = json.loads(response["body"])

#         assert "GET request received" in response_body["message"]
#         if (
#             multi_values_qstr_params
#             and "debug" in multi_values_qstr_params.keys()
#             and bool(strtobool(multi_values_qstr_params["debug"][0]))
#         ):
#             assert response_body["debug"] == "True"
#         else:
#             assert "debug" not in response_body


# class TestPost:
#     """Class to test POST events against the Lambda handler"""

#     # pylint: disable=not-callable
#     @pytest.mark.parametrize(
#         argnames="request_body, headers",
#         argvalues=[
#             ({"id": 42, "name": "mockdata"}, {"x-api-key": "key"}),
#             ({"id": 10, "name": "anothermock"}, None),
#             ({"id": 2, "name": "mockdata"}, None),
#         ],
#     )
#     # pylint: disable=too-many-arguments
#     # pylint: disable=no-self-use
#     def test_valid_request_post(
#         self,
#         mock_base_post_event: Dict[str, Any],
#         mock_context: LambdaContext,
#         request_body: Dict[str, Any],
#         headers: Dict[str, Any],
#     ):
#         """unit test for valid POST request to lambda handler"""

#         # Given a POST request with valid headers, query strings & body request params
#         expected_api_event = build_mock_event(
#             mock_api_event=mock_base_post_event, body=request_body, headers=headers,
#         )

#         # When: The event is passed to the Lambda handler
#         response: Dict[str, str] = app.lambda_handler(expected_api_event, mock_context)

#         # Then: 200 status code is returned
#         assert response["statusCode"] == HTTPStatus.OK.value
#         # Then: Explicit message returned
#         response_body: Dict = json.loads(response["body"])
#         assert response_body["message"] == (
#             "POST request received, processing "
#             f"OrderItem(id={request_body['id']}, name='{request_body['name']}')..."
#         )

#     # pylint: disable=not-callable
#     @pytest.mark.parametrize(
#         argnames="request_body",
#         argvalues=[
#             {"id": 42},
#             {"name": "mockdata"},
#             {"id": 42, "unknown": "mockdata"},
#             {},
#             None,
#             {"unknown": 42, "name": "mockdata"},
#         ],
#     )
#     # pylint: disable=no-self-use
#     def test_fail_body_schema_validation(
#         self,
#         mock_base_post_event: Dict[str, Any],
#         mock_context: LambdaContext,
#         request_body: Dict[str, Any],
#     ):
#         """unit test for invalid POST request due to invalid body payload schema"""

#         # Given a POST request with invalid body request params
#         unexpected_api_event = build_mock_event(mock_base_post_event, body=request_body)

#         # When: The event is passed to the Lambda handler
#         response: Dict[str, str] = app.lambda_handler(
#             unexpected_api_event, mock_context
#         )

#         # Then: 400 status code is returned
#         assert response["statusCode"] == HTTPStatus.BAD_REQUEST.value
#         # Then: Expected error message is returned
#         response_body: Dict = json.loads(response["body"])
#         assert "Error while parsing body request parameters" in response_body["message"]
#         assert "ValidationError(model='OrderItem'" in response_body["exception_details"]
#         assert (
#             "{'loc': ('name',)"
#             or "{'loc': ('id',)" in response_body["exception_details"]
#         )

#     # pylint: disable=not-callable
#     @pytest.mark.parametrize(
#         argnames="request_body",
#         argvalues=[
#             {"id": MAX_ORDER_ITEM_ID + 1, "name": "mockdata"},
#             {"id": MIN_ORDER_ITEM_ID - 1, "name": "mockdata"},
#         ],
#     )
#     # pylint: disable=no-self-use
#     def test_fail_invalid_id(
#         self,
#         mock_base_post_event: Dict[str, Any],
#         mock_context: LambdaContext,
#         request_body: Dict[str, Any],
#     ):
#         """unit test for invalid POST request due to invalid body payload values"""

#         # Given a POST request with invalid values for body request params
#         unexpected_api_event = build_mock_event(mock_base_post_event, body=request_body)

#         # When: The event is passed to the Lambda handler
#         response: Dict[str, str] = app.lambda_handler(
#             unexpected_api_event, mock_context
#         )

#         # Then: 400 status code is returned
#         assert response["statusCode"] == HTTPStatus.BAD_REQUEST.value
#         # Then: Expected error message is returned
#         response_body: Dict = json.loads(response["body"])
#         assert "Error while parsing body request parameters" in response_body["message"]
#         assert (
#             "ValidationError(model='OrderItem'"
#             and "'loc': ('id',)" in response_body["exception_details"]
#         )
#         if request_body["id"] > MAX_ORDER_ITEM_ID:
#             assert (
#                 "ensure this value is less than or equal to 100"
#                 in response_body["exception_details"]
#             )
#         if request_body["id"] < MIN_ORDER_ITEM_ID:
#             assert (
#                 "ensure this value is greater than or equal to 1"
#                 in response_body["exception_details"]
#             )

#     # pylint: disable=not-callable
#     @pytest.mark.parametrize(
#         argnames="request_body", argvalues=[{"id": 42, "name": "no spaces please"},],
#     )
#     # pylint: disable=no-self-use
#     def test_fail_invalid_name(
#         self,
#         mock_base_post_event: Dict[str, Any],
#         mock_context: LambdaContext,
#         request_body: Dict[str, Any],
#     ):
#         """unit test for invalid POST request due to invalid body payload values"""

#         # Given a POST request with invalid values for body request params
#         unexpected_api_event = build_mock_event(mock_base_post_event, body=request_body)

#         # When: The event is passed to the Lambda handler
#         response: Dict[str, str] = app.lambda_handler(
#             unexpected_api_event, mock_context
#         )

#         # Then: 400 status code is returned
#         assert response["statusCode"] == HTTPStatus.BAD_REQUEST.value
#         # Then: Expected error message is returned
#         response_body: Dict = json.loads(response["body"])
#         assert "Error while parsing body request parameters" in response_body["message"]
#         assert (
#             "ValidationError(model='OrderItem'"
#             and "'loc': ('name',)" in response_body["exception_details"]
#         )
#         assert (
#             "'msg': 'string does not match regex" in response_body["exception_details"]
#         )
