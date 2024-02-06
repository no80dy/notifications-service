import asyncio
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends
from integration.brokers import RabbitMQBroker, get_message_broker
from integration.storages import MongoStorage, get_storage
from schemas.notifications import (
    EmailGeneralNotificationSchemaRefactor,
    EmailPersonalNotificationSchemaRefactor,
)


class BaseEmailService(ABC):
    storage_collection_name = "email_notifications"

    @abstractmethod
    async def handle_message(self, notification_data: dict) -> None:
        pass


class GeneralEmailService(BaseEmailService):
    def __init__(
        self, broker: RabbitMQBroker, storage: MongoStorage, broker_queue_name: str
    ) -> None:
        self.broker = broker
        self.storage = storage
        self.broker_queue_name = broker_queue_name

    async def _insert_notifications_in_storage(
        self, notifications: list[EmailGeneralNotificationSchemaRefactor]
    ) -> None:
        await self.storage.insert_elements(
            [notification.model_dump(mode="json") for notification in notifications],
            self.storage_collection_name,
        )

    async def handle_message(self, **kwargs: Any) -> None:
        notifications = [
            EmailGeneralNotificationSchemaRefactor(
                user_id=user_id,
                producer_id=uuid.uuid4(),
                subject=kwargs["subject"],
                body=kwargs["body"],
            )
            for user_id in kwargs["users_ids"]
        ]
        await asyncio.gather(
            self._insert_notifications_in_storage(notifications),
            self.broker.publish_many(notifications, self.broker_queue_name),
        )


class PersonalEmailService(BaseEmailService):
    def __init__(
        self,
        broker: RabbitMQBroker,
        storage: MongoStorage,
        subject: str,
        template_name: str,
        broker_queue_name: str,
    ) -> None:
        self.broker = broker
        self.storage = storage
        self.subject = subject
        self.template_name = template_name
        self.broker_queue_name = broker_queue_name

    async def _insert_notification_in_storage(
        self, notification: EmailPersonalNotificationSchemaRefactor
    ) -> None:
        await self.storage.insert_element(
            notification.model_dump(mode="json"),
            self.storage_collection_name,
        )

    async def handle_message(self, **kwargs: Any) -> None:
        notification = EmailPersonalNotificationSchemaRefactor(
            user_id=kwargs["user_id"],
            producer_id=uuid.uuid4(),
            subject=self.subject,
            template_name=self.template_name,
        )
        await asyncio.gather(
            self._insert_notification_in_storage(notification),
            self.broker.publish_one(notification, self.broker_queue_name),
        )


@lru_cache
def get_film_selection_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return PersonalEmailService(
        broker,
        storage,
        "A weekly selection of movies for you",
        "personal-film-selection.html",
        "notifications.film_selection_email_notification",
    )


@lru_cache
def get_film_release_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return PersonalEmailService(
        broker,
        storage,
        "New movie and TV series releases at the end of the end of the month",
        "new-films-releases.html",
        "notifications.film_release_email_notification",
    )


@lru_cache
def get_welcome_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return PersonalEmailService(
        broker,
        storage,
        "Welcome to PRACTIX!",
        "welcome.html",
        "notifications.welcome_message_email_notification",
    )


@lru_cache
def get_manager_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> GeneralEmailService:
    return GeneralEmailService(
        broker, storage, "notifications.manager_email_notification"
    )
