from faststream.rabbit.fastapi import RabbitRouter

from core.config import settings


router = RabbitRouter(
	host=settings.rabbitmq_host,
	port=settings.rabbitmq_port,
	login=settings.rabbitmq_login,
	password=settings.rabbitmq_password
)


@router.subscriber("emails_queue")
async def handle_emails_queue():
	pass
