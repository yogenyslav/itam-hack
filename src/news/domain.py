from pydantic import BaseModel, Field, ConfigDict


class NewsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str = Field(
        ...,
        min_length=5,
        example="Сегодня пары у Егорова будут в 13:00. Там он расскажет обо всех тонкостях МЛя.",
    )
    image_url: str = Field(
        ..., min_length=5, example="http://localhost:10001/static/news/1.jpg"
    )


class NewsCreate(NewsBase):
    ...


class NewsDto(NewsBase):
    id: int = Field(..., example=1)
