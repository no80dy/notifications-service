import asyncio
import uuid
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, WebSocket
from integration.websocket import WebSocketRouteTable, get_websocket_route_table
from integration.http import get_users_data


class WebSocketSenderService:
    def __init__(self, websocket_route_table: WebSocketRouteTable) -> None:
        self.websocket_route_table = websocket_route_table

    async def handle_message(self, data: dict):
        user_id, producer_id = data["user_id"], data["producer_id"]
        connection = self.websocket_route_table.get_websocket_by_user_id(user_id)
        if not connection:
            return None
        users = await get_users_data([producer_id, ])
        if len(users) != 1:
            raise ValueError(f"Expected two users, found {len(users)}")
        await connection.send_text(
            f"The user {users[0].username} liked your comment"
        )


class WebSocketReceiverService:
    def __init__(self, websocket_route_table: WebSocketRouteTable):
        self.websocket_route_table = websocket_route_table

    async def connect(self, user_id: uuid.UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.websocket_route_table.add_pair_in_table(user_id, websocket)
        while True:
            await asyncio.sleep(1)


@lru_cache
def get_websocket_sender_service(
    websocket_route_table: Annotated[
        WebSocketRouteTable, Depends(get_websocket_route_table)
    ]
) -> WebSocketSenderService:
    return WebSocketSenderService(websocket_route_table)


@lru_cache
def get_websocket_receiver_service(
    websocket_route_table: Annotated[
        WebSocketRouteTable, Depends(get_websocket_route_table)
    ]
) -> WebSocketReceiverService:
    return WebSocketReceiverService(websocket_route_table)
