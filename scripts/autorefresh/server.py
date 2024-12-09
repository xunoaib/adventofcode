import asyncio

import websockets

connected_clients = set()

async def handler(websocket, path):
    # Register the client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            if message == "refresh":
                print("Received 'refresh' signal. Broadcasting to clients.")
                tasks = [
                    asyncio.create_task(client.send("refresh"))
                    for client in connected_clients
                    if client != websocket
                ]
                await asyncio.gather(*tasks)
    except websockets.ConnectionClosed:
        print("A client disconnected.")
    finally:
        connected_clients.remove(websocket)

server = websockets.serve(handler, "localhost", 8765)

print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
