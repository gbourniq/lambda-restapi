from fastapi import APIRouter, Depends

from .example import router as example_router
from .stuff import router as stuff_router
from lambda_restapi.api.dependencies.common import verify_api_key

router = APIRouter()

router.include_router(example_router, prefix="/example", tags=["Example"])
router.include_router(
    stuff_router,
    prefix="/stuff",
    tags=["Stuff"],
    dependencies=[Depends(verify_api_key)],
)
