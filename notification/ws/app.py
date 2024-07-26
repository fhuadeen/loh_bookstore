import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import asyncio
import websockets

from ws.config import NOTIFICATION_SERVER_HOST

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def notify_clients(message):
    if connected_clients:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main(websocket):
    await register(websocket)
    async for message in websocket:
        print(f"Received message: {message}")
        await notify_clients(message)

start_server = websockets.serve(main, NOTIFICATION_SERVER_HOST, 5004)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
