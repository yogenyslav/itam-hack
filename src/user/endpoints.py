from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import (
    get_current_user,
    get_user_repository,
    get_hackathon_repository,
)
from src.user.domain import UserDto
from src.user.repository import UserRepository
from src.hackathon.domain import HackathonTeamLfgEnrollmentDto, EnrollmentStatus
from src.hackathon.repository import HackathonRepository
from src.utils.logging import get_logger


router = APIRouter(prefix="/users", tags=["users"])

log = get_logger(__name__)


@router.post("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user_data: UserDto,
    current_user: UserDto = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository),
):
    try:
        if user_data.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        user_db = repository.get(user_id=user_data.id)
        repository.update(user_db, user_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/profile/me", response_model=UserDto, status_code=status.HTTP_200_OK)
async def me(current_user: UserDto = Depends(get_current_user)) -> UserDto:
    return current_user


@router.get(
    "/profile/team_enrollments", response_model=list[HackathonTeamLfgEnrollmentDto]
)
async def get_enrolled_teams(
    enrollment_status: EnrollmentStatus | None = EnrollmentStatus.pending,
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return [
            HackathonTeamLfgEnrollmentDto.model_validate(enrollment)
            for enrollment in repository.get_team_enrollments(
                user_id=current_user.id, enrollment_status=enrollment_status
            )
        ]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
