from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue

rabbitmq_broker: RabbitBroker | None = None


async def configure_rabbit_exchange():
    await rabbitmq_broker.declare_exchange(
        RabbitExchange(name="notifications", type=ExchangeType.FANOUT)
    )


async def configure_rabbit_queues():
    await rabbitmq_broker.declare_queue(
        RabbitQueue(
            name="notifications.film_selection_email_notification", durable=True
        )
    )
    await rabbitmq_broker.declare_queue(
        RabbitQueue(name="notifications.film_release_email_notification", durable=True)
    )
    await rabbitmq_broker.declare_queue(
        RabbitQueue(
            name="notifications.welcome_message_email_notification", durable=True
        )
    )
    await rabbitmq_broker.declare_queue(
        RabbitQueue(name="notifications.manager_email_notification", durable=True)
    )


def get_rabbitmq():
    return rabbitmq_broker
