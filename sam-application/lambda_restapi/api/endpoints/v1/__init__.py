"""This module defines the main router among all api/v1 endpoints"""

from fastapi import APIRouter, Depends

from lambda_restapi.api.endpoints.v1.example import router as example_router
from lambda_restapi.api.endpoints.v1.stuff import router as stuff_router
from lambda_restapi.api.dependencies.common import verify_secret_key

router = APIRouter()

router.include_router(example_router, prefix="/example", tags=["Example"])
router.include_router(
    stuff_router,
    prefix="/stuff",
    tags=["Stuff"],
    dependencies=[Depends(verify_secret_key)],
)
