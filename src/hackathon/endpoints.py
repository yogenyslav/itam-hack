from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import get_current_user, get_hackathon_repository
from src.hackathon.domain import (
    HackathonCreate,
    HackathonDto,
    HackathonTagCount,
    HackathonTeamLfgCreate,
    HackathonTeamLfgDto,
    HackathonTeamLfgEnrollmentDto,
    EnrollmentStatus,
)
from src.hackathon.repository import HackathonRepository
from src.hackathon import service
from src.user.domain import UserDto, UserInternalRole
from src.utils.logging import get_logger


router = APIRouter(prefix="/hackathons", tags=["hackathons"])

log = get_logger("HackathonEndpoints")


@router.post("/create", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_hackathons(
    hackathons: list[HackathonCreate],
    repository: HackathonRepository = Depends(get_hackathon_repository),
    current_user: UserDto = Depends(get_current_user),
) -> int:
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return repository.add(hackathons)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/upcoming", response_model=list[HackathonDto])
async def get_upcoming_hackathons(
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return [
            HackathonDto.model_validate(hack)
            for hack in repository.get_all(upcoming=True)
        ]
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tags", response_model=list[HackathonTagCount])
async def get_hackathon_tags(
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return [
            HackathonTagCount(tag=tag[0], count=tag[1]) for tag in repository.get_tags()
        ]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/teams/create", status_code=status.HTTP_201_CREATED)
async def create_hackathon_team(
    team_data: HackathonTeamLfgCreate,
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        repository.add_team_lfg(team_data, current_user.id)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teams", response_model=list[HackathonTeamLfgDto])
async def get_hackathon_teams_lfg(
    hackathon_id: int | None = None,
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return [
            HackathonTeamLfgDto.model_validate(team)
            for team in repository.get_teams_lfg(hackathon_id=hackathon_id)
        ]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/teams/join", status_code=status.HTTP_201_CREATED)
async def join_hackathon_team_lfg(
    team_id: int,
    role_name: str,
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        repository.join_team_lfg(team_id, current_user.id, role_name)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/teams/enrollments")
async def get_hackathon_team_lfg_enrollments(
    team_id: int,
    enrollment_status: EnrollmentStatus = EnrollmentStatus.pending,
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        team_db = repository.get(team_id=team_id)
        if current_user.id != team_db.leader_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return [
            HackathonTeamLfgEnrollmentDto.model_validate(team)
            for team in repository.get_team_enrollments(
                team_id=team_id, enrollment_status=enrollment_status
            )
        ]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/teams/accept_enrollment", status_code=status.HTTP_204_NO_CONTENT)
async def accept_hackathon_team_lfg_enrollment(
    enrollment_id: int,
    repository: HackathonRepository = Depends(get_hackathon_repository),
    current_user: UserDto = Depends(get_current_user),
):
    try:
        repository.accept_team_enrollment(enrollment_id=enrollment_id)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
