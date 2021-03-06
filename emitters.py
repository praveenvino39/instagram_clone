import websockets
import asyncio


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send({"type": "chat_message", "like_count": "47"})
        await websocket.recv()


loop = asyncio.get_event_loop()
loop.run_until_complete(hello('ws://127.0.0.1:8000/post/like-count/12/'))
print("Fin de la boucle !")
