import asyncio
import datetime
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Annotated, Any

import httpx
from core.config import settings
from core.jinja2 import template_env
from fastapi import Depends
from integration.brokers import RabbitMQBroker, get_message_broker
from integration.storages import MongoStorage, get_storage
from schemas.notifications import EmailNotificationSchema
from schemas.users import UserInformation


async def get_users_data(users_ids: list[uuid.UUID]) -> list[UserInformation]:
    joined_users_ids = "&users_ids=".join([str(user_id) for user_id in users_ids])
    url = f"{settings.auth_service_url}/?users_ids={joined_users_ids}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return [UserInformation(**data) for data in response.json()]


class BaseEmailService(ABC):
    storage_collection_name: str = "email_notifications"
    broker_queue_name: str = "email_queue"

    @abstractmethod
    async def handle_message(self, data: dict) -> None:
        pass

    @abstractmethod
    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        pass


class BasePersonalEmailService(BaseEmailService):
    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        self.broker = broker
        self.storage = storage

    async def _insert_notification_in_storage(
        self, notification: EmailNotificationSchema
    ) -> None:
        await self.storage.insert_element(
            notification.model_dump(mode="json"),
            self.storage_collection_name,
        )

    async def handle_message(self, data: dict) -> None:
        users = await get_users_data(
            [
                data["user_id"],
            ]
        )

        if not users:
            raise ValueError("No user found")

        user = users[0]
        notification = await self.make_email_message(
            username=user.username, email=user.email, **data
        )
        await asyncio.gather(
            self._insert_notification_in_storage(notification),
            self.broker.publish_one(notification, self.broker_queue_name),
        )

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        raise NotImplementedError("Method make_email_message not implemented")


class BaseGeneralEmailService(BaseEmailService):
    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        self.broker = broker
        self.storage = storage

    async def _create_notifications(
        self, users: list[UserInformation], **kwargs: Any
    ) -> list[EmailNotificationSchema]:
        notifications = []
        for user in users:
            content = await self.make_email_message(
                user_id=user.id, email=user.email, **kwargs
            )
            notifications.append(EmailNotificationSchema(**content.model_dump()))
        return notifications

    async def _insert_notifications_in_storage(
        self, notifications: list[EmailNotificationSchema]
    ) -> None:
        await self.storage.insert_elements(
            [notification.model_dump(mode="json") for notification in notifications],
            self.storage_collection_name,
        )

    async def handle_message(self, data: dict) -> None:
        users = await get_users_data(data["users_ids"])

        if not users:
            raise ValueError("No users found")

        notifications = await self._create_notifications(users, **data)
        await asyncio.gather(
            self._insert_notifications_in_storage(notifications),
            self.broker.publish_many(notifications, self.broker_queue_name),
        )

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        raise NotImplementedError("Method make_email_message not implemented")


class ManagerEmailService(BaseGeneralEmailService):
    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        return EmailNotificationSchema(
            user_id=kwargs["user_id"],
            email_from=kwargs["email_from"],
            email_to=kwargs["email"],
            subject=kwargs["subject"],
            body=kwargs["body"],
        )


class FilmSelectionEmailService(BasePersonalEmailService):
    subject_text = "Еженедельная подборка фильмов для вас"
    template_name = "personal-film-selection.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        template = template_env.get_template(self.template_name)
        body = template.render(
            username=kwargs["username"], films_ids=kwargs["films_ids"]
        )
        return EmailNotificationSchema(
            user_id=kwargs["user_id"],
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


class FilmReleaseEmailService(BasePersonalEmailService):
    subject_text = "Новые релизы фильмов и сериалов в этом месяце"
    template_name = "new-films-releases.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        body = template_env.get_template(self.template_name).render(
            username=kwargs["username"],
            month=datetime.datetime.now().strftime("%B"),
            watched_count=kwargs["watched_count"],
        )
        return EmailNotificationSchema(
            user_id=kwargs["user_id"],
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


class WelcomeEmailService(BasePersonalEmailService):
    subject_text = "Добро пожаловать в PRACTIX"
    template_name = "welcome.html"

    def __init__(self, broker: RabbitMQBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> EmailNotificationSchema:
        body = template_env.get_template(self.template_name).render(
            username=kwargs["username"]
        )
        return EmailNotificationSchema(
            user_id=kwargs["user_id"],
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


@lru_cache
def get_personal_film_selection_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> FilmSelectionEmailService:
    return FilmSelectionEmailService(broker, storage)


@lru_cache
def get_new_film_releases_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> FilmReleaseEmailService:
    return FilmReleaseEmailService(broker, storage)


@lru_cache
def get_welcome_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> WelcomeEmailService:
    return WelcomeEmailService(broker, storage)


@lru_cache
def get_manager_email_service(
    broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> ManagerEmailService:
    return ManagerEmailService(broker, storage)
