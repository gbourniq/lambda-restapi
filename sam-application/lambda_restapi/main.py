"""
This module defines the Lambda handler and uses Mangum as an adapter for
the FastAPI application so it can send and receive information from API Gateway
to Lambda and vice versa.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from lambda_restapi.api.endpoints import router as api_router
from lambda_restapi.api.errors import http422_error_handler, http_error_handler
from lambda_restapi.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    DEBUG,
    PROJECT_NAME,
    ROOT_PATH,
    VERSION,
)


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, root_path=ROOT_PATH)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

    app.include_router(api_router, prefix=API_PREFIX)


lambda_handler = Mangum(get_application(), enable_lifespan=False)
