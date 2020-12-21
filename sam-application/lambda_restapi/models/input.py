"""This module defines pydantic models for incoming HTTP body requests"""
from pydantic import BaseModel, Field

from lambda_restapi.helpers.constants import MAX_ORDER_ITEM_ID, MIN_ORDER_ITEM_ID
from lambda_restapi.models.common import DateTimeModelMixin, IDModelMixin


class InputExample(IDModelMixin, DateTimeModelMixin, BaseModel):
    """Dummy input"""

    a: int = Field(..., title="Input value a")  # pylint: disable=invalid-name
    b: int = Field(..., title="Input value b")  # pylint: disable=invalid-name


class OrderItem(BaseModel):
    """Expected data sent via the body request parameters"""

    id: int = Field(
        ...,
        description="Item ID",
        ge=MIN_ORDER_ITEM_ID,
        le=MAX_ORDER_ITEM_ID,
        example=42,
    )
    name: str = Field(
        ...,
        description="Item name (no whitespace)",
        max_length=30,
        example="item_name",
        regex=r"^\S+$",
    )


# class UserModel(BaseModel):
#     """Mock UserModel class to demonstrate validator and root_validator"""

#     username: str
#     password1: str
#     password2: str

#     @classmethod
#     @validator("username")
#     def is_admin(cls, username: str):
#         """Validate the username is admin"""
#         if username != "admin":
#             # must raise ValueError, TypeError, or AssertionError when not compliant
#             raise ValueError("Username must be admin!")
#         return username

#     @classmethod
#     @root_validator
#     def check_passwords_match(cls, values):
#         """Validates provided password1 and password2 are the same"""
#         pw1, pw2 = values.get("password1"), values.get("password2")
#         if pw1 is not None and pw2 is not None and pw1 != pw2:
#             raise ValueError("passwords do not match")
#         return values
