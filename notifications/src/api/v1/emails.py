from fastapi import Depends
from core.config import settings
from faststream.kafka.fastapi import KafkaRouter
from services.emails import get_email_service, EmailService
from schemas.emails import (
    InputNewFilmsReleases,
    InputPersonalFilmSelection,
    InputWelcomeMessage,
)

router = KafkaRouter(settings.kafka_brokers)


@router.subscriber("personal-film-selection", group_id="emails")
async def handle_personal_film_selection(
    message: InputPersonalFilmSelection,
    email_service: EmailService = Depends(get_email_service)
):
    """
    Обработчик получает сообщение о персональной подборке фильмов для
    каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
    для воркера
    """
    await email_service.send_data_to_rabbitmq(message.model_dump())
    pass


@router.subscriber("new-films-release", group_id="emails")
async def handle_new_films_releases(
    message: InputNewFilmsReleases,
    email_service: EmailService = Depends(get_email_service)
):
    """
    Обработчик получает сообщение с данными о новых релизах фильмов,
    отправляя это всё в RabbitMQ для email воркера
    """
    await email_service.send_data_to_rabbitmq(message.model_dump())
    pass


@router.subscriber("welcome-message", group_id="emails")
async def handle_welcome_message(
    message: InputWelcomeMessage,
    email_service: EmailService = Depends(get_email_service)
):
    """
    Обработчик получает сообщение с данными о пользователе,
    который зарегистрировался и отправляет их в RabbitMQ
    для воркера
    """
    await email_service.send_data_to_rabbitmq(message.model_dump())
    pass
