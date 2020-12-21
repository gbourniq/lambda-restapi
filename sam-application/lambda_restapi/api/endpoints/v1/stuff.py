"""
This module defines operations for the following /api/v1/stuff endpoint
"""

from typing import List

from aws_lambda_powertools.metrics import MetricUnit
from fastapi import APIRouter, Body, Depends, File, Form, Path, UploadFile, status
from starlette.exceptions import HTTPException

from lambda_restapi.api.dependencies.common import CommonQueryParams
from lambda_restapi.core.logging import logger, metrics
from lambda_restapi.helpers import strings
from lambda_restapi.helpers.aws_services import get_s3_client, get_ssm_parameter
from lambda_restapi.helpers.constants import (
    CustomExceptionCodes,
    MetricsData,
    SSMParametersKeys,
)
from lambda_restapi.models.input import OrderItem
from lambda_restapi.models.output import BucketNames

router = APIRouter()


@router.get("/{item_id}", response_model=BucketNames)
def get_stuff(
    config: CommonQueryParams = Depends(CommonQueryParams),
    item_id: int = Path(..., title="Item ID", le=200, example=3),
) -> List[str]:
    """
    This endpoint post an fake item order to...

    - **item_id** (int): Item ID - path paramater
    - **debug** (bool): debug - query string parameter
    """

    if item_id == 42 and config.debug:
        raise HTTPException(
            status_code=CustomExceptionCodes.HTTP_419_CREATION_FAILED.value,
            detail=strings.DUMMY_ERROR_MESSAGE,
        )

    s3_client = get_s3_client()

    # Log provided ID
    logger.info(f"Given id: {item_id}")

    # Get SSM variable when in debug mode
    amzlinux2_latest_ami = get_ssm_parameter(SSMParametersKeys.AMZ_LINUX2_LATEST.value)
    logger.info(f"Variable from SSM: {amzlinux2_latest_ami}")

    # Use S3 client to log current bucket names
    response = s3_client.list_buckets()
    if current_buckets := response.get("Buckets", []):
        current_buckets = [b.get("Name") for b in current_buckets]
    logger.info(f"Current buckets: {current_buckets}")

    if config.debug:
        # Use Custom Metrics to log the number of current buckets
        metrics.add_dimension(
            name=MetricsData.DIMENSION_NAME.value,
            value=MetricsData.DIMENSION_VALUE.value,
        )
        metrics.add_metric(
            name=MetricsData.NAME.value,
            unit=MetricUnit.Count,
            value=len(current_buckets),
        )

    return {
        "buckets": current_buckets,
        "debug": config.debug,
        "model_name": config.model_name,
    }


@router.post("/", response_model=OrderItem, status_code=status.HTTP_201_CREATED)
def post_stuff(order_item: OrderItem = Body(...)):
    """
    This endpoint post an fake item order to...

    - **order_item** (OrderItem): Order object to post
    """
    # Process order_item and return value
    return order_item


@router.post("/upload-files-and-form-data/", status_code=status.HTTP_202_ACCEPTED)
async def upload_files_and_form_data(
    file_A: bytes = File(...), file_B: UploadFile = File(...), token: str = Form(...),
):
    return {
        "file_size": len(file_A),
        "token": token,
        "fileb_content_type": file_B.content_type,
    }
