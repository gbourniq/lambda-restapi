from starlette.requests import Request
from starlette.responses import JSONResponse

from lambda_restapi.api.errors.exceptions import MyCustomException
from lambda_restapi.helpers.constants import CustomExceptionCodes


async def creation_error_handler(_: Request, exc: MyCustomException,) -> JSONResponse:
    return JSONResponse(
        content={"errors": f"{exc.name}"},
        status_code=CustomExceptionCodes.HTTP_419_CREATION_FAILED.value,
    )
