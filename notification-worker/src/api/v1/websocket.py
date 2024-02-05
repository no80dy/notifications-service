import time
import uuid
from typing import Annotated

import jwt
from core.config import settings
from fastapi import APIRouter, Depends, Query, WebSocketException, status
from fastapi.responses import HTMLResponse
from faststream.rabbit.fastapi import RabbitRouter
from schemas.entity import InputLikeCommentMessage
from services.websocket import (
    WebSocketReceiverService,
    WebSocketSenderService,
    get_websocket_receiver_service,
    get_websocket_sender_service,
)
from starlette.websockets import WebSocket

router = APIRouter()
rabbit_router = RabbitRouter()


async def decode_token(token: Annotated[str, Query()]) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        raise WebSocketException(
            code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA, reason="Incorrect signature"
        )
    except jwt.InvalidTokenError:
        raise WebSocketException(
            code=status.WS_1009_INVALID_TOKEN, reason="Invalid token"
        )


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Annotated[dict, Depends(decode_token)],
    reciever_service: Annotated[
        WebSocketReceiverService, Depends(get_websocket_receiver_service)
    ],
):
    await reciever_service.connect(uuid.UUID(token["user_id"]), websocket)
