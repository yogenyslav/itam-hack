from sqlalchemy import Integer, String, ForeignKey, Table, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.data import Base
from src.user.domain import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    internal_role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.student)
    password: Mapped[str] = mapped_column(String)

    tg_user = relationship(
        "TgUser", primaryjoin="User.id == TgUser.user_id", back_populates="user"
    )
    student_info = relationship(
        "StudentInfo",
        primaryjoin="User.id == StudentInfo.user_id",
        back_populates="user",
    )
    skills = relationship(
        "Skill",
        secondary="user_skills",
        back_populates="users",
    )
    roles = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
    )


class TgUser(Base):
    __tablename__ = "tg_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)

    user = relationship(
        "User", primaryjoin="TgUser.user_id == User.id", back_populates="tg_user"
    )


class StudentInfo(Base):
    __tablename__ = "students_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    graduation_year: Mapped[int] = mapped_column(Integer)
    major: Mapped[str] = mapped_column(String(30))
    faculty: Mapped[str] = mapped_column(String(30))
    portfolio_url: Mapped[str] = mapped_column(String, nullable=True)
    about: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="student_info")


user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    skill_name: Mapped[str] = mapped_column(String(80), index=True)

    users = relationship(
        "User",
        secondary="user_skills",
        back_populates="skills",
    )


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
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
