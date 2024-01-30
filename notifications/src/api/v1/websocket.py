from fastapi import APIRouter, Depends
from typing import Annotated
from services.websocket import WebSocketService, get_websocket_service
from schemas.websocket import InputCommentLikeMessage, OutputComentLikeMessage

router = APIRouter()


@router.post(
    "/like",
    response_model=list[OutputComentLikeMessage],
    summary="Отправка события о лайке в воркер",
    description="Публикация в RabbitMQ и запись в MongoDB нотификации",
    response_description="Информация о нотификации",
)
async def handle_likes(
    message: InputCommentLikeMessage,
    websocket_service: Annotated[InputCommentLikeMessage, Depends(get_websocket_service)]
):
    return await websocket_service.handle_message(message.model_dump())
