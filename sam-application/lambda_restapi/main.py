"""
This module defines the Lambda handler and uses Mangum as an adapter for
the FastAPI application so it can send and receive information from API Gateway
to Lambda and vice versa.
"""

from fastapi import FastAPI
from mangum import Mangum

from lambda_restapi.api.api_v1.api import router as api_router
from lambda_restapi.constants import API_V1_STR, PROJECT_NAME, ROOT_PATH

app = FastAPI(title=PROJECT_NAME, root_path=ROOT_PATH)

app.include_router(api_router, prefix=API_V1_STR)


@app.get("/ping")
def pong():
    """
    Sanity check.

    This will let the user know that the service is operational.

    And this path operation will:
    * show a lifesign

    """
    return {"ping": "pong!"}


lambda_handler = Mangum(app, enable_lifespan=False)
