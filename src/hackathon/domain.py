from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class PrizeType(int, Enum):
    money = 0
    merchandise = 1
    other = 2


class HackathonTagCreate(BaseModel):
    tag: str = Field(..., min_length=1, max_length=50)


class HackathonTagDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(...)
    tag: str = Field(..., min_length=1, max_length=50)


class HackathonBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=80, example="Кокос Hackathon 2023")
    registration_finish: datetime = Field(
        ..., example=datetime.now() + timedelta(days=1)
    )
    team_minimum_size: Optional[int] = Field(None, ge=1, example=1)
    team_maximum_size: int = Field(..., ge=1, example=5)
    prize_type: PrizeType = Field(..., example=PrizeType.money)
    money_prize: Optional[int] = Field(None, ge=0, example=1000000)


class HackathonCreate(HackathonBase):
    tags: list[HackathonTagCreate] = Field(
        ...,
        min_items=1,
        max_items=10,
        example=[{"tag": "Веб-разработка"}, {"tag": "Мобильная разработка"}],
    )


class HackathonDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tags: list[HackathonTagDto] = Field(
        ...,
        min_items=1,
        max_items=10,
        example=[
            {"id": 1, "tag": "Веб-разработка"},
            {"id": 2, "tag": "Мобильная разработка"},
        ],
    )
