import json
import threading

import docker
from simple_websocket_server import WebSocketServer, WebSocket

ws_clients = {}
containers = []
client = docker.from_env()


class WsClient(WebSocket):
    def handle(self):
        ws_client_update_containers_list()

    def connected(self):
        global ws_clients
        ws_clients[self] = self

    def handle_close(self):
        global ws_clients
        ws_clients.pop(self)


def container_set(container):
    value = {
        'name': container.name,
        'attrs': container.attrs,
        'labels': container.labels
    }

    # Ищем индекс контейнера с таким же ID в списке
    idx = next(iter([i for i, v in enumerate(containers) if v['attrs']['Id'] == value['attrs']['Id']]), None)

    if idx is not None:
        containers[idx] = value
    else:
        containers.append(value)


def docker_events():
    for event in client.events(decode=True):
        if event.get('id'):
            container = client.containers.get(event['id'])
            container_set(container)
            ws_client_update_containers_list()
            print('UPDATED!')


def ws_client_update_containers_list():
    for ws in ws_clients:
        ws.send_message(json.dumps({
            'action': 'update',
            'type': 'containers_list',
            'data': containers,
        }))


def run():
    for container in client.containers.list(all=True):
        container_set(container)

    server = WebSocketServer('0.0.0.0', 6789, WsClient)
    server.serve_forever()


t1 = threading.Thread(target=run)
t2 = threading.Thread(target=docker_events)

t1.start()
t2.start()
