from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.emails import (
    InputFilmReleaseMessage,
    InputFilmSelectionMessage,
    InputManagerMessage,
    InputWelcomeMessage,
    OutputEmailMessage,
)
from services.emails import (
    FilmReleaseEmailService,
    FilmSelectionEmailService,
    ManagerEmailService,
    WelcomeEmailService,
    get_manager_email_service,
    get_new_film_releases_email_service,
    get_personal_film_selection_email_service,
    get_welcome_email_service,
)

router = APIRouter()


@router.post(
    "/personal-film-selection",
    response_model=list[OutputEmailMessage],
    summary="Отправка события персональной выборки фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_personal_film_selection(
    message: InputFilmSelectionMessage,
    email_service: FilmSelectionEmailService = Depends(
        get_personal_film_selection_email_service
    ),
) -> OutputEmailMessage:
    """
    Обработчик получает сообщение о персональной подборке фильмов для
    каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
    для воркера
    """
    return await email_service.handle_message(message.model_dump())


@router.post(
    "/new-films-release",
    response_model=list[OutputEmailMessage],
    summary="Отправка события релиза новых фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_new_films_releases(
    message: InputFilmReleaseMessage,
    email_service: FilmReleaseEmailService = Depends(
        get_new_film_releases_email_service
    ),
) -> OutputEmailMessage:
    """
    Обработчик получает сообщение с данными о новых релизах фильмов,
    отправляя это всё в RabbitMQ для email воркера
    """
    return await email_service.handle_message(message.model_dump())


@router.post(
    "/welcome-message",
    response_model=list[OutputEmailMessage],
    summary="Отправка события преветствия после регистрации в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_welcome_message(
    message: InputWelcomeMessage,
    email_service: WelcomeEmailService = Depends(get_welcome_email_service),
) -> OutputEmailMessage:
    """
    Обработчик получает сообщение с данными о пользователе,
    который зарегистрировался и отправляет их в RabbitMQ
    для воркера
    """
    return await email_service.handle_message(message.model_dump())


@router.post(
    "/manager-message",
    response_model=list[OutputEmailMessage],
    summary="Отправка события персональной выборки фильмов в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о сообщении, переданном в воркер",
)
async def handle_manager_message(
    message: InputManagerMessage,
    email_service: Annotated[ManagerEmailService, Depends(get_manager_email_service)],
) -> list[OutputEmailMessage]:
    """
    Обработчик получает сообщения пришедшие с панели менеджера
    для отправки уведомлений и отправляет их в RabbitMQ для воркера
    """
    return [
        message for message in await email_service.handle_message(message.model_dump())
    ]
