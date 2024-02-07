from faststream.rabbit import RabbitBroker

rabbitmq_broker: RabbitBroker | None = None


def get_rabbitmq_broker():
    return rabbitmq_broker
