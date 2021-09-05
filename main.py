from websocket_server_lib import WSServer
from docker_lib import Docker


docker_client = Docker()
docker_client.start()

ws_server = WSServer()
ws_server.start()

while True:
    update = docker_client.updates_json.get()
    ws_server.server.send_message_to_all(update.json())


# print('DONE')
