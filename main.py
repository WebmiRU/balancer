import json
import threading
import docker
from simple_websocket_server import WebSocketServer, WebSocket

ws_clients = {}
containers = {}
client = docker.from_env()


class WsClient(WebSocket):
    def handle(self):
        self.send_message('MESSAGE: ' + self.data)
        for k, v in containers.items():
            # if v['name'] == 'redis_test':
            self.send_message(json.dumps({'Name': v['name'], 'State': v['attrs']['State']['Running']}))

    def connected(self):
        global ws_clients
        ws_clients[self] = self

    def handle_close(self):
        global ws_clients
        ws_clients.pop(self)


def container_set(container):
    key = container.attrs['Id']
    value = {
        'name': container.name,
        'attrs': container.attrs,
        'labels': container.labels
    }

    containers[key] = value


def docker_events():
    for event in client.events(decode=True):
        if event.get('id'):
            container = client.containers.get(event['id'])
            container_set(container)
            ws_client_notify()
            print('UPDATED!')


def ws_client_notify():
    for ws in ws_clients:
        for k, v in containers.items():
            # if v['name'] == 'redis_test':
            ws.send_message(json.dumps({'Name': v['name'], 'State': v['attrs']['State']['Running']}))


def run():
    for container in client.containers.list(all=True):
        container_set(container)

    server = WebSocketServer('0.0.0.0', 6789, WsClient)
    server.serve_forever()


t1 = threading.Thread(target=run)
t2 = threading.Thread(target=docker_events)

t1.start()
t2.start()
