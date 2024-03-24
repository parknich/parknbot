import asyncio
import websockets

async def connect_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message from server: {message}")
        
asyncio.run(connect_to_server)