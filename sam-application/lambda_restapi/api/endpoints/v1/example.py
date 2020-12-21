"""
This module defines operations for the following /api/v1/example endpoint
"""

from fastapi import APIRouter

from lambda_restapi.models.input import InputExample
from lambda_restapi.models.output import OutputExample

router = APIRouter()


@router.get("/")
def example_get():
    """
    Say hej!

    This will greet you properly

    And this path operation will:
    * return "hej!"
    """
    return {"msg": "Hej!"}


@router.post("/", response_model=OutputExample)
def example_endpoint(inputs: InputExample):
    """
    Multiply two values

    This will multiply two inputs.

    And this path operation will:
    * return a*b
    """
    return {"a": inputs.a, "b": inputs.b, "result": inputs.a * inputs.b}
