import asyncio
import pprint
import time
import websockets

x1 = 101
x2 = 202
websocketClients = {}


class Server:
    async def handler(websocket, path):
        global websocketClients
        websocketClients[websocket] = websocket

        try:
            async for request in websocket:
                print("MESSAGE: " + request)
                await websocket.send("Hello world!")
        except:
            print('EXCEPTION!!!')
            websocketClients.pop(websocket)

    def f1(self):
        global x1
        while True:
            x1 = x1 + 1
            print(x1)
            time.sleep(1)

    def f2(self):
        global x1
        global websocketClients

        while True:
            x1 = x1 + 1
            print(x1)
            time.sleep(1)
            print(len(websocketClients))

    async def main(self):
        print(f"Старт цикла событий: {time.strftime('%X')}")
        await websockets.serve(self.handler, "localhost", 6789)

        await asyncio.gather(asyncio.to_thread(self.f1), asyncio.to_thread(self.f2))

        print(f"Завершение цикла событий: {time.strftime('%X')}")


s = Server()
asyncio.run(s.main())
# asyncio.get_event_loop().run_until_complete(main())
