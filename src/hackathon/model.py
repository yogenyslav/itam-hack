from datetime import datetime
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Table,
    Column,
    DateTime,
    Enum,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base
from src.hackathon.domain import PrizeType


class Hackathon(Base):
    __tablename__ = "hackathons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    registration_start: Mapped[datetime] = mapped_column(DateTime)
    registration_finish: Mapped[datetime] = mapped_column(DateTime)
    team_minimum_size: Mapped[int] = mapped_column(Integer)
    team_maximum_size: Mapped[int] = mapped_column(Integer)
    prize_type: Mapped[int] = mapped_column(Enum(PrizeType), nullable=False)
    money_prize: Mapped[int] = mapped_column(Integer, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_offline: Mapped[bool] = mapped_column(Boolean, nullable=False)
    place: Mapped[str] = mapped_column(String(120), nullable=True)
    image: Mapped[str] = mapped_column(String(120), nullable=True)

    tags = relationship(
        "HackathonTag", secondary="hackathons_to_tags", back_populates="hackathons"
    )


hackathons_to_tags = Table(
    "hackathons_to_tags",
    Base.metadata,
    Column("hackathon_id", Integer, ForeignKey("hackathons.id")),
    Column("tag_id", Integer, ForeignKey("hackathon_tags.id")),
)


class HackathonTag(Base):
    __tablename__ = "hackathon_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)

    hackathons = relationship(
        "Hackathon", secondary="hackathons_to_tags", back_populates="tags"
    )
