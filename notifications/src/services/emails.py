import asyncio
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Annotated, Any

from fastapi import Depends
from integration.brokers import RabbitMQBroker, get_message_broker
from integration.storages import MongoStorage, get_storage
from schemas.emails import (
    OutputFilmReleaseNotification,
    OutputFilmSelectionNotification,
    OutputManagerNotification,
    OutputWelcomeNotification,
)
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
            await self.make_email_notification(
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

    async def make_email_notification(self, **kwargs: Any):
        raise NotImplementedError(
            "make_email_notification not implemented inside the class"
        )


class PersonalEmailService(BaseEmailService):
    def __init__(
        self,
        broker: RabbitMQBroker,
        storage: MongoStorage,
        broker_queue_name: str,
    ) -> None:
        self.broker = broker
        self.storage = storage
        self.broker_queue_name = broker_queue_name

    async def _insert_notification_in_storage(
        self, notification: EmailPersonalNotificationSchemaRefactor
    ) -> None:
        await self.storage.insert_element(
            notification.model_dump(mode="json"),
            self.storage_collection_name,
        )

    async def handle_message(self, **kwargs: Any) -> None:
        notification = await self.make_email_notification(**kwargs)
        await asyncio.gather(
            self._insert_notification_in_storage(notification),
            self.broker.publish_one(notification, self.broker_queue_name),
        )

    async def make_email_notification(self, **kwargs: Any):
        raise NotImplementedError(
            "make_email_notification not implemented inside the class"
        )


class FilmSelectionEmailService(PersonalEmailService):
    subject = "A weekly selection of movies for you"
    template_name = "personal-film-selection.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(
            broker, storage, "notifications.film_selection_email_notification"
        )

    async def make_email_notification(
        self, **kwargs: Any
    ) -> OutputFilmSelectionNotification:
        return OutputFilmSelectionNotification(
            user_id=kwargs["user_id"],
            producer_id=uuid.uuid4(),
            subject=self.subject,
            films_ids=kwargs["films_ids"],
            template_name=self.template_name,
        )


class FilmReleaseEmailService(PersonalEmailService):
    subject = "New movie and TV series releases at the end of the end of the month"
    template_name = "new-films-releases.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage):
        super().__init__(
            broker, storage, "notifications.film_release_email_notification"
        )

    async def make_email_notification(
        self, **kwargs: Any
    ) -> OutputFilmReleaseNotification:
        return OutputFilmReleaseNotification(
            user_id=kwargs["user_id"],
            producer_id=uuid.uuid4(),
            subject=self.subject,
            watched_count=kwargs["watched_count"],
            films_ids=kwargs["films_ids"],
            template_name=self.template_name,
        )


class WelcomeEmailService(PersonalEmailService):
    subject = "Welcome to PRACTIX!"
    template_name = "welcome.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(
            broker, storage, "notifications.welcome_message_email_notification"
        )

    async def make_email_notification(self, **kwargs: Any) -> OutputWelcomeNotification:
        return OutputWelcomeNotification(
            user_id=kwargs["user_id"],
            producer_id=uuid.uuid4(),
            subject=self.subject,
            template_name=self.template_name,
        )


class ManagerEmailNotificationService(GeneralEmailService):
    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage, "notifications.manager_email_notification")

    async def make_email_notification(self, **kwargs: Any) -> OutputManagerNotification:
        return OutputManagerNotification(
            user_id=kwargs["user_id"],
            producer_id=kwargs["producer_id"],
            subject=kwargs["subject"],
            body=kwargs["body"],
        )


@lru_cache
def get_film_selection_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return FilmSelectionEmailService(broker, storage)


@lru_cache
def get_film_release_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return FilmReleaseEmailService(broker, storage)


@lru_cache
def get_welcome_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalEmailService:
    return WelcomeEmailService(broker, storage)


@lru_cache
def get_manager_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> GeneralEmailService:
    return ManagerEmailNotificationService(broker, storage)
