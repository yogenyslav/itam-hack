from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from src.tags.domain import (
    RoleDto,
    SkillDto,
    TeamGoalDto,
)


class UserInternalRole(str, Enum):
    admin = "admin"
    student = "student"


class SurveyCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    roles: list[RoleDto] = Field(
        ...,
        examples=[
            {"role_name": "Backend developer"},
            {"role_name": "Frontend developer"},
        ],
    )
    goals: list[TeamGoalDto] = Field(
        ...,
        examples=[
            {"goal_name": "Научиться новому"},
            {"goal_name": "Пополнить портфолио"},
        ],
    )
    tg_username: str = Field(
        ..., min_length=1, max_length=60, examples=["lasuria_hilbert"]
    )


class UserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    email: str = Field(
        ..., min_length=1, max_length=50, examples=["test-updated@test.com"]
    )
    first_name: str = Field(..., min_length=1, max_length=50, examples=["Михаил"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Сурначев"])
    internal_role: Optional[UserInternalRole] = Field(
        None, min_length=1, max_length=50, examples=["student"]
    )
    level: float = Field(..., ge=0, examples=[4.7])
    tg_username: Optional[str] = Field(
        None, min_length=1, max_length=60, examples=["mihail_surnachev"]
    )
    graduation_year: Optional[date] = Field(None, examples=[date(2023, 1, 1)])
    image_url: Optional[str] = Field(
        None, examples=["https://localhost:9999/static/test.png"]
    )
    skills: Optional[list[SkillDto]] = Field(
        None, examples=[{"id": 1, "skill_name": "Linear Algebra"}]
    )
    roles: Optional[list[RoleDto]] = Field(
        None,
        examples=[
            {"id": 1, "role_name": "Backend developer"},
            {"id": 2, "role_name": "Frontend developer"},
        ],
    )
    goals: Optional[list[TeamGoalDto]] = Field(
        None,
        examples=[
            {"id": 1, "goal_name": "Научиться новому"},
            {"id": 2, "goal_name": "Пополнить портфолио"},
        ],
    )
