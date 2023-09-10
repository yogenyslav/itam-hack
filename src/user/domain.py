from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from src.tags.domain import (
    SkillCreate,
    RoleCreate,
    TeamGoalCreate,
    RoleDto,
    SkillDto,
    TeamGoalDto,
)


class UserInternalRole(str, Enum):
    admin = "admin"
    student = "student"


# class UserTeamRole(str, Enum):
#     graphic_designer = "graphic_designer"
#     product_designer = "product_designer"
#     project_manager = "project_manager"
#     backend = "backend_developer"
#     frontend = "frontend_developer"
#     mobile = "mobile_developer"
#     ml = "ml"
#     business_analyst = "business_analyst"
#     fullstack = "fullstack"


class SurveyCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    roles: list[RoleCreate] = Field(
        ...,
        example=[
            {"role_name": "Backend developer"},
            {"role_name": "Frontend developer"},
        ],
    )
    goals: list[TeamGoalCreate] = Field(
        ...,
        example=[
            {"goal_name": "Научиться новому"},
            {"goal_name": "Пополнить портфолио"},
        ],
    )
    tg_username: str = Field(
        ..., min_length=1, max_length=60, example="lasuria_hilbert"
    )


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
    graduation_year: Optional[date] = Field(None, example=date(2023, 1, 1))
    image_url: Optional[str] = Field(
        None, example="https://localhost:9999/static/test.png"
    )
    skills: Optional[list[SkillDto]] = Field(
        None, example=[{"id": 1, "skill_name": "Linear Algebra"}]
    )
    roles: Optional[list[RoleDto]] = Field(
        None,
        example=[
            {"id": 1, "role_name": "Backend developer"},
            {"id": 2, "role_name": "Frontend developer"},
        ],
    )
    goals: Optional[list[TeamGoalDto]] = Field(
        None,
        example=[
            {"id": 1, "goal_name": "Научиться новому"},
            {"id": 2, "goal_name": "Пополнить портфолио"},
        ],
    )
