import asyncio

import websockets


async def send_refresh_signal():
    uri = "ws://localhost:8765"  # Replace with your WebSocket server's URL
    async with websockets.connect(uri) as websocket:
        await websocket.send("refresh")
        print("Sent 'refresh' signal to the server.")

asyncio.run(send_refresh_signal())
