from fastapi import Depends, HTTPException, status
from src.auth.jwt import decode_jwt, oauth2_scheme
from src.data.sql import SQLManager
from src.user.domain import UserDto
from src.tags.domain import RoleDto, SkillDto, TeamGoalDto
from src.user.repository import UserRepository
from src.hackathon.repository import HackathonRepository
from src.news.repository import NewsRepository
from src.tags.repository import TagsRepository
from src.stats.repository import StatsRepository
from src.utils.logging import get_logger

log = get_logger(__name__)


async def get_db() -> SQLManager:
    """Get the database connection"""
    return SQLManager(get_logger("db"))


async def get_user_repository(db: SQLManager = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_hackathon_repository(
    db: SQLManager = Depends(get_db),
) -> HackathonRepository:
    return HackathonRepository(db)


async def get_news_repository(
    db: SQLManager = Depends(get_db),
) -> NewsRepository:
    return NewsRepository(db)


async def get_tags_repository(
    db: SQLManager = Depends(get_db),
) -> TagsRepository:
    return TagsRepository(db)


async def get_stats_repository(
    db: SQLManager = Depends(get_db),
) -> TagsRepository:
    return StatsRepository(db)


async def get_current_user(
    access_token: str | None = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserDto | None:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (current_user)",
        )
    user_id = decode_jwt(access_token)
    user_db = user_repository.get(user_id=user_id)

    roles = [RoleDto.model_validate(role) for role in user_db.roles]
    skills = [SkillDto.model_validate(skill) for skill in user_db.skills]
    goals = [TeamGoalDto.model_validate(goal) for goal in user_db.goals]

    user = UserDto(
        id=user_db.id,
        email=user_db.email,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        internal_role=user_db.internal_role,
        level=user_db.level,
        tg_username=user_db.tg_username,
        graduation_year=user_db.graduation_year,
    )
    user.roles = roles
    user.skills = skills
    user.goals = goals
    return user
