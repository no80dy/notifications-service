import uuid

from fastapi import APIRouter, Depends, status, WebSocketException, Query
import time
from fastapi.responses import HTMLResponse
import jwt
from starlette.websockets import WebSocket
from typing import Annotated
from faststream.rabbit.fastapi import RabbitRouter
from services.websocket import (
	get_websocket_sender_service,
	WebSocketSenderService,
	WebSocketReceiverService,
	get_websocket_receiver_service
)
from core.config import settings


from schemas.entity import InputLikeCommentMessage

router = APIRouter()
rabbit_router = RabbitRouter()


# def decode_token(
# 	websocket: WebSocket,
# 	token: Annotated[str, Query()]
# ) -> dict:
# 	try:
# 		decoded_token = jwt.decode(
# 			token, settings.jwt_secret_key,
# 			algorithms=[settings.jwt_algorithm]
# 		)
# 		return decoded_token if decoded_token['exp'] >= time.time() else None
# 	except jwt.ExpiredSignatureError:
# 		raise WebSocketException(
# 			code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
# 			reason="Incorrect signature"
# 		)
# 	except jwt.InvalidTokenError:
# 		raise WebSocketException(
# 			code=status.WS_1009_INVALID_TOKEN,
# 			reason="Invalid token"
# 		)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def index():
	return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(
	websocket: WebSocket,
	# token: Annotated[str, Query()],
	reciever_service: Annotated[
		WebSocketReceiverService, Depends(get_websocket_receiver_service)
	]
):
	# try:
	# 	decoded_token = jwt.decode(
	# 		token, settings.jwt_secret_key,
	# 		algorithms=[settings.jwt_algorithm]
	# 	)
	# 	token_data = decoded_token if decoded_token['exp'] >= time.time() else None
	# except jwt.ExpiredSignatureError:
	# 	raise WebSocketException(
	# 		code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA,
	# 		reason="Incorrect signature"
	# 	)
	# except jwt.InvalidTokenError:
	# 	raise WebSocketException(
	# 		code=status.WS_1009_INVALID_TOKEN,
	# 		reason="Invalid token"
	# 	)
	# await websocket.accept()
	# while True:
	# 	data = await websocket.receive_text()
	# 	await websocket.send_text(f"Message text was: {data}")
	token_data = uuid.UUID("72ccba11-d548-4bf8-ba4e-bec34c703642")
	await reciever_service.connect(token_data, websocket)
