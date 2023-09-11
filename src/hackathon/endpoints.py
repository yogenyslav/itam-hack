from fastapi import APIRouter, Depends, HTTPException, status, Path, UploadFile
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


@router.post("/{hackathon_id}/image")
async def upload_hackathon_image(
    file: UploadFile,
    hackathon_id: int = Path(..., ge=1),
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        hackathon = repository.get(hackathon_id=hackathon_id)
        if not hackathon:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "hackathon not found")

        if not file:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "no file provided")
        with open(f"static/hackathon_{hackathon_id}_{file.filename}", "wb") as buffer:
            buffer.write(await file.read())

        url = f"http://localhost:9999/static/hackathon_{hackathon_id}_{file.filename}"
        hackathon.image = url
        repository.update(hackathon)

        return {"url": url}
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


@router.get("/{hackathon_id}", response_model=HackathonDto)
async def get_hack_by_id(
    hackathon_id: int = Path(..., ge=1),
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return HackathonDto.model_validate(repository.get(hackathon_id=hackathon_id))
    except HTTPException as e:
        log.debug(str(e))
        raise e
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


@router.get("/teams/my", response_model=list[HackathonTeamLfgDto])
async def get_my_teams(
    current_user: UserDto = Depends(get_current_user),
    repository: HackathonRepository = Depends(get_hackathon_repository),
):
    try:
        return [
            HackathonTeamLfgDto.model_validate(team)
            for team in repository.get_teams_lfg(user_id=current_user.id)
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
        if not team_db:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "team not found")
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

        enrollment = repository.get(enrollment_id=enrollment_id)

        if not enrollment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "enrollment not found")

        if current_user.id == enrollment.team.leader_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        repository.accept_team_enrollment(enrollment_id=enrollment_id)

    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/teams/reject_enrollment", status_code=status.HTTP_204_NO_CONTENT)
async def reject_hackathon_team_lfg_enrollment(
    enrollment_id: int,
    repository: HackathonRepository = Depends(get_hackathon_repository),
    current_user: UserDto = Depends(get_current_user),
):
    try:
        enrollment = repository.get(enrollment_id=enrollment_id)
        if not enrollment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "enrollment not found")
        if current_user.id == enrollment.team.leader_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        repository.reject_team_enrollment(enrollment_id=enrollment_id)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.debug(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
