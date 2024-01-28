from typing import Annotated

from fastapi import APIRouter, Depends
from schemas.notifications import NotificationModel
from services.notifications import NotificationsService, get_notifications_service

from .auth import security_jwt

router = APIRouter()


@router.get(
    "/",
    response_model=list[NotificationModel],
    summary="Просмотр всех уведомлений пользователя",
    description="Выдача всех уведомлений, прикрепленных к конкретному пользователю",
    response_description="Список уведомлений, хранящихся в хранилище сервиса",
)
async def get_user_notifications(
    user: Annotated[dict, Depends(security_jwt)],
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> list[NotificationModel]:
    return await notifications_service.get_user_notifications(user["user_id"])
