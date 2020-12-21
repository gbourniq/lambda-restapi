from typing import List

from pydantic import BaseModel, Field

from lambda_restapi.models.common import DateTimeModelMixin, IDModelMixin


class OutputExample(IDModelMixin, DateTimeModelMixin, BaseModel):
    a: int = Field(..., title="Input value a")
    b: int = Field(..., title="Input value b")
    result: int = Field(..., title="Result of a * b")


class BucketNames(IDModelMixin, DateTimeModelMixin, BaseModel):
    buckets: List[str] = Field(..., title="List of current buckets")
    debug: bool = Field(..., title="Debug mode")
    model_name: str = Field(..., title="Model name")
