from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class UserStatsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    days_in_club: int = Field(..., example=150)
    hack_wins: int = Field(..., example=2)
    hack_participated: int = Field(..., example=5)
    messages_in_chats: int = Field(..., example=1285)
    avg_responsibility: float = Field(..., example=5.0)
    avg_communications: float = Field(..., example=5.0)
    avg_competence: float = Field(..., example=4.99)
    avg_interest: float = Field(..., example=5.0)
    avg_leadership: float = Field(..., example=4.05)


class UserStatsDto(UserStatsBase):
    ...


class UserStatsCreate(UserStatsBase):
    user_id: int = Field(..., example=1)


class GraphBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    x: float = Field(..., example=0)
    y: float = Field(..., example=1.2)


class GraphDto(GraphBase):
    ...


class GraphCreate(GraphBase):
    ...


class UserStatsGraphBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserStatsGraphDto(UserStatsGraphBase):
    interests_graph: list[GraphCreate] = Field(..., example=[{"x": 0, "y": 1.2}])


class UserStatsGraphCreate(UserStatsGraphBase):
    user_id: int = Field(..., example=1)
    interests_graph: list[GraphCreate] = Field(..., example=[{"x": 0, "y": 1.2}])


class StatsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StatsDto(StatsBase):
    stats: UserStatsDto = Field(...)
    suggestion: str = Field(..., example="Потенциальный лидер")
    stats_graphs: UserStatsGraphDto = Field(...)


class StatsCreate(StatsBase):
    stats: UserStatsCreate = Field(...)
    suggestion: str = Field(..., example="Потенциальный лидер")
    stats_graphs: UserStatsGraphCreate = Field(...)
