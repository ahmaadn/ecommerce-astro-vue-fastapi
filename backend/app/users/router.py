from fastapi import APIRouter, status

from app.auth.dependencies import is_user_active

from .schemas import UserPublic

router = r = APIRouter(prefix="/users", tags=["users"])


@r.get("/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
async def get_user_by_id(current_user: is_user_active):
    return current_user
