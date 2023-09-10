from pydantic import BaseModel, Field, ConfigDict


class SkillDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    skill_name: str = Field(..., min_length=1, max_length=80, example="Python")


class SkillCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_name: str = Field(..., min_length=1, max_length=80, example="Python")


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


class TeamGoalDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    goal_name: str = Field(
        ..., min_length=1, max_length=80, example="Backend developer"
    )


class TeamGoalCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    goal_name: str = Field(
        ..., min_length=1, max_length=50, example="Backend developer"
    )
