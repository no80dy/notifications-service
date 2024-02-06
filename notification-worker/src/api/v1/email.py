from typing import Annotated

from core.config import settings
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from schemas.entity import (
    InputFilmReleaseNotification,
    InputFilmSelectionNotification,
    InputLikeCommentNotification,
    InputManagerNotification,
    InputWelcomeNotification,
)
from services.email import (
    FilmReleaseEmailSenderService,
    FilmSelectionEmailSenderService,
    ManagerEmailSenderService,
    WelcomeEmailSenderService,
    get_film_release_sender_service,
    get_film_selection_email_sender_service,
    get_manager_sender_service,
    get_welcome_sender_service,
)
from services.websocket import WebSocketSenderService, get_websocket_sender_service

router = RabbitRouter(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    login=settings.rabbitmq_login,
    password=settings.rabbitmq_password,
)


@router.subscriber("notifications.manager_email_notification")
async def handle_general_email_notification(
    message: InputManagerNotification,
    email_service: Annotated[
        ManagerEmailSenderService, Depends(get_manager_sender_service)
    ],
):
    await email_service.handle_message(**message.model_dump())


@router.subscriber("notifications.film_release_email_notification")
async def handle_film_release_email_notification(
    message: InputFilmReleaseNotification,
    email_service: Annotated[
        FilmReleaseEmailSenderService, Depends(get_film_release_sender_service)
    ],
):
    await email_service.handle_message(**message.model_dump())


@router.subscriber("notifications.notifications.welcome_message_email_notification")
async def handle_welcome_message_email_notification(
    message: InputWelcomeNotification,
    email_service: Annotated[
        WelcomeEmailSenderService, Depends(get_welcome_sender_service)
    ],
):
    await email_service.handle_message(**message.model_dump())


@router.subscriber("notifications.notifications.film_selection_email_notification")
async def handle_film_selection_email_notification(
    message: InputFilmSelectionNotification,
    email_service: Annotated[
        FilmSelectionEmailSenderService,
        Depends(get_film_selection_email_sender_service),
    ],
):
    await email_service.handle_message(**message.model_dump())


@router.subscriber("notifications.websockets_notification")
async def handle_websockets_notification(
    message: InputLikeCommentNotification,
    sender_service: Annotated[
        WebSocketSenderService, Depends(get_websocket_sender_service)
    ],
):
    await sender_service.handle_message(message.model_dump())
