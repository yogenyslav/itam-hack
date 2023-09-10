from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.data.dependencies import get_news_repository, get_current_user
from src.news.repository import NewsRepository
from src.news.domain import NewsDto, NewsCreate
from src.user.domain import UserDto, UserInternalRole
from src.utils.logging import get_logger

router = APIRouter(prefix="/news", tags=["news"])

log = get_logger(__name__)


@router.get("/", response_model=list[NewsDto])
async def get_news(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=0, le=100),
    news_repository: NewsRepository = Depends(get_news_repository),
):
    try:
        return [
            NewsDto.model_validate(news)
            for news in news_repository.get_all(offset, limit)
        ]
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_news(
    news_data: list[NewsCreate],
    current_user: UserDto | None = Depends(get_current_user),
    repository: NewsRepository = Depends(get_news_repository),
):
    try:
        if current_user.internal_role != UserInternalRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return repository.add(news_data)
    except HTTPException as e:
        log.debug(str(e))
        raise e
    except Exception as e:
        log.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
