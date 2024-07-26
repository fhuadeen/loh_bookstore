from typing import Dict
import abc
import json

from loh_utils.event_bus import RabbitMQ
import websockets

from api.config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USERNAME,
    RABBITMQ_PASSWORD,
    INVENTORY_QUEUE,
    NOTIFICATION_SERVER_HOST,
)


def publish(
    msg: Dict,
    queue_name: str = INVENTORY_QUEUE,
    delivery_mode: bool = True
):
    """Publishes data to event bus

    Args:
        msg (Dict): message to be published
        queue_name (str, optional): queue to publish message to. Defaults to INVENTORY_QUEUE.
        delivery_mode (bool, optional): If delivery to be persistent or not. Defaults to True.
    """

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

class BaseNotificator(abc.ABC):
    """Base client for notification"""
    def __init__(self, notification_server_host: str = NOTIFICATION_SERVER_HOST):
        self.uri = f"ws://{notification_server_host}"

    @abc.abstractmethod
    async def send_notification(self, message):
        pass

class WebSocketsNotificator(BaseNotificator):
    "client for notification websockets"
    async def send_notification(self, message) -> None:
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(message))
            print(f"Sent message: {message}")
