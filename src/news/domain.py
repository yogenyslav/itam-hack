from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class NewsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str = Field(
        ...,
        min_length=5,
        examples=[
            "Сегодня пары у Егорова будут в 13:00. Там он расскажет обо всех тонкостях МЛя."
        ],
    )


class NewsCreate(NewsBase):
    ...


class NewsDto(NewsBase):
    id: int = Field(..., examples=[1])
    image_url: Optional[str] = Field(
        None,
        min_length=5,
        examples=["http://localhost:9999/static/news_1_news_image.jpg"],
    )
