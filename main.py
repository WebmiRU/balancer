#!/bin/python3

import docker
from pprint import pprint

client = docker.from_env()

if __name__ == '__main__':
    for c in client.containers.list():
        x = client.containers.get('f264a5a06e')
        pprint(c.labels)

