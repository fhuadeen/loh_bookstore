from typing import Dict

# from loh_utils.event_bus import RabbitMQ

from api.config import (
    event_bus,
    INVENTORY_QUEUE,
)
# from api.services import BooksInventory


# eb = RabbitMQ(
#     host=RABBITMQ_HOST,
#     port=RABBITMQ_PORT,
#     username=RABBITMQ_USERNAME,
#     password=RABBITMQ_PASSWORD,
# )

def publish(
    msg: Dict,
    queue_name: str = INVENTORY_QUEUE,
    delivery_mode: bool = True
) -> None:
    """Publishes data to event bus

    Args:
        msg (Dict): message to be published
        queue_name (str, optional): queue to publish message to. Defaults to INVENTORY_QUEUE.
        delivery_mode (bool, optional): If delivery to be persistent or not. Defaults to True.
    """

    event_bus.publish(
        queue_name=queue_name,
        message=msg,
        delivery_mode=delivery_mode,
    )

def consume_products_update() -> None:
    """Function to consume product update message"""
    event_bus.consume(
        queue_name=INVENTORY_QUEUE,
        callback_fxn=BooksInventory.update_products_units,
    )
