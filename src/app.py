from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router
from src.auth.endpoints import router as auth_router


def create_app():
    _app = FastAPI(
        name="Itam Hacks",
        description="Itam Hacks API",
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(api_router)
    _app.include_router(auth_router)
    return _app
