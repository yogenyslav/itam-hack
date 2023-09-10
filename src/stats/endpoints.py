from fastapi import APIRouter, Depends, HTTPException, status, Path
from src.stats.domain import StatsDto, UserStatsDto, UserStatsGraphDto
from src.user.domain import UserDto, UserInternalRole
from src.stats.repository import StatsRepository
from src.data.dependencies import get_current_user, get_stats_repository
from src.utils.logging import get_logger


router = APIRouter(prefix="/stats", tags=["stats"])
log = get_logger(__name__)


@router.get("/{user_id}", response_model=StatsDto | None)
async def get_user_stats(
    user_id: int = Path(..., title="User ID", ge=1),
    current_user: UserDto = Depends(get_current_user),
    stats_repository: StatsRepository = Depends(get_stats_repository),
):
    try:
        if current_user.role != UserInternalRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authorized to get user stats",
            )
        stats = stats_repository.get(user_id=user_id, stats=True)
        if not stats:
            return None

        graph = stats_repository.get(user_id=user_id, graph=True)
        if not graph:
            return None

        return StatsDto(
            stats=[UserStatsDto.model_validate(**stat) for stat in stats],
            suggestion="Потенциальный лидер",
            stats_graphs=[UserStatsGraphDto.model_validate(**g) for g in graph],
        )
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.error(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
