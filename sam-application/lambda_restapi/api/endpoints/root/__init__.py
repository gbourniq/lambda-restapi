"""This module defines the main router among all ROOT endpoints"""
from fastapi import APIRouter

from .healthcheck import router as healthcheck_router

router = APIRouter()

router.include_router(healthcheck_router, include_in_schema=False)
