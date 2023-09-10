from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import get_tags_repository, get_current_user
from src.user.domain import UserDto, UserInternalRole
from src.tags.domain import (
    RoleCreate,
    RoleDto,
    TeamGoalCreate,
    TeamGoalDto,
    SkillCreate,
    SkillDto,
)
from src.tags.repository import TagsRepository
from src.utils.logging import get_logger


router = APIRouter(prefix="/tags", tags=["tags"])

log = get_logger(__name__)


@router.post("/roles/create")
async def create_roles(
    roles_data: list[RoleCreate],
    current_user: UserDto | None = Depends(get_current_user),
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only admin can create skills",
            )
        return repository.add_roles(roles_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/roles", response_model=list[RoleDto])
async def get_roles(
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        return [RoleDto.model_validate(role) for role in repository.get_all_roles()]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/goals/create")
async def create_goals(
    goals_data: list[TeamGoalCreate],
    current_user: UserDto | None = Depends(get_current_user),
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only admin can create skills",
            )
        return repository.add_goals(goals_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/goals", response_model=list[TeamGoalDto])
async def get_goals(
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        return [TeamGoalDto.model_validate(goal) for goal in repository.get_all_goals()]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/skills/create")
async def create_skills(
    skills_data: list[SkillCreate],
    current_user: UserDto | None = Depends(get_current_user),
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only admin can create skills",
            )
        return repository.add_skills(skills_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/skills", response_model=list[SkillDto])
async def get_skills(
    repository: TagsRepository = Depends(get_tags_repository),
):
    try:
        return [SkillDto.model_validate(skill) for skill in repository.get_all_skills()]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
