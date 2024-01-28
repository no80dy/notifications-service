import uuid
from functools import lru_cache
from typing import Annotated

from core.config import settings
from fastapi import Depends
from integration.storages import MongoStorage, get_storage
from schemas.emails import OutputEmailMessage
from schemas.notifications import NotificationModel


class NotificationsService:
    def __init__(self, storage: MongoStorage) -> None:
        self.storage = storage

    async def get_user_notifications(
        self, user_id: uuid.UUID
    ) -> list[NotificationModel]:
        notifications = await self.storage.find_elements_by_properties(
            {"user_id": user_id}, settings.mongodb_notifications_collection_name
        )
        return [
            NotificationModel(
                notification_id=notification["notification_id"],
                user_id=notification["user_id"],
                content=OutputEmailMessage(**notification["content"]),
            )
            for notification in notifications
        ]


@lru_cache
def get_notifications_service(
    storage: Annotated[MongoStorage, Depends(get_storage)]
) -> NotificationsService:
    return NotificationsService(storage)
