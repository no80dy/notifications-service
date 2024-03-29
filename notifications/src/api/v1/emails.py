from typing import Annotated

from fastapi import APIRouter, Depends
from schemas.emails import (
    InputFilmReleaseNotification,
    InputFilmSelectionNotification,
    InputManagerNotification,
    InputWelcomeNotification,
)
from services.emails import (
    FilmReleaseEmailService,
    FilmSelectionEmailService,
    ManagerEmailNotificationService,
    WelcomeEmailService,
    get_film_release_email_service,
    get_film_selection_email_service,
    get_manager_email_service,
    get_welcome_email_service,
)

router = APIRouter()


@router.post(
    "/personal-film-selection",
    summary="Отправка события персональной выборки фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_personal_film_selection(
    message: InputFilmSelectionNotification,
    email_service: Annotated[
        FilmSelectionEmailService, Depends(get_film_selection_email_service)
    ],
):
    """
    Обработчик получает сообщение о персональной подборке фильмов для
    каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
    для воркера
    """
    await email_service.handle_message(**message.model_dump())


@router.post(
    "/new-films-release",
    summary="Отправка события релиза новых фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_new_films_releases(
    message: InputFilmReleaseNotification,
    email_service: Annotated[
        FilmReleaseEmailService, Depends(get_film_release_email_service)
    ],
):
    """
    Обработчик получает сообщение с данными о новых релизах фильмов,
    отправляя это всё в RabbitMQ для email воркера
    """
    await email_service.handle_message(**message.model_dump())


@router.post(
    "/welcome-message",
    summary="Отправка события преветствия после регистрации в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_welcome_message(
    message: InputWelcomeNotification,
    email_service: Annotated[WelcomeEmailService, Depends(get_welcome_email_service)],
):
    """
    Обработчик получает сообщение с данными о пользователе,
    который зарегистрировался и отправляет их в RabbitMQ
    для воркера
    """
    await email_service.handle_message(**message.model_dump())


@router.post(
    "/manager-message",
    summary="Отправка события персональной выборки фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_manager_message(
    message: InputManagerNotification,
    email_service: Annotated[
        ManagerEmailNotificationService, Depends(get_manager_email_service)
    ],
):
    """
    Обработчик получает сообщения пришедшие с панели менеджера
    для отправки уведомлений и отправляет их в RabbitMQ для воркера
    """
    await email_service.handle_message(**message.model_dump())
