from fastapi import APIRouter

from .healthcheck import router as healthcheck_router

router = APIRouter()

router.include_router(healthcheck_router, prefix="", include_in_schema=False)
