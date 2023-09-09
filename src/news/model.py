from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    content: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
