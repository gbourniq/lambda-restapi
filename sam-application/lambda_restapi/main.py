"""
This module defines the Lambda handler and uses Mangum as an adapter for
the FastAPI application so it can send and receive information from API Gateway
to Lambda and vice versa.
"""
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from lambda_restapi.api.endpoints.root import router as root_router
from lambda_restapi.api.endpoints.v1 import router as api_router
from lambda_restapi.api.errors import (
    creation_error_handler,
    http422_error_handler,
    http_error_handler,
)
from lambda_restapi.api.errors.exceptions import MyCustomException
from lambda_restapi.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    ASSETS_PATH,
    DEBUG,
    DESCRIPTION,
    PROJECT_NAME,
    ROOT_PATH,
    VERSION,
)


def get_application() -> FastAPI:

    # Initialise FastAPI app
    application = FastAPI(
        title=PROJECT_NAME,
        description=DESCRIPTION,
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
        debug=DEBUG,
        version=VERSION,
        root_path=ROOT_PATH,
    )

    # Allowed hosts
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom middleware
    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """Add the `x-process-time` response header to every requests."""
        start_time = time.time()
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(time.time() - start_time)
        return response

    # Exception handlers
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(MyCustomException, creation_error_handler)

    # Routes
    application.include_router(root_router, prefix="")
    application.include_router(api_router, prefix=API_PREFIX)

    # Add mount static files for generated assets to be downloadable
    application.mount(
        f"/{ASSETS_PATH.name}", StaticFiles(directory=f"/{ASSETS_PATH}"), name="static",
    )

    return application


app = get_application()
lambda_handler = Mangum(app, enable_lifespan=False)
