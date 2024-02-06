# import uuid
# from functools import lru_cache
# from typing import Annotated
#
# import httpx
# from core.config import settings
# from fastapi import Depends
# from integration.storages import MongoStorage, get_storage
# from schemas.notifications import EmailNotificationSchema, PushNotificationSchema, EmailNotificationSchemaRefactor
# from schemas.users import UserInformation
#
#
# class NotificationsService:
#     def __init__(self, storage: MongoStorage) -> None:
#         self.storage = storage
#
#     async def get_email_notifications(
#         self, user_id: uuid.UUID
#     ) -> list[EmailNotificationSchema]:
#         notifications = await self.storage.find_elements_by_properties(
#             {"user_id": user_id}, "email_notifications"
#         )
#         return [
#             EmailNotificationSchema(**notification) for notification in notifications
#         ]
#
#
# @lru_cache
# def get_notifications_service(
#     storage: Annotated[MongoStorage, Depends(get_storage)]
# ) -> NotificationsService:
#     return NotificationsService(storage)
