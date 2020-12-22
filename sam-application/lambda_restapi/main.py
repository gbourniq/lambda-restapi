"""
This module defines the Lambda handler and uses Mangum as an adapter for
the FastAPI application so it can send and receive information from API Gateway
to Lambda and vice versa.
"""
import time
from typing import Any, Callable, Dict

from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import (
    APIGatewayEventIdentity,
    APIGatewayEventRequestContext,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from lambda_restapi.api.endpoints import router as main_router
from lambda_restapi.api.errors import (
    creation_error_handler,
    http422_error_handler,
    http_error_handler,
)
from lambda_restapi.core.config import (
    ALLOWED_HOSTS,
    API_PREFIX,
    DEBUG,
    DESCRIPTION,
    LOG_FULL_EVENT,
    PROJECT_NAME,
    ROOT_PATH,
    VERSION,
)
from lambda_restapi.core.logging import logger, metrics
from lambda_restapi.helpers.exceptions import MyCustomException


def get_application() -> FastAPI:
    """Returns a FastAPI application"""
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
    # pylint: disable=unused-variable
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
    application.include_router(main_router)

    # Add mount static files for generated assets to be downloadable
    # application.mount(
    #     f"/{ASSETS_PATH.name}",
    #     StaticFiles(directory=f"/{ASSETS_PATH}"),
    #     name="static",
    # )

    return application


app = get_application()


@lambda_handler_decorator
def middleware_before_after(
    handler: Callable, event: Dict[str, Any], context: LambdaContext
) -> Dict[str, Any]:
    """
    Custom middleware to run logic before, and after each Lambda invocation
    synchronously, for eg. to initialise database connections or fail early
    before calling the lambda handler, and for any clean up operations afterwards.
    """
    # Convert the incoming Dict event to a APIGatewayProxyEvent.
    event: APIGatewayProxyEvent = APIGatewayProxyEvent(event)

    # Log request method and path
    logger.info(
        f"{event.http_method} request to {event.path} on "
        f"{event.multi_value_headers.get('Host').pop()}"
    )

    # Get APIGatewayEventRequestContext and APIGatewayEventIdentity objects
    request_context: APIGatewayEventRequestContext = event.request_context
    identity: APIGatewayEventIdentity = request_context.identity

    # Append user to logs (if integration with IAM/Cognito), or source IP
    logger.structure_logs(
        append=True, user=identity.user if identity.user else identity.source_ip,
    )

    # Invoke Lambda
    response = handler(event, context)

    return response


@logger.inject_lambda_context(log_event=LOG_FULL_EVENT)
@metrics.log_metrics(raise_on_empty_metrics=False)
def lambda_handler(
    event: APIGatewayProxyEvent, context: LambdaContext
) -> Dict[str, Any]:
    """Sample Lambda function
    Args:
        event (Dict[str, Any]): API Gateway Lambda Proxy Input Format.
        context (LambdaContext): Lambda Context runtime methods and attributes.
    Returns:
        Dict[str, Any]: JSON response to return to the API Gateway
    """

    asgi_handler = Mangum(app, lifespan="auto", api_gateway_base_path="dev")

    # Call the instance with the event arguments
    response = asgi_handler(event, context)

    return response
