import json
from flask import Flask, render_template, session, copy_current_request_context
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

x = [1, 2, 3]

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send('ECHO:' + message)
        ws.send(json.dumps(x))


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()