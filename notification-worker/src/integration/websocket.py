import uuid
from functools import lru_cache

from fastapi import WebSocket


class WebSocketRouteTable:
    def __init__(self):
        self.connections: dict[uuid.UUID, WebSocket] = {}

    def get_websocket_by_user_id(self, _id: uuid.UUID):
        return self.connections[_id]

    def add_pair_in_table(self, _id: uuid.UUID, websocket: WebSocket):
        self.connections[_id] = websocket


@lru_cache(maxsize=1)
def get_websocket_route_table() -> WebSocketRouteTable:
    return WebSocketRouteTable()
