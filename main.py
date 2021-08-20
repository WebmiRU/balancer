import asyncio
from pprint import pprint
import time
import websockets


class Server:
    ws_clients = {}

    async def handler(self, ws, path):
        self.ws_clients[ws] = ws

        try:
            async for request in ws:
                print("MESSAGE: " + request)
                await ws.send("Hello world!")
        except:
            self.ws_clients.pop(ws)

    def f1(self):
        while True:
            print('F1')
            time.sleep(1)

    def f2(self):
        while True:
            print('COUNT: %s' % len(self.ws_clients))
            time.sleep(1)

    async def run(self):
        await websockets.serve(self.handler, "localhost", 6789)
        await asyncio.gather(asyncio.to_thread(self.f1), asyncio.to_thread(self.f2))


server = Server()
asyncio.run(server.run())
