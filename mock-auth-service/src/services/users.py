import uuid

from db.postgresql import get_session
from fastapi import Depends
from models.entity import User
from schemas.entity import UserInformationResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, db: AsyncSession):
        self.session = db

    async def get_users_info(
        self, users_ids: list[uuid.UUID]
    ) -> list[UserInformationResponse]:
        users = (
            await self.session.execute(select(User).where(User.id.in_(users_ids)))
        ).scalars()

        if not users:
            return []

        return [
            UserInformationResponse(
                id=user.id, username=user.username, email=user.email
            )
            for user in users
        ]


async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db)
