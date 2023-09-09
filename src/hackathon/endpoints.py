from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import get_current_user, get_hackathon_repository
from src.hackathon.domain import HackathonCreate
from src.hackathon.repository import HackathonRepository
from src.user.domain import UserDto, UserRole
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
    if current_user.internal_role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return repository.add(hackathons)
