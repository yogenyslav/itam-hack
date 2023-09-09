from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class UserInternalRole(str, Enum):
    admin = "admin"
    student = "student"


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    email: str = Field(
        ..., min_length=1, max_length=50, example="test-updated@test.com"
    )
    first_name: str = Field(..., min_length=1, max_length=50, example="Михаил")
    last_name: str = Field(..., min_length=1, max_length=50, example="Сурначев")
    internal_role: UserInternalRole = Field(
        ..., min_length=1, max_length=50, example="student"
    )
    level: float = Field(..., ge=0, example=4.7)
