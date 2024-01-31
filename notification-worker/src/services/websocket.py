from functools import lru_cache


class WebSocketService:
    async def send_notification(self, data: dict) -> None:
        pass


@lru_cache
def get_websocket_service():
    return WebSocketService()
