from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from integration.rabbitmq import get_rabbitmq, RabbitBroker


class RabbitSubscriber:
	def __init__(self, broker: RabbitBroker):
		self.broker = broker

	async def subscribe(self, queue: str):
		pass


@lru_cache
def get_rabbit_subscriber(
	broker: Annotated[RabbitBroker, Depends(get_rabbitmq)]
) -> RabbitSubscriber:
	return RabbitSubscriber(broker)
