import asyncio
import websockets

async def handle_client(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received message from client: {message}")
        # Process the message and send a response if necessary
        response = f"Received: {message}"
        await websocket.send(response)

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
