from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", include_in_schema=False)
def pong():
    """
    Sanity check.

    This will let the user know that the service is operational.

    And this path operation will:
    * show a lifesign

    """
    return {"ping": "pong!"}
