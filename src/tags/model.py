from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_name: Mapped[str] = mapped_column(String(80), index=True)

    users = relationship(
        "User",
        secondary="user_skills",
        back_populates="skills",
    )


user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(80), index=True)

    users = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
    )
    teams = relationship(
        "HackathonTeamLfg",
        secondary="team_roles",
        back_populates="required_roles",
    )


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class TeamGoal(Base):
    __tablename__ = "team_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    goal_name: Mapped[str] = mapped_column(String(50), index=True)

    users = relationship(
        "User",
        secondary="user_team_goals",
        back_populates="goals",
    )


user_team_goals = Table(
    "user_team_goals",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("team_goal_id", Integer, ForeignKey("team_goals.id")),
)
