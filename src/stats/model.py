from sqlalchemy import Integer, String, ForeignKey, Column, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base


class UserStats(Base):
    __tablename__ = "user_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    days_in_club: Mapped[int] = mapped_column(Integer, default=0)
    hack_wins: Mapped[int] = mapped_column(Integer, default=0)
    hack_participated: Mapped[int] = mapped_column(Integer, default=0)
    messages_in_chats: Mapped[int] = mapped_column(Integer, default=0)
    avg_responsibility: Mapped[float] = mapped_column(Float, default=0)
    avg_communications: Mapped[float] = mapped_column(Float, default=0)
    avg_competence: Mapped[float] = mapped_column(Float, default=0)
    avg_interest: Mapped[float] = mapped_column(Float, default=0)
    avg_leadership: Mapped[float] = mapped_column(Float, default=0)

    user = relationship("User", back_populates="stats")


class UserStatsGraph(Base):
    __tablename__ = "user_stats_graph"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    interests_graph: Mapped[list["InterestsGraph"]] = relationship(
        "InterestsGraph", back_populates="stats_graph"
    )

    user = relationship("User", back_populates="stats_graph")


class InterestsGraph(Base):
    __tablename__ = "graph"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stats_graph_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_stats_graph.id")
    )
    x: Mapped[float] = mapped_column(Float, default=0)
    y: Mapped[float] = mapped_column(Float, default=0)

    stats_graph = relationship("UserStatsGraph", back_populates="interests_graph")
