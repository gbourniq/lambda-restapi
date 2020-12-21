"""This module defines common Mixins to be use across Pydantic models"""
import datetime

from pydantic import BaseModel, Field, validator


class DateTimeModelMixin(BaseModel):
    """Mixin to add datetime information to models"""

    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @classmethod
    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
        cls, value: datetime.datetime,  # noqa: N805  # noqa: WPS110
    ) -> datetime.datetime:
        """Returns current datetime if none provided"""
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    """Mixin to add an id field to models"""

    id_: int = Field(0, alias="id")
