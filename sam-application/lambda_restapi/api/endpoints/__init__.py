from fastapi import APIRouter

from .example import router as example_router
from .healthcheck import router as healthcheck_router

router = APIRouter()
router.include_router(example_router)
router.include_router(healthcheck_router)
