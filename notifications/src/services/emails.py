import datetime
import uuid
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Annotated

import httpx
from core.config import settings
from core.jinja2 import template_env
from fastapi import Depends
from faststream.rabbit import RabbitBroker
from integration.rabbitmq import get_rabbitmq
from integration.storages import MongoStorage, get_storage
from schemas.emails import OutputEmailMessage
from schemas.users import User


async def get_users_data(user_id: uuid.UUID) -> list[User]:
    url = f"http://localhost:8001/auth/api/v1/users/?users_ids={user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return [User(**data) for data in response.json()]


class IEmailService(ABC):
    @abstractmethod
    async def handle_message(self, data: dict) -> OutputEmailMessage:
        pass

    @abstractmethod
    async def make_email_message(self, context: dict) -> OutputEmailMessage:
        pass


class BasePersonalEmailService(IEmailService):
    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        self.broker = broker
        self.storage = storage

    async def handle_message(self, data: dict) -> OutputEmailMessage:
        user_data = await get_users_data(data["user_id"])

        if not user_data:
            raise ValueError("No user found")

        email_content = await self.make_email_message(
            {**user_data[0].model_dump(), **data}
        )
        await self.load_data_to_storage(data["user_id"], email_content.model_dump())
        return email_content

    async def load_data_to_storage(
        self, user_id: uuid.UUID, email_content: dict
    ) -> None:
        result = await self.storage.insert_element(
            {
                "notification_id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "content": email_content,
            },
            settings.mongodb_notifications_collection_name,
        )
        print(result)

    async def publish_data_to_broker(self):
        pass

    async def make_email_message(self, context: dict) -> OutputEmailMessage:
        raise NotImplementedError("Method make_email_message not implemented")


class PersonalFilmSelectionEmailService(BasePersonalEmailService):
    subject_text = "Еженедельгая подборка фильмов для вас"
    template_name = "personal-film-selection.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, context: dict) -> OutputEmailMessage:
        template = template_env.get_template(self.template_name)
        body = template.render(
            username=context["username"], films_ids=context["films_ids"]
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=context["email"],
            subject=self.subject_text,
            body=body,
        )


class NewFilmsReleasesEmailService(BasePersonalEmailService):
    subject_text = "Новые релизы фильмов и сериалов в этом месяце"
    template_name = "new-films-releases.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, context: dict) -> OutputEmailMessage:
        body = template_env.get_template(self.template_name).render(
            username=context["username"],
            month=datetime.datetime.now().strftime("%B"),
            watched_count=context["watched_count"],
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=context["email"],
            subject=self.subject_text,
            body=body,
        )


class WelcomeMessageEmailService(BasePersonalEmailService):
    subject_text = "Добро пожаловать в PRACTIX"
    template_name = "welcome.html"

    def __init__(self, broker: RabbitBroker, storage: MongoStorage) -> None:
        super().__init__(broker, storage)

    async def make_email_message(self, context: dict) -> OutputEmailMessage:
        body = template_env.get_template(self.template_name).render(
            username=context["username"]
        )
        return OutputEmailMessage(
            email_from="admin@example.com",
            email_to=context["email"],
            subject=self.subject_text,
            body=body,
        )


@lru_cache
def get_personal_film_selection_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> PersonalFilmSelectionEmailService:
    return PersonalFilmSelectionEmailService(broker, storage)


@lru_cache
def get_new_film_releases_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> NewFilmsReleasesEmailService:
    return NewFilmsReleasesEmailService(broker, storage)


@lru_cache
def get_welcome_email_service(
    broker: Annotated[RabbitBroker, Depends(get_rabbitmq)],
    storage: Annotated[MongoStorage, Depends(get_storage)],
) -> WelcomeMessageEmailService:
    return WelcomeMessageEmailService(broker, storage)
