import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from schemas.entity import UserInformationResponse
from services.users import UserService, get_user_service

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.get(
    "/users",
    description="Получение информации о пользователях по их идентификаторам",
    response_description="Список содержащий информацию о запрашиваемых пользователях",
    response_model=list[UserInformationResponse],
)
async def get_users(
    users_ids: Annotated[
        list[uuid.UUID], Query(description="Идентификаторы пользователей")
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserInformationResponse]:
    return await user_service.get_users_info(users_ids)
