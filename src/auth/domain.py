from pydantic import BaseModel, Field, ConfigDict
from src.user.domain import UserInternalRole


class AuthBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., example="test@test.com", min_length=5, max_length=50)
    password: str = Field(..., example="test123456", min_length=8, max_length=256)


class Signup(AuthBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "first_name": "Роберт",
                    "last_name": "Ласурия",
                    "internal_role": "student",
                }
                # },
                # {
                #     "first_name": "Дмитрий",
                #     "last_name": "Сурначев",
                #     "internal_role": "student",
                # },
            ]
        }
    )

    first_name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)
    internal_role: UserInternalRole = Field(UserInternalRole.student)


class Login(AuthBase):
    ...


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
