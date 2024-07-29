

from api.config import (
    event_bus,
    INVENTORY_QUEUE,
)
from api.services import BooksInventory

def consume_products_update() -> None:
    """Function to consume product update message"""
    event_bus.consume(
        queue_name=INVENTORY_QUEUE,
        callback_fxn=BooksInventory.update_products_units,
    )
