from faststream.rabbit import RabbitBroker


rabbitmq: RabbitBroker | None = None


def get_rabbitmq():
	return rabbitmq
