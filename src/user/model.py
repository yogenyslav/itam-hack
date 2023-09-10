from datetime import date
from sqlalchemy import Integer, String, Enum, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base
from src.user.domain import UserInternalRole
from src.tags.model import Role, Skill, TeamGoal
from src.stats.model import UserStats, UserStatsGraph


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    internal_role: Mapped[str] = mapped_column(
        Enum(UserInternalRole), default=UserInternalRole.student
    )
    password: Mapped[str] = mapped_column(String)
    level: Mapped[float] = mapped_column(Float, default=0)
    tg_username: Mapped[str] = mapped_column(String(60), nullable=True)
    graduation_year: Mapped[date] = mapped_column(Date, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    skills: Mapped[list["Skill"]] = relationship(
        "Skill",
        secondary="user_skills",
        back_populates="users",
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
    )
    teams = relationship(
        "HackathonTeamLfg",
        secondary="team_members",
        back_populates="members",
    )
    enrollments = relationship(
        "HackathonTeamLfgEnrollment",
        back_populates="user",
    )
    teams_created = relationship(
        "HackathonTeamLfg",
        back_populates="leader",
    )
    goals: Mapped[list["TeamGoal"]] = relationship(
        "TeamGoal",
        secondary="user_team_goals",
        back_populates="users",
    )
    stats: Mapped["UserStats"] = relationship("UserStats", back_populates="user")
    stats_graph: Mapped["UserStatsGraph"] = relationship(
        "UserStatsGraph", back_populates="user"
    )


# class TgUser(Base):
#     __tablename__ = "tg_users"

#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
#     first_name: Mapped[str] = mapped_column(String(30))
#     tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
#     last_name: Mapped[str] = mapped_column(String(30), nullable=True)

#     user = relationship(
#         "User", primaryjoin="TgUser.user_id == User.id", back_populates="tg_user"
#     )


# class StudentInfo(Base):
#     __tablename__ = "students_info"

#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
#     graduation_year: Mapped[int] = mapped_column(Integer)
#     major: Mapped[str] = mapped_column(String(30))
#     faculty: Mapped[str] = mapped_column(String(30))
#     portfolio_url: Mapped[str] = mapped_column(String, nullable=True)
#     about: Mapped[str] = mapped_column(String, nullable=True)

#     user = relationship("User", back_populates="student_info")
