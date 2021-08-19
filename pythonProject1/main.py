import json
from pprint import pprint

import docker
import redis as redis

rds = redis.Redis(host='localhost', port=6379, db=0)
client = docker.from_env()
containers = client.containers.list()


def container_set(container):
    key = 'container:' + container.attrs['Id']
    value = {
        'name': container.name,
        'attrs': container.attrs,
        'labels': container.labels
    }

    rds.set(key, json.dumps(value))


for container in client.containers.list():
    container_set(container)

for event in client.events(decode=True):
    if event.get('id'):
        container = client.containers.get(event['id'])
        container_set(container)
        print('UPDATED!')

    # pprint(event)
