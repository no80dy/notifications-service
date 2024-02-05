from typing import Annotated
from fastapi import Depends
from schemas.entity import InputEmailMessage, InputLikeCommentMessage
from services.email import EmailService, get_email_service
from services.websocket import WebSocketSenderService, get_websocket_sender_service
from integration.rabbitmq import get_rabbitmq_broker
from faststream.rabbit.fastapi import RabbitRouter
from core.config import settings

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
    await email_service.handle_message(message.model_dump())


@router.subscriber("websockets_queue")
async def get_message(
    message: InputLikeCommentMessage,
    sender_service: Annotated[
        WebSocketSenderService, Depends(get_websocket_sender_service)
    ],
):
    await sender_service.handle_message(message.model_dump())
