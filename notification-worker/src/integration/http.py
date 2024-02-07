import httpx
import uuid

from core.config import settings
from schemas.entity import UserInformation


async def get_users_data(users_ids: list[uuid.UUID]) -> list[UserInformation]:
    joined_users_ids = "&users_ids=".join([str(user_id) for user_id in users_ids])
    url = f"{settings.auth_service_url}/?users_ids={joined_users_ids}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return [UserInformation(**data) for data in response.json()]
