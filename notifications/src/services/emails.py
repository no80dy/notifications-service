from functools import lru_cache
from fastapi import Depends
from faststream.rabbit import RabbitBroker
from warehouse.rabbitmq import get_rabbitmq


class EmailService:
	def __init__(
		self, rabbit: RabbitBroker
	):
		pass

	async def send_data_to_rabbitmq(self, data: dict) -> None:
		pass


@lru_cache
async def get_email_service(
	broker: RabbitBroker = Depends(get_rabbitmq)
) -> EmailService:
	return EmailService(broker)
