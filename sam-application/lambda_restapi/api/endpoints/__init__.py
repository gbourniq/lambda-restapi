from fastapi import APIRouter

from lambda_restapi.api.endpoints.root import router as root_router
from lambda_restapi.api.endpoints.v1 import router as api_router
from lambda_restapi.core.config import API_PREFIX

router = APIRouter()

router.include_router(root_router, prefix="")
router.include_router(api_router, prefix=f"{API_PREFIX}/v1")
