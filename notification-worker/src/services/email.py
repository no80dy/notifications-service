import datetime
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import lru_cache
from typing import Annotated, Any

import httpx
from aiosmtplib import SMTP
from core.config import settings
from core.jinja2 import template_env
from fastapi import Depends
from integration.smtp import get_smtp_client
from schemas.entity import UserInformation


async def get_users_data(users_ids: list[uuid.UUID]) -> list[UserInformation]:
    joined_users_ids = "&users_ids=".join([str(user_id) for user_id in users_ids])
    url = f"{settings.auth_service_url}/?users_ids={joined_users_ids}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return [UserInformation(**data) for data in response.json()]


class BaseEmailSenderService:
    def __init__(self, smtp_client: SMTP):
        self.smtp_client = smtp_client

    async def send_email(
        self, email_from: str, email_to: str, subject: str, body: str
    ) -> None:
        message = MIMEMultipart()
        message["From"] = email_from
        message["To"] = email_to
        message["Subject"] = subject
        message.attach(
            MIMEText(
                body,
                "html",
            )
        )

        await self.smtp_client.send_message(
            message, sender=email_from, recipients=email_to
        )

    async def handle_message(self, user_id: uuid.UUID, producer_id: uuid.UUID) -> None:
        raise NotImplementedError(
            "method handle_message not implemented inside the class"
        )


class BasePersonalEmailSenderService(BaseEmailSenderService):
    def __init__(self, smtp_client: SMTP) -> None:
        super().__init__(smtp_client)

    async def handle_message(self, user_id: uuid.UUID, producer_id: uuid, **kwargs: Any) -> None:
        users_ids = [user_id, producer_id, ]
        if not all(users_ids):
            raise ValueError("Invalid users ids")
        users = await get_users_data(users_ids)
        if len(users) != 2:
            raise ValueError(f"Expected two users, found {len(users)}")
        user, producer = users[0], users[1]
        body = await self._render_template(username=user.username, **kwargs)
        await self.send_email(
            email_from=producer.email,
            email_to=user.email,
            subject=kwargs["subject"],
            body=body,
        )

    async def _render_template(self, **kwargs: Any) -> str:
        raise NotImplementedError(
            "method _render_tamplate not implemented inside the class"
        )


class ManagerEmailSenderService(BasePersonalEmailSenderService):
    def __init__(self, smtp_client: SMTP) -> None:
        super().__init__(smtp_client)

    async def _render_template(self, **kwargs: Any) -> str:
        return kwargs["body"]


class FilmReleaseEmailSenderService(BasePersonalEmailSenderService):
    def __init__(self, smtp_client: SMTP) -> None:
        super().__init__(smtp_client)

    async def _render_template(self, **kwargs: Any) -> str:
        return template_env.get_template(kwargs["template_name"]).render(
            username=kwargs["username"],
            month=datetime.datetime.now().strftime("%B"),
            films_ids=kwargs["films_ids"],
            watched_count=kwargs["watched_count"],
        )


class FilmSelectionEmailSenderService(BasePersonalEmailSenderService):
    def __init__(self, smtp_client: SMTP):
        super().__init__(smtp_client)

    async def _render_template(self, **kwargs: Any) -> str:
        return template_env.get_template(kwargs["template_name"]).render(
            username=kwargs["username"], films_ids=kwargs["films_ids"]
        )


class WelcomeEmailSenderService(BasePersonalEmailSenderService):
    def __init__(self, smtp_client: SMTP):
        super().__init__(smtp_client)

    async def _render_template(self, **kwargs: Any):
        return template_env.get_template(kwargs["template_name"]).render(
            username=kwargs["username"],
        )


@lru_cache
def get_manager_sender_service(
    smtp_client: Annotated[SMTP, Depends(get_smtp_client)]
) -> ManagerEmailSenderService:
    return ManagerEmailSenderService(smtp_client)


@lru_cache
def get_welcome_sender_service(
    smtp_client: Annotated[SMTP, Depends(get_smtp_client)]
) -> WelcomeEmailSenderService:
    return WelcomeEmailSenderService(smtp_client)


@lru_cache
def get_film_release_sender_service(
    smtp_client: Annotated[SMTP, Depends(get_smtp_client)]
) -> FilmReleaseEmailSenderService:
    return FilmReleaseEmailSenderService(smtp_client)


@lru_cache
def get_film_selection_email_sender_service(
    smtp_client: Annotated[SMTP, Depends(get_smtp_client)]
) -> FilmSelectionEmailSenderService:
    return FilmSelectionEmailSenderService(smtp_client)
