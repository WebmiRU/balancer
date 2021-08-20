import asyncio
import json
from pprint import pprint
import time
import websockets
import docker


class Server:
    ws_clients = {}
    containers = {}
    client = docker.from_env()

    def __init__(self):
        for container in self.client.containers.list(all=True):
            self.container_set(container)

    def container_set(self, container):
        key = container.attrs['Id']
        value = {
            'name': container.name,
            'attrs': container.attrs,
            'labels': container.labels
        }

        self.containers[key] = value

    def docker_events(self):
        for event in self.client.events(decode=True):
            if event.get('id'):
                container = self.client.containers.get(event['id'])
                self.container_set(container)
                self.ws_client_notify()
                print('UPDATED!')

    async def ws_client_notify(self):
        for ws in self.ws_clients:
            for k, v in self.containers.items():
                await ws.send(json.dumps({'Name': v['name'], 'State': v['attrs']['State']['Running']}))

    async def ws_handler(self, ws, path):
        self.ws_clients[ws] = ws

        try:
            async for request in ws:
                await self.ws_client_notify()
                print("MESSAGE: " + request)
        except:
            self.ws_clients.pop(ws)

    async def run(self):
        await websockets.serve(self.ws_handler, '0.0.0.0', 6789)
        # await self.docker_events()
        await asyncio.gather(asyncio.to_thread(self.docker_events))


server = Server()
asyncio.run(server.run())
# asyncio.get_event_loop().run_until_complete(server.run())
