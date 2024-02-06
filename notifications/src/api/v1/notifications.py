# from typing import Annotated
#
# from fastapi import APIRouter, Depends
# from schemas.notifications import EmailNotificationSchema
# from services.notifications import NotificationsService, get_notifications_service
#
# from .auth import security_jwt
#
# router = APIRouter()
#
#
# # TODO: Сделать пагинацию, т.к. из-за большого количества сообщений могут быть задержки
# @router.get(
#     "/notifications",
#     response_model=list[EmailNotificationSchema],
#     summary="Просмотр всех уведомлений пользователя",
#     description="Выдача всех уведомлений, прикрепленных к конкретному пользователю",
#     response_description="Список уведомлений, хранящихся в хранилище сервиса",
# )
# async def get_user_notifications(
#     user: Annotated[dict, Depends(security_jwt)],
#     notifications_service: NotificationsService = Depends(get_notifications_service),
# ) -> list[EmailNotificationSchema]:
#     return await notifications_service.get_email_notifications(user["user_id"])
