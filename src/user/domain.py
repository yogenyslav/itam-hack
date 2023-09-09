from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class UserInternalRole(str, Enum):
    admin = "admin"
    student = "student"


class SkillDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_name: str = Field(..., min_length=1, max_length=80, example="Python")


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    email: str = Field(
        ..., min_length=1, max_length=50, example="test-updated@test.com"
    )
    first_name: str = Field(..., min_length=1, max_length=50, example="Михаил")
    last_name: str = Field(..., min_length=1, max_length=50, example="Сурначев")
    internal_role: Optional[UserInternalRole] = Field(
        ..., min_length=1, max_length=50, example="student"
    )
    level: float = Field(..., ge=0, example=4.7)
    tg_username: Optional[str] = Field(
        None, min_length=1, max_length=60, example="mihail_surnachev"
    )
    skills: Optional[list[SkillDto]] = Field(
        None, example=[{"id": 1, "skill_name": "Linear Algebra"}]
    )


class RoleCreate(BaseModel):
    role_name: str = Field(
        ..., min_length=1, max_length=80, example="Backend developer"
    )


class RoleDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    role_name: str = Field(
        ..., min_length=1, max_length=80, example="Backend developer"
    )
