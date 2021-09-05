import json
import queue
import threading
import time

import docker


class ToJson:
    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


class Container:
    def __init__(self, attrs):
        self.id = attrs['Id']
        self.is_running = attrs['State']['Running']
        self.name = attrs['Name'][1:]
        self.image = attrs['Image']


class EventContainer(ToJson):
    def __init__(self, container):
        self.type = 'EVENT:UPDATE'
        self.target = 'CONTAINER'
        self.platform = 'DOCKER'
        self.data = container


class EventContainersAll(ToJson):
    def __init__(self, containers):
        self.type = 'EVENT:UPDATE'
        self.target = 'CONTAINERS_ALL'
        self.platform = 'DOCKER'
        self.data = containers


class Docker(threading.Thread):
    __containers = {}
    updates_json = queue.Queue()

    def __init__(self):
        super().__init__()
        self.client = docker.from_env()
        self.update_all_containers()

    def get(self, container_id: str):
        pass

    def get_all(self):
        return EventContainersAll(self.__containers).json()

    def update_all_containers(self, try_counter=0):
        if try_counter > 0:
            print("TRY COUNTER %s" % try_counter)
            time.sleep(1)

        if try_counter > 10:  # FATAL ERROR
            pass

        self.__containers = {}

        try:
            for container in self.client.containers.list(all=True):
                print(json.dumps(container.attrs))
                print('-' * 98)
                item = Container(container.attrs)
                self.__containers[item.id] = item

            # Заменить на список всех контейнеров в JSON-формате
            containers_all = EventContainersAll(self.__containers)
            self.updates_json.put(containers_all.json())
        except Exception as e:
            print("DOCKER NOT FOUND ALL ERR")
            print(e)
            self.update_all_containers(try_counter + 1)

    def events(self):
        for event in self.client.events(decode=True):
            try:
                if event.get('Type') == 'container':
                    get_container = self.client.containers.get(event.get('id'))
                    get_container.reload()

                    container = Container(get_container.attrs)
                    self.__containers[container.id] = container

                    event_container = EventContainer(container)
                    self.updates_json.put(event_container.json())
                else:
                    print("EVENT TYPE: %s" % event.get('Type'))
            # except docker.errors.NotFound:
            except Exception as e:
                print("DOCKER NOT FOUND ERR")
                print(e)
                self.update_all_containers()

    def run(self):
        self.events()
