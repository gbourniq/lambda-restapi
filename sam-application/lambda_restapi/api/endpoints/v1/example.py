"""
This module defines operations for the following /api/v1/example endpoint
"""

from fastapi import APIRouter

from lambda_restapi.models.input import InputExample
from lambda_restapi.models.output import OutputExample

router = APIRouter()


@router.get("/")
def example_get():
    """Simple GET request to return hey!"""
    return {"msg": "Hey!"}


@router.post("/", response_model=OutputExample)
def example_endpoint(inputs: InputExample):
    """Endpoint to multiply two inputs and return a*b"""
    return {"a": inputs.a, "b": inputs.b, "result": inputs.a * inputs.b}
