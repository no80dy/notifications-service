import datetime

import httpx
import uuid
from functools import lru_cache

from fastapi import Depends
from faststream.rabbit import RabbitBroker
from warehouse.rabbitmq import get_rabbitmq
from schemas.users import User
from core.jinja2 import template_env


class BasePersonalEmailService:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def _make_get_request(self, url: str) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()

    async def enrich_user_data(self, user_id: uuid.UUID) -> list[User]:
        url = f'http://localhost:8001/auth/api/v1/users/?users_ids={user_id}'
        result = await self._make_get_request(url)
        return [User(**data) for data in result]

    async def handle_message(self, data: dict):
        user_data = await self.enrich_user_data(data['user_id'])

        if not user_data:
            raise ValueError('No user found')

        data['username'] = user_data[0].username
        return await self.render_to_html(data)

    async def render_to_html(self, data: dict):
        return 'Error'


class PersonalFilmSelectionEmailService(BasePersonalEmailService):
    def __init__(self, broker: RabbitBroker):
        super().__init__(broker)

    async def render_to_html(self, context: dict):
        template = template_env.get_template('personal-film-selection.html')
        return template.render(**context)


class NewFilmsReleasesEmailService(BasePersonalEmailService):
    def __init__(self, broker: RabbitBroker):
        super().__init__(broker)

    async def render_to_html(self, context: dict):
        template = template_env.get_template('new-films-releases.html')
        return template.render(
            month=datetime.datetime.now().strftime('%B'),
            **context
        )


class WelcomeMessageEmailService(BasePersonalEmailService):
    def __init__(self, broker: RabbitBroker):
        super().__init__(broker)

    async def render_to_html(self, context: dict):
        template = template_env.get_template('welcome.html')
        return template.render(**context)


@lru_cache
def get_personal_film_selection_email_service(
    broker: RabbitBroker = Depends(get_rabbitmq),
) -> PersonalFilmSelectionEmailService:
    return PersonalFilmSelectionEmailService(broker)


@lru_cache
def get_new_film_releases_email_service(
    broker: RabbitBroker = Depends(get_rabbitmq),
) -> NewFilmsReleasesEmailService:
    return NewFilmsReleasesEmailService(broker)


@lru_cache
def get_welcome_email_service(
    broker: RabbitBroker = Depends(get_rabbitmq),
) -> WelcomeMessageEmailService:
    return WelcomeMessageEmailService(broker)
