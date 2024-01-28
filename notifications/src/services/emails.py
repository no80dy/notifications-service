import datetime
import uuid
from functools import lru_cache
from typing import Annotated, Any

import httpx
from core.config import settings
from core.jinja2 import template_env
from fastapi import Depends
from faststream.rabbit import RabbitBroker
from integration.rabbitmq import get_rabbitmq
from integration.storages import MongoStorage, get_storage
from schemas.emails import OutputEmailMessage
from schemas.notifications import NotificationModel
from schemas.users import UserInformation


async def get_users_data(users_ids: list[uuid.UUID]) -> list[UserInformation]:
    joined_users_ids = "&".join([str(user_id) for user_id in users_ids])
    url = f"http://localhost:8001/auth/api/v1/users/?users_ids={joined_users_ids}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return [UserInformation(**data) for data in response.json()]


class BasePersonalEmailService:
    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        self.broker = broker
        self.storage = storage

    async def _create_notification(
        self, user: UserInformation, **kwargs: Any
    ) -> NotificationModel:
        content = await self.make_email_message(
            username=user.username,
            email=user.email,
            **kwargs,
        )
        return NotificationModel(
            notification_id=uuid.uuid4(), user_id=user.id, content=content
        )

    async def _insert_notification_in_storage(
        self, notification: NotificationModel
    ) -> None:
        await self.storage.insert_element(
            notification.model_dump(mode='json'), settings.mongodb_notifications_collection_name
        )

    async def handle_message(self, data: dict) -> OutputEmailMessage:
        user = (
            await get_users_data(
                [
                    data["user_id"],
                ]
            )
        )[0]

        if not user:
            raise ValueError("No user found")

        notification = await self._create_notification(user, **data)
        await self._insert_notification_in_storage(notification)
        return notification.content

    async def publish_data_to_broker(self):
        pass

    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        raise NotImplementedError("Method make_email_message not implemented")


class BaseGeneralEmailService:
    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        self.broker = broker
        self.storage = storage

    async def _create_notifications(
        self, users: list[UserInformation], **kwargs: Any
    ) -> list[NotificationModel]:
        notifications = []
        for user in users:
            content = await self.make_email_message(
                username=user.username, email=user.email, **kwargs
            )
            notifications.append(
                NotificationModel(
                    notification_id=uuid.uuid4(), user_id=user.id, content=content
                )
            )
        return notifications

    async def _insert_notifications_in_storage(
        self, notifications: list[NotificationModel]
    ) -> None:
        await self.storage.insert_elements(
            [notification.model_dump(mode='json') for notification in notifications],
            settings.mongodb_notifications_collection_name,
        )

    async def handle_message(self, data: dict) -> list[OutputEmailMessage]:
        users = await get_users_data(data["users_ids"])

        if not users:
            raise ValueError("No users found")

        notifications = await self._create_notifications(users, **data)
        await self._insert_notifications_in_storage(notifications)
        return [notification.content for notification in notifications]

    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        raise NotImplementedError("Method make_email_message not implemented")


class ManagerEmailService(BaseGeneralEmailService):
    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        template = template_env.from_string(kwargs["body"])
        body = template.render(username=kwargs["username"])
        return OutputEmailMessage(
            email_from=kwargs["email_from"],
            email_to=kwargs["email"],
            subject=kwargs["subject"],
            body=body,
        )


class FilmSelectionEmailService(BasePersonalEmailService):
    subject_text = "Еженедельгая подборка фильмов для вас"
    template_name = "personal-film-selection.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        template = template_env.get_template(self.template_name)
        body = template.render(
            username=kwargs["username"], films_ids=kwargs["films_ids"]
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


class FilmReleaseEmailService(BasePersonalEmailService):
    subject_text = "Новые релизы фильмов и сериалов в этом месяце"
    template_name = "new-films-releases.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        body = template_env.get_template(self.template_name).render(
            username=kwargs["username"],
            month=datetime.datetime.now().strftime("%B"),
            watched_count=kwargs["watched_count"],
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


class WelcomeEmailService(BasePersonalEmailService):
    subject_text = "Добро пожаловать в PRACTIX"
    template_name = "welcome.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, **kwargs: Any) -> OutputEmailMessage:
        body = template_env.get_template(self.template_name).render(
            username=kwargs["username"]
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=kwargs["email"],
            subject=self.subject_text,
            body=body,
        )


@lru_cache
def get_personal_film_selection_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> FilmSelectionEmailService:
    return FilmSelectionEmailService(broker, storage)


@lru_cache
def get_new_film_releases_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> FilmReleaseEmailService:
    return FilmReleaseEmailService(broker, storage)


@lru_cache
def get_welcome_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> WelcomeEmailService:
    return WelcomeEmailService(broker, storage)


@lru_cache
def get_manager_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> ManagerEmailService:
    return ManagerEmailService(broker, storage)
