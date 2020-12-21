"""
This module defines common dependencies such as common query parameters
"""

from enum import Enum
from typing import NoReturn, Optional

from fastapi import Header
from pydantic import BaseModel, Field

from lambda_restapi.core.config import SECRET_KEY_HEADER
from lambda_restapi.helpers.exceptions import MyCustomException


class ModelName(str, Enum):
    """
    Enum which set a number of model names which
    can be seleted as query/path parameters
    """

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class CommonQueryParams(BaseModel):
    """Callable dependency that expects 2 query parameters
    Args:
        debug (bool, optional). Defaults to False.
        model_name (str). Defaults to "resnet".
    Returns:
        (dict). dict containing those values
    """

    debug: Optional[bool] = Field(title="Debug mode", default=False)
    model_name: ModelName = Field(title="Model name", default=ModelName.resnet.value)


async def verify_api_key(x_api_key: str = Header(...),) -> NoReturn:
    """Depencies to check if provided x-api-key is valid."""
    if x_api_key != str(SECRET_KEY_HEADER):
        raise MyCustomException(name="x-api-key header invalid")
    return x_api_key
