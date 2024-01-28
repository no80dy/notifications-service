from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.responses import JSONResponse
from schemas.emails import (
    InputFilmReleaseMessage,
    InputFilmSelectionMessage,
    InputManagerMessage,
    InputWelcomeMessage,
)
from services.emails import (
    FilmReleaseEmailService,
    FilmSelectionEmailService,
    WelcomeEmailService,
    ManagerEmailService,
    get_new_film_releases_email_service,
    get_personal_film_selection_email_service,
    get_welcome_email_service,
    get_manager_email_service
)
from schemas.emails import OutputEmailMessage

router = APIRouter()


@router.post("/personal-film-selection")
async def handle_personal_film_selection(
    message: InputFilmSelectionMessage,
    email_service: FilmSelectionEmailService = Depends(
        get_personal_film_selection_email_service
    ),
) -> JSONResponse:
    """
    Обработчик получает сообщение о персональной подборке фильмов для
    каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
    для воркера
    """
    return JSONResponse(
        (await email_service.handle_message(message.model_dump())).model_dump()
    )


@router.post("/new-films-release")
async def handle_new_films_releases(
    message: InputFilmReleaseMessage,
    email_service: FilmReleaseEmailService = Depends(
        get_new_film_releases_email_service
    ),
) -> JSONResponse:
    """
    Обработчик получает сообщение с данными о новых релизах фильмов,
    отправляя это всё в RabbitMQ для email воркера
    """
    return JSONResponse(
        (await email_service.handle_message(message.model_dump())).model_dump()
    )


@router.post("/welcome-message")
async def handle_welcome_message(
    message: InputWelcomeMessage,
    email_service: WelcomeEmailService = Depends(get_welcome_email_service),
) -> JSONResponse:
    """
    Обработчик получает сообщение с данными о пользователе,
    который зарегистрировался и отправляет их в RabbitMQ
    для воркера
    """
    return JSONResponse(
        (await email_service.handle_message(message.model_dump())).model_dump()
    )


@router.post("/manager-message")
async def handle_manager_message(
    message: InputManagerMessage,
    email_service: Annotated[ManagerEmailService, Depends(get_manager_email_service)]
) -> list[OutputEmailMessage]:
    """
    Обработчик получает сообщения пришедшие с панели менеджера
    для отправки уведомлений и отправляет их в RabbitMQ для воркера
    """
    result = (await email_service.handle_message(message.model_dump()))
    return [message for message in result]
