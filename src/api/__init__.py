from fastapi import APIRouter
from src.user.endpoints import router as user_router
from src.hackathon.endpoints import router as hackathon_router
from src.news.endpoints import router as news_router
from src.tags.endpoints import router as tags_router
from src.stats.endpoints import router as stats_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)
api_router.include_router(hackathon_router)
api_router.include_router(news_router)
api_router.include_router(tags_router)
api_router.include_router(stats_router)
