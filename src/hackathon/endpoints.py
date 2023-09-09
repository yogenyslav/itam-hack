from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import get_current_user, get_hackathon_repository
from src.hackathon.domain import HackathonCreate, HackathonDto, HackathonTagCount
from src.hackathon.repository import HackathonRepository
from src.hackathon import service
from src.user.domain import UserDto, UserInternalRole
from src.utils.logging import get_logger


router = APIRouter(prefix="/hackathons", tags=["hackathons"])

log = get_logger("HackathonEndpoints")


# TODO: какой сакральный смысл try except?
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
