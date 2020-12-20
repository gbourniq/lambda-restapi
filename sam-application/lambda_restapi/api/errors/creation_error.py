from starlette.requests import Request
from starlette.responses import JSONResponse

from lambda_restapi.api.errors.exceptions import MyCustomException
from lambda_restapi.core.constants import CustomExceptionCodes


async def creation_error_handler(_: Request, exc: MyCustomException,) -> JSONResponse:
    return JSONResponse(
        content={"errors": f"CustomException: {exc.errors()}"},
        status_code=CustomExceptionCodes.HTTP_419_CREATION_FAILED,
    )
