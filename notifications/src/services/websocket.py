import httpx
import uuid
import asyncio
from typing import Annotated
from functools import lru_cache
from fastapi import Depends
from integration.brokers import RabbitMQBroker, get_message_broker
from integration.storages import MongoStorage, get_storage
from core.config import settings
from schemas.users import UserInformation
from schemas.websocket import InputCommentLikeMessage, OutputComentLikeMessage


async def get_users_data(users_ids: list[uuid.UUID]) -> list[UserInformation]:
	joined_users_ids = "&users_ids=".join([str(user_id) for user_id in users_ids])
	url = f"{settings.auth_service_url}/?users_ids={joined_users_ids}"
	async with httpx.AsyncClient() as client:
		response = await client.get(url)
		return [UserInformation(**data) for data in response.json()]


class WebSocketService:
	mongo_collection_name = "websocket"
	broker_queue_name = "websocket_queue_like"

	def __init__(self, broker: RabbitMQBroker, storage: MongoStorage):
		self.broker = broker
		self.storage = storage

	async def create_output_comment_like(
		self, message: InputCommentLikeMessage
	) -> OutputComentLikeMessage:
		return OutputComentLikeMessage(
			consumer_id=message.consumer_id,
			producer_id=message.producer_id,
			comment_id=message.comment_id
		)

	async def send_notification(self, message: OutputComentLikeMessage) -> None:
		await asyncio.gather(
			self.storage.insert_element(
				message.model_dump(),
				self.mongo_collection_name
			),
			self.broker.publish_one(
				message, self.broker_queue_name
			)
		)

	async def handle_message(self, message: InputCommentLikeMessage) -> OutputComentLikeMessage:
		notification = await self.create_output_comment_like(message)
		await self.send_notification(notification)
		return notification


@lru_cache
def get_websocket_service(
	broker: Annotated[RabbitMQBroker, Depends(get_message_broker)],
	storage: Annotated[MongoStorage, Depends(get_storage)]
):
	return WebSocketService(broker, storage)
