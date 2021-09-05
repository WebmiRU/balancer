from websocket_server import WebsocketServer
import threading


class WSServer(threading.Thread):
    def __init__(self):
        super().__init__()

    def new_client(self, client, server):
        server.send_message_to_all("Hey all, a new client has joined us")

    def client_left(self, client, server):
        print("Client left")

    def message_received(self, client, server, message):
        print("MESSAGE: %s" % message)
        server.send_message(client, "MESSAGE: %s" % message)

    def run(self):
        self.server = WebsocketServer(5000, host='0.0.0.0')
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.server.run_forever()
