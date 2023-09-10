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
from src.hackathon.domain import PrizeType, EnrollmentStatus
from src.tags.model import Role


class Hackathon(Base):
    __tablename__ = "hackathons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    registration_start: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    registration_finish: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    registration_url: Mapped[str] = mapped_column(String, nullable=True)
    website: Mapped[str] = mapped_column(String, nullable=True)
    team_minimum_size: Mapped[int] = mapped_column(Integer, nullable=True)
    team_maximum_size: Mapped[int] = mapped_column(Integer, nullable=False)
    prize_type: Mapped[str] = mapped_column(Enum(PrizeType), nullable=False)
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
    teams = relationship("HackathonTeamLfg", back_populates="hackathon")


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


team_roles = Table(
    "team_roles",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("hackathon_teams.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("hackathon_teams.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class HackathonTeamLfg(Base):
    __tablename__ = "hackathon_teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hackathon_id: Mapped[int] = mapped_column(Integer, ForeignKey("hackathons.id"))
    leader_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(80), nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    required_members: Mapped[int] = mapped_column(Integer, nullable=True)

    leader = relationship("User", back_populates="teams_created")
    required_roles: Mapped[list["Role"]] = relationship(
        "Role", secondary="team_roles", back_populates="teams", uselist=True
    )
    members = relationship(
        "User", secondary="team_members", back_populates="teams", uselist=True
    )
    hackathon = relationship("Hackathon", back_populates="teams")
    enrollments = relationship("HackathonTeamLfgEnrollment", back_populates="team")


class HackathonTeamLfgEnrollment(Base):
    __tablename__ = "hackathon_team_enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(EnrollmentStatus), default=EnrollmentStatus.pending
    )
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("hackathon_teams.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    team = relationship("HackathonTeamLfg", back_populates="enrollments")
    user = relationship("User", back_populates="enrollments")


class HackathonTeamLfgInvite(Base):
    __tablename__ = "hackathon_team_invites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("hackathon_teams.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    team = relationship("HackathonTeamLfg", back_populates="invites")
    user = relationship("User", back_populates="invites")
