from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class UserRole(str, Enum):
    admin = "admin"
    student = "student"


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    email: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    internal_role: UserRole = Field(..., min_length=1, max_length=50)
