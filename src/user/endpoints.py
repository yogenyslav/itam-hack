from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from src.data.dependencies import (
    get_current_user,
    get_user_repository,
    get_hackathon_repository,
)
from src.user.domain import (
    UserDto,
    SurveyCreate,
)
from src.user.repository import UserRepository
from src.hackathon.domain import HackathonTeamLfgEnrollmentDto, EnrollmentStatus
from src.hackathon.repository import HackathonRepository
from src.utils.logging import get_logger


router = APIRouter(prefix="/users", tags=["users"])

log = get_logger(__name__)


@router.post("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
    user_data: UserDto,
    current_user: UserDto | None = Depends(get_current_user),
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
async def me(current_user: UserDto | None = Depends(get_current_user)) -> UserDto:
    return current_user


@router.get(
    "/profile/team_enrollments", response_model=list[HackathonTeamLfgEnrollmentDto]
)
async def get_enrolled_teams(
    enrollment_status: EnrollmentStatus | None = EnrollmentStatus.pending,
    current_user: UserDto | None = Depends(get_current_user),
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


# @router.post("/profile/:user_id/invite")
# async def invite_user(
#     user_id: int,
#     team_id: int,
#     current_user: UserDto | None = Depends(get_current_user),
#     repository: HackathonRepository = Depends(get_hackathon_repository),
# ):
#     try:
#         repository.invite_user(user_id=user_id, team_id=team_id)
#     except HTTPException as e:
#         log.debug(str(e))
#         raise e
#     except Exception as e:
#         log.debug(str(e))
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/survey")
async def create_survey(
    survey_data: SurveyCreate,
    current_user: UserDto | None = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository),
):
    try:
        user_db = repository.get(user_id=current_user.id)
        current_user.tg_username = survey_data.tg_username

        repository.update(user_db, current_user, survey=survey_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/avatar")
async def update_picture(
    file: UploadFile,
    current_user: UserDto = Depends(get_current_user),
    repository: UserRepository = Depends(get_user_repository),
):
    try:
        file_ext = file.content_type.split("/")[-1]
        with open(f"static/avatar_{current_user.id}.{file_ext}", "wb") as buffer:
            buffer.write(await file.read())

        url = f"http://localhost:9999/static/avatar_{current_user.id}.{file_ext}"
        current_user.image_url = url
        user_db = repository.get(user_id=current_user.id)
        repository.update(user_db, current_user)

        return {"url": url}
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
