from typing import Dict

from loh_utils.event_bus import RabbitMQ

from api.config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    INVENTORY_QUEUE,
)

# class EventBus:
#     def __init__(self):
#         pass

def publish(
    msg: Dict,
    queue_name: str = INVENTORY_QUEUE,
    delivery_mode: bool = True
):

    eb = RabbitMQ(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
    )

    eb.publish(
        queue_name=queue_name,
        message=msg,
        delivery_mode=delivery_mode,
    )
