"""
This module defines the fastapi handler function for MyCustomException errors
"""

from starlette.requests import Request
from starlette.responses import JSONResponse

from lambda_restapi.helpers.constants import CustomExceptionCodes
from lambda_restapi.helpers.exceptions import MyCustomException


async def creation_error_handler(_: Request, exc: MyCustomException,) -> JSONResponse:
    """Fastapi handler function for MyCustomException errors"""
    return JSONResponse(
        content={"errors": f"{exc.name}"},
        status_code=CustomExceptionCodes.HTTP_419_CREATION_FAILED.value,
    )
