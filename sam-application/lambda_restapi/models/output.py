"""This module defines pydantic models for HTTP body responses"""

from typing import List

from pydantic import BaseModel, Field

from lambda_restapi.models.common import DateTimeModelMixin, IDModelMixin


class OutputExample(IDModelMixin, DateTimeModelMixin, BaseModel):
    """Dummy output schema"""

    a: int = Field(..., title="Input value a")  # pylint: disable=invalid-name
    b: int = Field(..., title="Input value b")  # pylint: disable=invalid-name
    result: int = Field(..., title="Result of a * b")


class BucketNames(IDModelMixin, DateTimeModelMixin, BaseModel):
    """Dummy output schema"""

    buckets: List[str] = Field(..., title="List of current buckets")
    debug: bool = Field(..., title="Debug mode")
    model_name: str = Field(..., title="Model name")
