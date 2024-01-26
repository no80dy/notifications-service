from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

rabbitmq_broker: RabbitBroker | None = None


async def configure_rabbit_exchange():
    await rabbitmq_broker.declare_exchange(
        RabbitExchange(name="notification-exchange", type=ExchangeType.FANOUT)
    )


async def configure_rabbit_queue():
    await rabbitmq_broker.declare_queue(RabbitQueue(name="emails-queue", durable=True))
