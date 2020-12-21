"""This module contains all endpoints at the root path level /"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def pong():
    """Healthcheck endpoint to ensure the service is operational."""
    return {"ping": "pong!"}
