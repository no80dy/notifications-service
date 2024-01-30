from typing import Annotated

from core.config import settings
from fastapi import Depends
from faststream.rabbit.fastapi import RabbitRouter
from schemas.entity import InputEmailMessage, InputWebSocketMessage
from services.email import EmailService, get_email_service
from services.websocket import WebSocketService, get_websocket_service

router = RabbitRouter(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    login=settings.rabbitmq_login,
    password=settings.rabbitmq_password,
)


@router.subscriber("emails_queue")
async def handle_emails_queue(
    message: InputEmailMessage,
    email_service: Annotated[EmailService, Depends(get_email_service)],
):
    pass


@router.subscriber("wobsocket_queue")
async def handle_websocket_queue(
    message: InputWebSocketMessage,
    websocket_service: Annotated[WebSocketService, Depends(get_websocket_service)],
):
    pass
