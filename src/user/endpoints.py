from fastapi import APIRouter, Depends, HTTPException, status
from src.data.dependencies import get_current_user
from src.user.domain import UserDto


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserDto, status_code=status.HTTP_200_OK)
async def me(current_user: UserDto = Depends(get_current_user)) -> UserDto:
    return current_user
