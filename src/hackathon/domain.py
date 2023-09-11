from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from src.tags.domain import RoleDto, RoleCreate
from src.user.domain import UserDto


class PrizeType(str, Enum):
    money = "money"
    merchandise = "merchandise"
    other = "other"


class EnrollmentStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    denied = "denied"


class HackathonTagCreate(BaseModel):
    tag: str = Field(..., min_length=1, max_length=50)


class HackathonTagDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    tag: str = Field(..., min_length=1, max_length=50)


class HackathonTagCount(BaseModel):
    tag: str = Field(..., min_length=1, max_length=50)
    count: int = Field(..., ge=0, examples=[1])


class HackathonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(
        ..., min_length=1, max_length=80, examples=["Кокос Hackathon 2023"]
    )
    registration_start: datetime = Field(..., examples=[datetime.now()])
    registration_finish: datetime = Field(
        ..., examples=[datetime.now() + timedelta(days=1)]
    )
    registration_url: Optional[str] = Field(None, examples=["https://google.com"])
    team_minimum_size: Optional[int] = Field(None, ge=1, examples=[1])
    team_maximum_size: int = Field(..., ge=1, examples=[5])
    prize_type: PrizeType = Field(..., examples=[PrizeType.money])
    money_prize: Optional[int] = Field(None, ge=0, examples=[1000000])
    start_date: datetime = Field(..., examples=[datetime.now() + timedelta(days=2)])
    end_date: datetime = Field(..., examples=[datetime.now() + timedelta(days=3)])
    description: str = Field(..., min_length=1, examples=["Описание хакатона"])
    is_offline: bool = Field(..., examples=[True])
    place: Optional[str] = Field(
        None, min_length=1, max_length=120, examples=["Москва"]
    )
    image: Optional[str] = Field(
        None,
        min_length=1,
        max_length=120,
        examples=["http://localhost:9999/static/image.png"],
    )


class HackathonCreate(HackathonBase):
    tags: list[HackathonTagCreate] = Field(
        ...,
        examples=[{"tag": "Веб-разработка"}, {"tag": "Мобильная разработка"}],
    )


class HackathonDto(HackathonBase):
    id: int = Field(..., ge=1, examples=[1])
    tags: list[HackathonTagDto] = Field(
        ...,
        examples=[
            {"id": 1, "tag": "Веб-разработка"},
            {"id": 2, "tag": "Мобильная разработка"},
        ],
    )


class HackathonTeamLfgBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hackathon_id: int = Field(..., ge=1, examples=[1])
    title: str = Field(..., min_length=1, max_length=80, examples=["Команда 1"])
    description: str = Field(..., min_length=1, examples=["Описание команды"])
    required_members: int = Field(..., ge=1, examples=[3])


class HackathonTeamLfgCreate(HackathonTeamLfgBase):
    required_roles: list[RoleCreate] = Field(
        ...,
        examples=[
            {"role_name": "Backend developer"},
            {"role_name": "Frontend developer"},
            {"role_name": "ML engineer"},
        ],
    )


class HackathonTeamLfgDto(HackathonTeamLfgBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., ge=1, examples=[1])
    leader_id: int = Field(..., ge=1, examples=[1])
    members: list[UserDto] = Field(...)
    required_roles: list[RoleDto] = Field(
        ...,
        examples=[
            {"id": 1, "role_name": "Backend developer"},
            {"id": 2, "role_name": "Frontend developer"},
            {"id": 3, "role_name": "ML engineer"},
        ],
    )


class HackathonTeamLfgEnrollmentDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., ge=1, examples=[1])
    team_id: int = Field(..., ge=1, examples=[1])
    user_id: int = Field(..., ge=1, examples=[1])
    role_name: str = Field(
        ..., min_length=1, max_length=80, examples=["Backend developer"]
    )
    status: EnrollmentStatus = Field(..., examples=[EnrollmentStatus.pending])
