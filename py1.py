from collections import deque
from flask import Flask, render_template
from flask_uwsgi_websocket import GeventWebSocket

app = Flask(__name__)
ws = GeventWebSocket(app)

users = {}
backlog = deque(maxlen=10)

@app.route('/')
def index():
    return render_template('index.html')

@ws.route('/websocket')
def chat(ws):
    users[ws.id] = ws

    while True:
        msg = ws.receive()
        if len(msg) > 0:
            for id in users:
                users[id].send(msg)
        else:
            break

    del users[ws.id]

if __name__ == '__main__':
    app.run(debug=True, gevent=100)