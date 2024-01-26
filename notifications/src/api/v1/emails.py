from faststream.kafka.fastapi import KafkaRouter

from core.config import settings
from schemas.emails import (
	InputWelcomeMessage,
	InputNewFilmsReleases,
	InputPersonalFilmSelection
)


router = KafkaRouter(settings.kafka_brokers)


@router.subscriber(
	'personal-film-selection',
	group_id='emails'
)
async def handle_personal_film_selection(
	message: InputPersonalFilmSelection
):
	"""
	Обработчик получает сообщение о персональной подборке фильмов для
	каждого пользователя и отправляет эти данные с шаблонов в RabbitMQ
	для воркера
	"""
	pass


@router.subscriber(
	'new-films-release',
	group_id='emails'
)
async def handle_new_films_releases(
	message: InputNewFilmsReleases
):
	"""
	Обработчик получает сообщение с данными о новых релизах фильмов,
	отправляя это всё в RabbitMQ для email воркера
	"""
	pass


@router.subscriber(
	'welcome-message',
	group_id='emails'
)
async def handle_welcome_message(
	message: InputWelcomeMessage
):
	"""
	Обработчик получает сообщение с данными о пользователе,
	который зарегистрировался и отправляет их в RabbitMQ
	для воркера
	"""
	pass
