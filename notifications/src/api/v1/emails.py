from core.config import settings
from fastapi import Depends, APIRouter
from fastapi.responses import HTMLResponse
from faststream.kafka.fastapi import KafkaRouter
from schemas.emails import (
    InputNewFilmsReleases,
    InputPersonalFilmSelection,
    InputWelcomeMessage,
)
from services.emails import (
    PersonalFilmSelectionEmailService,
    NewFilmsReleasesEmailService,
    WelcomeMessageEmailService,
    get_personal_film_selection_email_service,
    get_new_film_releases_email_service,
    get_welcome_email_service
)
from schemas.users import User

# router = KafkaRouter('localhost:9094')
#
#
# @router.subscriber(
#     "personal-film-selection"
# )

router = APIRouter()


@router.post(
    '/personal-film-selection'
)
async def handle_personal_film_selection(
    message: InputPersonalFilmSelection,
    email_service: PersonalFilmSelectionEmailService = Depends(get_personal_film_selection_email_service),
) -> HTMLResponse:
    """
    Обработчик получает сообщение о персональной подборке фильмов для
    каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
    для воркера
    """
    return HTMLResponse(
        await email_service.handle_message(message.model_dump())
    )


# @router.subscriber("new-films-release", group_id="emails")
@router.post(
    '/new-films-release'
)
async def handle_new_films_releases(
    message: InputNewFilmsReleases,
    email_service: NewFilmsReleasesEmailService = Depends(get_new_film_releases_email_service),
):
    """
    Обработчик получает сообщение с данными о новых релизах фильмов,
    отправляя это всё в RabbitMQ для email воркера
    """
    return HTMLResponse(
        await email_service.handle_message(message.model_dump())
    )


# # @router.subscriber("welcome-message", group_id="emails")
@router.post(
    '/welcome-message'
)
async def handle_welcome_message(
    message: InputWelcomeMessage,
    email_service: WelcomeMessageEmailService = Depends(get_welcome_email_service),
):
    """
    Обработчик получает сообщение с данными о пользователе,
    который зарегистрировался и отправляет их в RabbitMQ
    для воркера
    """
    return HTMLResponse(
        await email_service.handle_message(message.model_dump())
    )
