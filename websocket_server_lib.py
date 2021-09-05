import json
import threading
from types import SimpleNamespace

from websocket_server import WebsocketServer

from docker_lib import Docker


class Error:
    def __init__(self, code: int = 0, message: str = None, data=None):
        self.type = 'ERROR'
        self.code = code
        self.message = message
        self.data = data

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


class WSServer(threading.Thread):
    def __init__(self, port: int = 5000, host: str = '0.0.0.0'):
        super().__init__()

        self.server = WebsocketServer(port, host)
        self.docker_client = Docker()
        self.docker_events_queue = self.docker_client.updates_json
        self.docker_client.start()

    def docker_events_queue_process(self):
        while True:
            update = self.docker_client.updates_json.get()
            self.server.send_message_to_all(update)

    # @staticmethod
    # def new_client(client, server):
    #     server.send_message_to_all("Hey all, a new client has joined us")
    #
    # @staticmethod
    # def client_left(self, client, server):
    #     print("Client left")

    def message_received(self, client, server, message):
        print("MESSAGE: %s" % message)
        server.send_message(client, "MESSAGE: %s" % message)

        try:
            msg = json.loads(message, object_hook=lambda d: SimpleNamespace(**d))
            if msg.platform == 'DOCKER':  # for DOCKER platform
                if msg.type == 'GET':  # for GET message type
                    if msg.target == 'CONTAINERS_ALL':
                        server.send_message(client, self.docker_client.get_all())

        except Exception as e:
            server.send_message(client, Error(999, "Message processing error").json())
            print(e)

    def run(self):
        threading.Thread(target=self.docker_events_queue_process).start()

        # self.server.set_fn_new_client(self.new_client)
        # self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()
