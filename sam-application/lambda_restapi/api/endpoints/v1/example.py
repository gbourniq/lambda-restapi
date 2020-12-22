"""
This module defines operations for the following /api/v1/example endpoint
"""

from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayEventIdentity,
)
from fastapi import APIRouter
from starlette.requests import Request

from lambda_restapi.models.input import InputExample
from lambda_restapi.models.output import OutputExample

router = APIRouter()


@router.get("/")
def example_get(request: Request):
    """Simple GET request to return hey with source IP"""
    try:
        # get identity details if Lambda triggered by API Gateway Proxy event
        event: APIGatewayProxyEvent = APIGatewayProxyEvent(request.scope["aws.event"])
        identity: APIGatewayEventIdentity = event.request_context.identity
    except KeyError as _:  # no aws.event key in the request score
        return {"msg": "Hello local test client"}
    else:
        return {"msg": f"Hello {identity.source_ip}"}


@router.post("/", response_model=OutputExample)
def example_endpoint(inputs: InputExample):
    """Endpoint to multiply two inputs and return a*b"""
    return {"a": inputs.a, "b": inputs.b, "result": inputs.a * inputs.b}
