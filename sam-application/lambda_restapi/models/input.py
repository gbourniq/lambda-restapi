from pydantic import BaseModel, Field

from lambda_restapi.models.common import DateTimeModelMixin, IDModelMixin


class InputExample(IDModelMixin, DateTimeModelMixin, BaseModel):
    a: int = Field(..., title="Input value a")
    b: int = Field(..., title="Input value b")
